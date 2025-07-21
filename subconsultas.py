import sqlite3

conn = sqlite3.connect('fabrica_chocolate.db')
cursor = conn.cursor()

# Executando a consulta - Nomes das crianças que não compraram chocolates
cursor.execute('''
    SELECT CRI.nome
    FROM Criança cri
    LEFT JOIN Chocolate choco ON cri.CPF = choco.CPF_CRIANCA
    WHERE choco.CPF_CRIANCA IS NULL;
''')

# Pegando os resultados
resultados = cursor.fetchall()

# Exibindo os nomes
for linha in resultados:
    print(linha[0])

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
