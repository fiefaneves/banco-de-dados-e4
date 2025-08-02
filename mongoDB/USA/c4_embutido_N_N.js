// Conecta ao banco de dados 'fabrica_de_chocolate'
db = connect("mongodb://localhost/fabrica_de_chocolate");

// Limpa a coleção para garantir um estado inicial limpo
db.chocolates_embutido_N_N.drop();

print("--- CENÁRIO 4: Array de Documentos Embutidos N-para-N ---");

// --- I) Implementação ---
print("\n1. Inserindo dados...");
db.chocolates_embutido_N_N.insertOne({
  _id: "choco_bc_04",
  nome: "Barra Clássica",
  tipo: "Vegano",
  ingredientes: [
    { nome: "Cacau", origem: "Bahia" },
    { nome: "Açúcar de Coco", origem: "Indonésia" },
    { nome: "Manteiga de Cacau", origem: "Gana" }
  ]
});
print("Dados inseridos com sucesso.");

// --- II) Consulta ---
print("\n2. Executando consulta...");
print("Consulta: Quais são os nomes dos ingredientes usados no chocolate com nome = 'Barra Clássica'?");

const resultado = db.chocolates_embutido_N_N.find(
  { nome: "Barra Clássica" },
  { _id: 0, "ingredientes.nome": 1 }
).toArray();

printjson(resultado);
