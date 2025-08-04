from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Conecta ao banco de dados
uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fabrica_de_chocolate"]

# Limpa as coleções
db.responsaveis_refs.drop()
db.criancas_refs.drop()

print("--- CENÁRIO 3: Array de Referências (Responsável com array de crianças) ---")

# I) Implementação
print("\n1. Inserindo dados...")

# Inserir crianças
criancas_data = [
    {"_id": "crianca001", "nome": "Charlie Bucket", "cpf": "11111111111", "data_nascimento": "2010-05-15"},
    {"_id": "crianca002", "nome": "Violet Beauregarde", "cpf": "33333333333", "data_nascimento": "2011-03-10"},
    {"_id": "crianca003", "nome": "Augustus Gloop", "cpf": "55555555555", "data_nascimento": "2009-12-25"}
]
db.criancas_refs.insert_many(criancas_data)

# Inserir responsável com array de referências para crianças
db.responsaveis_refs.insert_one({
  "_id": "resp001",
  "nome": "João Silva",
  "cpf": "12345678901",
  "endereco": {
    "rua": "Rua das Flores, 123",
    "cep": "12345678",
    "bairro": "Centro",
    "estado": "São Paulo"
  },
  "contatos": ["(11) 99999-9999"],
  "criancas_ids": ["crianca001", "crianca002", "crianca003"]  # Array de referências
})
print("Dados inseridos com sucesso.")

# II) Consulta
print("\n2. Executando consulta...")
print("Consulta: Quais são os nomes das crianças que são acompanhadas pelo responsável com nome = 'João Silva'?")

# Busca o responsável João Silva
resp_doc = db.responsaveis_refs.find_one({"nome": "João Silva"})
if resp_doc:
    # Busca crianças usando os IDs do array
    criancas = db.criancas_refs.find({"_id": {"$in": resp_doc["criancas_ids"]}})
    print("Crianças acompanhadas por João Silva:")
    for crianca in criancas:
        print(f"- {crianca['nome']}")
else:
    print("Responsável não encontrado.")