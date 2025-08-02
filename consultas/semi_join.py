import sqlite3
conn = sqlite3.connect("fabrica_chocolate.db")
cursor = conn.cursor()

#Semi-Join: Crianças que Sofreram Acidente
cursor.execute("""
    SELECT c.Nome_Crianca
    FROM Responsavel_Crianca c
    WHERE EXISTS (
        SELECT * 
        FROM Visita v
        JOIN Acidente a ON v.CPF_Crianca = a.CPF_Crianca_Visita
        WHERE v.CPF_Crianca = c.CPF_CRIANCA
    );
""")
resultados = cursor.fetchall()

if resultados:
    print("Resultado:")
    for (nome,) in resultados:
        print(f"  - {nome}")
else:
    print("Nenhuma criança com acidente encontrado.")

conn.close()
print("Consulta finalizada.")