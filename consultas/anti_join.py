import sqlite3

conn = sqlite3.connect("fabrica_chocolate.db")
cursor = conn.cursor()

cursor.execute(
"""
    SELECT I.COD, I.Nome, I.Marca
    FROM Ingrediente I
    WHERE NOT EXISTS (
        SELECT *
        FROM USA U
        WHERE U.COD_INGREDIENTE = I.COD
    )
    ORDER BY I.Nome;
"""
)

resultado = cursor.fetchall()

print("Ingredientes não utilizados:")

if resultado:
    for i, linha in enumerate(resultado, 1):
        print(f"{i:2d}. COD: {linha[0]}, Nome: {linha[1]}, Marca: {linha[2]}")
else:
    print("Todos os ingredientes estão sendo utilizados!")

conn.close()