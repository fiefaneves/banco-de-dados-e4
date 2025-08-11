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

print("--- CENÁRIO 3: Criança com ARRAY de REFERÊNCIAS para 'visitas' ---")

# --- I) Implementação ---
print("\n1. Inserindo dados...")

db.visita_fabricas.insert_one({
    "_id": "11.222.333/0001-44",
    "data_fundacao": "1990-09-01",
    "visitas_ids": ["vis201","vis202"]
})

db.visitas.insert_many([
    {
        "_id": "vis201",
        "data_visita": "2025-08-10",
        "crianca_id": "crianca002",
        "nome": "Violet Beauregarde",
        "cpf": "22222222222",
        "data_nascimento": "2011-05-15"
    },
    {
        "_id": "vis202",
        "data_visita": "2025-09-02",
        "crianca_id": "crianca001",
        "nome": "Charlie Bucket",
        "cpf": "11111111111",
        "data_nascimento": "2010-05-15"
    }
])

print("Dados inseridos com sucesso.")

# --- II) Consulta ---
print("\n2. Executando consulta...")
print("Consulta: Buscar a data de visita e nome da criança que visitaram a fábrica de CNPJ = 11.222.333/0001-44.")

fabrica_doc = db.visita_fabricas.find_one({"_id": "11.222.333/0001-44"})
if fabrica_doc:
    ids = fabrica_doc.get("visitas_ids", [])
    if ids:
        visitas = list(db.visitas.find({"_id": {"$in": ids}}).sort("data_visita", 1))
        print(f"Visitas da fábrica {fabrica_doc['_id']}:")
        for v in visitas:
            print(f"- {v.get('data_visita')} | Criança: {v.get('nome')}")
    else:
        print("A fábrica não possui visitas referenciadas.")
else:
    print("Fábrica não encontrada.")

