from pyrogram import Client, filters
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE")
discord_webhook = os.getenv("DISCORD_WEBHOOK")
keywords = ["senha", "cpf", "rg"] 

app = Client("my_session", api_id=api_id, api_hash=api_hash, phone_number=phone)

with app:
    print(" Sessão iniciada!")
@app.on_message(filters.text)
def alerta_discord(client, message):
    texto = message.text.lower()
    if any(palavra in texto for palavra in keywords):
        conteudo = f"Palavra-chave detectada em mensagem:\n\n**Texto:** {message.text}\n**De:** {message.from_user.first_name if message.from_user else 'Desconhecido'}"
        data = {"content": conteudo}
        response = requests.post(discord_webhook, json=data)
        print("Alerta enviado para o Discord")

app.run()