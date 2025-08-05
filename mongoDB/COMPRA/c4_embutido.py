from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Conecta ao banco de dados
uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fabrica_de_chocolate"]

def cenario_4(db):
    db.criancas.drop()

    print("--- CENÁRIO 1: Array de Referências (Criança com referências a Chocolate) ---")

    db.criancas.insert_many([
        {
            "_id": "crianca001",
            "nome": "Charlie Bucket",
            "cpf": "11111111111",
            "data_nascimento": "2010-05-15",
            "responsavel_id": "resp001",
            "chocolates": [
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
            ]
        }, 
        {
            "_id": "crianca002",
            "nome": "Augustus Gloop",
            "cpf": "22222222222",
            "data_nascimento": "2010-06-10",
            "responsavel_id": "resp002",
            "chocolates": [
                {
                    "_id": "chocolate003",
                    "nome": "Chocolate Branco",
                    "tipo" : "Branco",
                },
                {
                    "_id": "chocolate004",
                    "nome": "Chocolate Marrom",
                    "tipo" : "Ao leite",
                },
            ]
        },
        {
            "_id": "crianca003",
            "nome": "Veruca Salt",
            "cpf": "33333333333",
            "data_nascimento": "2010-07-20",
            "responsavel_id": "resp003",
            "chocolates": [
                {
                    "_id": "chocolate005",
                    "nome": "Chocolate Meio Amargo",
                    "tipo" : "Meio Amargo",
                },
                {
                    "_id": "chocolate006",
                    "nome": "Chocolate Amargo com Avelã",
                    "tipo" : "Amargo com Avelã",
                }
            ]
        }
    ])

    print("Dados inseridos com sucesso.")

    print("\nConsulta: Quais são os nomes das crianças que compraram chocolates do tipo 'Ao Leite' ou 'Amargo'?")
    crianca_docs = db.criancas.find({"chocolates.tipo": {"$in": ["Ao Leite", "Amargo"]}})
    if crianca_docs:
        for crianca in crianca_docs:
            print(f"Criança que comprou chocolate do tipo 'Ao Leite' ou 'Amargo': {crianca['nome']}")
    else:
        print("Nenhuma criança encontrada.")