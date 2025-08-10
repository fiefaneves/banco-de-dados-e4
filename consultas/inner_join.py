import sqlite3

conn = sqlite3.connect('fabrica_chocolate.db')
cursor = conn.cursor()

# Todos os chocolates e os nomes dos seus respectivos ingredientes
cursor.execute("""
    SELECT
        C.Nome AS Nome_Chocolate,
        I.Nome AS Nome_Ingrediente
    FROM Chocolate C
    INNER JOIN USA U ON C.ID = U.ID_CHOCOLATE
    INNER JOIN Ingrediente I ON U.COD_INGREDIENTE = I.COD
    ORDER BY C.Nome, I.Nome;
""")

resultados = cursor.fetchall()

for linha in resultados:
    print(linha)

conn.close()