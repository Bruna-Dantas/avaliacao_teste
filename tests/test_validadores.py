import pytest

from biblioteca.validators import (
    validar_autor,
    validar_isbn,
    validar_livro,
    validar_titulo,
)


@pytest.mark.parametrize("valor", ["", "   ", None])
@pytest.mark.parametrize("validar", [validar_isbn, validar_titulo, validar_autor])
def test_texto_invalido(validar, valor):
    with pytest.raises(ValueError):
        validar(valor)


@pytest.mark.parametrize("valor", ["a", "Dom Casmurro", "978-85-359-0277-5"])
def test_texto_valido(valor):
    assert validar_titulo(valor) is None


def test_validar_livro_com_dados_corretos():
    assert validar_livro("123", "Dom Casmurro", "Machado de Assis", 1) is None
