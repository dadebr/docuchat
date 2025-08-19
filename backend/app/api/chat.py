from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.rag_service import rag_service
from app.models.database import SessionLocal, DocumentCollection
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter(prefix="/chat", tags=["Chat"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ChatRequest(BaseModel):
    collection_id: int
    message: str
    top_k: Optional[int] = 3

class ChatResponse(BaseModel):
    response: str
    collection_name: str
    sources_count: int

@router.post("/", response_model=ChatResponse)
def chat_with_collection(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """Conversar com uma coleção de documentos"""
    # Verificar se a coleção existe
    collection = db.query(DocumentCollection).filter(
        DocumentCollection.id == request.collection_id
    ).first()
    
    if not collection:
        raise HTTPException(status_code=404, detail="Coleção não encontrada")
    
    # Realizar consulta RAG
    response = rag_service.query_collection(
        collection_name=collection.name,
        query=request.message,
        top_k=request.top_k
    )
    
    return ChatResponse(
        response=response,
        collection_name=collection.name,
        sources_count=request.top_k
    )

@router.get("/health")
def health_check():
    """Verificar se o serviço de chat está funcionando"""
    return {"status": "healthy", "service": "chat"}

@router.get("/collections/{collection_id}/status")
def get_collection_status(
    collection_id: int,
    db: Session = Depends(get_db)
):
    """Verificar status de uma coleção para chat"""
    collection = db.query(DocumentCollection).filter(
        DocumentCollection.id == collection_id
    ).first()
    
    if not collection:
        raise HTTPException(status_code=404, detail="Coleção não encontrada")
    
    # Verificar se o índice existe
    index = rag_service.load_collection_index(collection.name)
    
    return {
        "collection_name": collection.name,
        "is_indexed": index is not None,
        "document_count": collection.document_count,
        "ready_for_chat": index is not None
    }
