import pypdf
import docx
import os

def extract_text_from_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    try:
        if ext == ".pdf":
            reader = pypdf.PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        elif ext == ".docx":
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif ext == ".txt":
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        elif ext == ".eml":
            import email
            from email import policy
            with open(file_path, 'rb') as f:
                msg = email.message_from_binary_file(f, policy=policy.default)
                body = msg.get_body(preferencelist=('plain'))
                text = body.get_content() if body else str(msg.get_payload())
        else:
            raise ValueError(f"Unsupported file format: {ext}")
            
    except Exception as e:
        return f"Error extracting text: {str(e)}"
        
    return text
