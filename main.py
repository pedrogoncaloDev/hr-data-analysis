from etl.extractor import  ExtractorExcel

extractor_funcionarios = ExtractorExcel("data/funcionarios.xlsx")
extractor_departamentos = ExtractorExcel("data/departamentos.xlsx")
data_funcionarios = extractor_funcionarios.extract()
data_departamentos = extractor_departamentos.extract()

print('teste')



