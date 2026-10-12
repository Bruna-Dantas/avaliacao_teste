"""Persistência dos livros em SQLite."""
from biblioteca.livro import Livro


class LivroRepository:
    def __init__(self, conexao):
        self.conexao = conexao
        self.conexao.execute(
            "CREATE TABLE IF NOT EXISTS livros ("
            "isbn TEXT PRIMARY KEY, "
            "titulo TEXT NOT NULL, "
            "autor TEXT NOT NULL, "
            "quantidade INTEGER NOT NULL)"
        )
        self.conexao.commit()

    def salvar(self, livro):
        self.conexao.execute(
            "INSERT INTO livros (isbn, titulo, autor, quantidade) VALUES (?, ?, ?, ?)",
            (livro.isbn, livro.titulo, livro.autor, livro.quantidade),
        )
        self.conexao.commit()

    def atualizar(self, livro):
        self.conexao.execute(
            "UPDATE livros SET quantidade = ? WHERE isbn = ?",
            (livro.quantidade, livro.isbn),
        )
        self.conexao.commit()

    def buscar(self, isbn):
        cursor = self.conexao.execute(
            "SELECT isbn, titulo, autor, quantidade FROM livros WHERE isbn = ?",
            (isbn,),
        )
        linha = cursor.fetchone()
        if linha is None:
            return None
        return Livro(linha[0], linha[1], linha[2], linha[3])
