"""Regras de negócio da biblioteca."""


class Biblioteca:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def cadastrar(self, livro):
        if self.repositorio.buscar(livro.isbn) is not None:
            raise ValueError("Livro já cadastrado")
        self.repositorio.salvar(livro)

    def consultar(self, isbn):
        livro = self.repositorio.buscar(isbn)
        if livro is None:
            raise KeyError(f"Livro não encontrado: {isbn}")
        return livro

    def disponivel(self, isbn):
        livro = self.consultar(isbn)
        return livro.quantidade > 0

    def emprestar(self, isbn):
        livro = self.consultar(isbn)
        if livro.quantidade == 0:
            raise ValueError("Sem exemplares disponíveis")
        livro.quantidade -= 1
        self.repositorio.atualizar(livro)

    def devolver(self, isbn):
        livro = self.consultar(isbn)
        livro.quantidade += 1
        self.repositorio.atualizar(livro)
