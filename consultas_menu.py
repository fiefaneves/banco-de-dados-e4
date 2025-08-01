import sqlite3
import sys

def conectar_db():
    """Conecta ao banco de dados"""
    try:
        conn = sqlite3.connect('fabrica_chocolate.db')
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None

def executar_consulta(query, titulo, descricao):
    """Executa uma consulta e exibe os resultados formatados"""
    print(f"\n{'='*80}")
    print(f"CONSULTA: {titulo}")
    print(f"{'='*80}")
    print(f"Descrição: {descricao}")
    print(f"\nSQL:")
    print(query)
    print(f"\nResultados:")
    print("-" * 80)
    
    conn = conectar_db()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        if resultados:
            # Obter nomes das colunas
            colunas = [description[0] for description in cursor.description]
            
            # Imprimir cabeçalho
            header = " | ".join(f"{col:20s}" for col in colunas)
            print(header)
            print("-" * len(header))
            
            # Imprimir resultados
            for linha in resultados:
                linha_str = " | ".join(f"{str(valor):20s}" for valor in linha)
                print(linha_str)
            
            print(f"\nTotal de registros encontrados: {len(resultados)}")
        else:
            print("Nenhum resultado encontrado.")
            
    except sqlite3.Error as e:
        print(f"Erro ao executar consulta: {e}")
    
    finally:
        conn.close()

def consulta_left_join():
    """LEFT JOIN - Nomes das crianças que não compraram chocolates"""
    query = """
    SELECT CRI.nome as Nome_Crianca
    FROM Crianca cri
    LEFT JOIN Chocolate choco ON cri.CPF = choco.CPF_CRIANCA
    WHERE choco.CPF_CRIANCA IS NULL;
    """
    
    executar_consulta(
        query, 
        "LEFT JOIN - Criancas sem Chocolates",
        "Mostra o nome das criancas que não compraram chocolates"
    )

def consulta_inner_join():
    """INNER JOIN - Chocolates e seus ingredientes"""
    query = """
    SELECT
        C.Nome AS Nome_Chocolate,
        I.Nome AS Nome_Ingrediente
    FROM Chocolate C
    INNER JOIN USA U ON C.ID = U.ID_CHOCOLATE
    INNER JOIN Ingrediente I ON U.COD_INGREDIENTE = I.COD
    ORDER BY C.Nome, I.Nome;
    """
    
    executar_consulta(
        query,
        "INNER JOIN - Chocolates e Ingredientes",
        "Lista todos os chocolates com seus respectivos ingredientes"
    )

def consulta_union():
    """UNION - Todos os CPFs do sistema"""
    query = """
    SELECT CPF, 'Responsavel' as Tipo
    FROM Responsavel 
    UNION
    SELECT CPF, 'Crianca' as Tipo
    FROM Crianca
    UNION
    SELECT CPF, 'Funcionario' as Tipo
    FROM Funcionario
    ORDER BY CPF;
    """
    
    executar_consulta(
        query,
        "UNION - Todos os CPFs do Sistema",
        "Mostra todos os CPFs cadastrados no sistema com seus tipos"
    )

def consulta_semi_join():
    """SEMI-JOIN - Crianças que sofreram acidentes"""
    query = """
    SELECT c.nome as Nome_Crianca
    FROM Crianca c
    WHERE EXISTS (
        SELECT * 
        FROM Visita v
        JOIN Acidente a ON v.CPF_Crianca = a.CPF_Crianca_Visita
        WHERE v.CPF_Crianca = c.CPF
    );
    """
    
    executar_consulta(
        query,
        "SEMI-JOIN - Criancas com Acidentes",
        "Lista criancas que sofreram acidentes durante as visitas"
    )

def consulta_anti_join():
    """ANTI-JOIN - Responsáveis sem criança"""
    query = """
        SELECT R.NOME
        FROM RESPONSAVEL R
        WHERE NOT EXISTS (
            SELECT *
            FROM CRIANCA C
            WHERE C.CPF_RESPONSAVEL = R.CPF
        )
    """
    
    executar_consulta(
        query,
        "ANTI-JOIN - Responsáveis sem criança",
        "Mostra os responsáveis que não tem criança"
    )

def consulta_group_by_having():
    """GROUP BY HAVING - Tribos com mais de 1 Oompa-Loompa"""
    query = """
    SELECT 
        TRIBO,
        COUNT(*) as Total_OompaLoompas
    FROM OompaLoompa
    GROUP BY TRIBO
    HAVING COUNT(*) > 1
    ORDER BY Total_OompaLoompas DESC;
    """
    
    executar_consulta(
        query,
        "GROUP BY HAVING - Tribos com mais de 1 Oompa-Loompa",
        "Tribos que têm mais de 1 OompaLoompa"
    )

def consulta_subconsulta_escalar():
    """Subconsulta Escalar - Contagem de ingredientes por chocolate"""
    query = """
    SELECT
        C.Nome as Nome_Chocolate,
        (SELECT COUNT(*) FROM USA U WHERE U.ID_CHOCOLATE = C.ID) as Qtd_Ingredientes
    FROM Chocolate C
    ORDER BY Qtd_Ingredientes DESC, C.Nome;
    """
    
    executar_consulta(
        query,
        "SUBCONSULTA ESCALAR - Ingredientes por Chocolate",
        "Conta quantos ingredientes cada chocolate utiliza"
    )

def consulta_subconsulta_linha():
    """Subconsulta de Linha - Chocolates com mesma data de validade e tipo do CHOC001, exceto ele mesmo"""
    query = """
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
    """
    
    executar_consulta(
        query,
        "SUBCONSULTA DE LINHA - Chocolates com mesma data de validade e tipo do CHOC001",
        "Chocolates que têm a mesma data de validade e tipo do chocolate 'CHOC001', exceto ele mesmo"
    )

def consulta_subconsulta_tabela():
    """Subconsulta de Tabela - Responsáveis por Crianças Acidentadas com Alta Gravidade"""
    query = """
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
    """
    
    executar_consulta(
        query,
        "SUBCONSULTA DE TABELA - Responsáveis por Crianças Acidentadas com Alta Gravidade",
        "Responsáveis por crianças que sofreram acidentes de alta gravidade"
    )


def verificar_banco():
    """Verifica se o banco de dados existe e tem dados"""
    conn = conectar_db()
    if not conn:
        print("Não foi possível conectar ao banco de dados!")
        print("\nCertifique-se de executar:")
        print("1. python create_table.py")
        print("2. python insert_data.py")
        return False
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) FROM Responsavel")
        if cursor.fetchone()[0] == 0:
            print("Banco de dados vazio!")
            print("\nExecute: python insert_data.py")
            conn.close()
            return False
    except sqlite3.Error:
        print("Tabelas não encontradas!")
        print("\nExecute primeiro: python create_table.py")
        conn.close()
        return False
    
    conn.close()
    return True

def menu_principal():
    """Menu principal da aplicação"""
    print("CONSULTAS - FÁBRICA DE CHOCOLATE")
    print("=" * 50)
    
    if not verificar_banco():
        return
    
    opcoes = {
        '1': ('LEFT JOIN - Criancas sem Chocolates', consulta_left_join),
        '2': ('INNER JOIN - Chocolates e seus ingredientes', consulta_inner_join),
        '3': ('UNION - Todos os CPFs', consulta_union),
        '4': ('SEMI-JOIN - Criancas com Acidentes', consulta_semi_join),
        '5': ('ANTI-JOIN - Responsáveis sem crianças', consulta_anti_join),
        '6': ('GROUP BY HAVING - Tribos com mais de 1 Oompa-Loompa', consulta_group_by_having),
        '7': ('SUBCONSULTA ESCALAR - Ingredientes por Chocolate', consulta_subconsulta_escalar),
        '8': ('SUBCONSULTA DE LINHA - Chocolates com mesma data de validade e tipo do CHOC001', consulta_subconsulta_linha),
        '9': ('SUBCONSULTA DE TABELA - Responsáveis por Crianças Acidentadas com Alta Gravidade', consulta_subconsulta_tabela),
        '10': ('EXECUTAR TODAS AS CONSULTAS', None),
        '0': ('SAIR', None)
    }
    
    while True:
        print(f"\n{'='*50}")
        print("MENU DE CONSULTAS")
        print("="*50)
        
        for key, (desc, _) in opcoes.items():
            if key == '10':
                print(f"\n{key}. {desc}")
            elif key == '0':
                print(f"{key}.  {desc}")
            else:
                print(f" {key}. {desc}")
        
        escolha = input(f"\n{'='*50}\nEscolha uma opção: ").strip()
        
        if escolha == '0':
            print("\n Obrigado por usar o sistema da Fábrica de Chocolate! ")
            break
            
        elif escolha == '10':
            print("\nEXECUTANDO TODAS AS CONSULTAS...")
            print("=" * 80)
            
            for key in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                if opcoes[key][1]:
                    opcoes[key][1]()
                    input("\nPressione ENTER para continuar...")
            
            print(f"\n{'='*80}")
            print("TODAS AS CONSULTAS FORAM EXECUTADAS!")
            print("="*80)
            
        elif escolha in opcoes and opcoes[escolha][1] is not None:
            opcoes[escolha][1]()
            
        else:
            print("Opção inválida! Tente novamente.")
        
        if escolha != '10' and escolha != '0':
            input("\nPressione ENTER para voltar ao menu...")

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\nPrograma interrompido pelo usuário. Até logo!")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        print("Por favor, verifique se o banco de dados está configurado corretamente.")
