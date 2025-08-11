from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Conecta ao banco de dados
uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fabrica_de_chocolate"]

def c1(db):
    db.maquina.drop()
    db.setor.drop()

    print("--- CENÁRIO 1: Referência Simples (Setor com referência a máquina) ---")
    
    db.maquina.insert_one({
        "_id": "0001",
        "modelo": "Raptor-22",
        "data_instalacao": "20/07/2003"
    })

    db.setor.insert_one({
        "_codigo": "22",
        "nome": "QA",
        "finalidade": "controle de qualidade",
        "data_criacao": "15/04/2000",
        "fabrica_cnpj": "123456",
        "maquina_id": "0001"
    })


    print("Dados inseridos com sucesso!")


    print("Consulta: Qual é o modelo da máquina do setor com finalidade = 'controle de qualidade'?")

    setor_doc = db.setor.find_one({"finalidade": "controle de qualidade"})
    if setor_doc:
        maquina_id = setor_doc["maquina_id"]
        maquina_doc = db.maquina.find_one({"_id": maquina_id})
        if maquina_doc:
            print(f"Modelo da máquina: {maquina_doc['modelo']}")
        else:
            print("Máquina não encontrada")
    else:
        print("Setor não encontrado")

if __name__ == "__main__":
    c1(db)
    