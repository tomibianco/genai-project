import os
import requests
from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse, PlainTextResponse
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
WPP_ACCESS_TOKEN = os.getenv("WPP_ACCESS_TOKEN")
WPP_ID = os.getenv("WPP_ID")
WPP_NUMBER = os.getenv("WPP_NUMBER")
WPP_VERIFY_TOKEN = os.getenv("WPP_VERIFY_TOKEN")

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "API de WhatsApp funcionando correctamente"}


@app.get("/webhook", response_class=PlainTextResponse)
def verify_webhook(
    hub_mode: str = Query(None),
    hub_challenge: str = Query(None),
    hub_verify_token: str = Query(None)
):
    try:
        if hub_mode and hub_verify_token:
            if hub_mode == "subscribe" and hub_verify_token == WPP_VERIFY_TOKEN:
                return hub_challenge
        raise Exception("Invalid request")
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


# Recibir mensajes de WhatsApp
@app.post("/webhook_2")
async def receive_message(request: Request):
    data = await request.json()

    if "entry" in data:
        for entry in data["entry"]:
            for change in entry["changes"]:
                if "messages" in change["value"]:
                    message = change["value"]["messages"][0]
                    sender_phone = message["from"]
                    text = message["text"]["body"]

                    print(f"📩 Mensaje recibido de {sender_phone}: {text}")
                    send_whatsapp_message(sender_phone, f"Recibí tu mensaje: {text}")

    return {"status": "ok"}

# Enviar mensajes de WhatsApp
def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v17.0/{WPP_NUMBER}/messages"
    headers = {"Authorization": f"Bearer {WPP_ACCESS_TOKEN}", "Content-Type": "application/json"}
    payload = {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": message}}

    response = requests.post(url, json=payload, headers=headers)
    print("✅ Mensaje enviado" if response.status_code == 200 else f"❌ Error: {response.text}")