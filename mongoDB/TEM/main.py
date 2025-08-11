from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from c1_referencia import c1
from c2_embutido import c2
from c3_referencia import c3
from c4_embutido import c4

def main(db):
    c1(db=db)
    c2(db=db)
    c3(db=db)
    c4(db=db)

if __name__ == "__main__":
    # Conecta ao banco de dados
    uri = "mongodb+srv://fmn:dbuserfmn@cluster10.icefi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster10"
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Testa a conexão
    print("Conectando ao MongoDB...")
    
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
        exit()

    db = client["fabrica_de_chocolate"]
    main(db=db)

    client.close()
    