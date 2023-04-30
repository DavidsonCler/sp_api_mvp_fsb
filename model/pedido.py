from sqlalchemy import Column, Integer, DateTime, Float, String
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union, Optional
from  model import Base, Comentario, Produto


class Pedido(Base):
    __tablename__ = 'pedido'

    nf = Column("pk_pedido", Integer, primary_key=True)
    valor = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())
    cpf_cliente = Column(Integer, unique=True, nullable=False)
    nome_cliente = Column(String(140), unique=True)
    endereco_cliente = Column(String(200))
    telefone_cliente = Column(Integer)
    
    # Definição dos relacionamentos entre: comentario e pedido, e produto e pedido .
    # Essa relação é implicita, não está salva na tabela 'pedido',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario",
                                cascade="all, delete",
                                passive_deletes=True,
                               
                               )
    produtos = relationship("Produto",
                            cascade="all, delete",
                            passive_deletes=True,
                            )
    
    
  
    def __init__(self, nome_cliente: str, cpf_cliente: int, endereco_cliente: str, telefone_cliente: int, data_insercao:Union[DateTime, None] = None):
        """
        Cria um Pedido

        Arguments:
            nome_cliente: nome do cliente.
            cpf_cliente: documento do cliente not_null
            telefone_cliente: numero para contato do cliente
            endereco_cliente: endereço da residencia do cliente
            valor: valor total de um pedido em Float, não declarado no método construtor,
            com todos as instâncias de pedido inicialmente com 0.0 atribuído no valor_total
        """
        self.nome_cliente = nome_cliente
        self.cpf_cliente = cpf_cliente
        self.endereco_cliente = endereco_cliente
        self.telefone_cliente = telefone_cliente 
        self.valor = 0.0
              
        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
   
    
    def valor_pedido(self, produto: Produto, opt:int = 0):
        """
        Adiciona um valor total de um produto + o valor já atribuído na instância de pedido,
        ou subtrai o valor do produto excluído do pedido, com a variável op definindo qual a tratativa, assim atualizando-o
            Arguments:

            valor: valor que consta no pedido
            valor_total: valor total do produto que será somado ao valor do pedido
        """
        if opt == 1:
            self.valor -= produto.valor_total
        else:        
            self.valor += produto.valor_total 
    
    
    def adiciona_produto(self, produto:Produto):
        """ 
        Adiciona um novo produto ao Pedido e também o atualiza o valor do pedido com a função 
        'def valor_pedido(self, produto: Produto)'
        
        """
        self.produtos.append(produto)
        self.valor_pedido(produto)
    
        
    def adiciona_comentario(self, comentario:Comentario):
        """ 
        Adiciona um novo comentário ao Pedido
        
        """
        self.comentarios.append(comentario)

  
   
   