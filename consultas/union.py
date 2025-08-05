#Consulta que devolve todos os CPFs do schema
import sqlite3

conn = sqlite3.connect("fabrica_chocolate.db")
cursor = conn.cursor()

cursor.execute(
"""
    SELECT CPF_RESPONSAVEL as CPF, 'Responsavel' as Tipo
    FROM Responsavel_Crianca
    UNION
    SELECT CPF_CRIANCA as CPF, 'Crianca' as Tipo
    FROM Responsavel_Crianca
    UNION
    SELECT CPF, 'Funcionario' as Tipo
    FROM Funcionario
    ORDER BY CPF;
"""
)

resultado = cursor.fetchall()

print("     TODOS OS CPFs DO SISTEMA")

if resultado:
    for i, linha in enumerate(resultado, 1):
        print(f"{i:2d}. {linha[0]} {linha[1]}")
    print(f"\nTotal: {len(resultado)} CPFs encontrados")
else:
    print("Nenhum CPF encontrado no sistema.")

conn.close()