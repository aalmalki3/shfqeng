import io
import requests
import pdfplumber
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class FileRequest(BaseModel):
    file_url: str

@app.post("/extract-text")
async def extract_pdf_text(request: FileRequest):
    try:
        # 1. تحميل الملف من الرابط
        response = requests.get(request.file_url)
        response.raise_for_status() # التأكد من أن الرابط يعمل
        
        # 2. فتح الملف من الذاكرة كـ Stream
        with pdfplumber.open(io.BytesIO(response.content)) as pdf:
            full_text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"
        
        # 3. إرجاع النص المستخرج
        if not full_text.strip():
            raise HTTPException(status_code=400, detail="الملف فارغ أو لا يحتوي على نص مقروء")
            
        return {
            "status": "success",
            "extracted_text": full_text[:5000], # سنحدد الطول المبدئي لضمان الأداء
            "character_count": len(full_text)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ أثناء معالجة الملف: {str(e)}")

# هذا الجزء لتشغيل التطبيق محلياً للتجربة
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
