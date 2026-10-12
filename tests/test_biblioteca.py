import sqlite3

import pytest

from biblioteca.biblioteca import Biblioteca
from biblioteca.livro import Livro
from biblioteca.repository import LivroRepository


# ---------- Q6: fixtures ----------
@pytest.fixture
def biblioteca():
    conexao = sqlite3.connect(":memory:")
    return Biblioteca(LivroRepository(conexao))


@pytest.fixture
def livro_disponivel():
    return Livro("123", "Dom Casmurro", "Machado de Assis", 2)


@pytest.fixture
def livro_indisponivel():
    return Livro("456", "Vidas Secas", "Graciliano Ramos", 0)


def test_cadastrar_e_consultar_livro(biblioteca, livro_disponivel):
    # Arrange
    # Act
    biblioteca.cadastrar(livro_disponivel)
    resultado = biblioteca.consultar("123")
    # Assert
    assert resultado.titulo == "Dom Casmurro"
    assert resultado.quantidade == 2


def test_livro_disponivel(biblioteca, livro_disponivel):
    biblioteca.cadastrar(livro_disponivel)
    assert biblioteca.disponivel("123") is True


def test_livro_indisponivel(biblioteca, livro_indisponivel):
    biblioteca.cadastrar(livro_indisponivel)
    assert biblioteca.disponivel("456") is False


def test_emprestar_reduz_quantidade(biblioteca, livro_disponivel):
    # Arrange
    biblioteca.cadastrar(livro_disponivel)
    # Act
    biblioteca.emprestar("123")
    # Assert
    assert biblioteca.consultar("123").quantidade == 1


def test_devolver_aumenta_quantidade(biblioteca, livro_disponivel):
    biblioteca.cadastrar(livro_disponivel)
    biblioteca.devolver("123")
    assert biblioteca.consultar("123").quantidade == 3


def test_cadastro_com_dados_invalidos():
    with pytest.raises(ValueError):
        Livro("", "Dom Casmurro", "Machado de Assis", 1)


def test_cadastro_duplicado(biblioteca, livro_disponivel):
    biblioteca.cadastrar(livro_disponivel)
    with pytest.raises(ValueError, match="já cadastrado"):
        biblioteca.cadastrar(livro_disponivel)


def test_emprestar_livro_inexistente(biblioteca):
    with pytest.raises(KeyError):
        biblioteca.emprestar("999")


def test_emprestar_sem_exemplares(biblioteca, livro_indisponivel):
    biblioteca.cadastrar(livro_indisponivel)
    with pytest.raises(ValueError, match="Sem exemplares"):
        biblioteca.emprestar("456")


def test_devolver_livro_inexistente(biblioteca):
    with pytest.raises(KeyError):
        biblioteca.devolver("999")
