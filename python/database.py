import sqlite3

try:
    conn = sqlite3.connect("fabrica_de_chocolate.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE Responsavel (
            CPF TEXT PRIMARY KEY,
            Nome TEXT,
            End_rua TEXT,
            End_cep TEXT,
            End_bairro TEXT
            Estado TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE Fabrica (
            CNPJ TEXT PRIMARY KEY,
            data_fundacao DATE
        )
    """)

    cursor.execute("""
        CREATE TABLE Ingrediente (
            COD TEXT PRIMARY KEY,
            NOME TEXT NOT NULL,
            QTD REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE Produto (
            ID TEXT PRIMARY KEY,
            NOME TEXT NOT NULL,
            PRECO REAL,
            DATA_VAL DATE,
            DESC_PRODUTO TEXT -- Renomeado de DESC para evitar conflito com palavra reservada
        )
    """)

    cursor.execute("""
        CREATE TABLE Funcionario (
            CPF TEXT PRIMARY KEY,
            SALARIO REAL,
            NOME TEXT,
            CPF_CHEFE TEXT,
            CONSTRAINT FK_FUNC_SUPERVISOR FOREIGN KEY (CPF_CHEFE) REFERENCES Funcionario(CPF)
        )
    """)

    cursor.execute("""
        CREATE TABLE Criança (
            CPF TEXT PRIMARY KEY,
            nome TEXT,
            data_nascimento DATE,
            CPF_Responsavel TEXT,
            CONSTRAINT FK_CRIANCA_RESP FOREIGN KEY (CPF_Responsavel) REFERENCES Responsavel(CPF)
        )
    """)

    cursor.execute("""
        CREATE TABLE Setor (
            CNPJ_Fabrica TEXT,
            codigo TEXT,
            nome TEXT,
            finalidade TEXT,
            data_criacao DATE, -- Renomeado de data para data_criacao
            CONSTRAINT PK_SETOR PRIMARY KEY (CNPJ_Fabrica, codigo),
            CONSTRAINT FK_SETOR_FABRICA FOREIGN KEY (CNPJ_Fabrica) REFERENCES Fabrica(CNPJ)
        )
    """)

    cursor.execute("""
        CREATE TABLE Maquina (
            ID TEXT PRIMARY KEY,
            MODELO TEXT,
            DATA_INST DATE,
            CNPJ_Fabrica_Setor TEXT NOT NULL,
            COD_Setor TEXT NOT NULL,
            CONSTRAINT FK_MAQUINA_SETOR FOREIGN KEY (CNPJ_Fabrica_Setor, COD_Setor) REFERENCES Setor(CNPJ_Fabrica, codigo)
        )
    """)

    cursor.execute("""
        CREATE TABLE OompaLoompa (
            CPF_FUNC TEXT PRIMARY KEY,
            TRIBO TEXT,
            CONSTRAINT FK_OOMPA_FUNC FOREIGN KEY (CPF_FUNC) REFERENCES Funcionario(CPF)
        )
    """)

    cursor.execute("""
        CREATE TABLE Pessoa (
            CPF_FUNC TEXT PRIMARY KEY,
            CONSTRAINT FK_PESSOA_FUNC FOREIGN KEY (CPF_FUNC) REFERENCES Funcionario(CPF)
        )
    """)

    cursor.execute("""
        CREATE TABLE Chiclete (
            ID_PRODUTO TEXT PRIMARY KEY,
            CONSTRAINT FK_CHICLETE_PROD FOREIGN KEY (ID_PRODUTO) REFERENCES Produto(ID)
        )
    """)

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

    cursor.execute("""
        CREATE TABLE Contatos (
            CPF_Responsavel TEXT,
            Contatos TEXT,
            CONSTRAINT PK_CONTATOS PRIMARY KEY (CPF_Responsavel, Contatos),
            CONSTRAINT FK_CONTATOS_RESP FOREIGN KEY (CPF_Responsavel) REFERENCES Responsavel(CPF)
        )
    """)

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

    cursor.execute("""
        CREATE TABLE Acidente (
            ID TEXT PRIMARY KEY,
            data_acidente DATE,
            gravidade TEXT,
            musica TEXT,
            CPF_Criança_Visita TEXT,
            CNPJ_Fabrica_Visita TEXT,
            CONSTRAINT FK_ACID_VISITA FOREIGN KEY (CPF_Criança_Visita, CNPJ_Fabrica_Visita) REFERENCES Visita(CPF_Criança, CNPJ_Fabrica),
            CONSTRAINT AK_ACID_VISITA UNIQUE (CPF_Criança_Visita, CNPJ_Fabrica_Visita) -- Garante que uma visita tenha no máximo um acidente
        )
    """)

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

    cursor.execute("""
        CREATE TABLE USA (
            ID_PRODUTO TEXT,
            COD_INGREDIENTE TEXT,
            CONSTRAINT PK_USA PRIMARY KEY (ID_PRODUTO, COD_INGREDIENTE),
            CONSTRAINT FK_USA_PROD FOREIGN KEY (ID_PRODUTO) REFERENCES Produto(ID),
            CONSTRAINT FK_USA_INGR FOREIGN KEY (COD_INGREDIENTE) REFERENCES Ingrediente(COD)
        )
    """)

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

    conn.commit()
    conn.close()

    print("Criado com sucesso")

except sqlite3.Error as e:
    print(f"Erro ao criar tabelas: {e}")