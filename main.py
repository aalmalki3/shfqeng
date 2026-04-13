import io
import requests
import pdfplumber
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from xhtml2pdf import pisa
from jinja2 import Template

app = FastAPI()

# قالب HTML أنيق للتقرير
HTML_TEMPLATE = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <style>
        @page { size: A4; margin: 1cm; }
        body { font-family: 'Arial', sans-serif; color: #333; line-height: 1.6; background-color: #f4f7f6; }
        .header { background-color: #1a2a6c; color: white; padding: 20px; text-align: center; border-radius: 10px; }
        .section { background: white; padding: 15px; margin-top: 20px; border-left: 5px solid #1a2a6c; border-radius: 5px; }
        h1 { margin: 0; font-size: 24px; }
        h2 { color: #1a2a6c; border-bottom: 1px solid #ddd; padding-bottom: 5px; }
        .footer { text-align: center; font-size: 10px; color: #777; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>تقرير شفق الاستراتيجي لتطوير المسار المهني</h1>
        <p>تحليل ذكي مخصص بناءً على معايير سوق العمل السعودي</p>
    </div>
    
    <div class="section">
        <h2>تحليل السيرة الذاتية (ATS)</h2>
        <p>{{ analysis_content }}</p>
    </div>

    <div class="footer">
        تم توليد هذا التقرير بواسطة منصة شفق الذكية - جميع الحقوق محفوظة
    </div>
</body>
</html>
"""

class PDFRequest(BaseModel):
    analysis_text: str

@app.post("/generate-pdf")
async def generate_pdf(request: PDFRequest):
    try:
        # دمج النص في قالب HTML
        template = Template(HTML_TEMPLATE)
        html_content = template.render(analysis_content=request.analysis_text)
        
        # تحويل HTML إلى PDF في الذاكرة
        pdf_buffer = io.BytesIO()
        pisa_status = pisa.CreatePDF(io.BytesIO(html_content.encode("UTF-8")), dest=pdf_buffer)
        
        if pisa_status.err:
            raise HTTPException(status_code=500, detail="خطأ في توليد ملف PDF")
            
        pdf_buffer.seek(0)
        return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={
            "Content-Disposition": "attachment; filename=Shafaq_Report.pdf"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# أضف دالة extract_text السابقة هنا أيضاً ليبقى السيرفر يعمل بالوظيفتين
