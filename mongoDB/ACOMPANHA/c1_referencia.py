from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Conecta ao banco de dados
uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fabrica_de_chocolate"]

# Limpa as coleções
db.responsaveis.drop()
db.criancas.drop()

print("--- CENÁRIO 1: Referência Simples (Criança → Responsável) ---")

# I) Implementação
print("\n1. Inserindo dados...")
db.responsaveis.insert_one({
  "_id": "resp001",
  "nome": "João Silva",
  "cpf": "12345678901",
  "endereco": {
    "rua": "Rua das Flores, 123",
    "cep": "12345678",
    "bairro": "Centro",
    "estado": "São Paulo"
  },
  "contatos": ["(11) 99999-9999"]
})

db.criancas.insert_one({
  "_id": "crianca001",
  "nome": "Charlie Bucket",
  "cpf": "11111111111",
  "data_nascimento": "2010-05-15",
  "responsavel_id": "resp001"
})
print("Dados inseridos com sucesso.")

# II) Consulta
print("\n2. Executando consulta...")
print("Consulta: Quais são os nomes das crianças que são acompanhadas pelo responsável com nome = 'João Silva'?")

# Busca o responsável João Silva
resp_doc = db.responsaveis.find_one({"nome": "João Silva"})
if resp_doc:
    # Busca crianças que são acompanhadas por este responsável
    criancas = db.criancas.find({"responsavel_id": resp_doc["_id"]})
    print("Crianças acompanhadas por João Silva:")
    for crianca in criancas:
        print(f"- {crianca['nome']}")
else:
    print("Responsável não encontrado.")