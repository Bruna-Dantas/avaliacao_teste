"""Regras de validação dos dados de um livro."""


def validar_isbn(isbn):
    if not isbn or not isbn.strip():
        raise ValueError("ISBN inválido: não pode ser vazio")


def validar_titulo(titulo):
    if not titulo or not titulo.strip():
        raise ValueError("Título inválido: não pode ser vazio")


def validar_autor(autor):
    if not autor or not autor.strip():
        raise ValueError("Autor inválido: não pode ser vazio")


def validar_quantidade(quantidade):
    if quantidade < 0:
        raise ValueError("Quantidade inválida: não pode ser negativa")


def validar_livro(isbn, titulo, autor, quantidade):
    validar_isbn(isbn)
    validar_titulo(titulo)
    validar_autor(autor)
    validar_quantidade(quantidade)
