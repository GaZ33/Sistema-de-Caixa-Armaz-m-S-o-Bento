from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
# Todo: adicionar outras extensões conforme a implementação do projeto
# Bcrypt para hashing de senhas, Flask-Login para gerenciamento de sessões, etc.
# dotenv para carregar variáveis de ambiente, etc.
# flask_login para gerenciamento de sessões, etc.
# flask_migrate para migrações de banco de dados, etc.
# Carregando as variáveis do ambiente
load_dotenv()

app = Flask(__name__)

# Configurações do aplicativo
db_connection = os.getenv("DB_CONNECTION")
secret_key = os.getenv("SECRET_KEY")

# Configurações do Flask
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = db_connection

# Inicializando as extensões
db = SQLAlchemy(app)

# Criptografia
bcrypt = Bcrypt(app) 


from app.app.web.pages_controller import pages_blueprint
from app.app.web.user_controller import create_user_controller
from app.app.services.user_service import UserService
from app.app.repositories.user_repository import UserRepository

# Instanciar o repositório e o serviço
user_repository = UserRepository()  # Substitua pela implementação concreta
user_service = UserService(user_repository)

# Registrar o blueprint
user_blueprint = create_user_controller(user_service) # Criar o blueprint para as rotas de usuário
app.register_blueprint(user_blueprint, url_prefix='/api') # Registrar o blueprint para as rotas de usuário
app.register_blueprint(pages_blueprint) # Registrar o blueprint para renderização de páginas




