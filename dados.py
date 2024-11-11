import random
import sqlite3
import os
import sys
import shutil
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constantes
DATABASE_NAME = 'nomes.db'
MODEL_DATABASE_NAME = 'assets/modelo_nomes.db'

# Função para obter o caminho do arquivo de recurso
def resource_path(relative_path):
    """Retorna o caminho absoluto do arquivo, compatível com executáveis."""
    try:
        base_path = sys._MEIPASS  # Para executáveis criados com PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")  # Para execução em ambiente de desenvolvimento
    return os.path.join(base_path, relative_path)

# Função para inicializar o banco de dados se ele não existir
def inicializar_banco_de_dados():
    db_path = get_db_path()
    modelo_db_path = resource_path(MODEL_DATABASE_NAME)

    if not os.path.exists(db_path):
        shutil.copy(modelo_db_path, db_path)
        logging.info("Banco de dados 'nomes.db' copiado para a pasta do executável.")

# Função para obter o caminho do banco de dados
def get_db_path():
    """Retorna o caminho absoluto do banco de dados, dependendo do ambiente."""
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, DATABASE_NAME)

# Função para conectar ao banco de dados
def conectar_banco_de_dados():
    """Conecta ao banco de dados SQLite, inicializando se necessário."""
    db_path = get_db_path()
    try:
        inicializar_banco_de_dados()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                genero TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS adjetivos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                adjetivo TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ddd (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL
            )
        ''')
        conn.commit()
        return conn
    except sqlite3.Error as e:
        logging.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para obter um nome aleatório do banco de dados
def gerar_nome(genero=None):
    conn = conectar_banco_de_dados()
    if conn is None:
        return "Nome Desconhecido"
    
    cursor = conn.cursor()
    try:
        if genero in ["M", "F"]:
            cursor.execute('SELECT nome FROM nomes WHERE genero = ? ORDER BY RANDOM() LIMIT 1', (genero,))
        else:
            cursor.execute('SELECT nome FROM nomes ORDER BY RANDOM() LIMIT 1')
        resultado = cursor.fetchone()
    except sqlite3.Error as e:
        logging.error(f"Erro ao executar a consulta de nome: {e}")
        return "Nome Desconhecido"
    finally:
        conn.close()
    
    return resultado[0] if resultado else "Nome Desconhecido"

# Função para gerar um login baseado no nome e adjetivo
def gerar_login(nome):
    conn = conectar_banco_de_dados()
    if conn is None:
        return "login_default"
    
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT adjetivo FROM adjetivos ORDER BY RANDOM() LIMIT 1')
        resultado = cursor.fetchone()
    except sqlite3.Error as e:
        logging.error(f"Erro ao executar a consulta de adjetivo: {e}")
        return "login_default"
    finally:
        conn.close()

    adjetivo = resultado[0] if resultado else "oficial"
    primeiro_nome = nome.split()[0].lower() if nome else "usuario"
    sequencia_numerica = str(random.randint(10, 999))
    login = f"{primeiro_nome}{adjetivo}{sequencia_numerica}"

    return login[:16] if len(login) > 16 else login

# Função para gerar um CPF válido
def gerar_cpf_valido():
    def calcular_digito(digs):
        soma = sum([int(d) * (len(digs) + 1 - i) for i, d in enumerate(digs)])
        resto = (soma * 10) % 11
        return 0 if resto == 10 else resto

    nove_digitos = [random.randint(0, 9) for _ in range(9)]
    digito1 = calcular_digito(nove_digitos)
    digito2 = calcular_digito(nove_digitos + [digito1])

    return ''.join(map(str, nove_digitos + [digito1, digito2]))

# Função para gerar um número de celular válido
def gerar_numero_celular_completo():
    """Gera um número de celular válido e retorna ele em dois formatos: formatado e sem formatação."""
    conn = conectar_banco_de_dados()
    if conn is None:
        return "Número Inválido", "Número Inválido"
    
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT codigo FROM ddd ORDER BY RANDOM() LIMIT 1')
        ddd = cursor.fetchone()[0]
    except sqlite3.Error as e:
        logging.error(f"Erro ao buscar DDD: {e}")
        return "Número Inválido", "Número Inválido"
    finally:
        conn.close()

    numero_base = f"9{random.randint(10000000, 99999999)}"
    numero_formatado = f"({ddd}) {numero_base}"
    numero_sem_formatacao = f"{ddd}{numero_base}"

    return numero_formatado, numero_sem_formatacao

# Testando geração de nomes, logins, CPF e celular
if __name__ == "__main__":
    for genero in ["M", "F", None]:
        nome = gerar_nome(genero)
        login = gerar_login(nome)
        cpf = gerar_cpf_valido()
        celular = gerar_numero_celular_completo()
        print(f"Nome ({'Masculino' if genero == 'M' else 'Feminino' if genero == 'F' else 'Qualquer'}): {nome}")
        print(f"Login: {login}")
        print(f"CPF: {cpf}")
        print(f"Celular: {celular}\n")
