import sqlite3

conn = sqlite3.connect('fabrica_chocolate.db')
cursor = conn.cursor()

# Subconsulta de linha: Produto mais caro
cursor.execute('''
    SELECT NOME, PRECO
    FROM Produto
    WHERE PRECO = (
        SELECT MAX(PRECO)
        FROM Produto
    )
''')
for nome, preco in cursor.fetchall():
    print(f"Produto: {nome}")
    print(f"Preço: R$ {preco:.2f}")
    print("-" * 30)

# Subconsulta de tabela: Produtos que usam o ingrediente 'Avelã'
cursor.execute('''
    SELECT NOME
    FROM Produto
    WHERE ID IN (
        SELECT ID_PRODUTO
        FROM USA
        WHERE COD_INGREDIENTE = (
            SELECT COD FROM Ingrediente WHERE NOME = 'Avelã'
        )
    )
''')
for (nome,) in cursor.fetchall():
    print(f"Produto: {nome}")
    print("-" * 30)

conn.close()
