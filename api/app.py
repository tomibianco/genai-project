from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langserve import add_routes
from dotenv import load_dotenv
import uvicorn
import os


load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    title = "LangChain Server",
    version = "1.0"
)

model_chatgpt = ChatOpenAI(model="gpt-3.5-turbo-0125")
model_deepseek = ChatOllama(model="deepseek-r1:8b")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Actúa como vendedor experto con 20 años de experiencia"),
        ("user", "Question:{question}")
    ]
)

add_routes(
    app,
    prompt|model_chatgpt,
    path="/openai"
)

add_routes(
    app,
    prompt|model_deepseek,
    path="/deepseek"
)


if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)