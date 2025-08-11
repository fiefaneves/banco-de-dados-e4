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
    "_id": "visita001",
    "nome": "Charlie Bucket",
    "cpf": "11111111111",
    "data_nascimento": "2010-05-15",
    "responsavel_id": "resp001",
    "data_visita": "2025-08-10",
    "fabrica_id": "11.222.333/0001-44"
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

print("Dados inseridos com sucesso.")

# --- II) Consulta ---
print("\n2. Executando consulta...")
print("Consulta: Qual a data de fundação da fábrica visitada por Charlie Bucket?")

crianca_doc = db.visita_criancas.find_one({"nome": "Charlie Bucket"})
if crianca_doc:
    fabrica_id = crianca_doc.get("fabrica_id")
    if fabrica_id:
        fabrica_doc = db.visita_fabricas.find_one({"_id": fabrica_id})
        if fabrica_doc:
            print(f"Data de fundação da fábrica visitada por Charlie Bucket: {fabrica_doc.get('data_fundacao')}")
        else:
            print("Fábrica não encontrada.")
    else:
        print("Criança não possui fábrica associada.")
else:
    print("Criança não encontrada.")