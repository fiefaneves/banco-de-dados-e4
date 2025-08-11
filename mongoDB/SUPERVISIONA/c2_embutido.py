from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Conecta ao banco de dados
uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fabrica_de_chocolate"]

# Limpa a coleção de funcionários
db.funcionarios.drop()

print("--- CENÁRIO 2: Documento Embutido Simples (Subordinado com Chefe embutido) ---")

# I) Implementação
# Insere o subordinado com o documento do chefe embutido
db.funcionarios.insert_one({
  "_id": "func002",
  "nome": "Maria Souza",
  "cpf": "222.222.222-22",
  "salario": 3000,
  "chefe": {
    "nome": "João Silva",
    "cpf": "111.111.111-11",
    "salario": 5000
  }
})

# II) Consulta
print("\nConsulta: Qual é o nome do chefe do funcionário 'Maria Souza'?")

# Busca o funcionário 'Maria Souza' e extrai o nome do chefe
subordinado_doc = db.funcionarios.find_one({"nome": "Maria Souza"})
if subordinado_doc and "chefe" in subordinado_doc:
    print(f"O chefe de Maria Souza é: {subordinado_doc['chefe']['nome']}")
else:
    print("Funcionário 'Maria Souza' não encontrado ou não possui chefe.")