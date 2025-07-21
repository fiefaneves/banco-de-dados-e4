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

conn.close()