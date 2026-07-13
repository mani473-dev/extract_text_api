from fastapi import FastAPI, Request
from PyPDF2 import PdfReader
import io
import base64

app = FastAPI()


@app.post("/extract-text")
async def extract_text(request: Request):

    try:

        data = await request.json()

        base64_pdf = data["pdf_base64"]

        # Convert Base64 back to PDF bytes
        pdf_bytes = base64.b64decode(base64_pdf)

        pdf_file = io.BytesIO(pdf_bytes)

        reader = PdfReader(pdf_file)

        extracted_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                extracted_text += text + "\n"

        return {
            "status": "success",
            "extracted_text": extracted_text
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
