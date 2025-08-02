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
    """Remove todas as tabelas se existirem """
    conn = conectar_db()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    # Lista de tabelas na ordem inversa de criação (devido às FKs)
    tabelas = [
        'USA',
        'PRODUZ', 
        'Acidente',
        'Visita',
        'Contatos',
        'Pessoa',
        'OompaLoompa',
        'Maquina',
        'Setor',
        'Funcionario',
        'Chocolate',
        'Ingrediente',
        'Fabrica',
        'Responsavel_Crianca'
    ]
    
    try:
        # Desabilitar foreign keys temporariamente
        cursor.execute("PRAGMA foreign_keys = OFF")
        
        for tabela in tabelas:
            cursor.execute(f"DROP TABLE IF EXISTS {tabela}")
        
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
              
        # Responsavel_Crianca
        cursor.execute("""
            CREATE TABLE Responsavel_Crianca (
                CPF_CRIANCA TEXT PRIMARY KEY,
                CPF_RESPONSAVEL TEXT UNIQUE NOT NULL,
                Nome_Crianca TEXT NOT NULL,
                Nome_Responsavel TEXT NOT NULL,
                Data_Nascimento_Crianca DATE,
                Data_Nascimento_Responsavel DATE,
                End_cep TEXT,
                End_rua TEXT,
                End_bairro TEXT,
                End_estado TEXT
            )
        """)
        
        # Fabrica
        cursor.execute("""
            CREATE TABLE Fabrica (
                CNPJ TEXT PRIMARY KEY,
                Data_Fundacao DATE
            )
        """)
        
        # Ingrediente
        cursor.execute("""
            CREATE TABLE Ingrediente (
                COD TEXT PRIMARY KEY,
                Nome TEXT UNIQUE NOT NULL,
                Marca TEXT
            )
        """)
        
        # Chocolate
        cursor.execute("""
            CREATE TABLE Chocolate (
                ID TEXT PRIMARY KEY,
                Nome TEXT UNIQUE NOT NULL,
                Tipo TEXT,
                Data_Validade DATE,
                CPF_CRIANCA TEXT,
                CONSTRAINT FK_CHOC_CRIANCA FOREIGN KEY (CPF_CRIANCA) REFERENCES Responsavel_Crianca(CPF_CRIANCA)
            )
        """)
        
        # Funcionario
        cursor.execute("""
            CREATE TABLE Funcionario (
                CPF TEXT PRIMARY KEY,
                Nome TEXT NOT NULL,
                Salario REAL,
                CPF_CHEFE TEXT,
                CONSTRAINT FK_FUNC_SUPERVISOR FOREIGN KEY (CPF_CHEFE) REFERENCES Funcionario(CPF)
            )
        """)
        
        # Setor
        cursor.execute("""
            CREATE TABLE Setor (
                CNPJ_Fabrica TEXT,
                COD_SETOR TEXT,
                Nome TEXT NOT NULL,
                Finalidade TEXT NOT NULL,
                Data_Criacao DATE,
                CONSTRAINT PK_SETOR PRIMARY KEY (CNPJ_Fabrica, COD_SETOR),
                CONSTRAINT FK_SETOR_FABRICA FOREIGN KEY (CNPJ_Fabrica) REFERENCES Fabrica(CNPJ)
            )
        """)
        
        # Maquina
        cursor.execute("""
            CREATE TABLE Maquina (
                ID TEXT PRIMARY KEY,
                Modelo TEXT,
                Data_Instalacao DATE,
                CNPJ_Fabrica_Setor TEXT NOT NULL,
                COD_Setor TEXT NOT NULL,
                CONSTRAINT FK_MAQUINA_SETOR FOREIGN KEY (CNPJ_Fabrica_Setor, COD_Setor) 
                    REFERENCES Setor(CNPJ_Fabrica, COD_SETOR)
            )
        """)
        
        # OompaLoompa
        cursor.execute("""
            CREATE TABLE OompaLoompa (
                CPF_FUNCIONARIO TEXT PRIMARY KEY,
                Tribo TEXT,
                CONSTRAINT FK_OOMPA_FUNC FOREIGN KEY (CPF_FUNCIONARIO) REFERENCES Funcionario(CPF)
            )
        """)
        
        # Pessoa
        cursor.execute("""
            CREATE TABLE Pessoa (
                CPF_FUNCIONARIO TEXT PRIMARY KEY,
                Profissao TEXT,
                CONSTRAINT FK_PESSOA_FUNC FOREIGN KEY (CPF_FUNCIONARIO) REFERENCES Funcionario(CPF)
            )
        """)
        
        # Contatos
        cursor.execute("""
            CREATE TABLE Contatos (
                CPF_CRIANCA TEXT,
                Contatos TEXT,
                CONSTRAINT PK_CONTATOS PRIMARY KEY (CPF_CRIANCA, Contatos),
                CONSTRAINT FK_CONTATOS_CRIANCA FOREIGN KEY (CPF_CRIANCA) REFERENCES Responsavel_Crianca(CPF_CRIANCA)
            )
        """)
        
        # Visita
        cursor.execute("""
            CREATE TABLE Visita (
                CPF_CRIANCA TEXT,
                CNPJ_FABRICA TEXT,
                Data_Visita DATE,
                CONSTRAINT PK_VISITA PRIMARY KEY (CPF_CRIANCA, CNPJ_FABRICA, Data_Visita),
                CONSTRAINT FK_VISITA_CRIANCA FOREIGN KEY (CPF_CRIANCA) REFERENCES Responsavel_Crianca(CPF_CRIANCA),
                CONSTRAINT FK_VISITA_FABRICA FOREIGN KEY (CNPJ_FABRICA) REFERENCES Fabrica(CNPJ)
            )
        """)
        
        # Acidente
        cursor.execute("""
            CREATE TABLE Acidente (
                ID TEXT PRIMARY KEY,
                Data_Acidente DATE NOT NULL,
                Gravidade TEXT,
                Musica TEXT,
                CPF_CRIANCA_VISITA TEXT NOT NULL,
                CNPJ_FABRICA_VISITA TEXT NOT NULL,
                CONSTRAINT FK_ACID_VISITA FOREIGN KEY (CPF_CRIANCA_VISITA, CNPJ_FABRICA_VISITA) 
                    REFERENCES Visita(CPF_CRIANCA, CNPJ_FABRICA)
            )
        """)
        
        # PRODUZ
        cursor.execute("""
            CREATE TABLE PRODUZ (
                ID_CHOCOLATE TEXT,
                CPF_OOMPALOOMPA TEXT,
                ID_MAQUINA TEXT,
                CONSTRAINT PK_PRODUZ PRIMARY KEY (ID_CHOCOLATE, CPF_OOMPALOOMPA, ID_MAQUINA),
                CONSTRAINT FK_PRODUZ_CHOC FOREIGN KEY (ID_CHOCOLATE) REFERENCES Chocolate(ID),
                CONSTRAINT FK_PRODUZ_OOMPA FOREIGN KEY (CPF_OOMPALOOMPA) REFERENCES OompaLoompa(CPF_FUNCIONARIO),
                CONSTRAINT FK_PRODUZ_MAQ FOREIGN KEY (ID_MAQUINA) REFERENCES Maquina(ID)
            )
        """)
        
        # USA
        cursor.execute("""
            CREATE TABLE USA (
                ID_CHOCOLATE TEXT,
                COD_INGREDIENTE TEXT,
                CONSTRAINT PK_USA PRIMARY KEY (ID_CHOCOLATE, COD_INGREDIENTE),
                CONSTRAINT FK_USA_CHOC FOREIGN KEY (ID_CHOCOLATE) REFERENCES Chocolate(ID),
                CONSTRAINT FK_USA_INGR FOREIGN KEY (COD_INGREDIENTE) REFERENCES Ingrediente(COD)
            )
        """)
        
        # Confirmar criação
        conn.commit()
        print("\nTODAS AS TABELAS FORAM CRIADAS COM SUCESSO!")
        
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
    
    # Verificar se o arquivo do banco já existe
    if os.path.exists('fabrica_chocolate.db'):
        resposta = input("Banco de dados já existe. Deseja recriar? (s/n): ").strip().lower()
        if resposta == 's':
            if drop_tables_if_exist():
                print("Recriando tabelas...\n")
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
