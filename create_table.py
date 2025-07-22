import sqlite3
import os

def conectar_db():
    """Conecta ao banco de dados SQLite"""
    try:
        conn = sqlite3.connect('fabrica_chocolate.db')
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None

def drop_tables_if_exist():
    """Remove todas as tabelas se existirem (para recriação limpa)"""
    conn = conectar_db()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    # Lista de tabelas na ordem inversa de criação (devido às FKs)
    tabelas = [
        'BilheteDourado',
        'USA',
        'PRODUZ', 
        'Acidente',
        'Visita',
        'ContatosResponsavel',
        'Chiclete',
        'Chocolate',
        'Pessoa',
        'OompaLoompa',
        'Maquina',
        'Setor',
        'Criança',
        'Funcionario',
        'Produto',
        'Ingrediente',
        'Fabrica',
        'Responsavel'
    ]
    
    try:
        # Desabilitar foreign keys temporariamente
        cursor.execute("PRAGMA foreign_keys = OFF")
        
        for tabela in tabelas:
            cursor.execute(f"DROP TABLE IF EXISTS {tabela}")
            print(f"Tabela {tabela} removida (se existia)")
        
        # Reabilitar foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")
        
        conn.commit()
        print("Todas as tabelas foram removidas com sucesso!")
        return True
        
    except sqlite3.Error as e:
        print(f"Erro ao remover tabelas: {e}")
        return False
    
    finally:
        conn.close()

def criar_tabelas():
    """Cria todas as tabelas do banco de dados da fábrica de chocolate"""
    conn = conectar_db()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    try:
        # Habilitar foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")
        
        print("Criando tabelas...")
        print("-" * 50)
        
        # 1. Entidades que não dependem de outras
        print("1. Criando entidades independentes...")
        
        # Responsavel
        cursor.execute("""
            CREATE TABLE Responsavel (
                CPF TEXT PRIMARY KEY,
                Nome TEXT,
                End_rua TEXT,
                End_complemento TEXT,
                End_cep TEXT,
                End_bairro TEXT,
                End_estado TEXT
            )
        """)
        print("Tabela Responsavel criada")
        
        # Fabrica
        cursor.execute("""
            CREATE TABLE Fabrica (
                CNPJ TEXT PRIMARY KEY,
                data_fundacao DATE
            )
        """)
        print("Tabela Fabrica criada")
        
        # Ingrediente
        cursor.execute("""
            CREATE TABLE Ingrediente (
                COD TEXT PRIMARY KEY,
                NOME TEXT NOT NULL,
                QTD REAL
            )
        """)
        print("Tabela Ingrediente criada")
        
        # Produto
        cursor.execute("""
            CREATE TABLE Produto (
                ID TEXT PRIMARY KEY,
                NOME TEXT NOT NULL,
                PRECO REAL,
                DATA_VAL DATE,
                DESC_PRODUTO TEXT
            )
        """)
        print("Tabela Produto criada")
        
        # Funcionario
        cursor.execute("""
            CREATE TABLE Funcionario (
                CPF TEXT PRIMARY KEY,
                SALARIO REAL,
                NOME TEXT,
                CPF_CHEFE TEXT,
                CONSTRAINT FK_FUNC_SUPERVISOR FOREIGN KEY (CPF_CHEFE) REFERENCES Funcionario(CPF)
            )
        """)
        print("Tabela Funcionario criada")
        
        # 2. Entidades com dependências (FKs)
        print("\n2. Criando entidades com dependências...")
        
        # Criança
        cursor.execute("""
            CREATE TABLE Criança (
                CPF TEXT PRIMARY KEY,
                nome TEXT,
                data_nascimento DATE,
                CPF_Responsavel TEXT,
                CONSTRAINT FK_CRIANCA_RESP FOREIGN KEY (CPF_Responsavel) REFERENCES Responsavel(CPF)
            )
        """)
        print("Tabela Criança criada")
        
        # Setor
        cursor.execute("""
            CREATE TABLE Setor (
                CNPJ_Fabrica TEXT,
                COD_Setor TEXT,
                nome TEXT,
                finalidade TEXT,
                data_criacao DATE,
                CONSTRAINT PK_SETOR PRIMARY KEY (CNPJ_Fabrica, COD_Setor),
                CONSTRAINT FK_SETOR_FABRICA FOREIGN KEY (CNPJ_Fabrica) REFERENCES Fabrica(CNPJ)
            )
        """)
        print("Tabela Setor criada")
        
        # Maquina
        cursor.execute("""
            CREATE TABLE Maquina (
                ID TEXT PRIMARY KEY,
                MODELO TEXT,
                DATA_INST DATE,
                CNPJ_Fabrica_Setor TEXT NOT NULL,
                COD_Setor TEXT NOT NULL,
                CONSTRAINT FK_MAQUINA_SETOR FOREIGN KEY (CNPJ_Fabrica_Setor, COD_Setor) 
                    REFERENCES Setor(CNPJ_Fabrica, COD_Setor)
            )
        """)
        print("Tabela Maquina criada")
        
        # 3. Mapeamento da Hierarquia de Herança
        print("\n3. Criando hierarquia de herança...")
        
        # OompaLoompa
        cursor.execute("""
            CREATE TABLE OompaLoompa (
                CPF_FUNC TEXT PRIMARY KEY,
                TRIBO TEXT,
                CONSTRAINT FK_OOMPA_FUNC FOREIGN KEY (CPF_FUNC) REFERENCES Funcionario(CPF)
            )
        """)
        print("Tabela OompaLoompa criada")
        
        # Pessoa
        cursor.execute("""
            CREATE TABLE Pessoa (
                CPF_FUNC TEXT PRIMARY KEY,
                CONSTRAINT FK_PESSOA_FUNC FOREIGN KEY (CPF_FUNC) REFERENCES Funcionario(CPF)
            )
        """)
        print("Tabela Pessoa criada")
        
        # Chiclete
        cursor.execute("""
            CREATE TABLE Chiclete (
                ID_PRODUTO TEXT PRIMARY KEY,
                CONSTRAINT FK_CHICLETE_PROD FOREIGN KEY (ID_PRODUTO) REFERENCES Produto(ID)
            )
        """)
        print("Tabela Chiclete criada")
        
        # Chocolate
        cursor.execute("""
            CREATE TABLE Chocolate (
                ID_PRODUTO TEXT PRIMARY KEY,
                TIPO TEXT,
                RECHEIO TEXT,
                CPF_CRIANCA TEXT,
                CONSTRAINT FK_CHOCOLATE_PROD FOREIGN KEY (ID_PRODUTO) REFERENCES Produto(ID),
                CONSTRAINT FK_CHOCOLATE_CRIANCA FOREIGN KEY (CPF_CRIANCA) REFERENCES Criança(CPF)
            )
        """)
        print("Tabela Chocolate criada")
        
        # 4. Tabelas de Atributos Multivalorados e Relacionamentos
        print("\n4. Criando tabelas de relacionamentos...")
        
        # Contatos
        cursor.execute("""
            CREATE TABLE ContatosResponsavel (
                CPF_Responsavel TEXT,
                Contatos TEXT,
                CONSTRAINT PK_CONTATOS PRIMARY KEY (CPF_Responsavel, Contatos),
                CONSTRAINT FK_CONTATOS_RESP FOREIGN KEY (CPF_Responsavel) REFERENCES Responsavel(CPF)
            )
        """)
        print("Tabela Contatos criada")
        
        # Visita
        cursor.execute("""
            CREATE TABLE Visita (
                CPF_Criança TEXT,
                CNPJ_Fabrica TEXT,
                data_visita DATE,
                CONSTRAINT PK_VISITA PRIMARY KEY (CPF_Criança, CNPJ_Fabrica),
                CONSTRAINT FK_VISITA_CRIANCA FOREIGN KEY (CPF_Criança) REFERENCES Criança(CPF),
                CONSTRAINT FK_VISITA_FABRICA FOREIGN KEY (CNPJ_Fabrica) REFERENCES Fabrica(CNPJ)
            )
        """)
        print("Tabela Visita criada")
        
        # Acidente
        cursor.execute("""
            CREATE TABLE Acidente (
                ID TEXT PRIMARY KEY,
                data_acidente DATE,
                gravidade TEXT,
                musica TEXT,
                CPF_Criança_Visita TEXT,
                CNPJ_Fabrica_Visita TEXT,
                CONSTRAINT FK_ACID_VISITA FOREIGN KEY (CPF_Criança_Visita, CNPJ_Fabrica_Visita) 
                    REFERENCES Visita(CPF_Criança, CNPJ_Fabrica),
                CONSTRAINT AK_ACID_VISITA UNIQUE (CPF_Criança_Visita, CNPJ_Fabrica_Visita)
            )
        """)
        print("Tabela Acidente criada")
        
        # PRODUZ
        cursor.execute("""
            CREATE TABLE PRODUZ (
                ID_PRODUTO TEXT,
                CPF_OOMPALOOMPA TEXT,
                ID_MAQUINA TEXT,
                CONSTRAINT PK_PRODUZ PRIMARY KEY (ID_PRODUTO, CPF_OOMPALOOMPA, ID_MAQUINA),
                CONSTRAINT FK_PRODUZ_PROD FOREIGN KEY (ID_PRODUTO) REFERENCES Produto(ID),
                CONSTRAINT FK_PRODUZ_OOMPA FOREIGN KEY (CPF_OOMPALOOMPA) REFERENCES OompaLoompa(CPF_FUNC),
                CONSTRAINT FK_PRODUZ_MAQ FOREIGN KEY (ID_MAQUINA) REFERENCES Maquina(ID)
            )
        """)
        print("Tabela PRODUZ criada")
        
        # USA
        cursor.execute("""
            CREATE TABLE USA (
                ID_PRODUTO TEXT,
                COD_INGREDIENTE TEXT,
                quantidade REAL,
                CONSTRAINT PK_USA PRIMARY KEY (ID_PRODUTO, COD_INGREDIENTE),
                CONSTRAINT FK_USA_PROD FOREIGN KEY (ID_PRODUTO) REFERENCES Produto(ID),
                CONSTRAINT FK_USA_INGR FOREIGN KEY (COD_INGREDIENTE) REFERENCES Ingrediente(COD)
            )
        """)
        print("Tabela USA criada")
        
        # BilheteDourado
        cursor.execute("""
            CREATE TABLE BilheteDourado (
                COD TEXT PRIMARY KEY,
                CATEGORIA TEXT,
                DATA_ENCONTRADO DATE,
                LOCAL_COMPRA TEXT,
                ID_CHOCOLATE TEXT,
                CONSTRAINT FK_BILHETE_CHOCO FOREIGN KEY (ID_CHOCOLATE) REFERENCES Chocolate(ID_PRODUTO)
            )
        """)
        print("Tabela BilheteDourado criada")
        
        # Confirmar criação
        conn.commit()
        print("\n" + "="*60)
        print("TODAS AS TABELAS FORAM CRIADAS COM SUCESSO!")
        print("="*60)
        
        return True
        
    except sqlite3.Error as e:
        print(f"Erro ao criar tabelas: {e}")
        conn.rollback()
        return False
    
    finally:
        conn.close()

def verificar_tabelas():
    """Verifica se todas as tabelas foram criadas corretamente"""
    conn = conectar_db()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    try:
        # Listar todas as tabelas criadas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tabelas = cursor.fetchall()
        
        print("\nTabelas criadas no banco de dados:")
        print("-" * 40)
        for i, (tabela,) in enumerate(tabelas, 1):
            print(f"{i:2d}. {tabela}")
        
        print(f"\nTotal: {len(tabelas)} tabelas criadas")
        
    except sqlite3.Error as e:
        print(f"Erro ao verificar tabelas: {e}")
    
    finally:
        conn.close()

def main():
    """Função principal"""
    print("CRIAÇÃO DAS TABELAS - FÁBRICA DE CHOCOLATE")
    print("="*60)
    
    # Verificar se o arquivo do banco já existe
    if os.path.exists('fabrica_chocolate.db'):
        resposta = input("Banco de dados já existe. Deseja recriar? (s/n): ").strip().lower()
        if resposta == 's':
            if drop_tables_if_exist():
                print("Tabelas removidas. Criando novas tabelas...\n")
            else:
                print("Erro ao remover tabelas existentes.")
                return
        else:
            print("Operação cancelada.")
            return
    
    # Criar as tabelas
    if criar_tabelas():
        verificar_tabelas()
        
        print(f"\nBanco de dados criado: fabrica_chocolate.db")
    else:
        print("Falha na criação das tabelas.")

if __name__ == "__main__":
    main()
