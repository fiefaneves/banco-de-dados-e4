#Consulta que devolve todos os CPFs do schema
import sqlite3

conn = sqlite3.connect("fabrica_de_chocolate.db")
cursor = conn.cursor()

cursor.execute(
"""
    SELECT CPF
    FROM RESPONSAVEL 
        UNION
    SELECT CPF
    FROM CRIANCA 
    ORDER BY CPF
"""
)

conn.commit()
conn.close()