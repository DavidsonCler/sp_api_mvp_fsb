from pydantic import BaseModel
from model.comentario import Comentario
from typing import List



class ComentarioSchema(BaseModel):
    """ Define como um novo comentário a ser inserido deve ser representado
    """
    pedido_nf: int = 1
    texto: str = "O cliente só estará em casa às 21:02!"

class ComentarioDelSchema(BaseModel):
    """ 
    Define como deve ser a estrutura do dado retornado após uma requisição
    de remoção.
        
    Arguments:
        nf: Número da Nota Fiscal do Comentario
    """
    id: int = 1
    mesage: str = "Comentário removido"
    


class ComentarioBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita com base na nf do pedido.
    """
    id: int = 1
    pedido_nf: int =1


class ListagemComentariosSchema(BaseModel):
    """ Define como uma listagem de comentarios será retornada.
    """
    comentarios:List[ComentarioSchema]    
    
def apresenta_comentarios(comentarios: List[Comentario]):
    """ Retorna uma representação do comentarios seguindo o schema definido em
        ComentarioViewSchema.
    """
    result = []
  
    for comentario in comentarios:
        result.append({
            "id": comentario.id,
            "texto": comentario.texto,
          
        })

    return {"comentarios": result}