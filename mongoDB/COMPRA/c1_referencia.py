from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Conecta ao banco de dados
uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fabrica_de_chocolate"]

def cenario_1(db):
    db.chocolates.drop()
    db.criancas.drop()

    print("--- CENÁRIO 1: Referência Simples (Criança com referência a Chocolate) ---")

    db.chocolates.insert_many([
        {
            "_id": "chocolate001",
            "nome": "Chocolate ao Leite",
            "tipo" : "Ao Leite",
        },
        {
            "_id": "chocolate002",
            "nome": "Chocolate Amargo",
            "tipo" : "Amargo",
        },
        {
            "_id": "chocolate003",
            "nome": "Chocolate Branco",
            "tipo" : "Branco",
        }
    ])

    db.criancas.insert_many([
        {
            "_id": "crianca001",
            "nome": "Charlie Bucket",
            "cpf": "11111111111",
            "data_nascimento": "2010-05-15",
            "responsavel_id": "resp001",
            "chocolate_id": "chocolate001"
        }, 
        {
            "_id": "crianca002",
            "nome": "Augustus Gloop",
            "cpf": "22222222222",
            "data_nascimento": "2010-06-10",
            "responsavel_id": "resp002",
            "chocolate_id": "chocolate002"
        },
        {
            "_id": "crianca003",
            "nome": "Veruca Salt",
            "cpf": "33333333333",
            "data_nascimento": "2010-07-20",
            "responsavel_id": "resp003",
            "chocolate_id": "chocolate003"
        }
    ])

    print("Dados inseridos com sucesso.")

    print("\nConsulta: Quais são os nomes dos chocolates consumidos por Charlie Bucket?")
    crianca_doc = db.criancas.find_one({"nome": "Charlie Bucket"})
    if crianca_doc:
        chocolate_doc = db.chocolates.find({"_id": crianca_doc["chocolate_id"]})
        if chocolate_doc:
            for chocolate in chocolate_doc:
                print(f"Charlie Bucket consumiu o chocolate: {chocolate['nome']}")
        else:
            print("Chocolate não encontrado.")
    else:
        print("Criança não encontrada.")