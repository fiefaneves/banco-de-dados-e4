#Consulta que devolve todos os CPFs do schema
import sqlite3

conn = sqlite3.connect("fabrica_chocolate.db")
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

resultado = cursor.fetchall()

print("=" * 40)
print("     TODOS OS CPFs DO SISTEMA")
print("=" * 40)

if resultado:
    for i, linha in enumerate(resultado, 1):
        print(f"{i:2d}. {linha[0]}")
    print(f"\nTotal: {len(resultado)} CPFs encontrados")
else:
    print("Nenhum CPF encontrado no sistema.")

print("=" * 40)

conn.close()