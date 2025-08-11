from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Conecta ao banco de dados
uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fabrica_de_chocolate"]

# Limpa a coleção de funcionários
db.funcionarios.drop()

print("--- CENÁRIO 3: Array de Referências (Chefe com array de subordinados) ---")

# I) Implementação
# Insere os subordinados primeiro
db.funcionarios.insert_many([
  {"_id": "func002", "nome": "Maria Souza", "cpf": "222.222.222-22", "salario": 3000},
  {"_id": "func003", "nome": "Pedro Costa", "cpf": "333.333.333-33", "salario": 3500}
])

# Insere o chefe, com um array de _ids de seus subordinados
db.funcionarios.insert_one({
  "_id": "func001",
  "nome": "João Silva",
  "cpf": "111.111.111-11",
  "salario": 5000,
  "subordinados_ids": ["func002", "func003"]
})

# II) Consulta
print("\nConsulta: Quais são os nomes dos subordinados de 'João Silva'?")

# Busca o chefe 'João Silva'
chefe_doc = db.funcionarios.find_one({"nome": "João Silva"})
if chefe_doc and "subordinados_ids" in chefe_doc:
    subordinados_ids = chefe_doc["subordinados_ids"]
    # Busca todos os subordinados cujos _id estão no array
    subordinados_docs = db.funcionarios.find({"_id": {"$in": subordinados_ids}})
    print("Subordinados de João Silva:")
    for subordinado in subordinados_docs:
        print(f"- {subordinado['nome']}")
else:
    print("Chefe 'João Silva' não encontrado ou sem subordinados.")