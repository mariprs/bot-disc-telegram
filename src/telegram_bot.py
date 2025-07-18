#esse é o arquivo principal do bot do Telegram
#ele monitora mensagens em um chat específico e envia alertas para um webhook do Discord quando palavras-chave são detectadas
#para rodar, basta executar `python src/telegram_bot.py` no terminal (ou executar diretamente)

#BASIC USAGE
from pyrogram import Client, filters
import os
import requests
from dotenv import load_dotenv

#OCR
from PIL import Image
import pytesseract

#DB
from db.db import init_db, salvar_alerta

load_dotenv()
init_db()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE")
chat_id = int(os.getenv("CHAT_ID")) 
discord_webhook = os.getenv("DISCORD_WEBHOOK_URL")
keywords = os.getenv("KEYWORDS").split(",")

app = Client("my_session", api_id=api_id, api_hash=api_hash, phone_number=phone)
with app:
    print(" Sessão iniciada!")

@app.on_message(filters.text & filters.chat(chat_id)) 
# para pegar o chat_id, descomente a função abaixo
# def get_chat_id(client, message):
#     print("chat_id:", message.chat.id)

def alerta_discord(client, message):
    texto = message.text.lower()
    print(f"mensagem: {texto}")
    if any(palavra in texto for palavra in keywords):
        conteudo = f"Palavra-chave detectada em mensagem:\n\n**Texto:** {message.text}\n**De:** {message.from_user.first_name if message.from_user else 'Desconhecido'}"
        data = {"content": conteudo}
        response = requests.post(discord_webhook, json=data)
        salvar_alerta("texto", message.text, message.from_user.first_name if message.from_user else "Desconhecido")
        print("Alerta enviado para o Discord")

@app.on_message(filters.photo & filters.chat(chat_id))
def alerta_ocr(client, message):
    print("Img recebida")
    file_path = app.download_media(message.photo.file_id)
    if not file_path:
        print("Erro")
        return
    try:
        img = Image.open(file_path)
        texto = pytesseract.image_to_string(img, lang="por").lower()
        print(f"texto extraído: {texto}")

        if any (palavra in texto for palavra in keywords):
            if message.from_user:
                sender = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()
                sender_username = f"@{message.from_user.username}" if message.from_user.username else "Desconhecido"
                sender_is_bot = "Sim" if message.from_user.is_bot else "Não"
                conteudo = (
                    f"**Keyword encontrada em imagem:**\n```{texto}```\n"
                    f"**De:** {sender} ({sender_username}) - Bot: {sender_is_bot}"
                )
            else:
                conteudo = f"**Palavra-chave encontrada em imagem:**\n```{texto}```\n**De:** Usuário desconhecido"

            data = {"content": conteudo}
            response = requests.post(discord_webhook, json=data)
            salvar_alerta("imagem", texto, sender if message.from_user else "Desconhecido")
            print("Alerta enviado para o Discord")
    except Exception as e:  
        print(f"Erro ao processar imagem: {e}")
app.run()
