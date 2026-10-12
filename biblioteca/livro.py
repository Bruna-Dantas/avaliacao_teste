"""Entidade Livro."""
from biblioteca.validators import validar_livro


class Livro:
    def __init__(self, isbn, titulo, autor, quantidade):
        validar_livro(isbn, titulo, autor, quantidade)
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.quantidade = quantidade
