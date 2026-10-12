import sqlite3

import pytest

from biblioteca.livro import Livro
from biblioteca.repository import LivroRepository


@pytest.fixture
def repositorio():
    conexao = sqlite3.connect(":memory:")  
    yield LivroRepository(conexao)
    conexao.close()



def test_salvar_e_recuperar_livro(repositorio):
    # Arrange
    livro = Livro("123", "Dom Casmurro", "Machado de Assis", 2)
    # Act
    repositorio.salvar(livro)
    recuperado = repositorio.buscar("123")    
    # Assert: 
    assert recuperado.isbn == livro.isbn
    assert recuperado.titulo == livro.titulo
    assert recuperado.autor == livro.autor
    assert recuperado.quantidade == livro.quantidade


def test_dados_estao_realmente_no_banco(repositorio):
    repositorio.salvar(Livro("123", "Dom Casmurro", "Machado de Assis", 2))

    linha = repositorio.conexao.execute(
        "SELECT titulo, quantidade FROM livros WHERE isbn = '123'"
    ).fetchone()

    assert linha == ("Dom Casmurro", 2)


def test_atualizar_quantidade_persiste(repositorio):
    livro = Livro("123", "Dom Casmurro", "Machado de Assis", 2)
    repositorio.salvar(livro)
    livro.quantidade = 5

    repositorio.atualizar(livro)

    assert repositorio.buscar("123").quantidade == 5


def test_buscar_isbn_inexistente_retorna_none(repositorio):
    assert repositorio.buscar("999") is None
