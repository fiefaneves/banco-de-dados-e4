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

conn.close()
print("Consulta finalizada.")