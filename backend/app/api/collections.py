from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import os, shutil, uuid
from app.models.database import SessionLocal, DocumentCollection, Document
from app.services.rag_service import rag_service
from app.core.config import settings

router = APIRouter(prefix="/collections", tags=["Collections"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_collections(db: Session = Depends(get_db)):
    """Listar todas as coleções"""
    collections = db.query(DocumentCollection).filter(
        DocumentCollection.is_active == True
    ).all()
    return collections

@router.post("/")
def create_collection(name: str, description: str = "", db: Session = Depends(get_db)):
    """Criar nova coleção"""
    # Verificar se já existe
    existing = db.query(DocumentCollection).filter(
        DocumentCollection.name == name
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Coleção já existe")
    
    # Criar diretório
    collection_path = os.path.join(settings.DOCUMENTS_PATH, name)
    os.makedirs(collection_path, exist_ok=True)
    
    # Criar no banco
    collection = DocumentCollection(
        name=name,
        description=description
    )
    db.add(collection)
    db.commit()
    db.refresh(collection)
    
    return collection

@router.delete("/{collection_id}")
def delete_collection(collection_id: int, db: Session = Depends(get_db)):
    """Deletar coleção"""
    collection = db.query(DocumentCollection).filter(
        DocumentCollection.id == collection_id
    ).first()
    
    if not collection:
        raise HTTPException(status_code=404, detail="Coleção não encontrada")
    
    # Deletar documentos do banco
    db.query(Document).filter(Document.collection_id == collection_id).delete()
    
    # Deletar diretório
    collection_path = os.path.join(settings.DOCUMENTS_PATH, collection.name)
    if os.path.exists(collection_path):
        shutil.rmtree(collection_path)
    
    # Deletar índice
    rag_service.delete_collection_index(collection.name)
    
    # Deletar coleção
    db.delete(collection)
    db.commit()
    
    return {"message": "Coleção deletada com sucesso"}

@router.post("/{collection_id}/documents")
async def upload_documents(
    collection_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """Upload de documentos"""
    collection = db.query(DocumentCollection).filter(
        DocumentCollection.id == collection_id
    ).first()
    
    if not collection:
        raise HTTPException(status_code=404, detail="Coleção não encontrada")
    
    collection_path = os.path.join(settings.DOCUMENTS_PATH, collection.name)
    uploaded_files = []
    
    for file in files:
        # Gerar nome único
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(collection_path, unique_filename)
        
        # Salvar arquivo
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Salvar no banco
        document = Document(
            collection_id=collection_id,
            filename=unique_filename,
            original_name=file.filename,
            file_path=file_path,
            file_size=len(content),
            content_type=file.content_type
        )
        db.add(document)
        uploaded_files.append(file.filename)
    
    # Atualizar contador
    collection.document_count = db.query(Document).filter(
        Document.collection_id == collection_id
    ).count()
    
    db.commit()
    
    return {
        "message": f"{len(uploaded_files)} arquivos enviados",
        "files": uploaded_files
    }

@router.post("/{collection_id}/index")
def create_index(collection_id: int, db: Session = Depends(get_db)):
    """Criar índice para coleção"""
    collection = db.query(DocumentCollection).filter(
        DocumentCollection.id == collection_id
    ).first()
    
    if not collection:
        raise HTTPException(status_code=404, detail="Coleção não encontrada")
    
    collection_path = os.path.join(settings.DOCUMENTS_PATH, collection.name)
    
    success = rag_service.create_collection_index(
        collection.name, 
        collection_path
    )
    
    if success:
        # Marcar documentos como indexados
        db.query(Document).filter(
            Document.collection_id == collection_id
        ).update({"is_indexed": True})
        db.commit()
        
        return {"message": "Índice criado com sucesso"}
    else:
        raise HTTPException(status_code=500, detail="Erro ao criar índice")

@router.post("/{collection_id}/query")
def query_collection(
    collection_id: int, 
    query: str, 
    top_k: int = 3,
    db: Session = Depends(get_db)
):
    """Fazer consulta na coleção"""
    collection = db.query(DocumentCollection).filter(
        DocumentCollection.id == collection_id
    ).first()
    
    if not collection:
        raise HTTPException(status_code=404, detail="Coleção não encontrada")
    
    response = rag_service.query_collection(collection.name, query, top_k)
    
    return {
        "collection": collection.name,
        "query": query,
        "response": response
    }
