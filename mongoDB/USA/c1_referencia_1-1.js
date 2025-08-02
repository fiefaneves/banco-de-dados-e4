// Conecta ao banco de dados 'fabrica_de_chocolate'
db = connect("mongodb://localhost/fabrica_de_chocolate");

// Limpa as coleções para garantir um estado inicial limpo
db.chocolates.drop();
db.ingredientes.drop();

print("--- CENÁRIO 1: Referência 1-para-1 ---");

// --- I) Implementação ---
print("\n1. Inserindo dados...");
db.ingredientes.insertOne({
  _id: "ing_cacau_puro",
  nome: "Cacau Puro 100%",
  origem: "Amazônia"
});

db.chocolates.insertOne({
  _id: "choco_bc_01",
  nome: "Barra Clássica",
  tipo: "Amargo Intenso",
  ingrediente_principal_id: "ing_cacau_puro"
});
print("Dados inseridos com sucesso.");

// --- II) Consulta ---
print("\n2. Executando consulta...");
print("Consulta: Quais são os nomes dos ingredientes usados no chocolate com nome = 'Barra Clássica'?");

const resultado = db.chocolates.aggregate([
  { $match: { nome: "Barra Clássica" } },
  {
    $lookup: {
      from: "ingredientes",
      localField: "ingrediente_principal_id",
      foreignField: "_id",
      as: "info_ingrediente"
    }
  },
  {
    $project: {
      _id: 0,
      nome_ingrediente: { $arrayElemAt: ["$info_ingrediente.nome", 0] }
    }
  }
]).toArray();

printjson(resultado);
