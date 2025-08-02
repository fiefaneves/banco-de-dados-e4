// Conecta ao banco de dados 'fabrica_de_chocolate'
db = connect("mongodb://localhost/fabrica_de_chocolate");

// Limpa as coleções para garantir um estado inicial limpo
db.chocolates_ref.drop();
db.ingredientes_ref.drop();

print("--- CENÁRIO 3: Array de Referências N-para-N ---");

// --- I) Implementação ---
print("\n1. Inserindo dados...");
db.ingredientes_ref.insertMany([
  { _id: "ing_ref_01", nome: "Cacau" },
  { _id: "ing_ref_02", nome: "Açúcar de Coco" },
  { _id: "ing_ref_03", nome: "Manteiga de Cacau" }
]);

db.chocolates_ref.insertOne({
  _id: "choco_bc_03",
  nome: "Barra Clássica",
  tipo: "Vegano",
  ingredientes_ids: ["ing_ref_01", "ing_ref_02", "ing_ref_03"]
});
print("Dados inseridos com sucesso.");

// --- II) Consulta ---
print("\n2. Executando consulta...");
print("Consulta: Quais são os nomes dos ingredientes usados no chocolate com nome = 'Barra Clássica'?");

const resultado = db.chocolates_ref.aggregate([
  { $match: { nome: "Barra Clássica" } },
  {
    $lookup: {
      from: "ingredientes_ref",
      localField: "ingredientes_ids",
      foreignField: "_id",
      as: "lista_de_ingredientes"
    }
  },
  {
    $project: {
      _id: 0,
      nomes_dos_ingredientes: "$lista_de_ingredientes.nome"
    }
  }
]).toArray();

printjson(resultado);