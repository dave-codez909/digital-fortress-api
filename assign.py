# from fastapi import FastAPI
# from pydantic import BaseModel
# import google.generativeai as genai
# import os

# API_KEY = os.environ.get("API_KEY")

# app = FastAPI(
#     title = "summary.ai",
#     description = "A simple API for summarizing pdf",
#     version = "1.0.0"
# )

# class Item(BaseModel):
#     summary:str

# @app.get("/")
# async def home():
#     return {"message": "Welcome to summary.ai API"}

# def sender(message: str):
#     genai.configure(api_key=API_KEY)
#     model = genai.GenerativeModel(model_name='gemini-1.5-flash')


# @app.post("/summarize")
# async def summarize(item: Item):
#     response = sender(summarize.summary)
#     return response



from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import google.generativeai as genai
import os
from io import BytesIO
from PyPDF2 import PdfReader


API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable is not set")

app = FastAPI(
    title="summary.ai",
    description="A simple API for summarizing PDFs",
    version="1.0.0"
)

class SummaryResponse(BaseModel):
    summary: str

def extract_text_from_pdf(file: BytesIO) -> str:
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def generate_summary(text: str) -> str:
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Please summarize the following text in a concise manner:\n\n{text[:10000]}"  # Limit input size
    response = model.generate_content(prompt)
    return response.text

@app.on_event("startup")
async def startup_event():
    genai.configure(api_key=API_KEY)

@app.get("/")
async def home():
    return {"message": "Welcome to summary.ai API"}

@app.post("/summarize", response_model=SummaryResponse)
async def summarize(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        return {"error": "Only PDF files are supported"}

    contents = await file.read()
    pdf_file = BytesIO(contents)
    text = extract_text_from_pdf(pdf_file)
    
    if not text.strip():
        return {"error": "The PDF appears to be empty or unreadable"}

    summary = generate_summary(text)
    return SummaryResponse(summary=summary)