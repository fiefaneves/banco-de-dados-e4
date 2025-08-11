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

print("--- CENÁRIO 4: Criança EMBUTINDO VÁRIOS documentos de visita ---")

# --- I) Implementação ---
print("\n1. Inserindo dados...")

db.visita_criancas.insert_one({
    "_id": "crianca001",
    "nome": "Charlie Bucket",
    "cpf": "11111111111",
    "data_nascimento": "2010-05-15",
    "fabrica": [
        {
            "data_visita": "2025-08-10",
            "cnpj": "11.222.333/0001-44",
            "data_fundacao": "1990-09-01"
        },
        {
            "data_visita": "2025-09-02",
            "cnpj": "22.333.444/0001-55",
            "data_fundacao": "1995-03-12"
        }
    ]
})

print("Dados inseridos com sucesso.")

# --- II) Consulta ---
print("\n2. Executando consulta...")
print("Consulta: Listar as visitas embutidas da criança com nome = 'Charlie Bucket'.")

doc = db.visita_criancas.find_one({"nome": "Charlie Bucket"})
if doc and "fabrica" in doc:
    print(f"Visitas embutidas de {doc['nome']}:")
    for v in doc["fabrica"]:
        print(f"- {v.get('data_visita')} | Fábrica CNPJ: {v.get('cnpj')} | Fundação: {v.get('data_fundacao')}")
else:
    print("A criança não possui visitas embutidas.")
