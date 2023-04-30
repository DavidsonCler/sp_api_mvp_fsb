from sqlalchemy import Column, String, Integer, DateTime, Float
from datetime import datetime
from typing import Union
from sqlalchemy import ForeignKey

from model import Base


class Produto(Base):
    __tablename__ = 'produto'

    id = Column("pk_produto", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    quantidade = Column(Integer)
    valor = Column(Float)
    valor_total = Column(Float)
    data_insercao= Column(DateTime, default=datetime.now())
   
    # Definição do relacionamento entre o produto e um produto.
    # Aqui está sendo definido a coluna 'produto' que vai guardar
    # a referencia ao produto, a chave estrangeira que relaciona
    # um pedido ao produto.
    pedido_nf= Column("fk_pedido", Integer, ForeignKey("pedido.pk_pedido"), nullable=False)

    def __init__(self, nome: str, quantidade: int, valor: float, valor_total: float,
                 data_insercao: Union[DateTime, None] = None):
        """
        Cria um Produto

        Arguments:
            nome: nome do produto.
            quantidade: quantidade que se espera comprar daquele produto
            valor: valor esperado para o produto
            valor_total: valor total referente à cada produto de acordo com a quantidade
            data_insercao: data de quando o produto foi inserido à base
            
        """
        self.nome = nome
        self.quantidade = quantidade
        self.valor = valor
        self.valor_total = valor_total

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao