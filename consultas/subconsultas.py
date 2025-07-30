import sqlite3

conn = sqlite3.connect('fabrica_chocolate.db')
cursor = conn.cursor()

# Subconsulta de linha: Produtos com o mesmo preço e data de validade do produto 'PROD001'
cursor.execute("""
        SELECT 
            NOME, 
            TIPO
        FROM Chocolate
        WHERE (Data_Validade, Tipo) = (
            SELECT Data_Validade, Tipo
            FROM Chocolate
            WHERE ID = 'CHOC001'
        )
        AND ID != 'CHOC001'
""")

for nome, preco, data_val in cursor.fetchall():
    print(f"Produto: {nome}")
    print(f"Preço: R$ {preco:.2f}")
    print(f"Data de Validade: {data_val}")
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
