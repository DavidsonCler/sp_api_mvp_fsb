from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect

from sqlalchemy.exc import IntegrityError

from model import Session, Produto, Pedido, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS


info = Info(
    title="API - Space Pedidos - Davidson (Lista de Compras.old)", version="2.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
swagger_tag = Tag(name="Documentação",
                  description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(
    name="Produto", description="Adição, visualização e remoção de produtos de um pedido")
pedido_tag = Tag(
    name="Pedido", description="Adição, visualização e remoção de pedidos à base")
comentario_tag = Tag(
    name="Comentario", description="Adição de um comentário à um pedido cadastrado na base")
produtos_tag = Tag(name="Produtos de um pedido",
                   description="Adição de um produto à um pedido cadastrado na base")


@app.get('/', tags=[swagger_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi/swagger')

   # --------------------------------------------#
   #                                             #
   # Método add Pedido                           #
   #                                             #
   # --------------------------------------------#
@app.post('/pedido', tags=[pedido_tag],
          responses={"200": PedidoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_pedido(form: PedidoSchema):
    """Adiciona um novo Pedido à base de dados

    Retorna uma representação dos pedidos com produtos e comentários associados.
    """
    pedido = Pedido(
        nome_cliente=form.nome_cliente,
        endereco_cliente=form.endereco_cliente,
        cpf_cliente=form.cpf_cliente,
        telefone_cliente=form.telefone_cliente)
    logger.debug(f"Adicionando pedido do Cliente: '{pedido.nome_cliente}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(pedido)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado pedido do Cliente: '{pedido.nome_cliente}'")
        return apresenta_pedido(pedido), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Pedido com a mesma NF já salvo na base :/", pedido.nome_cliente
        logger.warning(
            f"Erro ao adicionar o pedido do Cliente: '{pedido.nome_cliente}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/", pedido.nome_cliente
        logger.warning(
            f"Erro ao adicionar o pedido do Cliente: '{pedido.nome_cliente}', {error_msg}")
        return {"mesage": error_msg}, 400

   # --------------------------------------------#
   #                                            #
   # Método add Produto                         #
   #                                            #
   # --------------------------------------------#
@app.post('/produto', tags=[produto_tag],
          responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(form:ProdutoSchema):
    """Adiciona de um novo produto à um pedido cadastrado na base identificado pela nf

    Retorna uma representação do pedido e e produtos associados.
    """
    # criando o produto
    pedido_nf = form.pedido_nf
    nome = form.nome
    quantidade = form.quantidade
    valor = form.valor
    valor_total = (quantidade * valor)

    # definindo variáveis
    logger.debug(f"Adicionando produtos ao pedido #{pedido_nf}")
    # criando conexão com a base

    session = Session()
    # fazendo a busca pelo pedido
    pedido: Pedido = session.query(Pedido).filter(Pedido.nf == pedido_nf).first()

    if not pedido:
        # se pedido não encontrado
        error_msg = "Pedido não foi encontrado :/"
        logger.warning(f"Erro ao adicionar produto ao pedido '{pedido_nf}', {error_msg}")
        raise (Exception (IntegrityError), error_msg)
     
    # definindo o objeto de Produto
    produto = Produto(nome, quantidade, valor, valor_total)
    
    
    
    pedido.adiciona_produto(produto)
    session.commit()
    # Criando logs
    logger.debug(f"Adicionando produto ao pedido:  #{pedido_nf}")
    logger.debug(f"Adicionando produto: '{produto.nome}' no pedido")
    return apresenta_pedido(pedido)
    
     
        
   #--------------------------------------------#
   #                                            #
   # Método listar Produtos                     #                 
   #                                            #
   #--------------------------------------------#
@app.get('/produtos', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_produtos():
    """Faz a busca por todos os Produtos cadastrados

    Retorna uma representação da listagem de produtos.
    """
    logger.debug(f"Coletando produtos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produtos = session.query(Produto).all()

    if not produtos:
        # se não há produtos cadastrados
        return {"produtos": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(produtos))
        # retorna a representação de produto
        print(produtos)
        return apresenta_produtos(produtos), 200
    
    
    
   #--------------------------------------------#
   #                                            #
   # Método /p listar Pedidos                   #                 
   #                                            #
   #--------------------------------------------#
@app.get('/pedidos', tags=[pedido_tag],
         responses={"200": ListagemPedidosSchema, "404": ErrorSchema})
def get_pedidos():
    """Faz a busca por todos os pedidos cadastrados

    Retorna uma representação da listagem de pedidos.
    """
    logger.debug(f"Coletando produtos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pedidos = session.query(Pedido).all()

    if not pedidos:
        # se não há pedidos cadastrados
        return {"pedidos": []}, 200
    else:
        logger.debug(f"%d pedidos encontrados" % len(pedidos))
        # retorna a representação de pedidos
        print(pedidos)
        return apresenta_pedidos(pedidos), 200
    
    
    
   #--------------------------------------------#
   #                                            #
   # Método p/ listar pedido requisitado        #                 
   #                                            #
   #--------------------------------------------#    
@app.get('/pedido', tags=[pedido_tag],
         responses={"200": PedidoViewSchema, "404": ErrorSchema})
def get_pedido(query: PedidoBuscaSchema):
    """Faz a busca por um Pedido a partir da NF do pedido

    Retorna uma representação do pedido e comentários associados.
    """
    nf = query.nf
    logger.debug(f"Coletando dados sobre pedido #{nf}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pedido = session.query(Pedido).filter(Pedido.nf == nf).first()

    if not pedido:
        # se o pedido não foi encontrado
        error_msg = "Pedido não encontrado na base :/"
        logger.warning(f"Erro ao buscar pedido... '{nf}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Pedido do cliente: '{pedido.nome_cliente}' encontrado! \nNF: '{nf}'")
        # retorna a representação de pedido
        return apresenta_pedido(pedido), 200
    
    
   #--------------------------------------------#
   #                                            #
   # Método p/ listar produtos de um            #
   # determinado pedido                         #
   #                                            #
   #--------------------------------------------#
@app.get('/produtos_pedido', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_produtos_pedido(query: ProdutoBuscaSchema):
    """Faz a busca por todos os Produtos de um pedido cadastrado

    Retorna uma representação da listagem de produtos por pedido.
    """
    
    pedido_nf=query.pedido_nf
    logger.debug(f"Coletando produtos do pedido NF: ", {pedido_nf})
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    
    produtos = session.query(Pedido.produtos).all
    produtos_pedido: Produto[produtos] = session.query(Produto).where(Produto.pedido_nf == pedido_nf)
    
    

    if not produtos:
        # se não há produtos cadastrados
        return {"produtos": []}, 200
    else:
        logger.debug(f"%d produtos encontrados", (produtos))
        # retorna a representação de produto
        print(produtos)
        return apresenta_produtos(produtos_pedido), 200
    

   #--------------------------------------------#
   #                                            #
   # Método p/ listar o produto requisitado     #                 
   #                                            #
   #--------------------------------------------#
@app.get('/produto', tags=[produto_tag],
         responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def get_produto(query: ProdutoBuscaSchema):
    """Faz a busca por um Produto a partir do id do produto

    Retorna uma representação dos produtos e comentários associados.
    """
    produto_id = query.id
    logger.debug(f"Coletando dados sobre produto #{produto_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produto = session.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao buscar produto '{produto_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Produto econtrado: '{produto.nome}'")
        # retorna a representação de produto
        return apresenta_produto(produto), 200
    
    
   #--------------------------------------------#
   #                                            #
   # Método p/ deletar o produto requisitado    #                 
   #                                            #
   #--------------------------------------------#
@app.delete('/produto', tags=[produto_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produto(query: ProdutoBuscaSchema):
    """Deleta um Produto a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    # capturando id na variavel passada pela query
    id = query.id
    try:
    # criando conexão com a base
        session = Session()
    
    # criando variável para manuseio do objeto produto
        produto =  session.query(Produto).filter(Produto.id == id).first()
        if not produto:
            raise Exception
        else:
            # retorna a representação da mensagem de confirmação
            logger.debug(f"Deletado produto #{id}")
            
            # criando variável para manuseio do objeto pedido
            pedido = session.query(Pedido).where(produto.pedido_nf == Pedido.nf).first()
    
            # subtraindo o valor do produto no pedido
            pedido.valor_pedido(produto, 1)
   
            # fazendo a remoção
            logger.debug(f"Deletando dados sobre produto #{id}")
            session.query(Produto).filter(Produto.id == id).delete()
            session.commit()
            return {"mesage": "Produto removido", "id": id, "nome":produto.nome}
       
    except Exception as e:
        # se o produto não foi encontrado
            error_msg = "Produto não encontrado na base :/"
            logger.warning(f"Erro ao deletar produto #'{id}', {error_msg}, traceback: {e.with_traceback}")
            {"Problema": error_msg}
            return "Erro ao deletar produto -> id: " + str(id) + "\n"+error_msg, 404
        
                     
   #--------------------------------------------#
   #                                            #
   # Método p/ deletar o pedido requisitado     #                 
   #                                            #
   #--------------------------------------------#
@app.delete('/pedido', tags=[pedido_tag],
            responses={"200": PedidoDelSchema, "404": ErrorSchema})
def del_pedido(query: PedidoBuscaSchema):
    """Deleta um Pedido a partir da NF informada

    Retorna uma mensagem de confirmação da remoção.
    """
    # criando variavel para a query
    nf = query.nf
    # criando conexão com a base
    session = Session()
    print (nf)
    logger.debug(f"Deletando dados sobre pedido e suas depenências... #{nf}")
   
    # fazendo a remoção do pedido e dependências -- 
    # Não consegui implementar o Cascade, deram muitos erros
    count = session.query(Pedido).filter(Pedido.nf == nf).delete()
    session.query(Produto).filter(Produto.pedido_nf == nf).delete()
    session.query(Comentario).filter(Comentario.pedido_nf == nf).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f" Pedido deletado  #{nf}")
        return {"mesage": "Pedido removido", "NF":nf}
    else:
        # se o pedido não foi encontrado
        error_msg = "Pedido não foi encontrado na base :/"
        logger.warning(f"Erro ao deletar pedido #NF:'{nf}', {error_msg}")
        return {"mesage": error_msg}, 404  
    
    
   #--------------------------------------------#
   #                                            #
   # Método p/ add um comentário no pedido      #                 
   #                                            #
   #--------------------------------------------#
@app.post('/comentario', tags=[comentario_tag],
          responses={"200": PedidoViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona de um novo comentário à um pedido cadastrado na base identificado pela NF

    Retorna uma representação dos pedidos e comentários associados.
    """
    # capturando dado do form
    pedido_nf = form.pedido_nf
    logger.debug(f"Adicionando comentários ao pedido #{pedido_nf}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo pedido
    pedido = session.query(Pedido).filter(Pedido.nf == pedido_nf).first()

    if not pedido:
        # se pedido não encontrado
        error_msg = "Pedido não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao pedido '{pedido_nf}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário ao pedido
    pedido.adiciona_comentario(comentario)
    session.commit()
    logger.debug(f"Adicionado comentário ao pedido #{pedido_nf}")

    # retorna a representação de pedido
    return apresenta_pedido(pedido), 200


   
   #--------------------------------------------#
   #                                            #
   # Método p/ listar comentarios de um            #
   # determinado pedido                         #
   #                                            #
   #--------------------------------------------#
@app.get('/comentarios_pedido', tags=[comentario_tag],
         responses={"200": ListagemComentariosSchema, "404": ErrorSchema})
def get_comentarios_pedido(query: ComentarioBuscaSchema):
    """Faz a busca por todos os Comentarios de um pedido cadastrado

    Retorna uma representação da listagem de comentarios por pedido.
    """
    
    pedido_nf=query.pedido_nf
    logger.debug(f"Coletando comentarios do pedido NF: ", {pedido_nf})
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    
    comentarios = session.query(Pedido.comentarios).all
    comentarios_pedido: Comentario[comentarios] = session.query(Comentario).where(Comentario.pedido_nf == pedido_nf)
    
    

    if not comentarios:
        # se não há comentarios cadastrados
        return {"comentarios": []}, 200
    else:
        logger.debug(f"%d comentarios encontrados", (comentarios))
        # retorna a representação de comentario
        print(comentarios)
        return apresenta_comentarios(comentarios_pedido), 200



   #--------------------------------------------#
   #                                            #
   # Método p/ deletar o comentário requisitado #                 
   #                                            #
   #--------------------------------------------#
@app.delete('/comentario', tags=[comentario_tag],
            responses={"200": ComentarioDelSchema, "404": ErrorSchema})
def del_comentario(query: ComentarioBuscaSchema):
    """Deleta um Comentário a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    # capturando id na variavel passada pela query
    id = query.id
    try:
    # criando conexão com a base
        session = Session()
    
    # criando variável para manuseio do objeto comentario
        comentario =  session.query(Comentario).filter(Comentario.id == id).first()
        if not comentario:
            raise Exception
        else:
            # retorna a representação da mensagem de confirmação
            logger.debug(f"Deletado comentario #{id}")
            
            # criando variável para manuseio do objeto pedido
            
    
            # subtraindo o valor do comentario no pedido
   
            # fazendo a remoção
            logger.debug(f"Deletando dados sobre comentario #{id}")
            session.query(Comentario).filter(Comentario.id == id).delete()
            session.commit()
            return {"mesage": "Comentario removido", "id": id, "nome":comentario.texto}
       
    except Exception as e:
        # se o comentario não foi encontrado
            error_msg = "Comentario não encontrado na base :/"
            logger.warning(f"Erro ao deletar comentario #'{id}', {error_msg}, traceback: {e.with_traceback}")
            {"Problema": error_msg}
            return "Erro ao deletar comentario -> id: " + str(id) + "\n"+error_msg, 404

#######################################################################################################################################################
#######################################################################################################################################################
