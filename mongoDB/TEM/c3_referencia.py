from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Conecta ao banco de dados
uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fabrica_de_chocolate"]

def c3(db):
    db.maquina.drop()
    db.setor.drop()

    print("\n\n\n--- CENÁRIO 3: Array de Referências (Setor com referências a máquinas) ---")
    
    db.maquina.insert_many([
        {
            "_id": "0001",
            "modelo": "Raptor-22",
            "data_instalacao": "20/07/2003"
        },
        {
            "_id": "0002",
            "modelo": "Penta-14",
            "data_instalacao": "27/10/2005"
        },
        {
            "_id": "0003",
            "modelo": "Volvo-17",
            "data_instalacao": "14/01/2010"
        },
        {
            "_id": "0004",
            "modelo": "Optium-61",
            "data_instalacao": "21/06/2020"
        }
    ])

    db.setor.insert_many([
        {
            "_codigo": "83",
            "nome": "Setor de Temperagem",
            "finalidade": "controle de temperatura",
            "data_criacao": "15/04/2000",
            "fabrica_cnpj": "123456",
            "maquina_ids": ["0001", "0003"]
        },
        {
            "_codigo": "92",
            "nome": "Setor de Moldagem",
            "finalidade": "formatação de produtos",
            "data_criacao": "10/03/2001",
            "fabrica_cnpj": "123456",
            "maquina_ids": ["0002", "0004"]
        }
    ])


    print("Dados inseridos com sucesso!")


    print("Consulta: Quais são os modelos das máquinas do setor com finalidade = 'formatação de produtos'?")

    setor_doc = db.setor.find_one({"finalidade": "formatação de produtos"})
    if setor_doc and "maquina_ids" in setor_doc:
        maquina_ids = setor_doc["maquina_ids"]
        maquinas_doc = db.maquina.find({"_id": {"$in": maquina_ids}})
        modelos = [maq["modelo"] for maq in maquinas_doc]
        print("Modelos: ", modelos)
    else:
        print("Setor não encontrado")

if __name__ == "__main__":
    c3(db)
    