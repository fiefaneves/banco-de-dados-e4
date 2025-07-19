#Consulta que devolve os chocolates sem bilhete dourado
import sqlite3

conn = sqlite3.connect("fabrica_de_chocolate.db")
cursor = conn.cursor()

cursor.execute(
"""
    SELECT CHOCO.NOME
    FROM CHOCOLATE CHOCO
    WHERE NOT EXISTS (
        SELECT 1
        FROM BILHETE DOURADO B 
        WHERE B.ID_CHOCOLATE = CHOCO.ID_PRODUTO
    )
"""
)

conn.commit()
conn.close()