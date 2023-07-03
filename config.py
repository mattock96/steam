from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

STEAM_API_KEY = '8AB7ABCBD0C22607085362EF8F758022'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'steam'
DB_USER = 'matheus'
DB_PASSWORD = 'admin'

url_object = URL.create(
    "postgresql+psycopg2",
    username="matheus",
    password="admin",  # plain (unescaped) text
    host="localhost",
    database="steam",
)

# Configurar a URL de conexão com o banco de dados
DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


# Criar uma instância do engine SQLAlchemy
engine = create_engine(url_object)

# Criar uma fábrica de sessões
Session = sessionmaker(bind=engine)
