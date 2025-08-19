import os
from typing import List, Optional
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.storage.storage_context import StorageContext
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.core.storage.vector_store import SimpleVectorStore
from llama_index.core.storage.docstore import SimpleDocumentStore
from app.core.config import settings

class RAGService:
    def __init__(self):
        self.setup_llm()
        self.indexes = {}
    
    def setup_llm(self):
        """Configurar LLM e embeddings com Ollama"""
        Settings.llm = Ollama(
            model=settings.DEFAULT_LLM_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            request_timeout=120.0
        )
        Settings.embed_model = OllamaEmbedding(
            model_name=settings.DEFAULT_EMBED_MODEL,
            base_url=settings.OLLAMA_BASE_URL
        )
    
    def create_collection_index(self, collection_name: str, documents_path: str) -> bool:
        """Criar índice para uma coleção de documentos"""
        try:
            if not os.path.exists(documents_path):
                return False
            
            # Carregar documentos
            documents = SimpleDirectoryReader(documents_path).load_data()
            
            if not documents:
                return False
            
            # Adicionar metadados
            for doc in documents:
                doc.metadata["collection"] = collection_name
            
            # Criar índice
            index = VectorStoreIndex.from_documents(documents)
            
            # Salvar índice
            storage_path = os.path.join(settings.INDEX_STORAGE_PATH, collection_name)
            index.storage_context.persist(persist_dir=storage_path)
            
            # Cache do índice
            self.indexes[collection_name] = index
            return True
            
        except Exception as e:
            print(f"Erro ao criar índice: {e}")
            return False
    
    def load_collection_index(self, collection_name: str) -> Optional[VectorStoreIndex]:
        """Carregar índice de uma coleção"""
        try:
            if collection_name in self.indexes:
                return self.indexes[collection_name]
            
            storage_path = os.path.join(settings.INDEX_STORAGE_PATH, collection_name)
            
            if not os.path.exists(storage_path):
                return None
            
            # Carregar contexto de storage
            storage_context = StorageContext.from_defaults(persist_dir=storage_path)
            
            # Carregar índice
            index = VectorStoreIndex.from_storage(storage_context)
            self.indexes[collection_name] = index
            return index
            
        except Exception as e:
            print(f"Erro ao carregar índice: {e}")
            return None
    
    def query_collection(self, collection_name: str, query: str, top_k: int = 3) -> str:
        """Fazer consulta em uma coleção"""
        try:
            index = self.load_collection_index(collection_name)
            
            if not index:
                return "Coleção não encontrada ou não indexada."
            
            query_engine = index.as_query_engine(similarity_top_k=top_k)
            response = query_engine.query(query)
            
            return str(response)
            
        except Exception as e:
            print(f"Erro na consulta: {e}")
            return f"Erro ao processar consulta: {str(e)}"
    
    def delete_collection_index(self, collection_name: str) -> bool:
        """Deletar índice de uma coleção"""
        try:
            storage_path = os.path.join(settings.INDEX_STORAGE_PATH, collection_name)
            
            if os.path.exists(storage_path):
                import shutil
                shutil.rmtree(storage_path)
            
            if collection_name in self.indexes:
                del self.indexes[collection_name]
            
            return True
            
        except Exception as e:
            print(f"Erro ao deletar índice: {e}")
            return False

# Instância global
rag_service = RAGService()
