from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Conecta ao banco de dados
uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fabrica_de_chocolate"]

# Limpa a coleção
db.criancas_com_responsavel.drop()

print("--- CENÁRIO 2: Documento Embutido Simples (Criança com Responsável embutido) ---")

# I) Implementação
print("\n1. Inserindo dados...")
db.criancas_com_responsavel.insert_one({
  "_id": "crianca001",
  "nome": "Charlie Bucket",
  "cpf": "11111111111",
  "data_nascimento": "2010-05-15",
  "responsavel": {
    "nome": "João Silva",
    "cpf": "12345678901",
    "endereco": {
      "rua": "Rua das Flores, 123",
      "cep": "12345678",
      "bairro": "Centro",
      "estado": "São Paulo"
    },
    "contatos": ["(11) 99999-9999"]
  }
})
print("Dados inseridos com sucesso.")

# II) Consulta
print("\n2. Executando consulta...")
print("Consulta: Quais são os nomes das crianças que são acompanhadas pelo responsável com nome = 'João Silva'?")

criancas = db.criancas_com_responsavel.find({"responsavel.nome": "João Silva"})
print("Crianças acompanhadas por João Silva:")
for crianca in criancas:
    print(f"- {crianca['nome']}")