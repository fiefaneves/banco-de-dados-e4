// Conecta ao banco de dados 'fabrica_de_chocolate'
db = connect("mongodb://localhost/fabrica_de_chocolate");

// Limpa a coleção para garantir um estado inicial limpo
db.chocolates_embutido_1_1.drop();

print("--- CENÁRIO 2: Embutido 1-para-1 ---");

// --- I) Implementação ---
print("\n1. Inserindo dados...");
db.chocolates_embutido_1_1.insertOne({
  _id: "choco_bc_02",
  nome: "Barra Clássica",
  tipo: "Amargo Intenso",
  ingrediente_principal: {
    nome: "Cacau Puro 100%",
    origem: "Amazônia"
  }
});
print("Dados inseridos com sucesso.");

// --- II) Consulta ---
print("\n2. Executando consulta...");
print("Consulta: Quais são os nomes dos ingredientes usados no chocolate com nome = 'Barra Clássica'?");

const resultado = db.chocolates_embutido_1_1.find(
  { nome: "Barra Clássica" },
  { _id: 0, "ingrediente_principal.nome": 1 }
).toArray();

printjson(resultado);