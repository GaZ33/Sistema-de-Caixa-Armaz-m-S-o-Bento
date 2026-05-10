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


from app.web.pages_controller import pages_blueprint
from app.web.user_controller import create_user_controller
from app.services.user_service import UserService
from app.web.conta_controller import create_conta_controller
from app.services.conta_service import ContaService
from app.web.log_pagamento_controller import create_log_pagamento_controller
from app.services.log_pagamento_service import LogPagamentoService
from app.web.log_alteracoes_controller import create_log_alteracoes_controller
from app.services.log_alteracoes_service import LogAlteracoesService
from app.web.produto_controller import create_produto_controller
from app.services.produto_service import ProdutoService
from app.web.produto_conta_controller import create_produto_conta_controller
from app.services.produto_conta_service import ProdutoContaService
from app.web.estoque_controller import create_estoque_controller
from app.services.estoque_service import EstoqueService
from app.web.log_estoque_controller import create_log_estoque_controller
from app.services.log_estoque_service import LogEstoqueService
from app.web.avisos_estoque_controller import create_avisos_estoque_controller
from app.services.avisos_estoque_service import AvisosEstoqueService
from app.web.modulo_controller import create_modulo_controller
from app.services.modulo_service import ModuloService
from app.web.perfil_acessos_controller import create_perfil_acessos_controller
from app.services.perfil_acessos_service import PerfilAcessosService
from app.repositories.user_repository import SQLAlchemyUserRepository
from app.repositories.conta_repository import SQLAlchemyContaRepository
from app.repositories.log_pagamento_repository import SQLAlchemyLogPagamentoRepository
from app.repositories.log_alteracoes_repository import SQLAlchemyLogAlteracoesRepository
from app.repositories.produto_repository import SQLAlchemyProdutoRepository
from app.repositories.produto_conta_repository import SQLAlchemyProdutoContaRepository
from app.repositories.estoque_repository import SQLAlchemyEstoqueRepository
from app.repositories.log_estoque_repository import SQLAlchemyLogEstoqueRepository
from app.repositories.avisos_estoque_repository import SQLAlchemyAvisosEstoqueRepository
from app.repositories.modulo_repository import SQLAlchemyModuloRepository
from app.repositories.perfil_acessos_repository import SQLAlchemyPerfilAcessosRepository

# Substituir UserRepository pela implementação concreta SQLAlchemyUserRepository
user_repository = SQLAlchemyUserRepository()  # Substitua pela implementação concreta
user_service = UserService(user_repository)

# Substituir ContaRepository pela implementação concreta SQLAlchemyContaRepository
conta_repository = SQLAlchemyContaRepository()  # Substitua pela implementação concreta
conta_service = ContaService(conta_repository)

# Instanciar o repositório e o serviço para LogPagamento
log_pagamento_repository = SQLAlchemyLogPagamentoRepository()  # Substitua pela implementação concreta
log_pagamento_service = LogPagamentoService(log_pagamento_repository)

# Instanciar o repositório e o serviço para LogAlteracoes
log_alteracoes_repository = SQLAlchemyLogAlteracoesRepository()  # Substitua pela implementação concreta
log_alteracoes_service = LogAlteracoesService(log_alteracoes_repository)

# Instanciar o repositório e o serviço para Produto
produto_repository = SQLAlchemyProdutoRepository()  # Substitua pela implementação concreta
produto_service = ProdutoService(produto_repository)

# Instanciar o repositório e o serviço para ProdutoConta
produto_conta_repository = SQLAlchemyProdutoContaRepository()  # Substitua pela implementação concreta
produto_conta_service = ProdutoContaService(produto_conta_repository)

# Instanciar o repositório e o serviço para Estoque
estoque_repository = SQLAlchemyEstoqueRepository()  # Substitua pela implementação concreta
estoque_service = EstoqueService(estoque_repository)

# Instanciar o repositório e o serviço para LogEstoque
log_estoque_repository = SQLAlchemyLogEstoqueRepository()  # Substitua pela implementação concreta
log_estoque_service = LogEstoqueService(log_estoque_repository)

# Instanciar o repositório e o serviço para AvisosEstoque
avisos_estoque_repository = SQLAlchemyAvisosEstoqueRepository()  # Substitua pela implementação concreta
avisos_estoque_service = AvisosEstoqueService(avisos_estoque_repository)

# Instanciar o repositório e o serviço para Modulo
modulo_repository = SQLAlchemyModuloRepository()  # Substitua pela implementação concreta
modulo_service = ModuloService(modulo_repository)

# Instanciar o repositório e o serviço para PerfilAcessos
perfil_acessos_repository = SQLAlchemyPerfilAcessosRepository()  # Substitua pela implementação concreta
perfil_acessos_service = PerfilAcessosService(perfil_acessos_repository)

# Registrar o blueprint
user_blueprint = create_user_controller(user_service) # Criar o blueprint para as rotas de usuário
app.register_blueprint(user_blueprint, url_prefix='/api') # Registrar o blueprint para as rotas de usuário
app.register_blueprint(pages_blueprint) # Registrar o blueprint para renderização de páginas

# Registrar o blueprint de Conta
conta_blueprint = create_conta_controller(conta_service)
app.register_blueprint(conta_blueprint, url_prefix='/api')

# Registrar o blueprint de LogPagamento
log_pagamento_blueprint = create_log_pagamento_controller(log_pagamento_service)
app.register_blueprint(log_pagamento_blueprint, url_prefix='/api')

# Registrar o blueprint de LogAlteracoes
log_alteracoes_blueprint = create_log_alteracoes_controller(log_alteracoes_service)
app.register_blueprint(log_alteracoes_blueprint, url_prefix='/api')

# Registrar o blueprint de Produto
produto_blueprint = create_produto_controller(produto_service)
app.register_blueprint(produto_blueprint, url_prefix='/api')

# Registrar o blueprint de ProdutoConta
produto_conta_blueprint = create_produto_conta_controller(produto_conta_service)
app.register_blueprint(produto_conta_blueprint, url_prefix='/api')

# Registrar o blueprint de Estoque
estoque_blueprint = create_estoque_controller(estoque_service)
app.register_blueprint(estoque_blueprint, url_prefix='/api')

# Registrar o blueprint de LogEstoque
log_estoque_blueprint = create_log_estoque_controller(log_estoque_service)
app.register_blueprint(log_estoque_blueprint, url_prefix='/api')

# Registrar o blueprint de AvisosEstoque
avisos_estoque_blueprint = create_avisos_estoque_controller(avisos_estoque_service)
app.register_blueprint(avisos_estoque_blueprint, url_prefix='/api')

# Registrar o blueprint de Modulo
modulo_blueprint = create_modulo_controller(modulo_service)
app.register_blueprint(modulo_blueprint, url_prefix='/api')

# Registrar o blueprint de PerfilAcessos
perfil_acessos_blueprint = create_perfil_acessos_controller(perfil_acessos_service)
app.register_blueprint(perfil_acessos_blueprint, url_prefix='/api')




