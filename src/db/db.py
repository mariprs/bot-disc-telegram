#esse é o arquivo principal do banco de dados
#ele cria a tabela keywords e define as funções para inicializar o banco e salvar alertas
# src/db/db.py
import sqlite3
from datetime import datetime
import os

DB_NAME = os.path.join(os.path.dirname(__file__), "keywords.db")

# Conexão reutilizável com timeout e concorrência segura
def get_connection():
    return sqlite3.connect(DB_NAME, timeout=10, check_same_thread=False)

def init_db():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT,
                conteudo TEXT,
                remetente TEXT,
                timestamp TEXT
            )
        ''')
        conn.commit()

def salvar_alerta(tipo, conteudo, remetente):
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO keywords (tipo, conteudo, remetente, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (tipo, conteudo, remetente, datetime.now().isoformat()))
            conn.commit()
    except sqlite3.OperationalError as e:
        print(f"[ERRO DB]: {e}")

def listar_alertas():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM keywords ORDER BY id DESC LIMIT 10')
        return c.fetchall()
