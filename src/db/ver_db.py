#esse arquivo pode ser substituído por um comando direto no terminal
#para ver os dados do banco, use:
# sqlite3 src/db/alertas.db
# e depois:
# SELECT * FROM alertas;
# ou use um visualizador de banco de dados SQLite, como o DB Browser for SQLite
import sqlite3

con = sqlite3.connect("src/db/keywords.db")
cur = con.cursor()

cur.execute("SELECT * FROM keywords")
rows = cur.fetchall()

for row in rows:
    print(row)

con.close()