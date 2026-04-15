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
    return {"message": "Shafaq Engine is Running Correctly"}

@app.post("/extract-text")
async def extract_pdf_text(request: FileRequest):
    try:
        # جلب الملف
        response = requests.get(request.file_url, timeout=10)
        response.raise_for_status()
        
        with pdfplumber.open(io.BytesIO(response.content)) as pdf:
            full_text = ""
            for page in pdf.pages:
                # تحسين الاستخراج: نستخدم layout=True لضمان الحفاظ على ترتيب الكلمات
                page_text = page.extract_text(layout=True, x_tolerance=2, y_tolerance=2)
                if page_text:
                    full_text += page_text + "\n"
        
        # تنظيف النص المستخرج من الرموز الغريبة التي تسبب الهلوسة
        cleaned_text = full_text.strip()
        
        if not cleaned_text:
            raise HTTPException(status_code=400, detail="فشل في استخراج نص مفهوم من الملف")
            
        return {
            "status": "success",
            "extracted_text": cleaned_text[:15000] # زدنا الحجم لضمان شمولية السيرة الذاتية
        }
    except Exception as e:
        # إذا كان الخطأ متعلقاً بالترميز، سنعرف هنا
        raise HTTPException(status_code=500, detail=f"Error in Shafaq Engine: {str(e)}")
