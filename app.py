from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

import os
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# LangSmith Tracking
os.environ["LANGSMITH_TRACING"] = "True"
os.environ["LANGSMITH_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Actúa como data scientist experto con 20 años de experiencia"),
        ("user", "Question:{question}")
    ]
)

# Streamlit Framework
st.title("Langchain Demo 1.0")
input_text = st.text_input("¿En qué puedo ayudarte hoy?")

# Deepseek-R1 en local
# llm = ChatOllama(model="deepseek-r1:8b")

# OpenAI ChatGPT LLM
llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if input_text:
    st.write(chain.invoke({"question": input_text}))