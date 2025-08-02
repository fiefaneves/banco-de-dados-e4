# 🍫 Sistema Fábrica de Chocolate

Sistema de banco de dados inspirado em **"A Fantástica Fábrica de Chocolate"** para gerenciar uma fábrica de doces com OompaLoompas, visitantes, produtos e acidentes.

## 🗂️ Estrutura do Projeto

### Arquivos Principais

- **`script_tabelas.sql`** - Script SQL original (Oracle) com definições das tabelas
- **`create_table.py`** - Script Python para criar todas as tabelas em SQLite
- **`insert_data.py`** - Script para inserir dados de exemplo para teste
- **`consultas_menu.py`** - Sistema completo de consultas com menu interativo
- **`README.md`** - Documentação

### 🗄️ Banco de Dados

- **`fabrica_chocolate.db`** - Banco SQLite criado automaticamente a partir de `create_table.py`

## 🎯 Como Usar o Sistema

1. **Criar as tabelas:**
   ```bash
   python create_table.py
   ```

2. **Inserir dados:**
   ```bash
   python insert_data.py
   ```

3. **Consultar dados:**
   ```bash
   python consultas_menu.py
   ```

### 🎮 Menu de Consultas

O sistema oferece um menu interativo com as seguintes opções:

- **Opções 1-9**: Executar consultas específicas
- **Opção 10**: Executar todas as consultas em sequência
- **Opção 0**: Sair do sistema

Cada consulta exibe:
- Descrição da operação
- Código SQL utilizado
- Resultados formatados em tabela
- Contagem total de registros encontrados

## 📊 Estrutura do Banco de Dados

![Modelo Relacional](modelo_relacional/image.png)

### Entidades Principais

1. **Responsavel** - Responsáveis pelas crianças
2. **Fabrica** - Dados da fábrica de chocolate
3. **Ingrediente** - Ingredientes usados na produção
4. **Chocolate** - Produtos de chocolate fabricados
5. **Funcionario** - Funcionários da fábrica
6. **Crianca** - Crianças que visitam a fábrica
7. **Setor** - Setores da fábrica
8. **Maquina** - Máquinas de produção

### Hierarquias de Herança

- **Funcionario**
  - OompaLoompa (com tribo)
  - Pessoa (funcionários humanos)

### Relacionamentos

- **Visita** - Crianças visitam a fábrica
- **Acidente** - Acidentes durante visitas
- **PRODUZ** - OompaLoompas produzem chocolates
- **USA** - Chocolates usam ingredientes
- **Contatos** - Contatos dos responsáveis

## 🛠️ Tecnologias Utilizadas

- **SQLite** - Banco de dados
- **Python 3** - Linguagem de programação
- **sqlite3** - Módulo Python para SQLite

## 📝 Consultas implementadas

1. **LEFT JOIN** - Crianças que não compraram chocolates.
2. **INNER JOIN** - Chocolates e seus ingredientes.
3. **UNION** - Todos os CPFs cadastrados no sistema.
4. **SEMI-JOIN** - Crianças que sofreram acidentes.
5. **ANTI-JOIN** - Responsáveis sem crianças.
6. **GROUP BY HAVING** - Tribos com mais de 1 OompaLoompa.
7. **Subconsulta Escalar** - Contagem de ingredientes por chocolate.
8. **Subconsulta de Linha** - Chocolates com mesma data de validade e tipo de CHOC001.
9. **Subconsulta de Tabela** - Responsáveis por crianças acidentadas com alta gravidade.

## 🤝 Como Contribuir

1. Clone o repositório
2. Crie suas modificações
3. Teste com os scripts de consulta
4. Documente as mudanças