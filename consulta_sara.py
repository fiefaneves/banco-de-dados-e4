import sqlite3
conn = sqlite3.connect("fabrica_chocolate.db")
cursor = conn.cursor()

#Semi-Join: Crianças que Sofreram Acidente
sql_semi_join = """
    SELECT c.nome
    FROM Criança c
    WHERE EXISTS (SELECT 1 
        FROM Visita v
        JOIN Acidente a ON v.CPF_Criança = a.CPF_Criança_Visita
        WHERE v.CPF_Criança = c.CPF
    );
"""
cursor.execute(sql_semi_join)
resultados = cursor.fetchall()

if resultados:
    print("Resultado:")
    for (nome,) in resultados:
        print(f"  - {nome}")
else:
    print("Nenhuma criança com acidente encontrado.")

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
    print("  - Nenhum produto encontrado.")

#Consulta com Parâmetro: Acidentes por Gravidade
parametro_gravidade = 'Grave'
sql_parametro = """
    SELECT
        c.nome,
        a.data_acidente,
        a.musica
    FROM Acidente a
    JOIN Visita v ON a.CPF_Criança_Visita = v.CPF_Criança
    JOIN Criança c ON v.CPF_Criança = c.CPF
    WHERE a.gravidade = ?
"""
cursor.execute(sql_parametro, (parametro_gravidade,))
resultados = cursor.fetchall()

if resultados:
    print("Resultado:")
    for nome, data, musica in resultados:
        print(f"  - Criança: {nome}, Data: {data}, Música: '{musica}'")
else:
    print(f"Nenhum acidente com gravidade '{parametro_gravidade}'")

conn.close()
print("Consultas finalizadas.")