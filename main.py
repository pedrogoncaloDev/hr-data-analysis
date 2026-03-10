from etl.extractor import  ExtractorExcel
from etl.transformer import DataFrameSchema, TransformerExcel


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


# print(df_employees_transformed.head(), df_departments_transformed.head())
print(df_employees_transformed.info(), df_departments_transformed.info())


