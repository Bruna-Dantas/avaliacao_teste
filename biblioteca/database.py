"""Conexão com o banco SQLite da aplicação."""
import sqlite3


def conectar(caminho="biblioteca.db"):
    return sqlite3.connect(caminho)
