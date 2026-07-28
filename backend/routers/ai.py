from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
import models
from typing import Dict, Any, Optional
import json
from ai_agent import process_prompt
from file_parser import extract_text_from_file
import os
import shutil
from datetime import datetime

def write_audit_log(prompt: str, extracted_data: dict, reply: str):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "extracted_data": extracted_data,
        "ai_reply": reply
    }
    with open("audit_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

def get_val(data, key):
    if isinstance(data, dict):
        val = data.get(key)
    else:
        val = getattr(data, key, None)
    
    # Treat empty strings and None as completely equivalent
    if not val or str(val).strip() == "":
        return None
    return str(val).strip()

def check_for_duplicate(db: Session, payload: dict) -> bool:
    fields_to_check = [
        "customerName", "complaintSource", "productName", 
        "productStrengthGrade", "batchLotNumber", "manufacturingDate", 
        "expiryDate", "quantityAffected", "complaintDate", 
        "detailedComplaintDescription"
    ]
    
    candidates = db.query(models.Complaint).all()
    payload_id = payload.get("id")
    
    for c in candidates:
        # Avoid flagging a complaint as a duplicate of ITSELF during a simple edit
        if payload_id and str(c.id) == str(payload_id):
            continue
            
        # Check if all 10 fields match exactly
        is_match = True
        for field in fields_to_check:
            if get_val(payload, field) != get_val(c, field):
                is_match = False
                break
                
        if is_match:
            return True
                
    return False

router = APIRouter(
    prefix="/api/ai",
    tags=["AI Agent"]
)

@router.post("/process_prompt")
def api_process_prompt(
    prompt: str = Form(...),
    current_data: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    try:
        data_dict = json.loads(current_data) if current_data else None
        result = process_prompt(prompt, data_dict)
        
        write_audit_log(prompt, result["data"], result["reply"])
        
        # Check for duplicates
        is_duplicate = check_for_duplicate(db, result["data"])
        
        return {
            "ai_message": result["reply"],
            "extracted_data": result["data"],
            "is_duplicate": is_duplicate
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process_document")
def api_process_document(
    file: UploadFile = File(...),
    current_data: Optional[str] = Form(None),
    db: Session = Depends(get_db)
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
        
        write_audit_log(f"Processed Document: {file.filename}\nExtracted Text:\n{extracted_text}", result["data"], result["reply"])
        
        # Check for duplicates
        is_duplicate = check_for_duplicate(db, result["data"])
        
        return {
            "ai_message": result["reply"],
            "extracted_data": result["data"],
            "is_duplicate": is_duplicate
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
