from pydantic import BaseModel
from typing import List
from model.pedido import Pedido
from model.produto import Produto
from datetime import datetime
# importando modelos
from schemas.comentario import ComentarioSchema
from schemas.produto import ProdutoSchema


class PedidoSchema(BaseModel):
    """ 
    Define como um novo pedido a ser inserido deve ser representado
    
    """
  
    data_insercao: datetime = '%d/%m/%Y'
    cpf_cliente: int = 14465488797
    nome_cliente: str = "Josiclésio Fonte Seca"
    endereco_cliente: str = "Av. Monsenhor - 80, Tijuca-RJ"    
    telefone_cliente: int = 2122526688

class PedidoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita com base na nf do pedido.
    """
    nf: int = 1
   


class ListagemPedidosSchema(BaseModel):
    """ Define como uma listagem de pedidos será retornada.
    """
    pedidos:List[PedidoSchema]


def apresenta_pedidos(pedidos: List[Pedido]):
    """ 
    Retorna uma representação do pedido seguindo o schema definido em
    PedidoViewSchema.
    """
    result = []
    for pedido in pedidos:
        result.append({
            "nf": pedido.nf,
           "data_insercao": pedido.data_insercao,
            "cpf_cliente": pedido.cpf_cliente,
            "nome_cliente": pedido.nome_cliente,
            "telefone_cliente": pedido.telefone_cliente,
            "endereco_cliente": pedido.endereco_cliente,
            "valor": pedido.valor
            
        })

    return {"pedidos": result}


class PedidoViewSchema(BaseModel):
    """ 
    Define como um pedido será retornado: pedido com produtos + comentários.
    
    """
    nf: int = 1
    valor: float = 56.30
    data_insercao: datetime = '%d/%m/%Y'
    cpf_cliente: int = 14465488797
    nome_cliente: str = "Josiclésio Fonte Seca"
    endereco_cliente: str = "Av. Monsenhor, Tijuca-RJ"    
    telefone_cliente: int = 2122526688
    total_produtos: int = 1
    produtos:List[ProdutoSchema]
    total_cometarios: int = 1
    comentarios:List[ComentarioSchema]


class PedidoDelSchema(BaseModel):
    """ 
    Define como deve ser a estrutura do dado retornado após uma requisição
    de remoção.
        
    Arguments:
        nf: Número da Nota Fiscal do pedido
    """
    nf: int = 1

def apresenta_pedido(pedido: Pedido):
        
    """
    Retorna uma representação do pedido seguindo o schema definido em
    PedidoViewSchema.
    
    """
    return {
            "nf": pedido.nf,
            "data_insercao": pedido.data_insercao,
            "cpf_cliente": pedido.cpf_cliente,
            "nome_cliente": pedido.nome_cliente,
            "telefone_cliente": pedido.telefone_cliente,
            "endereco_cliente": pedido.endereco_cliente,
            "valor": pedido.valor,
            "total_produtos": len(pedido.produtos),
            "produtos": [{  "id": p.id,
                            "pedido_nf": p.pedido_nf,
                            "nome": p.nome,
                            "quantidade": p.quantidade,
                            "valor": p.valor,
                            "valor_total": p.valor_total                         
                             } 
                            for p in pedido.produtos],
            "total_cometarios": len(pedido.comentarios),
            "comentarios": [{"texto": c.texto} for c in pedido.comentarios]
    }
    
    
    
def valor_pedido(self, produto: Produto, opt:int = 0):
        """
        Adiciona um valor total de um produto + o valor já atribuído na instância de pedido,
        ou subtrai o valor do produto excluído do pedido, com a variável opt definindo
        qual a tratativa, assim atualizando-o
            Arguments:

            valor: valor que consta no pedido
            valor_total: valor total do produto que será somado ao valor do pedido
        """
        if opt == 1:
            self.valor -= produto.valor_total
        else:        
            self.valor += produto.valor_total 