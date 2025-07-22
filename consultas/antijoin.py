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

print("=" * 50)
print("    CHOCOLATES SEM BILHETE DOURADO")
print("=" * 50)

if resultado:
    for i, linha in enumerate(resultado, 1):
        print(f"{i:2d}. Produto ID: {linha[0]}")
    print(f"\nTotal: {len(resultado)} chocolates sem bilhete dourado")
else:
    print("Todos os chocolates possuem bilhete dourado!")

print("=" * 50)

conn.close()