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

def inserir_dados():
    """Insere dados nas tabelas"""
    conn = conectar_db()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    try:
        # Inserir Responsáveis
        responsaveis = [
            ('12345678901', 'João Silva', '2018-05-15', 'Rua das Flores, 123', '12345678', 'Centro', 'São Paulo'),
            ('98765432109', 'Maria Santos', '1985-08-20', 'Av. Principal, 456', '87654321', 'Jardins', 'Rio de Janeiro'),
            ('55555555555', 'Carlos Oliveira', '1975-02-10', 'Rua Secundária, 789', '11223344', 'Bairro Novo', 'Belo Horizonte'),
            ('92277742541', 'Marcos Neto', '1999-06-12', 'Rua José, 100', '51000015', 'Graças', 'Recife')
        ] 
        
        cursor.executemany("""
            INSERT INTO Responsavel (CPF, Nome, Data_Nascimento, End_rua, End_cep, End_bairro, End_estado) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, responsaveis)
        
        # Inserir Contatos
        contatos = [
            ('12345678901', '(11) 99999-9999'),
            ('98765432109', '(21) 88888-8888')
        ]
        
        cursor.executemany("""
            INSERT INTO Contatos (CPF_RESPONSAVEL, Contatos) 
            VALUES (?, ?)
        """, contatos)
        
        # Inserir Fábrica
        cursor.execute("""
            INSERT INTO Fabrica (CNPJ, Data_Fundacao) 
            VALUES ('12345678000199', '1971-01-15')
        """)
        
        # Inserir Crianças
        criancas = [
            ('11111111111', 'Charlie Bucket', '2010-05-15', '12345678901'),
            ('22222222222', 'Veruca Salt', '2009-08-20', '98765432109'),
            ('33333333333', 'Violet Beauregarde', '2011-03-10', '12345678901'),
            ('44444444444', 'Mike Teavee', '2012-02-15', '55555555555')
        ]
        
        cursor.executemany("""
            INSERT INTO Crianca (CPF, Nome, Data_Nascimento, CPF_RESPONSAVEL) 
            VALUES (?, ?, ?, ?)
        """, criancas)
        
        # Inserir Funcionários
        funcionarios = [
            ('44444444444', 'Willy Wonka', 5000.00, None),  # Chefe supremo
            ('55555555555', 'Mike Teavee', 3000.00, '44444444444'),
            ('66666666666', 'Augustus Gloop', 2500.00, '44444444444'),
            ('77777777777', 'Grandpa Joe', 2800.00, '44444444444'),
            ('88888888888', 'Charlie Worker', 2200.00, '44444444444'),
            ('99999999999', 'Slugworth Spy', 2600.00, '44444444444')
        ]
        
        cursor.executemany("""
            INSERT INTO Funcionario (CPF, Nome, Salario, CPF_CHEFE) 
            VALUES (?, ?, ?, ?)
        """, funcionarios)
        
        # Inserir OompaLoompas
        oompas = [
            ('55555555555', 'Tribo do Cacau'),
            ('66666666666', 'Tribo do Açúcar'),
            ('77777777777', 'Tribo do Cacau'),
            ('88888888888', 'Tribo do Açúcar'),
            ('99999999999', 'Tribo do Chocolate')
        ]
        
        cursor.executemany("""
            INSERT INTO OompaLoompa (CPF_FUNCIONARIO, Tribo) 
            VALUES (?, ?)
        """, oompas)
        
        # Inserir Pessoa (Willy Wonka é uma pessoa)
        cursor.execute("""
            INSERT INTO Pessoa (CPF_FUNCIONARIO, Profissao) 
            VALUES ('44444444444', 'Proprietário da Fábrica')
        """)
        
        # Inserir Setor
        cursor.execute("""
            INSERT INTO Setor (CNPJ_Fabrica, COD_SETOR, Nome, Finalidade, Data_Criacao) 
            VALUES ('12345678000199', 'PROD001', 'Produção', 'Fabricação de chocolates e doces', '1971-02-01')
        """)
        
        # Inserir Máquina
        cursor.execute("""
            INSERT INTO Maquina (ID, Modelo, Data_Instalacao, CNPJ_Fabrica_Setor, COD_Setor) 
            VALUES ('MAQ001', 'ChocolateMaker 3000', '1975-06-15', '12345678000199', 'PROD001')
        """)
        
        # Inserir Ingredientes
        ingredientes = [
            ('ING001', 'Cacau', 'Marca Premium'),
            ('ING002', 'Açúcar', 'Açúcar Cristal'),
            ('ING003', 'Leite', 'Leite Integral'),
            ('ING004', 'Avelã', 'Avelã Europeia')
        ]
        
        cursor.executemany("""
            INSERT INTO Ingrediente (COD, Nome, Marca) 
            VALUES (?, ?, ?)
        """, ingredientes)
        
        # Inserir Chocolates
        chocolates = [
            ('CHOC001', 'Chocolate ao Leite Premium', 'Ao Leite', '2025-12-31', '11111111111'),
            ('CHOC002', 'Chocolate com Avelã', 'Ao Leite', '2025-11-30', '22222222222'),
            ('CHOC003', 'Chocolate Branco Premium', 'Branco', '2025-12-31', '11111111111'),
            ('CHOC005', 'Trufa Especial ao Leite', 'Ao Leite', '2025-12-31', None),
            ('CHOC004', 'Chocolate Meio Amargo', 'Meio Amargo', '2025-09-30', '22222222222'),
            ('CHOC006', 'Chocolate ao Leite Clássico', 'Ao Leite', '2025-12-31', None)
        ]
        
        cursor.executemany("""
            INSERT INTO Chocolate (ID, Nome, Tipo, Data_Validade, CPF_CRIANCA) 
            VALUES (?, ?, ?, ?, ?)
        """, chocolates)
        
        # Inserir Visitas
        visitas = [
            ('11111111111', '12345678000199', '2024-07-01'),
            ('22222222222', '12345678000199', '2024-07-01'),
            ('33333333333', '12345678000199', '2024-07-02')
        ]
        
        cursor.executemany("""
            INSERT INTO Visita (CPF_CRIANCA, CNPJ_FABRICA, Data_Visita) 
            VALUES (?, ?, ?)
        """, visitas)
        
        # Inserir Acidente (só para Veruca Salt)
        acidentes = [
            ('ACD001', '2024-07-01', 'Leve', 'Oompa Loompa Song', '22222222222', '12345678000199'),
            ('ACD002', '2024-07-01', 'Alta', 'Dangerous Oompa Loompa Song', '11111111111', '12345678000199')
        ]

        cursor.executemany("""
            INSERT INTO Acidente (ID, Data_Acidente, Gravidade, Musica, CPF_Crianca_Visita, CNPJ_Fabrica_Visita) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, acidentes)
        
        # Inserir Produção
        producao = [
            ('CHOC001', '55555555555', 'MAQ001'),
            ('CHOC002', '66666666666', 'MAQ001'),
            ('CHOC003', '77777777777', 'MAQ001'),
            ('CHOC004', '88888888888', 'MAQ001'),
            ('CHOC005', '99999999999', 'MAQ001'),
            ('CHOC001', '77777777777', 'MAQ001'),  # Mesmo chocolate produzido por dois OompaLoompas
            ('CHOC002', '55555555555', 'MAQ001')   # Mesmo chocolate produzido por dois OompaLoompas
        ]
        
        cursor.executemany("""
            INSERT INTO PRODUZ (ID_CHOCOLATE, CPF_OOMPALOOMPA, ID_MAQUINA) 
            VALUES (?, ?, ?)
        """, producao)
        
        # Inserir Uso de Ingredientes
        usos = [
            ('CHOC001', 'ING001'),  # Cacau no chocolate ao leite
            ('CHOC001', 'ING002'),  # Açúcar no chocolate ao leite
            ('CHOC001', 'ING003'),  # Leite no chocolate ao leite
            ('CHOC002', 'ING001'),  # Cacau no chocolate com avelã
            ('CHOC002', 'ING002'),  # Açúcar no chocolate com avelã
            ('CHOC002', 'ING003'),  # Leite no chocolate com avelã
            ('CHOC002', 'ING004'),  # Avelã no chocolate com avelã
            ('CHOC003', 'ING002'),  # Açúcar no chocolate branco
            ('CHOC003', 'ING003'),  # Leite no chocolate branco
            ('CHOC004', 'ING001'),  # Cacau no chocolate meio amargo
            ('CHOC004', 'ING002'),  # Açúcar no chocolate meio amargo
            ('CHOC005', 'ING001'),  # Cacau na trufa
            ('CHOC005', 'ING002'),  # Açúcar na trufa
            ('CHOC005', 'ING003'),  # Leite na trufa
            ('CHOC005', 'ING004')   # Avelã na trufa especial
        ]

        cursor.executemany("""
            INSERT INTO USA (ID_CHOCOLATE, COD_INGREDIENTE) 
            VALUES (?, ?)
        """, usos)
        
        # Confirmar todas as inserções
        conn.commit()
        print("\nTodos os dados foram inseridos com sucesso!")
        
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Erro ao inserir dados: {e}")
    
    finally:
        conn.close()

def verificar_dados():
    """Verifica se os dados foram inseridos corretamente"""
    conn = conectar_db()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    tabelas = [
        'Responsavel', 'Contatos', 'Fabrica', 'Crianca', 'Funcionario', 
        'OompaLoompa', 'Pessoa', 'Setor', 'Maquina', 'Ingrediente', 
        'Chocolate', 'Visita', 'Acidente', 'PRODUZ', 'USA'
    ]
    
    print("\nVerificação dos dados inseridos:")
    
    for tabela in tabelas:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
            count = cursor.fetchone()[0]
            print(f"{tabela:15s}: {count:3d} registros")
        except sqlite3.Error as e:
            print(f"{tabela:15s}: Erro - {e}")
    
    conn.close()

if __name__ == "__main__":
    print("INSERÇÃO DE DADOS - FÁBRICA DE CHOCOLATE")    
    inserir_dados()
    verificar_dados()
