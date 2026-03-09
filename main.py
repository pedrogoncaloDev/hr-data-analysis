from etl.extractor import  ExtractorExcel
from etl.transformer import TransformerExcel


extractor_employees = ExtractorExcel("data/employees.xlsx")
extractor_departaments = ExtractorExcel("data/departaments.xlsx")
data_employees = extractor_employees.extract()
data_departaments = extractor_departaments.extract()


df_employees, df_departments = TransformerExcel(data_employees, data_departaments).transform()


print(df_departments.info(), df_employees.info())


