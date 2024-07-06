from sqlalchemy import Column, String, Integer
from model.base import Base


class Filme(Base):
    __tablename__ = 'filme'

    id = Column("pk_filme", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    categoria = Column(String(140))
    ano = Column(Integer)

    # Definição do relacionamento entre o filme e o comentário.
    # Essa relação é implicita, não está salva na tabela 'filme',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.

    def __init__(self, nome:str, categoria:str, ano:int):
        """
        Cria um Filme

        Arguments:
            nome: nome do filme.
            quantidade: quantidade que se espera comprar daquele filme
            valor: valor esperado para o filme
            data_insercao: data de quando o filme foi inserido à base
        """
        self.nome = nome
        self.categoria = categoria
        self.ano = ano

    def __str___(self):
        return f"Nome: {self.nome}, Categoria: {self.categoria}, Ano: {self.ano}"

