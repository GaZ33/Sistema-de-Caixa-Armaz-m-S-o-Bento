from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum, DECIMAL, Float, Text
from sqlalchemy.orm import relationship
from app import db

class Perfil(db.Model):
    __tablename__ = 'perfil'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(35), nullable=False, unique=True)
    data_alteracao = Column(DateTime, nullable=True)
    data_criacao = Column(DateTime, nullable=False)

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    perfil_id = Column(Integer, ForeignKey('perfil.id'), nullable=False)
    nome = Column(String(20), nullable=False)
    sobrenome = Column(String(45), nullable=True)
    email = Column(String(85), nullable=True, unique=True)
    cpf = Column(String(45), nullable=True, unique=True)
    senha = Column(String(256), nullable=False)
    salt = Column(String(124), nullable=False)
    username = Column(String(25), nullable=False, unique=True)
    data_criacao = Column(DateTime, nullable=True)
    data_alteracao = Column(DateTime, nullable=True)
    telefone = Column(String(15), nullable=True)

class Conta(db.Model):
    __tablename__ = 'conta'

    id = Column(Integer, primary_key=True, autoincrement=True)
    funcionario = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    cliente = Column(Integer, ForeignKey('usuario.id'), nullable=True)
    data_criacao = Column(DateTime, nullable=False)
    data_alteracao = Column(DateTime, nullable=True)
    data_fechamento = Column(DateTime, nullable=True)
    status = Column(Enum("aberta", "fechada"), nullable=False)
    valor_total = Column(DECIMAL, nullable=False)

class LogPagamento(db.Model):
    __tablename__ = 'logPagamento'

    id = Column(Integer, primary_key=True, autoincrement=True)
    forma_pagamento = Column(Enum("dinheiro", "cartao_credito", "cartao_debito", "pix"), nullable=True)
    valor_pago = Column(DECIMAL, nullable=False)
    data_pagamento = Column(DateTime, nullable=True)
    conta_id = Column(Integer, ForeignKey('conta.id'), nullable=False)

class LogAlteracoes(db.Model):
    __tablename__ = 'logAlteracoes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    tabela_afetada = Column(String(45), nullable=True)
    acao = Column(Enum("insert", "update", "delete"), nullable=False)
    valor_antigo = Column(Text, nullable=True)
    valor_novo = Column(Text, nullable=True)
    data_evento = Column(DateTime, nullable=False)

class Produto(db.Model):
    __tablename__ = 'produto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(45), nullable=False)
    preco_unidade = Column(DECIMAL, nullable=False)
    unidade = Column(Enum("pacote", "unidade", "kg", "ml"), nullable=False)
    codigo = Column(String(25), nullable=False, unique=True)
    marca = Column(String(45), nullable=False)

class ProdutoConta(db.Model):
    __tablename__ = 'produtoConta'

    id = Column(Integer, primary_key=True, autoincrement=True)
    conta_id = Column(Integer, ForeignKey('conta.id'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produto.id'), nullable=False)
    quantidade = Column(Float, nullable=False)
    preco_unitario = Column(DECIMAL, nullable=False)
    subtotal = Column(DECIMAL, nullable=False)

class Estoque(db.Model):
    __tablename__ = 'estoque'

    id = Column(Integer, primary_key=True, autoincrement=True)
    produto_id = Column(Integer, ForeignKey('produto.id'), nullable=False)
    quantidade_atual = Column(Float, nullable=False)
    quantidade_minima = Column(Float, nullable=True)
    data_alteracao = Column(DateTime, nullable=True)

class LogEstoque(db.Model):
    __tablename__ = 'logEstoque'

    id = Column(Integer, primary_key=True, autoincrement=True)
    estoque_id = Column(Integer, ForeignKey('estoque.id'), nullable=False)
    movimentacao = Column(Enum("entrada", "saida"), nullable=True)
    quantidade = Column(Float, nullable=True)
    motivo = Column(Enum("venda", "reposicao", "perda"), nullable=True)

class AvisosEstoque(db.Model):
    __tablename__ = 'avisosEstoque'

    id = Column(Integer, primary_key=True, autoincrement=True)
    estoque_id = Column(Integer, ForeignKey('estoque.id'), nullable=False)
    descricao = Column(Text, nullable=True)
    status = Column(Enum("pendente", "visualizado", "resolvido"), nullable=True)

class Modulo(db.Model):
    __tablename__ = 'modulo'

    idmodulo = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(25), nullable=False, unique=True)
    codigo = Column(String(4), nullable=False, unique=True)

class PerfilAcessos(db.Model):
    __tablename__ = 'perfilAcessos'
    alterar = Column(Boolean, nullable=True)
    excluir = Column(Boolean, nullable=True)
    inserir = Column(Boolean, nullable=True)
    ler = Column(Boolean, nullable=True)

    idperfilAcessos = Column(Integer, primary_key=True, autoincrement=True)
    modulo_idmodulo = Column(Integer, ForeignKey('modulo.idmodulo'), nullable=False)
    perfil_id = Column(Integer, ForeignKey('perfil.id'), nullable=False)

