#esse é o arquivo principal do banco de dados
#ele cria a tabela keywords e define as funções para inicializar o banco e salvar alertas
import sqlite3
from datetime import datetime

import os
DB_NAME = os.path.join(os.path.dirname(__file__), "keywords.db")

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
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
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO keywords (tipo, conteudo, remetente, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (tipo, conteudo, remetente, datetime.now().isoformat()))
        conn.commit()

def listar_alertas():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM keywords ORDER BY id DESC LIMIT 10')
        return c.fetchall()