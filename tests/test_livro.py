import pytest

from biblioteca.livro import Livro


def test_criar_livro():
    # Arrange
    isbn, titulo, autor, quantidade = "123", "Dom Casmurro", "Machado de Assis", 3
    # Act
    livro = Livro(isbn, titulo, autor, quantidade)
    # Assert
    assert isinstance(livro, Livro)


def test_livro_guarda_isbn():
    livro = Livro("123", "Dom Casmurro", "Machado de Assis", 3)
    assert livro.isbn == "123"


def test_livro_guarda_titulo():
    livro = Livro("123", "Dom Casmurro", "Machado de Assis", 3)
    assert livro.titulo == "Dom Casmurro"


def test_livro_guarda_autor():
    livro = Livro("123", "Dom Casmurro", "Machado de Assis", 3)
    assert livro.autor == "Machado de Assis"


def test_livro_guarda_quantidade():
    livro = Livro("123", "Dom Casmurro", "Machado de Assis", 3)
    assert livro.quantidade == 3


@pytest.mark.parametrize("quantidade", [-5, -1])
def test_quantidade_invalida(quantidade):
    with pytest.raises(ValueError):
        Livro("123", "Dom Casmurro", "Machado de Assis", quantidade)


# Classe válida: 0 é o valor-limite mínimo; 1 e 2 são valores comuns
@pytest.mark.parametrize("quantidade", [0, 1, 2])
def test_quantidade_valida(quantidade):
    livro = Livro("123", "Dom Casmurro", "Machado de Assis", quantidade)
    assert livro.quantidade == quantidade
