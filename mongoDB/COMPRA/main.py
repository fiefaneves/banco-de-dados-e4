from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from c1_referencia import cenario_1
from c2_embutido import cenario_2
from c3_referencia import cenario_3
from c4_embutido import cenario_4

def main(db):
    cenario_1(db=db)
    cenario_2(db=db)
    cenario_3(db=db)
    cenario_4(db=db)

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
    