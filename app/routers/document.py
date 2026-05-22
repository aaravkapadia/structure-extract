# * POST /documents to upload a PDF
# * GET /documents/{id} and GET /documents (list)
# * PATCH /documents/{id} and DELETE /documents/{id}
# * File storage decision: local filesystem in container is fine for now (Railway has ephemeral disk caveat — flag this, deal with it in week 4 if it bites)
# * Download 200 clinical trial protocols from ClinicalTrials.gov, upload via your live API
# * End of week 1: working production system with real documents in it, no ML yet

import os
import shutil
from uuid import UUID, uuid4
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_session
from app.models.document import Document

router = APIRouter(prefix="/documents", tags=["documents"])

UPLOAD_DIR = "/app/data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("")
async def create_document(file: UploadFile = File(...), session: AsyncSession = Depends(get_session)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")
    stored_name = f"{uuid4()}.pdf"
    file_path = os.path.join(UPLOAD_DIR, stored_name)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    doc = Document(
        filename=file.filename,
        file_path=file_path,
        status="uploaded",
    )
    session.add(doc)
    await session.commit()
    await session.refresh(doc)
    return {
        "id": str(doc.id),
        "filename": doc.filename,
        "status": doc.status,
    }
    
@router.get("")
async def list_documents(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Document))
    docs = result.scalars().all()
    return [
        {"id": str(doc.id), "filename": doc.filename, "status": doc.status}
        for doc in docs
    ]

@router.get("/{doc_id}")
async def get_document(doc_id: UUID, session: AsyncSession = Depends(get_session)):
    doc = await session.get(Document, doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return {
        "id": str(doc.id),
        "filename": doc.filename,
        "status": doc.status,
        "uploaded_at": doc.uploaded_at.isoformat(),
    }
    
@router.patch("/{doc_id}")
async def update_document(doc_id: UUID, status: str | None = None, session: AsyncSession = Depends(get_session)):
    doc = await session.get(Document, doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    if status is not None:
        doc.status = status
    await session.commit()
    await session.refresh(doc)
    return {"id": str(doc.id), "filename": doc.filename, "status": doc.status}

@router.delete("/{doc_id}")
async def delete_document(doc_id: UUID, session: AsyncSession = Depends(get_session)):
    doc = await session.get(Document, doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    if doc.file_path and os.path.exists(doc.file_path):
        os.remove(doc.file_path)
    await session.delete(doc)
    await session.commit()
    return {"deleted": str(doc_id)}





