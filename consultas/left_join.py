import sqlite3

conn = sqlite3.connect('fabrica_chocolate.db')
cursor = conn.cursor()

# Nomes das crianças que não compraram chocolates
cursor.execute('''
    SELECT RC.Nome_Crianca
    FROM Responsavel_Crianca RC
    LEFT JOIN Chocolate choco ON RC.CPF_CRIANCA = choco.CPF_CRIANCA
    WHERE choco.CPF_CRIANCA IS NULL;
''')

# Pegando os resultados
resultados = cursor.fetchall()

# Exibindo os nomes
for linha in resultados:
    print(linha[0])

conn.close()