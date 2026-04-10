
from sqlalchemy import Column, ForeignKeyConstraint, Integer, String, Date, DateTime, Enum, DECIMAL, ForeignKey, Index
import sqlalchemy
from sqlalchemy.orm import relationship
from app import db


# Modelo para Usuarios
class Usuarios(db.Model):
    __tablename__ = 'Usuarios'
    idUsuarios = Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(String(45))

# Modelo para Cliente
class Cliente(db.Model):
    __tablename__ = 'Cliente'
    IDCliente = Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(String(45), nullable=False)
    CPF = Column(String(14), nullable=False)
    Telefone = Column(String(15))
    Email = Column(String(100))
    enderecos = relationship('Endereco', back_populates='cliente')
    contas = relationship('Conta', back_populates='cliente')

# Modelo para Endereco
class Endereco(db.Model):
    __tablename__ = 'Endereco'
    IDEndereco = Column(Integer, primary_key=True, autoincrement=True)
    Rua = Column(String(100), nullable=False)
    Bairro = Column(String(100), nullable=False)
    Cidade = Column(String(100), nullable=False)
    Estado = Column(String(50), nullable=False)
    Cliente_IDCliente = Column(Integer, ForeignKey('Cliente.IDCliente'), nullable=False)
    cliente = relationship('Cliente', back_populates='enderecos')
    __table_args__ = (
        Index('fk_Endereco_Cliente_idx', 'Cliente_IDCliente'),
    )

# Modelo para Funcionario
class Funcionario(db.Model):
    __tablename__ = 'Funcionario'
    IDFuncionario = Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(String(45), nullable=False)
    CPF = Column(String(14), nullable=False)
    Login = Column(String(50), nullable=False)
    Senha = Column(String(126), nullable=False)
    contas = relationship('Conta', back_populates='funcionario')

# Modelo para Conta
class Conta(db.Model):
    __tablename__ = 'Conta'
    IDConta = Column(Integer, primary_key=True, autoincrement=True)
    DataCriacao = Column(Date, nullable=False)
    DataModificacao = Column(DateTime)
    DataFechamento = Column(DateTime)
    Status = Column(Enum('aberta', 'fechada'), nullable=False)
    ValorTotal = Column(String(45), nullable=False)
    Cliente_IDCliente = Column(Integer, ForeignKey('Cliente.IDCliente'), nullable=False)
    Funcionario_IDFuncionario = Column(Integer, ForeignKey('Funcionario.IDFuncionario'), nullable=False)
    cliente = relationship('Cliente', back_populates='contas')
    funcionario = relationship('Funcionario', back_populates='contas')
    produtos_conta = relationship('ProdutoConta', back_populates='conta')
    __table_args__ = (
        Index('fk_Conta_Cliente1_idx', 'Cliente_IDCliente'),
        Index('fk_Conta_Funcionario1_idx', 'Funcionario_IDFuncionario'),
    )

# Modelo para Produto
class Produto(db.Model):
    __tablename__ = 'Produto'
    IDProduto = Column(Integer, primary_key=True, autoincrement=True)
    Nome = Column(String(45), nullable=False)
    Marca = Column(String(45), nullable=False)
    Quantidade = Column(Integer, nullable=False)
    Preco = Column(DECIMAL(10, 2), nullable=False)
    LimiteMnimo = Column(Integer, nullable=False)
    produtos_conta = relationship('ProdutoConta', back_populates='produto')

# Modelo para ProdutoConta
class ProdutoConta(db.Model):
    __tablename__ = 'ProdutoConta'
    IDProdutoConta = Column(Integer, primary_key=True, autoincrement=True)
    Quantidade = Column(Integer, nullable=False)
    PrecoUnitario = Column(DECIMAL(10, 2), nullable=False)
    Subtotal = Column(DECIMAL(10, 2), nullable=False)
    Conta_IDConta = Column(Integer, nullable=False)
    Conta_Funcionario_IDFuncionario = Column(Integer, nullable=False)
    Produto_IDProduto = Column(Integer, ForeignKey('Produto.IDProduto'), nullable=False)
    __table_args__ = (
        Index('fk_ProdutoConta_Conta1_idx', 'Conta_IDConta', 'Conta_Funcionario_IDFuncionario'),
        Index('fk_ProdutoConta_Produto1_idx', 'Produto_IDProduto'),
        sqlalchemy.ForeignKeyConstraint(
            ['Conta_IDConta', 'Conta_Funcionario_IDFuncionario'],
            ['Conta.IDConta', 'Conta.Funcionario_IDFuncionario'],
            name='fk_ProdutoConta_Conta1',
        ),
    )
    conta = relationship('Conta', back_populates='produtos_conta',
                        primaryjoin="and_(ProdutoConta.Conta_IDConta==Conta.IDConta, ProdutoConta.Conta_Funcionario_IDFuncionario==Conta.Funcionario_IDFuncionario)")
    produto = relationship('Produto', back_populates='produtos_conta')