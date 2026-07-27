from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import Dict, Any, Optional
import json
from ai_agent import process_prompt
from file_parser import extract_text_from_file
import os
import shutil

router = APIRouter(
    prefix="/api/ai",
    tags=["AI Agent"]
)

@router.post("/process_prompt")
def api_process_prompt(
    prompt: str = Form(...),
    current_data: Optional[str] = Form(None)
):
    try:
        data_dict = json.loads(current_data) if current_data else None
        result = process_prompt(prompt, data_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process_document")
def api_process_document(
    file: UploadFile = File(...),
    current_data: Optional[str] = Form(None)
):
    try:
        # Save temp file
        os.makedirs("temp_uploads", exist_ok=True)
        file_path = f"temp_uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Extract text
        extracted_text = extract_text_from_file(file_path)
        
        # Clean up
        os.remove(file_path)
        
        if extracted_text.startswith("Error"):
            raise HTTPException(status_code=400, detail=extracted_text)
            
        # Process extracted text with AI
        prompt = f"Extract complaint details from the following document text:\n\n{extracted_text}"
        data_dict = json.loads(current_data) if current_data else None
        
        result = process_prompt(prompt, data_dict)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
