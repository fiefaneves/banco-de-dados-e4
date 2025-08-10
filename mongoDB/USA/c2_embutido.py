from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Conecta ao banco de dados 'fabrica_de_chocolate' e define a versão do servidor API
uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fabrica_de_chocolate"]

# Limpa as coleções para garantir um estado inicial limpo
db.chocolates.drop()
db.ingredientes.drop()

print("CENÁRIO 2: Embutido")

print("\n1. Inserindo dados...")
db.chocolates.insert_one({
  "_id": "CHOC002",
  "nome": "Chocolate Ao Leite",
  "tipo": "Ao Leite",
  "ingredientes": [
    {
      "nome": "Cacau",
      "marca": "Amazônia"
    }
  ]
})
print("Dados inseridos com sucesso.")

# Consulta
print("\n2. Executando consulta...")
print("Consulta: Qual o nome do ingrediente usado no chocolate com nome = 'Chocolate Ao Leite'?")

resultado = db.chocolates.find_one({"nome": "Chocolate Ao Leite"})
if resultado and "ingredientes" in resultado:
  for ingrediente in resultado["ingredientes"]:
    print(f"Ingrediente: {ingrediente.get('nome', 'Desconhecido')}")
else:
  print("Chocolate 'Chocolate Ao Leite' não encontrado.")