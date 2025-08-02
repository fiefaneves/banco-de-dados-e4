from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Conecta ao banco de dados 'fabrica_de_chocolate' e define a versão do servidor API
uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fabrica_de_chocolate"]

# Limpa as coleções para garantir um estado inicial limpo
db.chocolates.drop()
db.ingredientes.drop()

print("--- CENÁRIO 1: Referência ---")

# --- I) Implementação ---
print("\n1. Inserindo dados...")
db.ingredientes.insert_one({
  "_id": "ing001",
  "nome": "Cacau Puro 100%",
  "marca": "Amazônia"
})

db.chocolates.insert_one({
  "_id": "choco001",
  "nome": "Barra Clássica",
  "tipo": "Amargo Intenso",
  "ingrediente_principal_id": "ing001"
})
print("Dados inseridos com sucesso.")

# --- II) Consulta ---
print("\n2. Executando consulta...")
print("Consulta: Quais são os nomes dos ingredientes usados no chocolate com nome = 'Barra Clássica'?")

# Busca o chocolate com nome 'Barra Clássica'
chocolate_doc = db.chocolates.find_one({"nome": "Barra Clássica"})
if chocolate_doc:
  ingrediente_id = chocolate_doc["ingrediente_principal_id"]
  ingrediente_doc = db.ingredientes.find_one({"_id": ingrediente_id})
  print("Ingredientes usados no chocolate 'Barra Clássica':")
  if ingrediente_doc:
    print(ingrediente_doc["nome"])
  else:
    print("Ingrediente não encontrado.")
else:
  print("Chocolate não encontrado.")


