from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Conexão
uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fabrica_de_chocolate"]

# Limpa coleções
db.visita_criancas.drop()
db.visita_fabricas.drop()
db.visitas.drop()

print("--- CENÁRIO 1: VISITA referenciando apenas UM documento (Criança) ---")

# --- I) Implementação ---
print("\n1. Inserindo dados...")

db.visita_criancas.insert_one({
    "_id": "crianca001",
    "nome": "Charlie Bucket",
    "cpf": "11111111111",
    "data_nascimento": "2010-05-15",
    "responsavel_id": "resp001"
})

db.visita_fabricas.insert_many([
    {
        "_id": "11.222.333/0001-44",
        "data_fundacao": "1990-09-01"
    },
    {
        "_id": "22.333.444/0001-55",
        "data_fundacao": "1995-03-12"
    }
])

db.visitas.insert_many([
    {
        "_id": "vis001",
        "data_visita": "2025-08-10",
        "crianca_id": "crianca001",
        "fabrica_cnpj": "11.222.333/0001-44"
    },
    {
        "_id": "vis002",
        "data_visita": "2025-09-02",
        "crianca_id": "crianca001",
        "fabrica_cnpj": "22.333.444/0001-55"
    }
])
print("Dados inseridos com sucesso.")

# --- II) Consulta ---
print("\n2. Executando consulta...")
print("Consulta: Quais são as visitas (data e CNPJ da fábrica) da criança com nome = 'Charlie Bucket'?")

crianca_doc = db.visita_criancas.find_one({"nome": "Charlie Bucket"})
if crianca_doc:
    visitas_cursor = db.visitas.find({"crianca_id": crianca_doc["_id"]}).sort("data_visita", 1)
    visitas = list(visitas_cursor)
    if visitas:
        print(f"Visitas de {crianca_doc['nome']}:")
        for v in visitas:
            print(f"- {v.get('data_visita')} | Fábrica CNPJ: {v.get('fabrica_cnpj')}")
    else:
        print("Nenhuma visita encontrada para a criança 'Charlie Bucket'.")
else:
    print("Criança não encontrada.")