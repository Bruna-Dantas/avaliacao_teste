# Mini Sistema de Biblioteca — Testes de Software I (Unidade I)

**Disciplina:** Testes de Software I · **Curso:** Ciência da Computação
**Aluno(a):** _______________ · **Matrícula:** _______________ · **Data de entrega:** _______________

Sistema de biblioteca em Python (cadastro, consulta, empréstimo e devolução de livros, com persistência em SQLite) acompanhado de uma suíte de testes progressiva: unitários → parametrizados → exceções → fixtures → mock/patch → integração → persistência → investigação de falhas → cobertura.

---

## 1. Instalação e execução

```bash
pip install pytest pytest-cov

python -m pytest -v                                         
python -m pytest -v -s                                     
python -m unittest tests.test_biblioteca_unittest -v         
python -m pytest --cov=biblioteca --cov-report=term-missing
```

## 2. Estrutura do projeto

```
biblioteca/
├── __init__.py
├── livro.py        
├── biblioteca.py     
├── repository.py     
├── validators.py     
└── database.py      
tests/
├── test_livro.py                
├── test_validadores.py         
├── test_biblioteca.py        
├── test_biblioteca_unittest.py  
├── test_biblioteca_mock.py     
├── test_repository.py         
├── test_integracao.py          
└── test_database.py        
```

## 3. Resultado geral da execução

| Verificação | Resultado |
|---|---|
| `python -m pytest -v` | **51 passed** em ~0,1 s, nenhuma falha |
| `python -m unittest tests.test_biblioteca_unittest -v` | **5 tests, OK** |
| Cobertura (`--cov=biblioteca`) | **100 %** (71 statements, 0 perdidos) |
| Cobertura antes de `test_database.py` | **96 %** (`database.py` com 0 %) |
| Mutação proposital (Q13) | **7 testes falharam** e detectaram o defeito |

> Execução realizada com Python 3.12.3, pytest 9.1.1 e pytest-cov 7.1.0.

| Arquivo de teste | Qtd. de testes | Status |
|---|---|---|
| `test_livro.py` | 10 (5 simples + 5 casos parametrizados) | ✅ todos passaram |
| `test_validadores.py` | 13 (parametrizados) | ✅ todos passaram |
| `test_biblioteca.py` | 10 | ✅ todos passaram |
| `test_biblioteca_unittest.py` | 5 | ✅ todos passaram |
| `test_biblioteca_mock.py` | 4 | ✅ todos passaram |
| `test_repository.py` | 4 | ✅ todos passaram |
| `test_integracao.py` | 4 | ✅ todos passaram |
| `test_database.py` | 1 | ✅ passou |

---

## Questão 1 — Construção e organização inicial do sistema

**Objetivo:** criar a primeira versão do sistema com separação clara entre aplicação e testes.

**Responsabilidade de cada módulo:**

| Módulo | Responsabilidade |
|---|---|
| `livro.py` | Classe `Livro` (isbn, titulo, autor, quantidade). Valida os dados ao ser construída, chamando `validar_livro`. |
| `validators.py` | Funções `validar_isbn`, `validar_titulo`, `validar_autor`, `validar_quantidade` e `validar_livro`. Lançam `ValueError` para texto vazio/em branco/`None` e quantidade negativa. |
| `biblioteca.py` | Classe `Biblioteca`, que recebe um repositório (injeção de dependência). Métodos: `cadastrar`, `consultar`, `disponivel`, `emprestar`, `devolver`. |
| `repository.py` | `LivroRepository`: cria a tabela `livros`, e implementa `salvar`, `atualizar` e `buscar` com SQL parametrizado. |
| `database.py` | `conectar(caminho="biblioteca.db")`: abre a conexão SQLite da aplicação. |

**Regras de domínio implementadas:**
- ISBN, título e autor não podem ser vazios; quantidade não pode ser negativa;
- não é possível cadastrar o mesmo ISBN duas vezes (`ValueError`);
- consultar, emprestar ou devolver livro inexistente lança `KeyError`;
- emprestar com quantidade zero lança `ValueError("Sem exemplares disponíveis")`.

**Resultado:** o sistema funciona de ponta a ponta (comprovado pelos testes de integração das Q9–Q12).
**Interpretação:** o design com injeção de dependência (`Biblioteca(repositorio)`) é a decisão que torna possível tanto o isolamento com mocks (Q7/Q8) quanto a integração com SQLite real (Q9–Q12).

---

## Questão 2 — Primeiros testes unitários com pytest

**Objetivo:** testar isoladamente criação de livro, ISBN, título, autor, quantidade, cadastro, consulta, disponibilidade, empréstimo e devolução, usando Arrange–Act–Assert.

**Onde está:** `tests/test_livro.py` (criação e atributos) e `tests/test_biblioteca.py` (operações).

```python
def test_criar_livro():
    # Arrange
    isbn, titulo, autor, quantidade = "123", "Dom Casmurro", "Machado de Assis", 3
    # Act
    livro = Livro(isbn, titulo, autor, quantidade)
    # Assert
    assert isinstance(livro, Livro)

def test_emprestar_reduz_quantidade(biblioteca, livro_disponivel):
    # Arrange
    biblioteca.cadastrar(livro_disponivel)
    # Act
    biblioteca.emprestar("123")
    # Assert
    assert biblioteca.consultar("123").quantidade == 1
```

**Resultado:** ✅ todos passaram (`test_criar_livro`, `test_livro_guarda_isbn/titulo/autor/quantidade`, `test_cadastrar_e_consultar_livro`, `test_livro_disponivel`, `test_livro_indisponivel`, `test_emprestar_reduz_quantidade`, `test_devolver_aumenta_quantidade`).
**Interpretação:** cada teste verifica um único comportamento. O requisito de identificar explicitamente Arrange/Act/Assert em pelo menos dois testes é atendido por `test_criar_livro` e `test_emprestar_reduz_quantidade` (também há comentários em `test_cadastrar_e_consultar_livro`).

---

## Questão 3 — Testes com unittest

**Objetivo:** reescrever pelo menos três funcionalidades já testadas com pytest usando `unittest`.

**Onde está:** `tests/test_biblioteca_unittest.py`, classe `TestBibliotecaUnittest` (cadastro/consulta, disponibilidade positiva e negativa, empréstimo e exceção). Usa `assertEqual`, `assertTrue`, `assertFalse`, `assertIsInstance` e `assertRaises`.

**Resultado:** ✅ `Ran 5 tests ... OK`, tanto via `unittest` quanto via `pytest`.

**Principal diferença observada:** no pytest os testes são funções simples com `assert` puro, e as fixtures são injetadas por parâmetro; no unittest é preciso criar uma classe que herda de `TestCase`, usar métodos `self.assertX(...)` específicos e preparar dados manualmente (`setUp` ou funções auxiliares, como `nova_biblioteca()`). O pytest é mais enxuto e dá mensagens de falha mais ricas; o unittest é mais verboso, porém faz parte da biblioteca padrão.

---

## Questão 4 — Parametrização, classes de equivalência e valores-limite

**Objetivo:** testar regras com vários conjuntos de dados, sendo uma delas obrigatoriamente a quantidade de exemplares.

**Onde está:** `test_livro.py` (quantidade) e `test_validadores.py` (textos).

| Entrada (quantidade) | Classe | Resultado esperado |
|---|---|---|
| -5 | inválida (negativo, longe do limite) | `ValueError` |
| -1 | inválida / **limite** (logo abaixo do mínimo) | `ValueError` |
| 0 | válida / **limite** (mínimo aceito) | Livro criado |
| 1 | válida (primeiro valor comum) | Livro criado |
| 2 | válida (valor comum) | Livro criado |

| Entrada (ISBN/título/autor) | Classe | Resultado esperado |
|---|---|---|
| `""` | inválida (vazio) | `ValueError` |
| `"   "` | inválida (só espaços) | `ValueError` |
| `None` | inválida (ausente) | `ValueError` |
| `"a"` | válida / **limite** (menor texto possível) | aceito |
| `"Dom Casmurro"`, `"978-85-359-0277-5"` | válida | aceito |

```python
@pytest.mark.parametrize("quantidade", [-5, -1])
def test_quantidade_invalida(quantidade): ...

@pytest.mark.parametrize("quantidade", [0, 1, 2])
def test_quantidade_valida(quantidade): ...

@pytest.mark.parametrize("valor", ["", "   ", None])
@pytest.mark.parametrize("validar", [validar_isbn, validar_titulo, validar_autor])
def test_texto_invalido(validar, valor): ...
```

**Resultado:** ✅ 5 casos de quantidade + 9 de texto inválido + 3 de texto válido, todos passaram.
**Interpretação / critério:** um representante por classe de equivalência mais os valores nas fronteiras (-1 | 0). O empilhamento de dois `parametrize` gera o produto cartesiano (3 validadores × 3 valores), cobrindo as três funções com uma única definição de teste.

---

## Questão 5 — Testando exceções

**Objetivo:** garantir que situações inválidas geram a exceção correta.

| Cenário | Exceção | Teste |
|---|---|---|
| Cadastro com dados inválidos | `ValueError` | `test_cadastro_com_dados_invalidos` |
| Cadastro duplicado | `ValueError` ("já cadastrado") | `test_cadastro_duplicado` |
| Empréstimo de livro inexistente | `KeyError` | `test_emprestar_livro_inexistente` |
| Empréstimo com quantidade zero | `ValueError` ("Sem exemplares") | `test_emprestar_sem_exemplares` |
| Devolução de livro inexistente | `KeyError` | `test_devolver_livro_inexistente` |

```python
with pytest.raises(ValueError, match="Sem exemplares"):
    biblioteca.emprestar("456")
```

A variante `assertRaises` está em `test_emprestar_livro_inexistente_gera_excecao` (`test_biblioteca_unittest.py`).

**Resultado:** ✅ todos passaram.
**Por que receber a exceção é sucesso:** a especificação do sistema diz que, nesses cenários, a operação **deve ser recusada**. A exceção é o comportamento correto; se o código aceitasse a operação silenciosamente, aí sim o teste falharia (`DID NOT RAISE`). O uso de `match=` ainda garante que a exceção seja pelo motivo certo.

---

## Questão 6 — Fixtures

**Objetivo:** eliminar repetição de preparação de dados.

```python
@pytest.fixture
def biblioteca():
    conexao = sqlite3.connect(":memory:")
    return Biblioteca(LivroRepository(conexao))

@pytest.fixture
def livro_disponivel():
    return Livro("123", "Dom Casmurro", "Machado de Assis", 2)

@pytest.fixture
def livro_indisponivel():
    return Livro("456", "Vidas Secas", "Graciliano Ramos", 0)
```

| Fixture | Usada em |
|---|---|
| `biblioteca` | 9 testes (todos de `test_biblioteca.py` que operam sobre o sistema) |
| `livro_disponivel` | `test_cadastrar_e_consultar_livro`, `test_livro_disponivel`, `test_emprestar_reduz_quantidade`, `test_devolver_aumenta_quantidade`, `test_cadastro_duplicado` |
| `livro_indisponivel` | `test_livro_indisponivel`, `test_emprestar_sem_exemplares` |

**Resultado:** ✅ todos passaram.
**Repetição eliminada:** sem fixtures, cada teste repetiria a criação da conexão SQLite em memória, do repositório, da `Biblioteca` e do `Livro` com seus quatro argumentos. Cada teste passa a conter apenas o que é específico do cenário, e cada teste recebe um banco novo, o que evita interferência entre testes.

---

## Questão 7 — Isolamento de dependências com Mock/Patch

**Dependência isolada:** o repositório (`LivroRepository`), que é quem acessa o SQLite.

```python
def test_emprestar_usa_repositorio_simulado():
    repositorio = Mock()
    livro = Livro("123", "Dom Casmurro", "Machado de Assis", 2)
    repositorio.buscar.return_value = livro
    biblioteca = Biblioteca(repositorio)

    biblioteca.emprestar("123")

    assert livro.quantidade == 1
    repositorio.buscar.assert_called_once_with("123")
    repositorio.atualizar.assert_called_once_with(livro)

@patch("biblioteca.repository.LivroRepository.buscar")
def test_disponivel_com_patch(mock_buscar): ...
```

**Resultado:** ✅ passaram. Há `return_value` configurado, `assert_called_once_with` e uso de `@patch`.
**Por que continua sendo unitário:** o que se testa é apenas a lógica de `Biblioteca.emprestar` (decrementar e pedir ao repositório para atualizar). Banco de dados, SQL e disco ficam fora do teste, substituídos por um objeto controlado; assim, uma falha só pode ser culpa da `Biblioteca`.

---

## Questão 8 — Comportamentos diferentes da dependência

**Dependência simulada:** `LivroRepository` (via `Mock`).
**Por que simular:** é difícil (e não determinístico) provocar de verdade "banco indisponível" ou respostas diferentes em chamadas sucessivas; com `side_effect` isso é trivial e repetível.

| Cenário | Configuração | Resultado esperado | Teste |
|---|---|---|---|
| Normal | `buscar.side_effect = [Livro(qtd=1), Livro(qtd=0)]` | 1ª consulta `True`, 2ª `False`, `buscar` chamado 2 vezes | `test_repositorio_comportamento_normal_retornos_sucessivos` |
| Falha | `atualizar.side_effect = sqlite3.OperationalError("banco indisponível")` | `emprestar` propaga `OperationalError` | `test_repositorio_falha_ao_atualizar` |

**Resultado:** ✅ ambos passaram.
**Interpretação:** o segundo teste documenta que a `Biblioteca` não esconde falhas de persistência, comportamento difícil de verificar com o banco real.

---

## Questão 9 — Primeiro teste de integração

**Objetivo:** cadastrar → pesquisar → confirmar disponibilidade → emprestar → consultar → confirmar redução, **sem mocks**.

```python
def test_integracao_cadastrar_pesquisar_emprestar(ambiente):
    biblioteca, _ = ambiente
    biblioteca.cadastrar(Livro("123", "Dom Casmurro", "Machado de Assis", 2))
    encontrado = biblioteca.consultar("123")
    assert encontrado.titulo == "Dom Casmurro"
    assert biblioteca.disponivel("123") is True
    biblioteca.emprestar("123")
    assert biblioteca.consultar("123").quantidade == 1
```

**Resultado:** ✅ passou.
**Interpretação:** `Livro`, `validators`, `Biblioteca`, `LivroRepository` e um SQLite real (em memória) trabalham juntos; nenhum `Mock` ou `patch` é utilizado.

---

## Questão 10 — Integração do fluxo completo

**Fluxo:** cadastrar → consultar → emprestar → consultar → devolver → consultar (`test_integracao_fluxo_completo`).

Verificações feitas: quantidade inicial 2 → após empréstimo 1 → após devolução 2, e o estado final é comparado campo a campo com `("123", "Dom Casmurro", "Machado de Assis", 2)`.

**Resultado:** ✅ passou. Também passaram `test_integracao_emprestimo_ate_acabar` (empresta o último exemplar, `disponivel` vira `False` e o próximo empréstimo gera `ValueError`) e `test_integracao_persistencia_apos_emprestimo`.
**Componentes integrados:** `Livro` + `validators` (criação), `Biblioteca` (regras), `LivroRepository` (SQL) e `sqlite3` (armazenamento).

---

## Questão 11 — Integração com persistência (SQLite)

**Objetivo:** comprovar que os dados são **realmente gravados e lidos**, e não apenas que `salvar()` foi chamado.

```python
@pytest.fixture
def repositorio():
    conexao = sqlite3.connect(":memory:")
    yield LivroRepository(conexao)
    conexao.close()

def test_salvar_e_recuperar_livro(repositorio):
    livro = Livro("123", "Dom Casmurro", "Machado de Assis", 2)
    repositorio.salvar(livro)
    recuperado = repositorio.buscar("123")
    assert recuperado.isbn == livro.isbn
    assert recuperado.titulo == livro.titulo
    assert recuperado.autor == livro.autor
    assert recuperado.quantidade == livro.quantidade
```

Outros testes: `test_dados_estao_realmente_no_banco` (faz `SELECT` direto na tabela), `test_atualizar_quantidade_persiste` e `test_buscar_isbn_inexistente_retorna_none`.

**Resultado:** ✅ os 4 passaram.
**Interpretação:** o banco `:memory:` é criado e descartado a cada teste, por isso não interfere no `biblioteca.db` usado pela aplicação (`database.conectar`). O `SELECT` direto garante que o dado está na tabela e não só em um objeto Python.

---

## Questão 12 — Fixture para testes de integração

```python
@pytest.fixture
def ambiente():
    conexao = sqlite3.connect(":memory:")                    # setup
    biblioteca = Biblioteca(LivroRepository(conexao))
    yield biblioteca, conexao                                # execução do teste
    conexao.close()                                          # teardown
```

Usada em 4 testes de `test_integracao.py`.

- **Setup:** cria banco em memória, tabela (feita pelo construtor do repositório) e a `Biblioteca` com repositório real.
- **Execução do teste:** o `yield` entrega `(biblioteca, conexao)` ao teste, que roda sobre um ambiente limpo.
- **Teardown:** o código após o `yield` fecha a conexão, mesmo se o teste falhar, liberando o recurso e descartando o banco.

**Resultado:** ✅ os 4 testes passaram.

---

## Questão 13 — Investigação de falhas

**Erro introduzido** em `Biblioteca.emprestar`: a linha `livro.quantidade -= 1` foi substituída por `pass` (empréstimo que não reduz o estoque).

**Execução:** `python -m pytest -q` → **7 failed, 44 passed**.

| Teste que detectou |
|---|
| `test_biblioteca.py::test_emprestar_reduz_quantidade` |
| `test_biblioteca_mock.py::test_emprestar_usa_repositorio_simulado` |
| `test_biblioteca_unittest.py::...::test_emprestar_reduz_quantidade` |
| `test_integracao.py::test_integracao_cadastrar_pesquisar_emprestar` |
| `test_integracao.py::test_integracao_fluxo_completo` |
| `test_integracao.py::test_integracao_persistencia_apos_emprestimo` |
| `test_integracao.py::test_integracao_emprestimo_ate_acabar` |

**Mensagem do framework (exemplo):**

```
>       assert biblioteca.consultar("123").quantidade == 1
E       AssertionError: assert 2 == 1
E        +  where 2 = <biblioteca.livro.Livro object ...>.quantidade
```

**Interpretação:** o estoque continuou em 2 após o empréstimo, quando deveria ser 1. A falha foi pega por três níveis de teste (unitário com pytest, unitário com unittest/mock e integração), o que mostra que a regra está bem protegida. O teste `test_integracao_emprestimo_ate_acabar` falhou por um motivo indireto: como o estoque nunca zera, `disponivel` continuava `True`.

**Correção:** restaurar `livro.quantidade -= 1`. Após a correção, `51 passed`.

---

## Questão 14 — Cobertura de testes

**Antes** (sem `test_database.py`):

```
Name                       Stmts   Miss  Cover   Missing
biblioteca/biblioteca.py      25      0   100%
biblioteca/database.py         3      3     0%   2-6
biblioteca/livro.py            8      0   100%
biblioteca/repository.py      18      0   100%
biblioteca/validators.py      17      0   100%
TOTAL                         71      3    96%
```

**Análise:** `database.py` (função `conectar`) nunca era exercitado, pois todos os testes criam a conexão diretamente com `sqlite3.connect(":memory:")`.

**Novo teste criado** (`tests/test_database.py`):

```python
def test_conectar_retorna_conexao_sqlite():
    conexao = conectar(":memory:")
    try:
        assert isinstance(conexao, sqlite3.Connection)
        assert conexao.execute("SELECT 1").fetchone() == (1,)
    finally:
        conexao.close()
```

**Depois:**

```
TOTAL    71 statements    0 miss    100%      (51 passed)
```

**Por que cobertura alta, isoladamente, não garante qualidade:** a cobertura mede apenas quais linhas foram **executadas**, não se o resultado foi **verificado**. Um teste sem `assert` (ou com assert fraco) pode atingir 100 %. Também não mede se os casos relevantes (valores-limite, combinações de entrada) foram testados. A Q13 mostra o contrário: o que provou a qualidade da suíte foi ela falhar quando um defeito foi inserido.

---

## Questão final — Teste unitário × teste de integração

| | Teste unitário | Teste de integração |
|---|---|---|
| **Exemplo** | `test_emprestar_usa_repositorio_simulado` (`test_biblioteca_mock.py`) | `test_integracao_fluxo_completo` (`test_integracao.py`) |
| **Componente testado** | `Biblioteca.emprestar`, isolada | O fluxo cadastrar → emprestar → devolver |
| **Dependências** | `LivroRepository` substituído por `Mock` (`return_value`, `assert_called_once_with`) | Nenhuma substituída |
| **Componentes reais** | Apenas `Biblioteca` e `Livro` | `Livro`, `validators`, `Biblioteca`, `LivroRepository` e SQLite (`:memory:`) |
| **Defeitos que pode achar** | Erro de lógica interna: não decrementar estoque, permitir empréstimo com estoque 0, exceção errada | Erros na **comunicação** entre componentes: SQL incorreto, dado não persistido, `atualizar` com `WHERE` errado, objeto reconstruído com campos trocados em `buscar` |

Um teste unitário diz *onde* está o problema (rápido, determinístico, localizado). Um teste de integração diz *se as peças funcionam juntas* (mais lento e menos preciso para localizar a causa). Um bug de SQL no `repository.py` passaria despercebido nos testes com mock, mas seria pego nos de integração; já um bug de regra em `emprestar` é apontado de forma mais direta pelo teste unitário.
