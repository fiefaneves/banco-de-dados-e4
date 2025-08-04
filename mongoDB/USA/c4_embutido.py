from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Conecta ao banco de dados 'fabrica_de_chocolate' e define a versão do servidor API
uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fabrica_de_chocolate"]

# Limpa as coleções para garantir um estado inicial limpo
db.chocolates.drop()
db.ingredientes.drop()

print("--- CENÁRIO 4: Array de Documentos Embutidos ---")

# --- I) Implementação ---
print("\n1. Inserindo dados...")
db.chocolates.insert_one({
  "_id": "choco004",
  "nome": "Trufa Especial ao Leite",
  "tipo": "Vegano",
  "ingredientes": [
    {"nome": "Cacau", "marca": "Amazônia"},
    {"nome": "Leite de avelã", "marca": "Brasil"},
    {"nome": "Manteiga de Cacau", "marca": "Amazônia"}
  ]
})
print("Dados inseridos com sucesso.")

# --- II) Consulta ---
print("\n2. Executando consulta...")
print("Consulta: Quais são os nomes dos ingredientes usados no chocolate com nome = 'Trufa Especial ao Leite'?")

resultado = db.chocolates.find_one({"nome": "Trufa Especial ao Leite"})
if resultado and "ingredientes" in resultado:
  ingredientes = resultado["ingredientes"]
  nomes = [ingrediente["nome"] for ingrediente in ingredientes]
  print("Ingredientes:", nomes)
else:
  print("Chocolate 'Trufa Especial ao Leite' não encontrado ou não possui ingredientes.")