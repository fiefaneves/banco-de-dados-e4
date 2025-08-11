from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Conecta ao banco de dados
uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fabrica_de_chocolate"]

def c2(db):
    db.setor.drop()

    print("\n\n\n--- CENÁRIO 2: Documento Embutido Simples (Setor máquina embutido) ---")
    
    db.setor.insert_one({
        "_codigo": "37",
        "nome": "Setor de Moagem",
        "finalidade": "processamento de cacau",
        "data_criacao": "15/02/2015",
        "fabrica_cnpj": "4441444",
        "maquinas": [
            {
                "_id": "427",
                "modelo": "Penta-14",
                "data_instalacao": "14/12/2020"
            }
        ]
    })




    print("Dados inseridos com sucesso!")


    print("Consulta: Qual é o modelo da máquina do setor com nome = 'Setor de Moagem'?")

    resultado = db.setor.find_one({"nome": "Setor de Moagem"})
    if resultado and "maquinas" in resultado:
        for maquina in resultado["maquinas"]:
            print(f"Máquina: {maquina.get('modelo', 'N/A')}")
    else:
        print("Setor 'Setor de Moagem' não encontrado")

if __name__ == "__main__":
    c2(db)
    