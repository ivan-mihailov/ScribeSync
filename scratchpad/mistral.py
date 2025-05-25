import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()  # This line loads the .env file
api_key = os.getenv("MISTRAL_API_KEY")  # Use os.getenv instead of os.environ

# Check if the API key is None
if api_key is None:
    raise ValueError("MISTRAL_API_KEY is not set. Please ensure it is saved in the Secrets section.")

client = Mistral(api_key=api_key)

filename = "assets/May_2025_with_handwriting_ScribeSync_Logo_Ticked_pages_1_3.pdf"
uploaded_pdf = client.files.upload(
    file={
        "file_name": filename,
        "content": open(filename, "rb"),
    },
    purpose="ocr"
)

signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)

ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document={
        "type": "document_url",
        "document_url": signed_url.url
    },
    include_image_base64=False
)

print(ocr_response)
