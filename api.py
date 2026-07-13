from fastapi import FastAPI, Request
from PyPDF2 import PdfReader
import io

app = FastAPI()


@app.post("/extract-text")
async def extract_text(request: Request):

    try:

        pdf_bytes = await request.body()

        # Temporary debugging
        print("PDF size:", len(pdf_bytes))
        print("First 50 bytes:", pdf_bytes[:50])
        print("Last 50 bytes:", pdf_bytes[-50:])

        pdf_file = io.BytesIO(pdf_bytes)

        pdf_reader = PdfReader(pdf_file)

        extracted_text = ""

        for page in pdf_reader.pages:
            page_text = page.extract_text()

            if page_text:
                extracted_text += page_text + "\n"

        return {
            "status": "success",
            "extracted_text": extracted_text
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e),
            "pdf_size": len(pdf_bytes) if 'pdf_bytes' in locals() else None,
            "first_50_bytes": str(pdf_bytes[:50]) if 'pdf_bytes' in locals() else None,
            "last_50_bytes": str(pdf_bytes[-50:]) if 'pdf_bytes' in locals() else None
        }
