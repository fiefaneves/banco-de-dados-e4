from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def executar_cenario_1():
    """Cenário 1: Referência Simples - Criança referencia Responsável"""
    print("=" * 80)
    print("CENÁRIO 1: REFERÊNCIA SIMPLES (Criança → Responsável)")
    print("=" * 80)
    
    uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["fabrica_de_chocolate"]
    
    # Limpa coleções
    db.responsaveis.drop()
    db.criancas.drop()
    
    # Inserir dados
    db.responsaveis.insert_one({
        "_id": "resp001",
        "nome": "João Silva",
        "cpf": "12345678901"
    })
    
    db.criancas.insert_one({
        "_id": "crianca001", 
        "nome": "Charlie Bucket",
        "cpf": "11111111111",
        "responsavel_id": "resp001"
    })
    
    # Consulta
    resp_doc = db.responsaveis.find_one({"nome": "João Silva"})
    if resp_doc:
        criancas = db.criancas.find({"responsavel_id": resp_doc["_id"]})
        print("Crianças acompanhadas por João Silva:")
        for crianca in criancas:
            print(f"- {crianca['nome']}")

def executar_cenario_2():
    """Cenário 2: Documento Embutido - Criança com Responsável embutido"""
    print("\n" + "=" * 80)
    print("CENÁRIO 2: DOCUMENTO EMBUTIDO (Criança com Responsável embutido)")
    print("=" * 80)
    
    uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["fabrica_de_chocolate"]
    
    db.criancas_com_responsavel.drop()
    
    db.criancas_com_responsavel.insert_one({
        "_id": "crianca001",
        "nome": "Charlie Bucket", 
        "cpf": "11111111111",
        "responsavel": {
            "nome": "João Silva",
            "cpf": "12345678901"
        }
    })
    
    criancas = db.criancas_com_responsavel.find({"responsavel.nome": "João Silva"})
    print("Crianças acompanhadas por João Silva:")
    for crianca in criancas:
        print(f"- {crianca['nome']}")

def executar_cenario_3():
    """Cenário 3: Array de Referências - Responsável com array de crianças"""
    print("\n" + "=" * 80)
    print("CENÁRIO 3: ARRAY DE REFERÊNCIAS (Responsável → Array de Crianças)")
    print("=" * 80)
    
    uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["fabrica_de_chocolate"]
    
    db.responsaveis_refs.drop()
    db.criancas_refs.drop()
    
    criancas_data = [
        {"_id": "crianca001", "nome": "Charlie Bucket", "cpf": "11111111111"},
        {"_id": "crianca002", "nome": "Violet Beauregarde", "cpf": "33333333333"},
        {"_id": "crianca003", "nome": "Augustus Gloop", "cpf": "55555555555"}
    ]
    db.criancas_refs.insert_many(criancas_data)
    
    db.responsaveis_refs.insert_one({
        "_id": "resp001",
        "nome": "João Silva",
        "cpf": "12345678901", 
        "criancas_ids": ["crianca001", "crianca002", "crianca003"]
    })
    
    resp_doc = db.responsaveis_refs.find_one({"nome": "João Silva"})
    if resp_doc:
        criancas = db.criancas_refs.find({"_id": {"$in": resp_doc["criancas_ids"]}})
        print("Crianças acompanhadas por João Silva:")
        for crianca in criancas:
            print(f"- {crianca['nome']}")

def executar_cenario_4():
    """Cenário 4: Documentos Embutidos Múltiplos - Responsável com crianças embutidas"""
    print("\n" + "=" * 80)
    print("CENÁRIO 4: DOCUMENTOS EMBUTIDOS MÚLTIPLOS (Responsável com crianças embutidas)")
    print("=" * 80)
    
    uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["fabrica_de_chocolate"]
    
    db.responsaveis_embutidos.drop()
    
    db.responsaveis_embutidos.insert_one({
        "_id": "resp001",
        "nome": "João Silva",
        "cpf": "12345678901",
        "criancas": [
            {"nome": "Charlie Bucket", "cpf": "11111111111", "idade": 14},
            {"nome": "Violet Beauregarde", "cpf": "33333333333", "idade": 13},
            {"nome": "Augustus Gloop", "cpf": "55555555555", "idade": 15}
        ]
    })
    
    resp_doc = db.responsaveis_embutidos.find_one({"nome": "João Silva"})
    if resp_doc and "criancas" in resp_doc:
        print("Crianças acompanhadas por João Silva:")
        for crianca in resp_doc["criancas"]:
            print(f"- {crianca['nome']}")

if __name__ == "__main__":
    print("RELACIONAMENTO 'ACOMPANHA' - CRIANÇA ↔ RESPONSÁVEL")
    print("Consulta: 'Quais crianças são acompanhadas pelo responsável João Silva?'")
    
    executar_cenario_1()
    executar_cenario_2() 
    executar_cenario_3()
    executar_cenario_4()
    
    print("\n" + "=" * 80)
    print("TODOS OS CENÁRIOS EXECUTADOS COM SUCESSO!")
    print("=" * 80)