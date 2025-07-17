# Bot para Monitoramento no Telegram -> Envio no Discord

Este projeto é um bot em Python que monitora mensagens em tempo real no Telegram e dispara alertas via webhook para um canal do Discord sempre que detecta palavras-chave sensíveis.

## ✨ Funcionalidades

- Monitoramento de mensagens em texto em um chat específico.
- Detecção de palavras-chave sensíveis.
- Envio de alertas formatados no Discord via webhook.
- Suporte a OCR (extração de texto de imagens enviadas no chat).

## ⚙️ Configuração

1. Clone o repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Crie um arquivo `.env` com o seguinte conteúdo:

```env
API_ID=...
API_HASH=...
PHONE=+55...
CHAT_ID=...
DISCORD_WEBHOOK_URL=...
KEYWORDS=senha,cpf,rg,cvv,código de segurança,agência,token,api,acesso,login,deleta depois,isso some,não salva,endereço,cep
```

4. Certifique-se de ter o Tesseract OCR instalado e com o idioma `por` disponível.

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

Pode ser necessário baixar o idioma manualmente em: https://tesseract-ocr.github.io/tessdoc/Data-Files

````
Para verificar se o tesseract tem o idioma desejado é necessário rodar
```tesseract --list-langs
````

## ▶️ Execução

Para rodar o bot:

```bash
python src/telegram_bot.py
```

## 🧪 Teste OCR manual

Há um arquivo de teste para verificar se o OCR está funcionando corretamente com uma imagem exemplo:

```bash
python src/test/test_ocr.py
```

## Dificuldades e Soluções

- **Erro de path no pytesseract**: Verifique o caminho correto para o executável do Tesseract. Use barra invertida `\` no Windows.
- **Erro ao carregar idioma 'por'**: Baixe o arquivo `por.traineddata` do [repositório oficial](https://github.com/tesseract-ocr/tessdata) e coloque na pasta `tessdata`.
- **Webhook não envia alerta**: Verifique se o nome da variável no `.env` está igual no código (`DISCORD_WEBHOOK_URL`).
- **Mensagem de erro 'NoneType is not iterable'**: Ocorre quando `KEYWORDS` está mal formatado. Corrija no `.env` como uma string simples separada por vírgulas (sem aspas).

## To Do

- Salvar mensagens e remetentes em banco de dados
- Criar `cloudbuild.yaml` para deploy automático no GCP
- Gravar vídeo demonstrativo
- Implementar envio da imagem no alerta do Discord
- Adicionar prioridades visuais baseadas nas palavras-chave
