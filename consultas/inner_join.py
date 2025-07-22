import sqlite3

conn = sqlite3.connect('fabrica_chocolate.db')
cursor = conn.cursor()

# Todos os produtos e os nomes dos seus respectivos ingredientes
cursor.execute('''
    SELECT
        P.NOME AS Nome_Produto,
        I.NOME AS Nome_Ingrediente
    FROM
        Produto P
    INNER JOIN
        USA U ON P.ID = U.ID_PRODUTO
    INNER JOIN
        Ingrediente I ON U.COD_INGREDIENTE = I.COD;
''')

resultados = cursor.fetchall()

for linha in resultados:
    print(linha)

conn.close()