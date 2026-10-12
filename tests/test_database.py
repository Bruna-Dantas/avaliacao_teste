import sqlite3

from biblioteca.database import conectar


def test_conectar_retorna_conexao_sqlite():
    conexao = conectar(":memory:")      
    try:
        assert isinstance(conexao, sqlite3.Connection)
        assert conexao.execute("SELECT 1").fetchone() == (1,)
    finally:
        conexao.close()
