from pydantic import BaseModel
from typing import Optional, List
from model.filme import Filme


class FilmeSchema(BaseModel):
    """ Define como um novo filme a ser inserido deve ser representado
    """
    nome: str = "De volta para o futuro!"
    categoria: Optional[str] = "Aventura"
    ano: int = 2000


class FilmeBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do filme.
    """
    nome: str = "Rambo"



class ListagemFilmesSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    filmes:List[FilmeSchema]


def apresenta_filmes(filmes: List[Filme]):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    for filme in filmes:
        result.append({
            "nome": filme.nome,
            "categoria": filme.categoria,
            "ano": filme.ano,
        })

    return {"filmes": result}


class FilmeViewSchema(BaseModel):
    """ Define como um filme será retornado: filme + comentários.
    """
    id: int = 1
    nome: str = "Rambo"
    categoria: Optional[str] = "Drama"
    ano: int = "2000"


class FilmeDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mensagem: str
    nome: str

def apresenta_filme(filme: Filme):
    """ Retorna uma representação do filme seguindo o schema definido em
       FilmeViewSchema.
    """
    return {
        "id": filme.id,
        "nome": filme.nome,
        "categoria": filme.categoria,
        "ano": filme.ano
    }
