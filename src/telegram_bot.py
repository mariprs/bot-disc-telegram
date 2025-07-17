#BASIC USAGE
from pyrogram import Client, filters
import os
import requests
from dotenv import load_dotenv

#OCR
from PIL import Image
import pytesseract

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE")
chat_id = int(os.getenv("CHAT_ID")) 
discord_webhook = os.getenv("DISCORD_WEBHOOK_URL")
keywords = os.getenv("KEYWORDS").split(",")

app = Client("my_session")
with app:
    print(" Sessão iniciada!")

@app.on_message(filters.text & filters.chat(chat_id)) 
# para pegar o chat_id, descomente a função abaixo
# def get_chat_id(client, message):
#     print("chat_id:", message.chat.id)

def alerta_discord(message):
    texto = message.text.lower()
    print(f"mensagem: {texto}")
    if any(palavra in texto for palavra in keywords):
        conteudo = f"Palavra-chave detectada em mensagem:\n\n**Texto:** {message.text}\n**De:** {message.from_user.first_name if message.from_user else 'Desconhecido'}"
        data = {"content": conteudo}
        response = requests.post(discord_webhook, json=data)
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
            conteudo = f"**Keyword encontrada em imagem:**\n ```{texto}```\n**De:** {message.from_user.first_name if message.from_user else 'User desconhecido'}"
            data = {"content": conteudo}
            response = requests.post(discord_webhook, json=data)
            print("Alerta enviado para o Discord")
    except Exception as e:  
        print(f"Erro ao processar imagem: {e}")
app.run()

# to do: save in db
# to do: .yaml for cloud upload
# to do: film for readme
# to do: extra surprise winkwink :^) (basically a way to save data from the message sender)
# to do: check if possible to send over image to discord
# to do: different priorities for different keywords