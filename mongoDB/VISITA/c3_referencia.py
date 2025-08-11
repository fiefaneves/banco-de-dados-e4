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
        "_id": "vis201",
        "data_visita": "2025-08-10",
        "crianca_id": "crianca001",
        "fabrica_cnpj": "11.222.333/0001-44"
    },
    {
        "_id": "vis202",
        "data_visita": "2025-09-02",
        "crianca_id": "crianca001",
        "fabrica_cnpj": "22.333.444/0001-55"
    }
])

db.visita_criancas.insert_one({
    "_id": "crianca001",
    "nome": "Charlie Bucket",
    "cpf": "11111111111",
    "data_nascimento": "2010-05-15",
    "visitas_ids": ["vis201", "vis202"] 
})

print("Dados inseridos com sucesso.")

# --- II) Consulta ---
print("\n2. Executando consulta...")
print("Consulta: Buscar a criança por nome e listar as visitas referenciadas em 'visitas_ids'.")

crianca_doc = db.visita_criancas.find_one({"nome": "Charlie Bucket"})
if crianca_doc:
    ids = crianca_doc.get("visitas_ids", [])
    if ids:
        visitas = list(db.visitas.find({"_id": {"$in": ids}}).sort("data_visita", 1))
        print(f"Visitas de {crianca_doc['nome']}:")
        for v in visitas:
            print(f"- {v.get('data_visita')} | Fábrica CNPJ: {v.get('fabrica_cnpj')}")
    else:
        print("A criança não possui visitas referenciadas.")
else:
    print("Criança não encontrada.")

