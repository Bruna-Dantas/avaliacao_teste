# Mini Sistema de Biblioteca — Testes de Software I (Unidade I)

Instalação: `pip install -r requirements.txt`

Execução (na raiz do projeto):

    python -m pytest -v                       # todos os testes (pytest + unittest)
    python -m pytest -v -s                    # com prints
    python -m unittest tests.test_biblioteca_unittest -v   # só unittest
    python -m pytest --cov=biblioteca --cov-report=term-missing   # cobertura

Mapa questão -> arquivo:
- Q1: biblioteca/
- Q2: tests/test_livro.py e tests/test_biblioteca.py
- Q3: tests/test_biblioteca_unittest.py
- Q4: tests/test_livro.py e tests/test_validadores.py
- Q5: tests/test_biblioteca.py (+ assertRaises em test_biblioteca_unittest.py)
- Q6: fixtures em tests/test_biblioteca.py
- Q7 e Q8: tests/test_biblioteca_mock.py
- Q9, Q10 e Q12: tests/test_integracao.py
- Q11: tests/test_repository.py (+ test_integracao.py)
- Q13: ver relatório (erro proposital em Biblioteca.emprestar)
- Q14: tests/test_database.py criado após a análise de cobertura
