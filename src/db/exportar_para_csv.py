#arquivo opcional para exportar os dados do banco de dados para um arquivo CSV caso deseje realizar uma análise de dados
#basta rodar o comando `python src/db/exportar_para_csv.py` no terminal (ou executar diretamente)
import sqlite3
import csv
import os
from dotenv import load_dotenv

load_dotenv()

db_name = os.getenv("DB_NAME") 
csv_name = os.getenv("CSV_NAME")

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# fetching dados
cursor.execute("SELECT * FROM keywords")
dados = cursor.fetchall()

# nome das colunas
colunas = ["id", "tipo", "conteudo", "remetente", "timestamp"]

# exportando
with open(csv_name, mode="w", newline="", encoding="utf-8") as arquivo_csv:
    writer = csv.writer(arquivo_csv)
    writer.writerow(colunas)
    writer.writerows(dados)   
  

conn.close()
print(f"exportado para {csv_name}")