import requests
import streamlit as st

def get_openai_response(input_text):
    response=requests.post("http://localhost:8000/openai/invoke",
    json={"input":{"question":input_text}})

    return response.json()["output"]["content"]

def get_deepseek_response(input_text):
    response=requests.post("http://localhost:8000/deepseek/invoke",
    json={"input":{"question":input_text}})

    return response.json()["output"]["content"]

st.title('Langchain Demo API')
input_text_1 = st.text_input("Hola, soy ChatGPT, ¿En qué puedo ayudarte?")
input_text_2 = st.text_input("Hola, soy Deepseek, ¿En qué puedo ayudarte?")

if input_text_1:
    st.write(get_openai_response(input_text_1))

if input_text_2:
    st.write(get_deepseek_response(input_text_2))