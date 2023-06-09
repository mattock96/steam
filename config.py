from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

STEAM_API_KEY = '8AB7ABCBD0C22607085362EF8F758022'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'steam'
DB_USER = 'db_manager'
DB_PASSWORD = 'Dbmanagerste@m2023'

# Configurar a URL de conexão com o banco de dados
DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Criar uma instância do engine SQLAlchemy
engine = create_engine(DB_URL)

# Criar uma fábrica de sessões
Session = sessionmaker(bind=engine)
