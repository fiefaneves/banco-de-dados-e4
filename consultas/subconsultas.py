import sqlite3

conn = sqlite3.connect('fabrica_chocolate.db')
cursor = conn.cursor()

# Subconsulta de linha: Chocolates com a mesma data de validade e tipo do chocolate 'CHOC001'
cursor.execute("""
        SELECT C1.Nome, C1.Tipo
        FROM Chocolate C1
        WHERE (C1.Data_Validade, C1.Tipo) = (
            SELECT C2.Data_Validade, C2.Tipo
            FROM Chocolate C2
            WHERE C2.ID = 'CHOC001'
        )
        AND C1.ID != 'CHOC001'
""")

for nome, tipo in cursor.fetchall():
    print(f"Nome: {nome}")
    print(f"Tipo: {tipo}")

print("\n")

# Subconsulta de tabela: Responsáveis por Crianças Acidentadas com Alta Gravidade
cursor.execute("""
    SELECT RC.Nome_Responsavel, RC.Nome_Crianca, RC.Data_Nascimento_Crianca
    FROM Responsavel_Crianca RC
    WHERE RC.CPF_CRIANCA IN (
        SELECT A.CPF_Crianca_Visita
        FROM ACIDENTE A
        WHERE A.GRAVIDADE = 'Alta'
    );
""")
for (nome_resp, nome_crianca, data_nasc) in cursor.fetchall():
    print(f"Nome do Responsável: {nome_resp}")
    print(f"Nome da Criança: {nome_crianca}")
    print(f"Data de Nascimento: {data_nasc}")

conn.close()
