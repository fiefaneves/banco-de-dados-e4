from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Conecta ao banco de dados
uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fabrica_de_chocolate"]

def cenario_2(db):
    db.criancas_com_chocolate_compra.drop()

    print("--- CENÁRIO 2: Documento Embutido Simples (Criança com chocolate embutido) ---")

    db.criancas_com_chocolate_compra.insert_many([
        {
            "_id": "crianca001",
            "nome": "Charlie Bucket",
            "cpf": "11111111111",
            "data_nascimento": "2010-05-15",
            "responsavel_id": "resp001",
            "chocolate": [
                {
                    "chocolate_id": "chocolate001",
                    "nome": "Chocolate ao Leite",
                    "tipo": "Ao Leite",
                }
            ]
        }, 
        {
            "_id": "crianca002",
            "nome": "Augustus Gloop",
            "cpf": "22222222222",
            "data_nascimento": "2010-06-10",
            "responsavel_id": "resp002",
            "chocolate": [
                {
                    "chocolate_id": "chocolate003",
                    "nome": "Chocolate Branco",
                    "tipo": "Branco",
                }
            ]
        },
        {
            "_id": "crianca003",
            "nome": "Veruca Salt",
            "cpf": "33333333333",
            "data_nascimento": "2010-07-20",
            "responsavel_id": "resp003",
            "chocolate": [
                {
                    "chocolate_id": "chocolate004",
                    "nome": "Chocolate Marrom",
                    "tipo": "Ao leite",
                }
            ]
        }
    ])

    print("Dados inseridos com sucesso.")

    print("\nConsulta: Quais são os nomes das crianças com chocolate do tipo 'Ao Leite'?")
    crianca_docs = db.criancas_com_chocolate_compra.find({"chocolates.tipo": "Ao Leite"})
    if crianca_docs:
        for crianca in crianca_docs:
            print(f"Criança: {crianca['nome']}")
    else:
        print("Nenhuma criança encontrada.")

if __name__ == "__main__":
    cenario_2(db)