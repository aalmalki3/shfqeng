import io
import requests
import pdfplumber
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class FileRequest(BaseModel):
    file_url: str

@app.get("/")
async def root():
    return {"message": "Shafaq Engine is Running"}

@app.post("/extract-text")
async def extract_pdf_text(request: FileRequest):
    try:
        response = requests.get(request.file_url)
        response.raise_for_status()
        
        with pdfplumber.open(io.BytesIO(response.content)) as pdf:
            full_text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"
        
        if not full_text.strip():
            raise HTTPException(status_code=400, detail="الملف فارغ")
            
        return {
            "status": "success",
            "extracted_text": full_text[:10000] # زدنا المساحة لتستوعب تقارير أطول
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
