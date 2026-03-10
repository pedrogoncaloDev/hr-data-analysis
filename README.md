# hr-data-analysis

## 📌 Visão Geral

Pipeline ETL completo para análise de dados de RH, desenvolvido em Python com foco em boas práticas de engenharia de software. O projeto extrai dados de planilhas Excel, transforma e normaliza os dados, e os carrega em um banco de dados SQL Server para posterior análise via Power BI.

Pontos que se destacam:

- Arquitetura ETL modular com separação clara de responsabilidades (SRP).
- Pipeline orientado a objetos com classes reutilizáveis e extensíveis.
- Upsert inteligente com `MERGE` do SQL Server — insere novos registros e atualiza os existentes.
- Configuração via `.env` para portabilidade entre ambientes.
- Logging estruturado em todas as camadas do pipeline.
- Type hints em todo o código para maior legibilidade e segurança.

## 🗂️ Estrutura do Projeto

```
hr-data-analysis/
├── data/
│   ├── employees.xlsx
│   └── departaments.xlsx
├── database/
│   ├── database_connection.py   ← classe base de conexão (reutilizável)
│   └── database_setup.py        ← criação do banco e tabelas
├── etl/
│   ├── extractor.py             ← E: leitura dos arquivos Excel
│   ├── transformer.py           ← T: normalização e conversão de tipos
│   └── loader.py                ← L: upsert no SQL Server
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.11+
- SQL Server com ODBC Driver 17 (ou superior)
- Power BI Desktop (para visualização dos dashboards)

### 🔧 Instalação

1. **Clone o repositório**:

```bash
git clone https://github.com/pedrogoncaloDev/hr-data-analysis.git
cd hr-data-analysis
```

2. **Crie e ative o ambiente virtual**:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**:

```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**:

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:

```env
DB_HOST=host
DB_PORT=port
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=name_database
DB_DRIVER=ODBC+Driver+17+for+SQL+Server
```

5. **Execute o pipeline**:

```bash
python main.py
```

## 🧩 Tecnologias & Decisões

- **Python 3.11+**: Type hints, dataclasses e orientação a objetos.
- **Pandas**: Leitura e transformação dos dados Excel.
- **SQLAlchemy 2.0**: ORM e gerenciamento de conexão com SQL Server.
- **PyODBC**: Driver de conexão com SQL Server via ODBC.
- **python-dotenv**: Gerenciamento de variáveis de ambiente.
- **Power BI**: Dashboards conectados diretamente ao SQL Server.

### Camadas do Pipeline

**Extractor (`etl/extractor.py`)**
- Leitura de arquivos `.xlsx` com Pandas.
- Retorna `pd.DataFrame` pronto para transformação.

**Transformer (`etl/transformer.py`)**
- Schema configurável via `DataFrameSchema` — sem colunas hardcoded.
- Conversão de datas, numéricos e booleanos com logging de valores inválidos.
- Trabalha com cópias dos DataFrames originais para evitar mutação.

**DatabaseConnection (`database/database_connection.py`)**
- Classe base herdada por `DatabaseSetup` e `Loader`.
- Engine cacheado — uma única conexão por instância.
- Método `dispose()` para encerramento seguro da conexão.

**DatabaseSetup (`database/database_setup.py`)**
- Cria o banco de dados caso não exista.
- Cria as tabelas com base nos models SQLAlchemy.
- Verificação de existência antes de criar — idempotente.

**Loader (`etl/loader.py`)**
- Upsert via `MERGE` do SQL Server.
- Insere novos registros e atualiza os existentes pela chave primária.
- `IDENTITY_INSERT ON/OFF` para respeitar os IDs vindos do Excel.

## 📊 Dashboards (Power BI)

Os dashboards são conectados diretamente ao banco `hr_db` no SQL Server e cobrem os seguintes temas:

- **Salários e custos** — distribuição salarial por cargo, nível e departamento.
- **Desempenho dos funcionários** — avaliações por área e correlação com horas extras.
- **Distribuição por departamento** — headcount, orçamento e localização.
- **Horas extras** — ranking de horas extras por funcionário e departamento.
- **Ativo vs inativo** — taxa de turnover e distribuição por status.

### Conectando o Power BI ao SQL Server

1. Abra o Power BI Desktop → `Obter Dados` → `SQL Server`
2. Preencha `Servidor: localhost` e `Banco de dados: hr_db`
3. Selecione as tabelas `employees` e `departments`
4. Crie o relacionamento: `employees.dep_id → departments.dep_id`

## About

Pipeline ETL para análise de dados de RH desenvolvido com Python, SQL Server e Power BI, aplicando boas práticas de engenharia de software como SRP, type hints, logging e configuração via variáveis de ambiente.
