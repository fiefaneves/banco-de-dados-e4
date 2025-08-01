#Consulta que devolve os responsáveis sem crianças
import sqlite3

conn = sqlite3.connect("fabrica_chocolate.db")
cursor = conn.cursor()

cursor.execute(
"""
    SELECT R.NOME
    FROM RESPONSAVEL R
    WHERE NOT EXISTS (
        SELECT *
        FROM CRIANCA C
        WHERE C.CPF_RESPONSAVEL = R.CPF
    )
"""
)

resultado = cursor.fetchall()

print("=" * 50)
print("    RESPONSÁVEIS SEM CRIANÇAS")
print("=" * 50)

if resultado:
    for i, linha in enumerate(resultado, 1):
        print(f"{i:2d}. Nome: {linha[0]}")
    print(f"\nTotal: {len(resultado)} responsáveis sem crianças")
else:
    print("Todos os responsáveis possuem crianças!")

print("=" * 50)

conn.close()