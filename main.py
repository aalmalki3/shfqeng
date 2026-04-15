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
        # 1. جلب الملف مع مهلة زمنية لضمان عدم التعليق
        response = requests.get(request.file_url, timeout=15)
        response.raise_for_status()
        
        # 2. فتح ملف الـ PDF من الذاكرة
        with pdfplumber.open(io.BytesIO(response.content)) as pdf:
            full_text = ""
            for page in pdf.pages:
                # 3. تحسين الاستخراج: x_tolerance يساعد في ربط الحروف العربية ببعضها
                # layout=True يحافظ على شكل الأسطر كما هي في السيرة الذاتية
                page_text = page.extract_text(layout=True, x_tolerance=1)
                if page_text:
                    full_text += page_text + "\n"
        
        # 4. تنظيف النص المستخرج
        # الذكاء الاصطناعي يهلوس إذا وجد نصوصاً فارغة أو رموزاً غريبة
        final_text = full_text.strip()
        
        if not final_text or len(final_text) < 10:
            raise HTTPException(status_code=400, detail="فشل المحرك في قراءة نص مفهوم، قد يكون الملف صورة (Scan)")
            
        return {
            "status": "success",
            "extracted_text": final_text[:12000] # مساحة كافية جداً للسير الذاتية الطويلة
        }
        
    except Exception as e:
        # إظهار الخطأ الحقيقي للمساعدة في التشخيص
        raise HTTPException(status_code=500, detail=f"Shafaq Engine Error: {str(e)}")
