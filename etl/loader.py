import logging
import pandas as pd
from sqlalchemy import text
from database.database_connection import DatabaseConnection

logger = logging.getLogger(__name__)


class Loader(DatabaseConnection):
	def __init__(self, primary_keys: dict[str, str], **kwargs):
		super().__init__(**kwargs)  # passa host, port, user... para DatabaseConnection
		self.primary_keys = primary_keys

	def _get_primary_key(self, table_name: str) -> str:
		pk_map = {
			"employees"  : "func_id",
			"departments": "dep_id"
		}
		if table_name not in pk_map:
			raise ValueError(f"Chave primária não definida para a tabela '{table_name}'")
		return pk_map[table_name]


	def _upsert(self, df: pd.DataFrame, table_name: str) -> None:
		engine = self.get_engine()
		pk     = self._get_primary_key(table_name)

		columns     = df.columns.tolist()
		update_cols = [col for col in columns if col != pk]

		set_clause    = ", ".join([f"target.{col} = source.{col}" for col in update_cols])
		insert_cols   = ", ".join(columns)
		insert_values = ", ".join([f"source.{col}" for col in columns])
		source_select = ", ".join([f":{col} AS {col}" for col in columns])  # ← era placeholders_as_cols

		merge_sql = f"""
			MERGE INTO {table_name} AS target
			USING (SELECT {source_select}) AS source
			ON target.{pk} = source.{pk}
			WHEN MATCHED THEN
				UPDATE SET {set_clause}
			WHEN NOT MATCHED THEN
				INSERT ({insert_cols}) VALUES ({insert_values});
		"""

		with engine.begin() as conn:
			for _, row in df.iterrows():
				conn.execute(text(merge_sql), row.to_dict())


	def _load_dataframe(self, df: pd.DataFrame, table_name: str) -> None:
		try:
			self._upsert(df, table_name)
			logger.info(f"Tabela '{table_name}' carregada com sucesso. ({len(df)} registros)")
		except Exception as e:
			logger.error(f"Erro ao carregar tabela '{table_name}': {e}")
			raise


	def load(self, dataframes: dict[str, pd.DataFrame]) -> None:
		try:
			logger.info("Iniciando carregamento dos dados...")
			for table_name, df in dataframes.items():
				self._load_dataframe(df, table_name)
			logger.info("Carregamento concluído.")
		except Exception as e:
			logger.error(f"Erro ao carregar dados: {e}")
			raise
		finally:
			self.dispose()