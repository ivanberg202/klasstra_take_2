# filename: python_project/app/schemas/ai.py
from pydantic import BaseModel

class AIRequest(BaseModel):
    input_text: str

class AIResponse(BaseModel):
    output_text: str
