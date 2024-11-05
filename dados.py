# src/dados.py

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

    # Copia o modelo de banco de dados se o arquivo não existir
    if not os.path.exists(db_path):
        shutil.copy(modelo_db_path, db_path)
        logging.info("Banco de dados 'nomes.db' copiado para a pasta do executável.")

# Função para obter o caminho do banco de dados
def get_db_path():
    """Retorna o caminho absoluto do banco de dados, dependendo do ambiente."""
    if getattr(sys, 'frozen', False):  # Se rodando como um executável
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, DATABASE_NAME)

# Função para conectar ao banco de dados com verificação robusta
def conectar_banco_de_dados():
    """Conecta ao banco de dados SQLite, inicializando se necessário.
    
    Retorna:
        Connection: objeto de conexão com o banco de dados, ou None em caso de falha.
    """
    db_path = get_db_path()
    try:
        # Verificar se o banco de dados já foi inicializado
        inicializar_banco_de_dados()
        conn = sqlite3.connect(db_path)
        
        # Verificar se o banco de dados possui as tabelas, caso contrário, criá-las
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS nomes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, genero TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS adjetivos (id INTEGER PRIMARY KEY AUTOINCREMENT, adjetivo TEXT NOT NULL)''')
        conn.commit()
        
        return conn
    except sqlite3.Error as e:
        logging.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para obter um nome aleatório do banco de dados com filtro de gênero
def gerar_nome(genero=None):
    """Gera um nome aleatório do banco de dados, com opção de filtro por gênero.
    
    Args:
        genero (str, opcional): "M" para masculino, "F" para feminino, ou None para qualquer gênero.
    
    Retorna:
        str: Nome aleatório ou "Nome Desconhecido" em caso de falha.
    """
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

# Função para gerar um login baseado no nome, adjetivo e uma sequência aleatória
def gerar_login(nome):
    """Gera um login baseado no primeiro nome, um adjetivo aleatório e uma sequência numérica aleatória.
    
    Args:
        nome (str): Nome da pessoa para criar o login.
    
    Retorna:
        str: Login gerado ou "login_default" em caso de falha.
    """
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

    # Gera uma sequência de 2 a 3 dígitos aleatórios
    sequencia_numerica = str(random.randint(10, 999))

    # Combina o primeiro nome, adjetivo e sequência numérica para formar o login
    login = f"{primeiro_nome}{adjetivo}{sequencia_numerica}"

    # Limita o login a no máximo 16 caracteres
    if len(login) > 16:
        login = login[:16]

    return login

# Função para gerar um CPF válido (apenas números, sem formatação)
def gerar_cpf_valido():
    """Gera um CPF válido conforme a regra de verificação dos dígitos finais.
    
    Retorna:
        str: CPF gerado como uma string de 11 dígitos (sem formatação).
    """
    def calcular_digito(digs):
        soma = sum([int(d) * (len(digs) + 1 - i) for i, d in enumerate(digs)])
        resto = (soma * 10) % 11
        return 0 if resto == 10 else resto

    # Gera os nove primeiros dígitos
    nove_digitos = [random.randint(0, 9) for _ in range(9)]
    digito1 = calcular_digito(nove_digitos)
    digito2 = calcular_digito(nove_digitos + [digito1])

    # Retorna o CPF sem formatação
    return ''.join(map(str, nove_digitos + [digito1, digito2]))

# Testando geração de nomes, logins e CPF válidos
if __name__ == "__main__":
    for genero in ["M", "F", None]:
        nome = gerar_nome(genero)
        login = gerar_login(nome)
        cpf = gerar_cpf_valido()
        print(f"Nome Gerado ({'Masculino' if genero == 'M' else 'Feminino' if genero == 'F' else 'Qualquer'}): {nome}")
        print(f"Login Gerado: {login}")
        print(f"CPF Gerado: {cpf}\n")
