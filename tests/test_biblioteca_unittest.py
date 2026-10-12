import sqlite3
import unittest

from biblioteca.biblioteca import Biblioteca
from biblioteca.livro import Livro
from biblioteca.repository import LivroRepository


def nova_biblioteca():
    return Biblioteca(LivroRepository(sqlite3.connect(":memory:")))


class TestBibliotecaUnittest(unittest.TestCase):

    def test_cadastrar_e_consultar_livro(self):
        biblioteca = nova_biblioteca()
        biblioteca.cadastrar(Livro("123", "Dom Casmurro", "Machado de Assis", 2))

        resultado = biblioteca.consultar("123")

        self.assertIsInstance(resultado, Livro)
        self.assertEqual(resultado.titulo, "Dom Casmurro")
        self.assertEqual(resultado.quantidade, 2)

    def test_livro_com_exemplares_esta_disponivel(self):
        biblioteca = nova_biblioteca()
        biblioteca.cadastrar(Livro("123", "Dom Casmurro", "Machado de Assis", 1))

        self.assertTrue(biblioteca.disponivel("123"))

    def test_livro_sem_exemplares_nao_esta_disponivel(self):
        biblioteca = nova_biblioteca()
        biblioteca.cadastrar(Livro("456", "Vidas Secas", "Graciliano Ramos", 0))

        self.assertFalse(biblioteca.disponivel("456"))

    def test_emprestar_reduz_quantidade(self):
        biblioteca = nova_biblioteca()
        biblioteca.cadastrar(Livro("123", "Dom Casmurro", "Machado de Assis", 2))

        biblioteca.emprestar("123")

        self.assertEqual(biblioteca.consultar("123").quantidade, 1)

    def test_emprestar_livro_inexistente_gera_excecao(self):
        biblioteca = nova_biblioteca()

        with self.assertRaises(KeyError):
            biblioteca.emprestar("999")


if __name__ == "__main__":
    unittest.main()
