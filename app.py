from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Filme
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
filme_tag = Tag(name="Filme", description="Adição, visualização e remoção de produtos à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um produtos cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/filme', tags=[filme_tag],
          responses={"200": FilmeViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_filme(form: FilmeSchema):
    """Adiciona um novo Filme à base de dados

    Retorna uma representação dos filmes e comentários associados.
    """
    filme = Filme(
        nome=form.nome,
        categoria=form.categoria,
        ano=form.ano)
    logger.debug(f"Adicionando produto de nome: '{filme.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(filme)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado filme de nome: '{filme.nome}'")
        return apresenta_filme(filme), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Filme de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar filme '{filme.nome}', {error_msg}")
        return {"mensagem": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar filme '{filme.nome}', {error_msg}")
        return {"mensagem": error_msg}, 400


@app.get('/filmes', tags=[filme_tag],
         responses={"200": ListagemFilmesSchema, "404": ErrorSchema})
def get_filmes():
    """Faz a busca por todos os Filme cadastrados

    Retorna uma representação da listagem de filmes.
    """
    logger.debug(f"Coletando filmes")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    filmes = session.query(Filme).all()

    if not filmes:
        # se não há filmes cadastrados
        return {"filmes": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(filmes))
        # retorna a representação de produto
        print(filmes)
        return apresenta_filmes(filmes), 200


@app.get('/filme', tags=[filme_tag],
         responses={"200": FilmeViewSchema, "404": ErrorSchema})
def get_filme(query: FilmeBuscaSchema):
    """Faz a busca por um Filmes a partir do id do produto

    Retorna uma representação dos filmes e comentários associados.
    """
    filme_nome = query.nome
    logger.debug(f"Coletando dados sobre filme #{filme_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    filme = session.query(Filme).filter(Filme.nome == filme_nome).first()

    if not filme:
        # se o filme não foi encontrado
        error_msg = "Filme não encontrado na base :/"
        logger.warning(f"Erro ao buscar filme '{filme_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Filme econtrado: '{filme.nome}'")
        # retorna a representação de filme
        return apresenta_filme(filme), 200


@app.delete('/filme', tags=[filme_tag],
            responses={"200": FilmeDelSchema, "404": ErrorSchema})
def del_filme(query: FilmeBuscaSchema):
    """Deleta um Filme a partir do nome de filme informado

    Retorna uma mensagem de confirmação da remoção.
    """
    filme_nome = unquote(unquote(query.nome))
    print(filme_nome)
    logger.debug(f"Deletando dados sobre filme #{filme_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Filme).filter(Filme.nome == filme_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado produto #{filme_nome}")
        return {"mensagem": "Produto removido", "id": filme_nome}
    else:
        # se o filme não foi encontrado
        error_msg = "Filme não encontrado na base :/"
        logger.warning(f"Erro ao deletar filme #'{filme_nome}', {error_msg}")
        return {"mensagem": error_msg}, 404


