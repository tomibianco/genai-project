from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv

# Cargar API Key de OpenAI desde .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Inicializar FastAPI
app = FastAPI()

# Modelo de mensaje entrante
class Message(BaseModel):
    sender: str
    message: str

# Inicializar modelo de IA con LangChain + OpenAI
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7, openai_api_key=OPENAI_API_KEY)

@app.post("/whatsapp-reply/")
async def reply_message(msg: Message):
    try:
        # Construir el prompt
        messages = [
            SystemMessage(content="Eres un vendedor experto que se dedica a vender en mi empresa de servicios de inteligencia artificial, debes preguntarle al cliente que necesita relacionado al tema"),
            HumanMessage(content=msg.message)
        ]

        # Generar respuesta con LangChain
        response = llm(messages)

        return {"reply": response.content}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))