# Bot para Monitoramento no Telegram -> Envio no Discord

Este projeto é um bot em Python que monitora mensagens em tempo real no Telegram e dispara alertas via webhook para um canal do Discord sempre que detecta palavras-chave sensíveis.

## ✨ Funcionalidades

- Monitoramento de mensagens em texto em um chat específico.
- Detecção de palavras-chave sensíveis.
- Envio de alertas formatados no Discord via webhook.
- Suporte a OCR (extração de texto de imagens enviadas no chat).
- Saving dos alertas em banco de dados local (`SQLite`).
- Criação de `.csv` para data analysis (extra!).
- Arquivo `cloudbuild.yaml` para deploy via Google Cloud Build.

## ⚙️ Configuração

1. Clone o repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Crie um arquivo `.env` com conteúdo de acordo com o arquivo .env.example

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
python src/test/ocr/test_ocr.py
```

## 🎲 Criação da DB && Export

O banco SQLite (`keywords.db`) é gerado automaticamente ao rodar o bot. Para a db funcionar, o trigger da keyword precisa ser ativado (ou seja, é preciso que uma das keywords seja digitada no grupo do telegram).
Caso deseje visualizar a table, rode o arquivo `src/db/ver_db.py`.
Para exportar para csv, basta rodar o arquivo `src/db/exportar_para_csv.py`.

## 🏗️ CI/CD

Este repositório inclui um `cloudbuild.yaml` para facilitar o deploy no Cloud Build do GCP.
O repositório contém dois arquivos de requirements.
O primeiro, `src/requirements.txt` possui tudo que você pode precisar localmente.
O segundo, `requirements-build.txt` é usado exclusivamente para o deploy. Como criei apenas o .yaml com a intenção de testar o projeto principal, evitei dependências desnecessárias associadas a outras features para consumir menos tempo e recursos em Cloud.
Para testar localmente, estando autenticado no gcloud (`gcloud auth login`) e com o projeto ativo no GCP, com o Cloud Build ativo e autorização de admin no bucket do projeto, use:

```bash
gcloud builds submit . --config=cloudbuild.yaml
```

Para configurar as variáveis, é necessário rodar
**Importante**: sem as variáveis de ambiente configuradas (seja através de `gcloud secrets` ou Dockerfile) e e seu project_id, o `cloudbuild.yaml` não funcionará. É necessário validar no Secret Manager do GCP e no próprio gerenciador dar permissão ao user do Cloud Build.
Será necessário armazenar o token recebido pelo telegram no .env para que a my_session.session seja iniciada e a build rode corretamente.

## 🎥 Demonstração básica

Veja a demonstração básica do bot em ação:

📽️ [Demonstração básica](./src/assets/demonstracao_funcionalidade_basica.gif)

## Dificuldades comuns

- **Erro de path no pytesseract**: Verifique o caminho correto para o executável do Tesseract. Use barra invertida `\` no Windows.
- **Erro ao carregar idioma 'por'**: Baixe o arquivo `por.traineddata` do [repositório oficial](https://github.com/tesseract-ocr/tessdata) e coloque na pasta `tessdata`.
- **Webhook não envia alerta**: Verifique se o nome da variável no `.env` está igual no código (`DISCORD_WEBHOOK_URL`).
- **Mensagem de erro 'NoneType is not iterable'**: Ocorre quando `KEYWORDS` está mal formatado. Corrija no `.env` como uma string simples separada por vírgulas (sem aspas).

## 🧠 Ideias para futura implementação

- Adicionar prioridades visuais baseadas em cada palavra-chave.
- Implementar envio da imagem original para o Discord.
- Implementar testes unitários automatizados para garantir que, de acordo com o aumento de complexidade do projeto, tudo estará funcionando conforme o esperado.
