import sqlite3
conn = sqlite3.connect("fabrica_chocolate.db")
cursor = conn.cursor()

#Subconsulta Escalar: Contagem de Ingredientes por Produto
sql_scalar = """
    SELECT
        p.NOME,
        (SELECT COUNT(*) FROM USA u WHERE u.ID_PRODUTO = p.ID)
    FROM Produto p;
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