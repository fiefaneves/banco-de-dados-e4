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

print("--- CENÁRIO 2: VISITA embutindo apenas UM documento (Fábrica) ---")

# --- I) Implementação ---
print("\n1. Inserindo dados...")
db.visita_criancas.insert_one({
    "_id": "crianca001",
    "nome": "Charlie Bucket",
    "cpf": "11111111111",
    "data_nascimento": "2010-05-15",
})

db.visitas.insert_many([
    {
        "_id": "vis101",
        "data_visita": "2025-08-10",
        "crianca_nome": "Charlie Bucket",   
        "crianca_cpf": "11111111111",
        "fabrica": {                       
            "cnpj": "11.222.333/0001-44",
            "data_fundacao": "1990-09-01"
        }
    },
    {
        "_id": "vis102",
        "data_visita": "2025-09-02",
        "crianca_nome": "Charlie Bucket",
        "crianca_cpf": "11111111111",
        "fabrica": {
            "cnpj": "22.333.444/0001-55",
            "data_fundacao": "1995-03-12"
        }
    }
])

print("Dados inseridos com sucesso.")

# --- II) Consulta ---
print("\n2. Executando consulta...")
print("Consulta: Visitas (data e CNPJ da fábrica) da criança com nome = 'Charlie Bucket' (sem referência).")

visitas_cursor = db.visitas.find({"crianca_nome": "Charlie Bucket"}).sort("data_visita", 1)
visitas = list(visitas_cursor)
if visitas:
    print("Visitas de Charlie Bucket:")
    for v in visitas:
        fab = v.get("fabrica", {})
        print(f"- {v.get('data_visita')} | Fábrica CNPJ: {fab.get('cnpj')} | Fundação: {fab.get('data_fundacao')}")
else:
    print("Nenhuma visita encontrada para 'Charlie Bucket'.")
