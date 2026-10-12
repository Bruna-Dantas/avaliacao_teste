import sqlite3
from unittest.mock import Mock, patch

import pytest

from biblioteca.biblioteca import Biblioteca
from biblioteca.livro import Livro
from biblioteca.repository import LivroRepository


def test_emprestar_usa_repositorio_simulado():
    # Arrange
    repositorio = Mock()
    livro = Livro("123", "Dom Casmurro", "Machado de Assis", 2)
    repositorio.buscar.return_value = livro
    biblioteca = Biblioteca(repositorio)
    # Act
    biblioteca.emprestar("123")
    # Assert
    assert livro.quantidade == 1
    repositorio.buscar.assert_called_once_with("123")
    repositorio.atualizar.assert_called_once_with(livro)



@patch("biblioteca.repository.LivroRepository.buscar")
def test_disponivel_com_patch(mock_buscar):
    mock_buscar.return_value = Livro("123", "Dom Casmurro", "Machado de Assis", 1)
    biblioteca = Biblioteca(LivroRepository(sqlite3.connect(":memory:")))

    resultado = biblioteca.disponivel("123")

    assert resultado is True
    mock_buscar.assert_called_once_with("123")


def test_repositorio_comportamento_normal_retornos_sucessivos():
    # Situação normal: a 1ª consulta devolve livro com estoque, a 2ª sem estoque
    repositorio = Mock()
    repositorio.buscar.side_effect = [
        Livro("123", "Dom Casmurro", "Machado de Assis", 1),
        Livro("123", "Dom Casmurro", "Machado de Assis", 0),
    ]
    biblioteca = Biblioteca(repositorio)

    assert biblioteca.disponivel("123") is True
    assert biblioteca.disponivel("123") is False
    assert repositorio.buscar.call_count == 2


def test_repositorio_falha_ao_atualizar():
    repositorio = Mock()
    repositorio.buscar.return_value = Livro("123", "Dom Casmurro", "Machado de Assis", 2)
    repositorio.atualizar.side_effect = sqlite3.OperationalError("banco indisponível")
    biblioteca = Biblioteca(repositorio)

    with pytest.raises(sqlite3.OperationalError):
        biblioteca.emprestar("123")
