from fastapi import FastAPI, Request
from PyPDF2 import PdfReader
import io

app = FastAPI()


@app.post("/extract-text")
async def extract_text(request: Request):

    try:
       
        pdf_bytes = await request.body()

        
        pdf_file = io.BytesIO(pdf_bytes)

       
        pdf_reader = PdfReader(pdf_file)

        
        extracted_text = ""

        for page in pdf_reader.pages:
            page_text = page.extract_text()

            if page_text:
                extracted_text += page_text + "\n"

        # Step 5: Return the extracted text
        return {
            "status": "success",
            "extracted_text": extracted_text
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }