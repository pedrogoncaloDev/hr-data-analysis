import logging
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from database.database_connection import DatabaseConnection

logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
	pass


class Department(Base):
	__tablename__ = "departments"

	dep_id            = Column(Integer, primary_key=True, autoincrement=False)
	nome_departamento = Column(String(100), nullable=False)
	gestor            = Column(String(100), nullable=False)
	localizacao       = Column(String(100), nullable=False)
	orcamento_anual   = Column(Integer, nullable=False)
	num_funcionarios  = Column(Integer, nullable=False)
	data_criacao      = Column(DateTime, nullable=False)
	status            = Column(Boolean, nullable=False)


class Employee(Base):
	__tablename__ = "employees"

	func_id              = Column(Integer, primary_key=True, autoincrement=False)
	nome                 = Column(String(100), nullable=False)
	dep_id               = Column(Integer, nullable=False)
	cargo                = Column(String(100), nullable=False)
	salario              = Column(Integer, nullable=False)
	data_admissao        = Column(DateTime, nullable=False)
	cidade               = Column(String(100), nullable=False)
	estado               = Column(String(2), nullable=False)
	nivel                = Column(String(50), nullable=False)
	avaliacao_desempenho = Column(Float, nullable=False)
	horas_extras_mes     = Column(Integer, nullable=False)
	ativo                = Column(Boolean, nullable=False)


class DatabaseSetup(DatabaseConnection):
	def _create_database(self) -> None:
		try:
			engine = create_engine(self._build_url("master"))
			
			with engine.connect() as conn:
				conn.execution_options(isolation_level="AUTOCOMMIT")
				exists = conn.execute(
					text("SELECT 1 FROM sys.databases WHERE name = :name"),
					{"name": self.db_name}
				).fetchone()

				if exists:
					logger.info(f"Banco de dados '{self.db_name}' já existe.")
				else:
					conn.execute(text(f"CREATE DATABASE {self.db_name}"))
					logger.info(f"Banco de dados '{self.db_name}' criado com sucesso.")

		except Exception as e:
			logger.error(f"Erro ao conectar ao SQL Server: {e}")
			raise


	def _create_tables(self) -> None:
		try:
			engine    = create_engine(self._build_url(self.db_name))
			inspector = inspect(engine)

			for model in Base.__subclasses__():
				name = model.__tablename__
				if inspector.has_table(name):
					logger.info(f"Tabela '{name}' já existe.")
				else:
					model.__table__.create(engine)
					logger.info(f"Tabela '{name}' criada com sucesso.")

		except Exception as e:
			logger.error(f"Erro ao criar tabelas: {e}")
			raise


	def run(self) -> None:
		logger.info(f"Iniciando setup do banco de dados '{self.db_name}'...")
		self._create_database()
		self._create_tables()
		logger.info("Setup concluído.")