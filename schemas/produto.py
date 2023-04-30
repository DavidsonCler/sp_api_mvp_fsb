from pydantic import BaseModel
from typing import Optional, List
from model.produto import Produto


class ProdutoSchema(BaseModel):
    """ Define como um novo produto a ser inserido deve ser representado
    """
    pedido_nf: int = 1
    nome: str = "Banana Prata"
    quantidade: Optional[int] = 12
    valor: float = 12.50
    valor_total: float = (quantidade * valor) #registrará o valor vezes a quantidade


class ProdutoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita com base no nome ou NF do pedido.
    """
    id: int = 1
    pedido_nf: int = 1
    mesage: str = "Produto removido",
    nome: str = "Paçoca 500g"


class ListagemProdutosSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    produtos:List[ProdutoSchema]


def apresenta_produtos(produtos: List[Produto]):
    """ Retorna uma representação do produtos seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    total_compra:float = 0.0
    for produto in produtos:
        total_compra:float = (total_compra + produto.valor_total)
        result.append({
            "id": produto.id,
            "nome": produto.nome,
            "quantidade": produto.quantidade,
            "valor": produto.valor,
            "valor_total": produto.valor_total
        })

    return {"produtos": result, "total_compra":total_compra}


class ProdutoViewSchema(BaseModel):
    """ Define como um produto será retornado: produto e seu valor total.
    """
    id: int = 1
    pedido_nf: int = 1
    nome: str = "Banana Prata"
    quantidade: Optional[int] = 12
    valor: float = 12.50
    valor_total: float = (quantidade * valor) #retornará o valor vezes a quantidade




class ProdutoDelSchema(BaseModel):
    """ 
    Define como deve ser a estrutura do dado retornado após uma requisição
    de remoção.
        
    Arguments:
        nf: Número da Nota Fiscal do pedido
    """
    id: int = 1
    mesage: str = "Produto removido"
  

def apresenta_produto(produto: Produto):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "id": produto.id,
        "pedido_nf": produto.pedido_nf,
        "nome": produto.nome,
        "quantidade": produto.quantidade,
        "valor": produto.valor,
        "valor_total": produto.valor_total
        }
