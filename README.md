# 🍫 Sistema Fábrica de Chocolate

Sistema de banco de dados inspirado em **"Charlie e a Fábrica de Chocolate"** para gerenciar uma fábrica de doces com OompaLoompas, visitantes, produtos e acidentes.

## � Estrutura do Projeto

### 📁 Arquivos Principais

- **`script_tabelas.sql`** - Script SQL original (Oracle) com definições das tabelas
- **`criar_tabelas_fabrica.py`** - Script Python para criar todas as tabelas em SQLite
- **`inserir_dados_exemplo.py`** - Script para inserir dados de exemplo para teste
- **`consultar_fabrica.py`** - Sistema completo de consultas com menu interativo
- **`consultas_simples.py`** - Consultas básicas e contagem de registros
- **`menu_principal.py`** - Menu principal do sistema
- **`README.md`** - Esta documentação

### 🗄️ Banco de Dados

- **`fabrica_chocolate.db`** - Banco SQLite criado automaticamente

## 🎯 Como Usar o Sistema

### Método 1: Menu Principal (Recomendado)
```bash
python menu_principal.py
```

### Método 2: Scripts Individuais

1. **Criar as tabelas:**
   ```bash
   python criar_tabelas_fabrica.py
   ```

2. **Inserir dados de exemplo:**
   ```bash
   python inserir_dados_exemplo.py
   ```

3. **Consultar dados (avançado):**
   ```bash
   python consultar_fabrica.py
   ```

4. **Consultas simples:**
   ```bash
   python consultas_simples.py
   ```

Para popular o banco com dados de teste:

```bash
python inserir_dados_exemplo.py
```

### 3. Consultar os Dados

#### Opção A: Menu Interativo (Recomendado)
```bash
python consultar_fabrica.py
```

Este script oferece um menu com opções:
- Consultar todas as tabelas
- Consultar funcionários e hierarquia
- Consultar produtos de chocolate
- Consultar visitas e acidentes
- Consultar produção
- Consultar ingredientes por produto

#### Opção B: Consultas Simples
```bash
python consultas_simples.py
```

Para consultas básicas e contagem de registros.

### 4. Sistema Original (Tabela Clientes)

O projeto também inclui o sistema original com tabela de clientes:

```bash
# Criar tabela de clientes
python table.py

# Consultar dados da tabela clientes
python consultar_dados.py
# ou
python menu_consultas.py
```

## 📊 Estrutura do Banco de Dados

### Entidades Principais

1. **Responsavel** - Responsáveis pelas crianças
2. **Fabrica** - Dados da fábrica de chocolate
3. **Ingrediente** - Ingredientes usados na produção
4. **Produto** - Produtos fabricados
5. **Funcionario** - Funcionários da fábrica
6. **Criança** - Crianças que visitam a fábrica
7. **Setor** - Setores da fábrica
8. **Maquina** - Máquinas de produção

### Hierarquias de Herança

- **Funcionario**
  - OompaLoompa (com tribo)
  - Pessoa (funcionários humanos)

- **Produto**
  - Chocolate (com tipo, recheio, criança associada)
  - Chiclete

### Relacionamentos

- **Visita** - Crianças visitam a fábrica
- **Acidente** - Acidentes durante visitas
- **PRODUZ** - OompaLoompas produzem produtos
- **USA** - Produtos usam ingredientes
- **BilheteDourado** - Bilhetes dourados em chocolates

## 🔍 Exemplos de Consultas

### Consulta de Funcionários com Hierarquia
```sql
SELECT 
    f1.NOME as Funcionario,
    f2.NOME as Chefe
FROM Funcionario f1
LEFT JOIN Funcionario f2 ON f1.CPF_CHEFE = f2.CPF
```

### Produtos de Chocolate por Criança
```sql
SELECT 
    p.NOME as Produto,
    c.TIPO,
    cr.nome as Crianca
FROM Produto p
JOIN Chocolate c ON p.ID = c.ID_PRODUTO
LEFT JOIN Criança cr ON c.CPF_CRIANCA = cr.CPF
```

### Visitas e Acidentes
```sql
SELECT 
    v.data_visita,
    c.nome as Crianca,
    a.gravidade
FROM Visita v
JOIN Criança c ON v.CPF_Criança = c.CPF
LEFT JOIN Acidente a ON v.CPF_Criança = a.CPF_Criança_Visita
```

## 🛠️ Tecnologias Utilizadas

- **SQLite** - Banco de dados
- **Python 3** - Linguagem de programação
- **sqlite3** - Módulo Python para SQLite

## 📝 Dados de Exemplo

O sistema inclui dados de exemplo com:
- 2 Responsáveis (Pais das crianças)
- 1 Fábrica (Fábrica do Willy Wonka)
- 3 Crianças (Charlie, Veruca, Violet)
- 3 Funcionários (Willy Wonka, 2 OompaLoompas)
- 4 Ingredientes (Cacau, Açúcar, Leite, Avelã)
- 3 Produtos (2 Chocolates, 1 Chiclete)
- 3 Visitas com 1 Acidente
- 1 Bilhete Dourado

## 🤝 Como Contribuir

1. Clone o repositório
2. Crie suas modificações
3. Teste com os scripts de consulta
4. Documente as mudanças

## 📄 Licença

Este projeto é para fins educacionais.

## Scripts Criados

- `criar_tabelas_fabrica.py`: Script em Python para criar as tabelas no banco de dados SQLite.
- `inserir_dados_exemplo.py`: Script em Python para inserir dados de exemplo nas tabelas.
- `consultar_fabrica.py`: Script em Python para consultas avançadas com menu interativo.
- `consultas_simples.py`: Script em Python para consultas básicas.
- `table.py`: Script original para criação da tabela de clientes.
- `consultar_dados.py`: Script para consultas na tabela de clientes.
- `menu_consultas.py`: Menu interativo para consultas na tabela de clientes.

## Considerações Finais

Este projeto é uma implementação educacional e pode ser expandido com mais funcionalidades, como:
- Sistema de login para acesso restrito
- Cadastro e gerenciamento de produtos e funcionários
- Relatórios de produção e visitas
- Integração com sistemas de pagamento e estoque