from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Conecta ao banco de dados
uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["fabrica_de_chocolate"]

# Limpa a coleção de funcionários
db.funcionarios.drop()

print("--- CENÁRIO 4: Documentos Embutidos Múltiplos (Chefe com subordinados embutidos) ---")

# I) Implementação
# Insere o chefe com um array de documentos de subordinados
db.funcionarios.insert_one({
  "_id": "func001",
  "nome": "João Silva",
  "cpf": "111.111.111-11",
  "salario": 5000,
  "subordinados": [
    {
      "nome": "Maria Souza",
      "cpf": "222.222.222-22",
      "salario": 3000
    },
    {
      "nome": "Pedro Costa",
      "cpf": "333.333.333-33",
      "salario": 3500
    }
  ]
})

# II) Consulta
print("\nConsulta: Quais são os nomes dos subordinados de 'João Silva'?")

# Busca o documento do chefe e percorre o array de subordinados embutidos
chefe_doc = db.funcionarios.find_one({"nome": "João Silva"})
if chefe_doc and "subordinados" in chefe_doc:
    print("Subordinados de João Silva:")
    for subordinado in chefe_doc["subordinados"]:
        print(f"- {subordinado['nome']}")
else:
    print("Chefe 'João Silva' não encontrado ou sem subordinados.")