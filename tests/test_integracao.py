import sqlite3

import pytest

from biblioteca.biblioteca import Biblioteca
from biblioteca.livro import Livro
from biblioteca.repository import LivroRepository


@pytest.fixture
def ambiente():
    conexao = sqlite3.connect(":memory:")
    biblioteca = Biblioteca(LivroRepository(conexao))
    yield biblioteca, conexao      
    conexao.close()


def test_integracao_cadastrar_pesquisar_emprestar(ambiente):
    biblioteca, _ = ambiente

    biblioteca.cadastrar(Livro("123", "Dom Casmurro", "Machado de Assis", 2))
    encontrado = biblioteca.consultar("123")
    assert encontrado.titulo == "Dom Casmurro"
    assert biblioteca.disponivel("123") is True

    biblioteca.emprestar("123")

    assert biblioteca.consultar("123").quantidade == 1


def test_integracao_fluxo_completo(ambiente):
    biblioteca, _ = ambiente

    biblioteca.cadastrar(Livro("123", "Dom Casmurro", "Machado de Assis", 2))
    assert biblioteca.consultar("123").quantidade == 2

    biblioteca.emprestar("123")
    assert biblioteca.consultar("123").quantidade == 1

    biblioteca.devolver("123")
    assert biblioteca.consultar("123").quantidade == 2

    final = biblioteca.consultar("123")
    assert (final.isbn, final.titulo, final.autor, final.quantidade) == (
        "123", "Dom Casmurro", "Machado de Assis", 2,
    )


def test_integracao_persistencia_apos_emprestimo(ambiente):
    biblioteca, conexao = ambiente
    biblioteca.cadastrar(Livro("123", "Dom Casmurro", "Machado de Assis", 2))

    biblioteca.emprestar("123")

    outro_repositorio = LivroRepository(conexao)
    assert outro_repositorio.buscar("123").quantidade == 1


def test_integracao_emprestimo_ate_acabar(ambiente):
    biblioteca, _ = ambiente
    biblioteca.cadastrar(Livro("123", "Dom Casmurro", "Machado de Assis", 1))

    biblioteca.emprestar("123")

    assert biblioteca.disponivel("123") is False
    with pytest.raises(ValueError, match="Sem exemplares"):
        biblioteca.emprestar("123")
