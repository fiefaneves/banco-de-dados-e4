import sqlite3
from datetime import datetime, date

def conectar_db():
    """Conecta ao banco de dados"""
    try:
        conn = sqlite3.connect('fabrica_chocolate.db')
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None

def inserir_dados_exemplo():
    """Insere dados de exemplo nas tabelas"""
    conn = conectar_db()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    try:
        # Inserir Responsáveis
        print("Inserindo Responsáveis...")
        responsaveis = [
            ('12345678901', 'Rua das Flores, 123', 'Apto 45', '12345678', 'Centro', 'São Paulo'),
            ('98765432109', 'Av. Principal, 456', '', '87654321', 'Jardins', 'Rio de Janeiro')
        ]
        
        cursor.executemany("""
            INSERT INTO Responsavel (CPF, End_rua, End_complemento, End_cep, End_bairro, End_estado) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, responsaveis)
        
        # Inserir Contatos
        print("Inserindo Contatos...")
        contatos = [
            ('12345678901', '(11) 99999-9999'),
            ('98765432109', '(21) 88888-8888')
        ]
        
        cursor.executemany("""
            INSERT INTO ContatosResponsavel (CPF_Responsavel, Contatos) 
            VALUES (?, ?)
        """, contatos)
        
        # Inserir Fábrica
        print("Inserindo Fábrica...")
        cursor.execute("""
            INSERT INTO Fabrica (CNPJ, data_fundacao) 
            VALUES ('12345678000199', '1971-01-15')
        """)
        
        # Inserir Criancas
        print("Inserindo Criancas...")
        criancas = [
            ('11111111111', 'Charlie Bucket', '2010-05-15', '12345678901'),
            ('22222222222', 'Veruca Salt', '2009-08-20', '98765432109'),
            ('33333333333', 'Violet Beauregarde', '2011-03-10', '12345678901')
        ]
        
        cursor.executemany("""
            INSERT INTO Crianca (CPF, nome, data_nascimento, CPF_Responsavel) 
            VALUES (?, ?, ?, ?)
        """, criancas)
        
        # Inserir Funcionários
        print("Inserindo Funcionários...")
        funcionarios = [
            ('44444444444', 5000.00, 'Willy Wonka', None),  # Chefe supremo
            ('55555555555', 3000.00, 'Mike Teavee', '44444444444'),
            ('66666666666', 2500.00, 'Augustus Gloop', '44444444444')
        ]
        
        cursor.executemany("""
            INSERT INTO Funcionario (CPF, SALARIO, NOME, CPF_CHEFE) 
            VALUES (?, ?, ?, ?)
        """, funcionarios)
        
        # Inserir OompaLoompas
        print("Inserindo OompaLoompas...")
        oompas = [
            ('55555555555', 'Tribo do Cacau'),
            ('66666666666', 'Tribo do Açúcar')
        ]
        
        cursor.executemany("""
            INSERT INTO OompaLoompa (CPF_FUNC, TRIBO) 
            VALUES (?, ?)
        """, oompas)
        
        # Inserir Pessoa (Willy Wonka é uma pessoa)
        print("Inserindo Pessoa...")
        cursor.execute("""
            INSERT INTO Pessoa (CPF_FUNC) 
            VALUES ('44444444444')
        """)
        
        # Inserir Setor
        print("Inserindo Setor...")
        cursor.execute("""
            INSERT INTO Setor (CNPJ_Fabrica, COD_Setor, finalidade, data_criacao) 
            VALUES ('12345678000199', 'Produção', 'Fabricação de chocolates e doces', '1971-02-01')
        """)
        
        # Inserir Máquina
        print("Inserindo Máquina...")
        cursor.execute("""
            INSERT INTO Maquina (ID, MODELO, DATA_INST, CNPJ_Fabrica_Setor, COD_Setor) 
            VALUES ('MAQ001', 'ChocolateMaker 3000', '1975-06-15', '12345678000199', 'Produção')
        """)
        
        # Inserir Ingredientes
        print("Inserindo Ingredientes...")
        ingredientes = [
            ('ING001', 'Cacau', 1000.50),
            ('ING002', 'Açúcar', 500.25),
            ('ING003', 'Leite', 200.75),
            ('ING004', 'Avelã', 150.00)
        ]
        
        cursor.executemany("""
            INSERT INTO Ingrediente (COD, NOME, QTD) 
            VALUES (?, ?, ?)
        """, ingredientes)
        
        # Inserir Produtos
        print("Inserindo Produtos...")
        produtos = [
            ('PROD001', 'Chocolate ao Leite Premium', 15.50, '2025-12-31', 'Chocolate cremoso ao leite'),
            ('PROD002', 'Chocolate com Avelã', 18.75, '2025-11-30', 'Chocolate com pedaços de avelã'),
            ('PROD003', 'Chiclete Explosivo', 5.25, '2026-06-15', 'Chiclete que explode sabores')
        ]
        
        cursor.executemany("""
            INSERT INTO Produto (ID, NOME, PRECO, DATA_VAL, DESC_PRODUTO) 
            VALUES (?, ?, ?, ?, ?)
        """, produtos)
        
        # Inserir Chocolates
        print("Inserindo Chocolates...")
        chocolates = [
            ('PROD001', 'Ao Leite', 'Sem recheio', '11111111111'),
            ('PROD002', 'Ao Leite', 'Avelã', '22222222222')
        ]
        
        cursor.executemany("""
            INSERT INTO Chocolate (ID_PRODUTO, TIPO, RECHEIO, CPF_CRIANCA) 
            VALUES (?, ?, ?, ?)
        """, chocolates)
        
        # Inserir Chiclete
        print("Inserindo Chiclete...")
        cursor.execute("""
            INSERT INTO Chiclete (ID_PRODUTO) 
            VALUES ('PROD003')
        """)
        
        # Inserir Visitas
        print("Inserindo Visitas...")
        visitas = [
            ('11111111111', '12345678000199', '2024-07-01'),
            ('22222222222', '12345678000199', '2024-07-01'),
            ('33333333333', '12345678000199', '2024-07-02')
        ]
        
        cursor.executemany("""
            INSERT INTO Visita (CPF_Crianca, CNPJ_Fabrica, data_visita) 
            VALUES (?, ?, ?)
        """, visitas)
        
        # Inserir Acidente (só para Veruca Salt)
        print("Inserindo Acidente...")
        cursor.execute("""
            INSERT INTO Acidente (ID, data_acidente, gravidade, musica, CPF_Crianca_Visita, CNPJ_Fabrica_Visita) 
            VALUES ('ACD001', '2024-07-01', 'Leve', 'Oompa Loompa Song', '22222222222', '12345678000199')
        """)
        
        # Inserir Produção
        print("Inserindo Produção...")
        producao = [
            ('PROD001', '55555555555', 'MAQ001'),
            ('PROD002', '66666666666', 'MAQ001')
        ]
        
        cursor.executemany("""
            INSERT INTO PRODUZ (ID_PRODUTO, CPF_OOMPALOOMPA, ID_MAQUINA) 
            VALUES (?, ?, ?)
        """, producao)
        
        # Inserir Uso de Ingredientes
        print("Inserindo Uso de Ingredientes...")
        usos = [
            ('PROD001', 'ING001', 100.0),  # Cacau no chocolate ao leite
            ('PROD001', 'ING002', 50.0),   # Açúcar no chocolate ao leite
            ('PROD001', 'ING003', 25.0),   # Leite no chocolate ao leite
            ('PROD002', 'ING001', 100.0),  # Cacau no chocolate com avelã
            ('PROD002', 'ING002', 50.0),   # Açúcar no chocolate com avelã
            ('PROD002', 'ING003', 25.0),   # Leite no chocolate com avelã
            ('PROD002', 'ING004', 30.0)    # Avelã no chocolate com avelã
        ]
        
        cursor.executemany("""
            INSERT INTO USA (ID_PRODUTO, COD_INGREDIENTE, quantidade) 
            VALUES (?, ?, ?)
        """, usos)
        
        # Inserir Bilhete Dourado
        print("Inserindo Bilhete Dourado...")
        cursor.execute("""
            INSERT INTO BilheteDourado (COD, CATEGORIA, DATA_ENCONTRADO, LOCAL_COMPRA, ID_CHOCOLATE) 
            VALUES ('BD001', 'Especial', '2024-06-15', 'Loja do Sr. Bucket', 'PROD001')
        """)
        
        # Confirmar todas as inserções
        conn.commit()
        print("\n✅ Todos os dados de exemplo foram inseridos com sucesso!")
        
    except sqlite3.Error as e:
        conn.rollback()
        print(f"❌ Erro ao inserir dados: {e}")
    
    finally:
        conn.close()

def verificar_dados():
    """Verifica se os dados foram inseridos corretamente"""
    conn = conectar_db()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    tabelas = [
        'Responsavel', 'ContatosResponsavel', 'Fabrica', 'Crianca', 'Funcionario', 
        'OompaLoompa', 'Pessoa', 'Setor', 'Maquina', 'Ingrediente', 
        'Produto', 'Chocolate', 'Chiclete', 'Visita', 'Acidente', 
        'PRODUZ', 'USA', 'BilheteDourado'
    ]
    
    print("\nVerificação dos dados inseridos:")
    print("-" * 50)
    
    for tabela in tabelas:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
            count = cursor.fetchone()[0]
            print(f"{tabela:15s}: {count:3d} registros")
        except sqlite3.Error as e:
            print(f"{tabela:15s}: Erro - {e}")
    
    conn.close()

if __name__ == "__main__":
    print("INSERÇÃO DE DADOS DE EXEMPLO - FÁBRICA DE CHOCOLATE")
    print("=" * 60)
    
    inserir_dados_exemplo()
    verificar_dados()
    
    print("\nAgora você pode usar os scripts de consulta:")
    print("- consultar_fabrica.py (consultas avançadas)")
    print("- consultas_simples.py (consultas básicas)")
