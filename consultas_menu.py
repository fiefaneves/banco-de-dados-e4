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
    FROM Criança cri
    LEFT JOIN Chocolate choco ON cri.CPF = choco.CPF_CRIANCA
    WHERE choco.CPF_CRIANCA IS NULL;
    """
    
    executar_consulta(
        query, 
        "LEFT JOIN - Crianças sem Chocolates",
        "Mostra o nome das crianças que não compraram chocolates"
    )

def consulta_inner_join():
    """INNER JOIN - Produtos e seus ingredientes"""
    query = """
    SELECT
        P.NOME AS Nome_Produto,
        I.NOME AS Nome_Ingrediente,
        U.quantidade AS Quantidade_Usada
    FROM Produto P
    INNER JOIN USA U ON P.ID = U.ID_PRODUTO
    INNER JOIN Ingrediente I ON U.COD_INGREDIENTE = I.COD
    ORDER BY P.NOME, I.NOME;
    """
    
    executar_consulta(
        query,
        "INNER JOIN - Produtos e Ingredientes",
        "Lista todos os produtos com seus respectivos ingredientes e quantidades"
    )

def consulta_union():
    """UNION - Todos os CPFs do sistema"""
    query = """
    SELECT CPF, 'Responsavel' as Tipo
    FROM Responsavel 
    UNION
    SELECT CPF, 'Criança' as Tipo
    FROM Criança
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
    FROM Criança c
    WHERE EXISTS (
        SELECT 1 
        FROM Visita v
        JOIN Acidente a ON v.CPF_Criança = a.CPF_Criança_Visita
        WHERE v.CPF_Criança = c.CPF
    );
    """
    
    executar_consulta(
        query,
        "SEMI-JOIN - Crianças com Acidentes",
        "Lista crianças que sofreram acidentes durante as visitas"
    )

def consulta_anti_join():
    """ANTI-JOIN - Chocolates sem bilhete dourado"""
    query = """
    SELECT 
        CHOCO.ID_PRODUTO as ID_Chocolate,
        P.NOME as Nome_Produto
    FROM CHOCOLATE CHOCO
    INNER JOIN Produto P ON CHOCO.ID_PRODUTO = P.ID
    WHERE NOT EXISTS (
        SELECT 1
        FROM BILHETEDOURADO B 
        WHERE B.ID_CHOCOLATE = CHOCO.ID_PRODUTO
    );
    """
    
    executar_consulta(
        query,
        "ANTI-JOIN - Chocolates sem Bilhete Dourado",
        "Mostra chocolates que não possuem bilhete dourado"
    )

def consulta_group_by_having():
    """GROUP BY HAVING - Tribos com múltiplos OompaLoompas"""
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
        "GROUP BY HAVING - Tribos Numerosas",
        "Tribos que têm mais de 1 OompaLoompa"
    )

def consulta_subconsulta_escalar():
    """Subconsulta Escalar - Contagem de ingredientes por produto"""
    query = """
    SELECT
        p.NOME as Nome_Produto,
        (SELECT COUNT(*) FROM USA u WHERE u.ID_PRODUTO = p.ID) as Qtd_Ingredientes
    FROM Produto p
    ORDER BY Qtd_Ingredientes DESC, p.NOME;
    """
    
    executar_consulta(
        query,
        "SUBCONSULTA ESCALAR - Ingredientes por Produto",
        "Conta quantos ingredientes cada produto utiliza"
    )

def consulta_subconsulta_linha():
    """Subconsulta de Linha - Produtos com mesmo preço e data"""
    query = """
    SELECT 
        NOME as Nome_Produto, 
        PRECO as Preco, 
        DATA_VAL as Data_Validade
    FROM Produto
    WHERE (PRECO, DATA_VAL) = (
        SELECT PRECO, DATA_VAL
        FROM Produto
        WHERE ID = 'PROD001'
    )
    AND ID != 'PROD001';
    """
    
    executar_consulta(
        query,
        "SUBCONSULTA DE LINHA - Produtos com Mesmo Preço e Validade",
        "Produtos que têm o mesmo preço e data de validade do PROD001"
    )

def consulta_subconsulta_tabela():
    """Subconsulta de Tabela - Produtos que usam Avelã"""
    query = """
    SELECT 
        P.NOME as Nome_Produto,
        P.PRECO as Preco
    FROM Produto P
    WHERE P.ID IN (
        SELECT U.ID_PRODUTO
        FROM USA U
        WHERE U.COD_INGREDIENTE = (
            SELECT I.COD 
            FROM Ingrediente I 
            WHERE I.NOME = 'Avelã'
        )
    );
    """
    
    executar_consulta(
        query,
        "SUBCONSULTA DE TABELA - Produtos com Avelã",
        "Produtos que utilizam Avelã como ingrediente"
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
    print("=" * 80)
    
    if not verificar_banco():
        return
    
    opcoes = {
        '1': ('LEFT JOIN - Crianças sem Chocolates', consulta_left_join),
        '2': ('INNER JOIN - Produtos e Ingredientes', consulta_inner_join),
        '3': ('UNION - Todos os CPFs', consulta_union),
        '4': ('SEMI-JOIN - Crianças com Acidentes', consulta_semi_join),
        '5': ('ANTI-JOIN - Chocolates sem Bilhete Dourado', consulta_anti_join),
        '6': ('GROUP BY HAVING - Tribos Numerosas', consulta_group_by_having),
        '7': ('SUBCONSULTA ESCALAR - Ingredientes por Produto', consulta_subconsulta_escalar),
        '8': ('SUBCONSULTA DE LINHA - Mesmo Preço e Validade', consulta_subconsulta_linha),
        '9': ('SUBCONSULTA DE TABELA - Produtos com Avelã', consulta_subconsulta_tabela),
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
            print("\n🍫 Obrigado por usar o sistema da Fábrica de Chocolate! 🍫")
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
