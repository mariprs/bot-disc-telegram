#esse é um arquivo teste para verificar se o pytesseract está funcionando corretamente
#você pode rodar esse arquivo diretamente para testar a extração de texto de uma imagem
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = Image.open(r"src\test\ocr\img_teste.png")
texto = pytesseract.image_to_string(img, lang="por")
print(texto)