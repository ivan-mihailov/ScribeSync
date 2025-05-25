from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentContentFormat
from dotenv import load_dotenv
import os

load_dotenv()
# Replace with your Azure endpoint and key
endpoint = os.getenv("AZURE_OCR_ENDPOINT")
key = os.getenv("AZURE_OCR_KEY")

# Path to your local document file (PDF, JPG, PNG, etc.)
document_path = "assets/May_2025_with_handwriting_ScribeSync_Logo_Ticked_pages_1_3.pdf"

# Create the client
document_intelligence_client  = DocumentIntelligenceClient(
     endpoint=endpoint,
     credential=AzureKeyCredential(key)
)

with open(document_path, "rb") as f:
    poller = document_intelligence_client.begin_analyze_document(
        model_id="prebuilt-layout",  # Use 'prebuilt-layout' for Markdown
        body=f,
        output_content_format=DocumentContentFormat.MARKDOWN
    )
    result = poller.result()

# Output results in Markdown
print("# Document Text\n")
print(result.content)

# for page_num, page in enumerate(result.pages, start=1):
#      print(f"## Page {page_num}\n")
#      for line in page.lines:
#           print(line.content)
#      print("\n---\n")
