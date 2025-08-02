from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Conecta ao banco de dados 'fabrica_de_chocolate' e define a versão do servidor API
uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fabrica_de_chocolate"]

print("--- CENÁRIO 3: Array de Referências ---")

# --- I) Implementação ---
print("\n1. Inserindo dados...")
db.ingredientes.insert_many([
  {"_id": "ing002", "nome": "Cacau", "marca": "Manaus"},
  {"_id": "ing003", "nome": "Açúcar", "marca": "Brasil"},
  {"_id": "ing004", "nome": "Chocolate", "marca": "Amazônia"}
])

db.chocolates.insert_one({
  "_id": "choco003",
  "nome": "Chocolate Meio Amargo",
  "tipo": "Meio Amargo",
  "ingredientes_ids": ["ing002", "ing003", "ing004"]
})
print("Dados inseridos com sucesso.")

# --- II) Consulta ---
print("\n2. Executando consulta...")
print("Consulta: Quais são os nomes dos ingredientes usados no chocolate com nome = 'Chocolate Meio Amargo'?")

# Busca o chocolate com nome 'Chocolate Meio Amargo'
chocolate = db.chocolates.find_one({"nome": "Chocolate Meio Amargo"})
if chocolate and "ingredientes_ids" in chocolate:
  ingredientes_ids = chocolate["ingredientes_ids"]
  ingredientes = db.ingredientes.find({"_id": {"$in": ingredientes_ids}})
  nomes = [ing["nome"] for ing in ingredientes]
  print("Ingredientes:", nomes)
else:
  print("Chocolate 'Chocolate Meio Amargo' não encontrado ou sem ingredientes.")
