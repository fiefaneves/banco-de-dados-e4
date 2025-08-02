from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Conecta ao banco de dados 'fabrica_de_chocolate' e define a versão do servidor API
uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fabrica_de_chocolate"]

print("--- CENÁRIO 2: Embutido---")

# --- I) Implementação ---
print("\n1. Inserindo dados...")
db.chocolates.insert_one({
  "_id": "choco002",
  "nome": "Chocolate com Avelã",
  "tipo": "Ao Leite",
  "ingrediente_principal": {
    "nome": "Cacau Puro 100%",
    "marca": "Amazônia"
  }
})
print("Dados inseridos com sucesso.")

# --- II) Consulta ---
print("\n2. Executando consulta...")
print("Consulta: Quais são os nomes dos ingredientes usados no chocolate com nome = 'Chocolate com Avelã'?")

resultado = db.chocolates.find_one({"nome": "Chocolate com Avelã"})
if resultado and "ingrediente_principal" in resultado:
  ingrediente = resultado["ingrediente_principal"]
  print(f"Ingrediente principal: {ingrediente.get('nome', 'Desconhecido')}")
else:
  print("Chocolate 'Chocolate com Avelã' não encontrado ou não possui ingrediente principal.")
