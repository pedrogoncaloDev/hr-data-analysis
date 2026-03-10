from etl.extractor import  ExtractorExcel
from etl.transformer import DataFrameSchema, TransformerExcel
from etl.loader import Loader
from database.database_setup import DatabaseSetup

import os
from dotenv import load_dotenv

# extractor
extractor_employees = ExtractorExcel("data/employees.xlsx")
extractor_departaments = ExtractorExcel("data/departaments.xlsx")
data_employees = extractor_employees.extract()
data_departaments = extractor_departaments.extract()


# transformer
schemas = {
    'employees': DataFrameSchema(
        date_columns=['data_admissao'],
		data_booleans=['ativo']
    ),
    'departments': DataFrameSchema(
        date_columns=['data_criacao'],
        numeric_columns=['orcamento_anual'],
		data_booleans=['status']
    )
}

transformer = TransformerExcel(schemas)

result = transformer.transform({
    'employees': data_employees,
    'departments': data_departaments,
})

df_employees_transformed = result['employees']
df_departments_transformed = result['departments']


# Load
load_dotenv()

conn_params = {
    "host"    : os.getenv("DB_HOST"),
    "port"    : int(os.getenv("DB_PORT")),
    "user"    : os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "db_name" : os.getenv("DB_NAME"),
    "driver"  : os.getenv("DB_DRIVER")
}

DatabaseSetup(**conn_params).run()

Loader(
    primary_keys={
        "employees"  : "func_id",
        "departments": "dep_id"
    },
    **conn_params
).load(result)