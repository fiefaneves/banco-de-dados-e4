import sqlite3

conn = sqlite3.connect('fabrica_chocolate.db')
cursor = conn.cursor()

# Subconsulta de linha: Chocolates com a mesma data de validade e tipo do chocolate 'CHOC001'
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

for nome, tipo in cursor.fetchall():
    print(f"Nome: {nome}")
    print(f"Tipo: {tipo}")
print("-" * 30)

# Subconsulta de tabela: Responsáveis por Crianças Acidentadas com Alta Gravidade
cursor.execute("""
    SELECT
        R.NOME,
        R.DATA_NASCIMENTO
    FROM
        RESPONSAVEL R
    WHERE
        R.CPF IN (
            SELECT C.CPF_RESPONSAVEL
            FROM CRIANCA C
            WHERE C.CPF IN (
                SELECT A.CPF_Crianca_Visita
                FROM ACIDENTE A
                WHERE A.GRAVIDADE = 'Alta'
        )
    );
""")
for (nome, data_nasc) in cursor.fetchall():
    print(f"Nome: {nome}")
    print(f"Data de Nascimento: {data_nasc}")
print("-" * 30)

conn.close()
