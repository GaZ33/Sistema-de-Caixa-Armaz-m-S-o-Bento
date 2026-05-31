# Sistema-de-Caixa-Armaz-m-S-o-Bento

## DER com ERAlchemy2

Voce pode gerar o DER automaticamente a partir da conexao do banco definida no .env.

1. Instale dependencias Python

	c:/Users/gasin/Desktop/GitHub/Sistema-de-Caixa-Armaz-m-S-o-Bento/.venv/Scripts/python.exe -m pip install ERAlchemy2 pymysql python-dotenv

2. (Opcional para PNG/SVG/PDF) Instale Graphviz no Windows

	winget install Graphviz.Graphviz

3. Se a instalacao do ERAlchemy2 falhar por pygraphviz no Windows, rode:

	c:/Users/gasin/Desktop/GitHub/Sistema-de-Caixa-Armaz-m-S-o-Bento/.venv/Scripts/python.exe -m pip install --force-reinstall --no-cache-dir pygraphviz --config-settings=--global-option=build_ext --config-settings=--global-option="-IC:\Program Files\Graphviz\include" --config-settings=--global-option="-LC:\Program Files\Graphviz\lib"

4. Gere o DER usando DB_CONNECTION

	c:/Users/gasin/Desktop/GitHub/Sistema-de-Caixa-Armaz-m-S-o-Bento/.venv/Scripts/python.exe tools/generate_erd.py --env-key DB_CONNECTION --output docs/der_armazem.png

5. Gere o DER usando DB_CONNECTION_TEST

	c:/Users/gasin/Desktop/GitHub/Sistema-de-Caixa-Armaz-m-S-o-Bento/.venv/Scripts/python.exe tools/generate_erd.py --env-key DB_CONNECTION_TEST --output docs/der_armazem_test.png

O script criado esta em tools/generate_erd.py.

O script ja tenta localizar automaticamente Graphviz em C:/Program Files/Graphviz/bin. Se necessario, defina GRAPHVIZ_BIN no ambiente.

## Testes

Os testes de integracao e CRUD usam MySQL (nao usam SQLite).

### 1) Configurar banco de testes

Defina no ambiente a variavel `DB_CONNECTION_TEST` apontando para um banco MySQL separado do banco de desenvolvimento:

```powershell
$env:DB_CONNECTION_TEST="mysql+pymysql://usuario:senha@localhost:3306/armazem_test"
```

Se `DB_CONNECTION_TEST` nao estiver definida, a suite sera pulada para evitar execucao acidental no banco principal.

### 2) Instalar dependencias de teste

```powershell
c:/python314/python.exe -m pip install pytest
```

### 3) Executar todos os testes

```powershell
c:/python314/python.exe -m pytest -q
```

### 4) Executar apenas um arquivo de teste

```powershell
c:/python314/python.exe -m pytest -q tests/test_users_crud.py
```
