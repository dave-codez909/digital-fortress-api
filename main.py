import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

class Message(BaseModel):
    message: str


app = FastAPI(
    title="DFI Ai",
    description="Digital Fortress AI powered API for customer support",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Welcome to Digital Fortress Institute AI powered API Support for customer "}

API_KEY = os.environ.get("API_KEY")




def sender(message: str):
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    prompt = f"""
        you are our ai assitant at digital fortress limited also known as DFI located at sasha road Dopemu Lagos Nigeria,
        We are here to provide digital skill trainig is various are of tech such as Web development Python for Beginners and Advance, Data science 
        cyber security, networking and UIUX, digital marketing and Ethical hacking and Mutltimedia
        here ae our contacts for more enquirie
        first phone number :+2349092337358
        second phone number : 2349092349810
        email 1 :  anthony@digitalfortressltd.com
        email 2 :  akowonjo@digitalfortressltd.com
        website : www.digitalfortressltd.com
        {message}"""
    response = model.generate_content(prompt)

    # Print the response
    return response.text


@app.post("/message")
def message(message: Message):
    response = sender(message.message)
    return response



