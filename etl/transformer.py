import pandas as pd
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

@dataclass
class DataFrameSchema:
	date_columns: list[str] = field(default_factory=list)
	numeric_columns: list[str] = field(default_factory=list)
	data_booleans: list[str] = field(default_factory=list)


class TransformerExcel:
	def __init__(self, schemas: dict[str, DataFrameSchema]):
		self.schemas = schemas


	def transform(self, dataframes: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
		result = {}

		for name, df in dataframes.items():
			if name not in self.schemas:
				logger.warning(f"Nenhum schema encontrado para '{name}', pulando...")
				result[name] = df.copy()
				continue

			result[name] = self._apply_schema(df.copy(), self.schemas[name])

		return result


	def _apply_schema(self, df: pd.DataFrame, schema: DataFrameSchema) -> pd.DataFrame:
		df = self._convert_dates(df, schema.date_columns)
		df = self._convert_numerics(df, schema.numeric_columns)
		df = self._convert_booleans(df, schema.data_booleans)
		return df


	def _convert_dates(self, df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
		for col in columns:
			if col not in df.columns:
				logger.warning(f"Coluna '{col}' não encontrada no DataFrame")
				continue

			converted = pd.to_datetime(df[col], errors='coerce')
			nulls = converted.isna().sum()
			if nulls > 0:
				logger.warning(f"{nulls} datas inválidas na coluna '{col}'")

			df[col] = converted
		return df


	def _convert_numerics(self, df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
		for col in columns:
			if col not in df.columns:
				logger.warning(f"Coluna '{col}' não encontrada no DataFrame")
				continue

			converted = pd.to_numeric(df[col], errors='coerce')
			nulls = converted.isna().sum()
			if nulls > 0:
				logger.warning(f"{nulls} valores numéricos inválidos na coluna '{col}'")

			df[col] = converted
		return df
	

	def _convert_booleans(self, df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
		mapping = {"VERDADEIRO": True, "FALSO": False, "Ativo": True, "Inativo": False}
		
		for col in columns:
			if col not in df.columns:
				logger.warning(f"Coluna '{col}' não encontrada no DataFrame")
				continue

			if df[col].dtype == bool:
				logger.info(f"Coluna '{col}' já é bool, pulando conversão")
				continue

			df[col] = df[col].map(mapping)
    
		return df