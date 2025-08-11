from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Conecta ao banco de dados
uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fabrica_de_chocolate"]

def c4(db):
    db.maquina.drop()
    db.setor.drop()

    print("\n\n\n--- CENÁRIO 4: Múltiplos Documentos Embutidos (Setor com máquinas embutidas) ---")
    
    db.setor.insert_one({
            "_codigo": "100",
            "nome": "Setor de Estoque",
            "finalidade": "armazenamento de matéria-prima",
            "data_criacao": "21/05/2005",
            "fabrica_cnpj": "522076",
            "maquinas": [
                {"_id": "1001", "modelo": "Gezi-32", "data_instalacao": "14/06/2011"},
                {"_id": "1015", "modelo": "Kenzi-45", "data_instalacao": "17/10/2013"},
                {"_id": "1018", "modelo": "Babol-03", "data_instalacao": "20/09/2015"},
            ]
        })


    print("Dados inseridos com sucesso!")


    print("Consulta: Quais são os modelos das máquinas do setor com nome = 'Setor de Estoque'?")

    resultado = db.setor.find_one({"nome": "Setor de Estoque"})
    if resultado and "maquinas" in resultado:
        maquinas = resultado["maquinas"]
        modelos = [maquina["modelo"] for maquina in maquinas]
        print("Modelos: ", modelos)
    else:
        print("Setor não encontrado")

if __name__ == "__main__":
    c4(db)
    