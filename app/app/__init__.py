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

from app.route.home import home_bp
app.register_blueprint(home_bp)

