"""Services module for DocuChat RAG application."""

from typing import List, Optional, Dict, Any
import os
import hashlib
from pathlib import Path
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    Settings
)
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from sqlalchemy.orm import Session
from ..models import Collection, Document
from ..core.config import settings


class RAGService:
    """Service for RAG operations using LlamaIndex and Ollama."""
    
    def __init__(self, db: Session):
        self.db = db
        self._setup_llama_index()
    
    def _setup_llama_index(self):
        """Configure LlamaIndex settings."""
        # Setup LLM
        Settings.llm = Ollama(
            model=settings.default_model,
            base_url=settings.ollama_base_url,
            temperature=0.1
        )
        
        # Setup embedding model
        Settings.embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )
        
        # Create directories
        os.makedirs(settings.vector_store_path, exist_ok=True)
        os.makedirs(settings.upload_path, exist_ok=True)
    
    def create_collection(self, name: str, description: str = None) -> Collection:
        """Create a new document collection."""
        collection = Collection(
            name=name,
            description=description
        )
        self.db.add(collection)
        self.db.commit()
        self.db.refresh(collection)
        
        # Create collection directory
        collection_path = Path(settings.vector_store_path) / collection.id
        collection_path.mkdir(exist_ok=True)
        
        return collection
    
    def get_collections(self) -> List[Collection]:
        """Get all active collections."""
        return self.db.query(Collection).filter(Collection.is_active == True).all()
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Get collection by ID."""
        return self.db.query(Collection).filter(Collection.id == collection_id).first()
    
    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection and its documents."""
        collection = self.get_collection(collection_id)
        if not collection:
            return False
        
        # Delete documents
        documents = self.db.query(Document).filter(Document.collection_id == collection_id).all()
        for doc in documents:
            # Remove file
            if os.path.exists(doc.file_path):
                os.remove(doc.file_path)
        
        # Delete from database
        self.db.query(Document).filter(Document.collection_id == collection_id).delete()
        self.db.delete(collection)
        self.db.commit()
        
        # Remove vector store directory
        import shutil
        collection_path = Path(settings.vector_store_path) / collection_id
        if collection_path.exists():
            shutil.rmtree(collection_path)
        
        return True
    
    def add_document(self, collection_id: str, file_path: str, filename: str) -> Optional[Document]:
        """Add a document to a collection and process it."""
        collection = self.get_collection(collection_id)
        if not collection:
            return None
        
        # Calculate file hash
        with open(file_path, 'rb') as f:
            content_hash = hashlib.sha256(f.read()).hexdigest()
        
        # Create document record
        document = Document(
            collection_id=collection_id,
            filename=filename,
            original_filename=filename,
            file_path=file_path,
            file_size=os.path.getsize(file_path),
            mime_type="text/plain",  # You might want to detect this properly
            content_hash=content_hash
        )
        
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        
        # Process document with LlamaIndex
        try:
            self._process_document(collection_id, file_path)
            document.processed = True
            
            # Update collection document count
            collection.document_count += 1
            self.db.commit()
            
        except Exception as e:
            print(f"Error processing document: {e}")
            document.processed = False
            self.db.commit()
        
        return document
    
    def _process_document(self, collection_id: str, file_path: str):
        """Process a document and add it to the vector store."""
        # Load documents
        documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
        
        # Collection vector store path
        storage_path = Path(settings.vector_store_path) / collection_id
        
        # Create or load index
        if (storage_path / "docstore.json").exists():
            # Load existing index
            storage_context = StorageContext.from_defaults(persist_dir=str(storage_path))
            index = load_index_from_storage(storage_context)
            # Add new documents
            for doc in documents:
                index.insert(doc)
        else:
            # Create new index
            index = VectorStoreIndex.from_documents(documents)
        
        # Persist index
        index.storage_context.persist(persist_dir=str(storage_path))
    
    def query_collection(self, collection_id: str, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Query a collection's documents."""
        collection = self.get_collection(collection_id)
        if not collection:
            return {"error": "Collection not found"}
        
        storage_path = Path(settings.vector_store_path) / collection_id
        
        if not (storage_path / "docstore.json").exists():
            return {"error": "No documents in collection"}
        
        try:
            # Load index
            storage_context = StorageContext.from_defaults(persist_dir=str(storage_path))
            index = load_index_from_storage(storage_context)
            
            # Create query engine
            query_engine = index.as_query_engine(
                similarity_top_k=top_k,
                streaming=False
            )
            
            # Execute query
            response = query_engine.query(query)
            
            return {
                "response": str(response),
                "source_nodes": [
                    {
                        "text": node.text,
                        "score": node.score,
                        "metadata": node.metadata
                    }
                    for node in response.source_nodes
                ] if hasattr(response, 'source_nodes') else []
            }
            
        except Exception as e:
            return {"error": f"Query failed: {str(e)}"}


# Export service
__all__ = ["RAGService"]
