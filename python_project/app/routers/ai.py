# filename: python_project/app/routers/ai.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import openai
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from app.schemas.ai import AIRequest, AIResponse
from app.core.database import get_db
from app.core.config import settings
from app.utils.roles import can_manage_users, can_create_announcements  # Adapt as needed

router = APIRouter(prefix="/ai", tags=["ai"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/generate", response_model=AIResponse)
def generate_text(
    payload: AIRequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Synchronous endpoint to call GPT-3.5-turbo to transform unstructured text 
    into a well-formatted announcement in German, French, and English.
    
    Requires a valid JWT token (role 'teacher', 'admin', or 'class_rep').
    Will sign the output with the teacher's name (from the token).
    """
    # 1. Decode JWT token to verify user role
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    role = decoded.get("role")
    if role not in ["teacher", "admin", "class_rep"]:
        raise HTTPException(status_code=403, detail="Not allowed to use AI endpoint")
    
    # Optional: get teacher's name from the token
    teacher_name = decoded.get("sub", "Teacher")

    # 2. Set OpenAI API key
    openai.api_key = settings.OPENAI_API_KEY
    if not openai.api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")

    # 3. Build the system prompt
# Adjusted system_prompt for the AI Assistant endpoint
    system_prompt = (
    "You are a helpful AI assistant for a school environment. "
    "You receive unstructured or minimal text from a teacher, and your goal is to produce "
    "an improved announcement or message in French, German, and English, always addressed to the parents. "
    "The French version should always appear first, followed by German and then English. "
    "Use clear paragraphs and line breaks. Label each section clearly as follows: 'Français', 'Deutsch', 'English'. "
    "Add a horizontal line (e.g., '---') between each language version to make them visually distinct. "
    "Ensure the grammar, spelling, and phrasing are correct and natural for each language. "
    "At the end of each message, include the appropriate team signature with 'F1' in every language, formatted as follows: \n\n"
    "Français: 'Cordialement, L'équipe de la F1'\n"
    "Deutsch: 'Mit freundlichen Grüßen, Das Team der F1'\n"
    "English: 'Kind regards, The Team of F1'\n\n"
    "Additionally, at the very beginning of your output, generate a single-line topic summary that captures the essence of the announcement. "
    "The topic line must strictly follow this format:\n"
    "Topic: [summary in French] | [summary in German] | [summary in English]\n\n"
    "Example email: \n\n"
    "Français:\nChers parents, \n\n"
    "Nous avons des poux dans la classe. Veuillez vérifier si votre enfant en a. "
    "Si c'est le cas, nous vous prions d'effectuer un premier traitement avec un produit de pharmacie "
    "avant le retour en classe (suivi d'un deuxième traitement après un délai recommandé). \n\n"
    "Cordialement,\nL'équipe de la F1\n\n"
    "---\n\n"
    "Deutsch:\nLiebe Eltern, \n\n"
    "wir haben Kopfläuse in der Klasse. Bitte überprüfen Sie, ob Ihr Kind Läuse oder Nissen hat. "
    "Falls vorhanden, bitten wir Sie, vor dem Schulbesuch eine Behandlung mit einem Läusemittel aus der Apotheke "
    "durchzuführen (und nach einer bestimmten Zeit eine weitere Behandlung). \n\n"
    "Mit freundlichen Grüßen,\nDas Team der F1\n\n"
    "---\n\n"
    "English:\nDear Parents, \n\n"
    "We have head lice in the class. Please check if your child has lice or nits. "
    "If so, we kindly ask you to treat your child with a lice treatment from the pharmacy before returning to school "
    "(and follow up with another treatment after a recommended interval). \n\n"
    "Kind regards,\nThe Team of F1\n\n"
    "Instructions for output: "
    "Ensure the output is well-formatted, with clear line breaks and distinct sections for each language. "
    "Always present the French version first, followed by German, and then English. "
    "Use a horizontal line (e.g., '---') to separate each language version. "
    "Do not combine multiple languages into one paragraph. "
    "Use professional and friendly language, and always include the correct team signature ('F1')."
)




    # Build user text: includes the raw user text
    user_text = (
        f"The teacher's name is {teacher_name}. "
        f"Here is the teacher's input:\n"
        f"{payload.input_text}"
    )

    # 4. Call the ChatCompletions API synchronously
    try:
        print("Calling openai.ChatCompletion.create with prompt:", user_text)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text},
            ],
            max_tokens=600,
            temperature=0.7,
        )
        print("Received ChatCompletion response:", response)
    except Exception as e:
        print("OpenAI API error:", e)
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {e}")
    
    # 5. Parse and return the AI's content
    ai_content = response["choices"][0]["message"]["content"].strip()
    return AIResponse(output_text=ai_content)
