from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Conecta ao banco de dados
uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fabrica_de_chocolate"]

# Limpa a coleção
db.responsaveis_embutidos.drop()

print("--- CENÁRIO 4: Documentos Embutidos Múltiplos (Responsável com crianças embutidas) ---")

# I) Implementação
print("\n1. Inserindo dados...")
db.responsaveis_embutidos.insert_one({
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
  "criancas": [  # Array de documentos embutidos
    {
      "nome": "Charlie Bucket",
      "cpf": "11111111111",
      "data_nascimento": "2010-05-15",
      "preferencia_chocolate": "Ao Leite"
    },
    {
      "nome": "Violet Beauregarde", 
      "cpf": "33333333333",
      "data_nascimento": "2011-03-10",
      "preferencia_chocolate": "Chiclete Especial"
    },
    {
      "nome": "Augustus Gloop",
      "cpf": "55555555555",
      "data_nascimento": "2009-12-25",
      "preferencia_chocolate": "Chocolate Alemão"
    }
  ]
})
print("Dados inseridos com sucesso.")

# II) Consulta
print("\n2. Executando consulta...")
print("Consulta: Quais são os nomes das crianças que são acompanhadas pelo responsável com nome = 'João Silva'?")

resp_doc = db.responsaveis_embutidos.find_one({"nome": "João Silva"})
if resp_doc and "criancas" in resp_doc:
    print("Crianças acompanhadas por João Silva:")
    for crianca in resp_doc["criancas"]:
        print(f"- {crianca['nome']}")
else:
    print("Responsável não encontrado ou sem crianças.")