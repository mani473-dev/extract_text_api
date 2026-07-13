from fastapi import FastAPI
import os
import io
import requests
import json
from PyPDF2 import PdfReader
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


baseURL = "https://iaaley-test.fa.ocs.oraclecloud.com"

username = os.getenv("username")
password = os.getenv("password")


def get_pdf_text(supplier_id):

    print("Entered Get Pdf text function")

    bc_pdf_text = {}

    url = f"{baseURL}/fscmRestApi/resources/11.13.18.05/suppliers/{supplier_id}/child/businessClassifications"


    response = requests.get(
        url,
        auth=HTTPBasicAuth(username, password),
        headers={"Accept": "application/json"}
    )

    response.raise_for_status()

    data = response.json()


    bc_links = {}


    for item in data.get("items", []):

        classification = item.get("Classification")

        bc_url = None


        for link in item.get("links", []):

            if link.get("rel") == "self":
                bc_url = link.get("href")
                break


        if bc_url:
            bc_links[classification] = bc_url + "/child/attachments"



    for attachment_name, link_url in bc_links.items():


        response = requests.get(
            link_url,
            auth=HTTPBasicAuth(username,password),
            headers={"Accept":"application/json"}
        )


        response.raise_for_status()

        attachment_data = response.json()


        if len(attachment_data.get("items", [])) != 0:


            links = attachment_data["items"][0]["links"]


            attachment_url = None


            for link in links:

                if link.get("name") == "FileContents":
                    attachment_url = link.get("href")
                    break



            if attachment_url is None:
                continue



            

            pdf_response = requests.get(
                attachment_url,
                auth=HTTPBasicAuth(username,password)
            )

            pdf_response.raise_for_status()


            pdf_bytes = pdf_response.content



            

            pdf_file = io.BytesIO(pdf_bytes)

            reader = PdfReader(pdf_file)


            text = ""


            for page in reader.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted + "\n"



            bc_pdf_text[attachment_name] = text



        else:

            print("No attachments found:", attachment_name)



    return bc_pdf_text



@app.post("/extract-supplier-document")
async def extract_supplier_document(request: dict):

    supplier_id = request.get("supplierId")


    if not supplier_id:
        return {
            "error":"supplierId is required"
        }


    result = get_pdf_text(supplier_id)


    return {
        "supplierId": supplier_id,
        "documents": result
    }
