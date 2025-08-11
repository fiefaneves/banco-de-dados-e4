from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Conecta ao banco de dados
uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fabrica_de_chocolate"]

# Limpa a coleção de funcionários
db.funcionarios.drop()

print("--- CENÁRIO 1: Referência Simples (Subordinado → Chefe) ---")

# I) Implementação
# Insere primeiro o chefe
db.funcionarios.insert_one({
  "_id": "func001",
  "nome": "João Silva",
  "cpf": "111.111.111-11",
  "salario": 5000
})

# Insere o subordinado, referenciando o _id do seu chefe
db.funcionarios.insert_one({
  "_id": "func002",
  "nome": "Maria Souza",
  "cpf": "222.222.222-22",
  "salario": 3000,
  "chefe_id": "func001"
})

# II) Consulta
print("\nConsulta: Qual é o nome do chefe do funcionário 'Maria Souza'?")

# Busca o funcionário 'Maria Souza'
subordinado_doc = db.funcionarios.find_one({"nome": "Maria Souza"})
if subordinado_doc and "chefe_id" in subordinado_doc:
    chefe_id = subordinado_doc["chefe_id"]
    chefe_doc = db.funcionarios.find_one({"_id": chefe_id})
    if chefe_doc:
        print(f"O chefe de Maria Souza é: {chefe_doc['nome']}")
    else:
        print("Chefe não encontrado.")
else:
    print("Funcionário 'Maria Souza' não encontrado ou não possui chefe.")