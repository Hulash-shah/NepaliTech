from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from Pipeline import process

app = FastAPI(title= "NepaliTech API")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
    
)


class TranslateRequest(BaseModel):
    text:str
    
    
class TranslateResponse(BaseModel):
    original : str
    nepali_translation : str
    simple_explanation_en : str
    simple_explanation_ne : str
    
    
@app.get("/health")
def health():
    return{"status": "ok"}




@app.post("/translate", response_model = TranslateResponse)
def translate(request: TranslateRequest):
    
    if not request.text.strip():
        raise HTTPException(
            status_code = 400,
            detail = "text cannot be empty"
        )
        
    result = process(request.text)
    
    return result