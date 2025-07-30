import sqlite3
conn = sqlite3.connect("fabrica_chocolate.db")
cursor = conn.cursor()

#Subconsulta Escalar: Contagem de Ingredientes por Produto
sql_scalar = """
        C.Nome as Nome_Chocolate,
        (SELECT COUNT(*) FROM USA U WHERE U.ID_CHOCOLATE = C.ID) as Qtd_Ingredientes
    FROM Chocolate C
    ORDER BY Qtd_Ingredientes DESC, C.Nome;
"""
    

cursor.execute(sql_scalar)
resultados = cursor.fetchall()

if resultados:
    print("Resultado:")
    for nome, qtd_ingredientes in resultados:
        print(f"  - Produto: '{nome}', Quantidade de Ingredientes: {qtd_ingredientes}")
else:
    print("Nenhum produto encontrado.")

conn.close()
print("Consulta finalizada.")