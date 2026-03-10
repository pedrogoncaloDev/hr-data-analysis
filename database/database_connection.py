import logging
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)


class DatabaseConnection:
	def __init__(self, host: str, port: int, user: str, password: str, db_name: str, driver: str = "ODBC+Driver+17+for+SQL+Server"):
		self.host     = host
		self.port     = port
		self.user     = user
		self.password = password
		self.db_name  = db_name
		self.driver   = driver
		self._engine  = None

	def _build_url(self, database: str = None) -> str:
		db = database or self.db_name
		return (
			f"mssql+pyodbc://{self.user}:{self.password}"
			f"@{self.host}:{self.port}/{db}"
			f"?driver={self.driver}"
		)

	def get_engine(self, database: str = None):
		if self._engine is None:
			self._engine = create_engine(self._build_url(database))
			logger.info("Conexão com o banco de dados estabelecida.")
		return self._engine

	def dispose(self):
		if self._engine:
			self._engine.dispose()
			self._engine = None
			logger.info("Conexão com o banco de dados encerrada.")