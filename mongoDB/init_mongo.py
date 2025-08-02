from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"

# Conecta ao banco de dados 'fabrica_de_chocolate' e define a versão do servidor API
client = MongoClient(uri, server_api=ServerApi('1'))

# Teste de conexão
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)