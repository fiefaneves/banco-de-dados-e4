#Consulta que devolve os chocolates sem bilhete dourado
import sqlite3

conn = sqlite3.connect("fabrica_chocolate.db")
cursor = conn.cursor()

cursor.execute(
"""
    SELECT CHOCO.ID_PRODUTO
    FROM CHOCOLATE CHOCO
    WHERE NOT EXISTS (
        SELECT 1
        FROM BILHETEDOURADO B 
        WHERE B.ID_CHOCOLATE = CHOCO.ID_PRODUTO
    )
"""
)

resultado = cursor.fetchall()

for linha in resultado:
    print(linha)


conn.close()