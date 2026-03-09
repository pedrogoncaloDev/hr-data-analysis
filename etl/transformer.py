import pandas as pd

class TransformerExcel:
	def __init__(self, df_employees: pd.DataFrame, df_departments: pd.DataFrame):
		self.df_employees = df_employees
		self.df_departments = df_departments
	

	def transform(self) -> tuple[pd.DataFrame, pd.DataFrame]:
		self._convert_dates()
		self._convert_annual_budget()


		return self.df_employees, self.df_departments
	

	def _convert_dates(self):
		self.df_departments['data_criacao'] = pd.to_datetime(self.df_departments['data_criacao'], errors='coerce')
		self.df_employees['data_admissao'] = pd.to_datetime(self.df_employees['data_admissao'], errors='coerce')

	def _convert_annual_budget(self):
		self.df_departments['orcamento_anual'] = pd.to_numeric(self.df_departments['orcamento_anual'], errors='coerce')