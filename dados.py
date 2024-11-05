# src/dados.py

import random
import sqlite3
import os
import sys
import shutil

# Função para obter o caminho do arquivo de recurso
def resource_path(relative_path):
    """Retorna o caminho absoluto do arquivo, compatível com executáveis"""
    try:
        # Para executáveis criados com PyInstaller
        base_path = sys._MEIPASS
    except AttributeError:
        # Para execução em ambiente de desenvolvimento
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Função para inicializar o banco de dados se ele não existir
def inicializar_banco_de_dados():
    db_path = get_db_path()
    modelo_db_path = resource_path("assets/modelo_nomes.db")

    # Copia o modelo de banco de dados se o arquivo não existir
    if not os.path.exists(db_path):
        shutil.copy(modelo_db_path, db_path)
        print("Banco de dados 'nomes.db' copiado para a pasta do executável.")

# Função para obter o caminho do banco de dados
def get_db_path():
    if getattr(sys, 'frozen', False):  # Se rodando como um executável
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, 'nomes.db')

# Função para conectar ao banco de dados com verificação robusta
def conectar_banco_de_dados():
    db_path = get_db_path()
    try:
        # Verificar se o banco de dados já foi inicializado
        inicializar_banco_de_dados()
        conn = sqlite3.connect(db_path)
        
        # Verificar se o banco de dados possui as tabelas, caso contrário, cria-las
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS nomes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS adjetivos (id INTEGER PRIMARY KEY AUTOINCREMENT, adjetivo TEXT NOT NULL)''')
        conn.commit()
        
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para obter um nome aleatório do banco de dados com verificação de falhas
def gerar_nome():
    conn = conectar_banco_de_dados()
    if conn is None:
        return "Nome Desconhecido"
    
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT nome FROM nomes ORDER BY RANDOM() LIMIT 1')
        resultado = cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Erro ao executar a consulta de nome: {e}")
        return "Nome Desconhecido"
    finally:
        conn.close()
    
    if resultado:
        return resultado[0]
    return "Nome Desconhecido"

# Função para gerar um login baseado no nome e adjetivo com verificação de falhas
def gerar_login(nome):
    conn = conectar_banco_de_dados()
    if conn is None:
        return "login_default"
    
    cursor = conn.cursor()
    
    # Obtém um adjetivo aleatório do banco de dados
    try:
        cursor.execute('SELECT adjetivo FROM adjetivos ORDER BY RANDOM() LIMIT 1')
        resultado = cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Erro ao executar a consulta de adjetivo: {e}")
        return "login_default"
    finally:
        conn.close()
    
    if resultado:
        adjetivo = resultado[0]
    else:
        adjetivo = "oficial"
    
    # Pega o primeiro nome da pessoa e cria um login
    primeiro_nome = nome.split()[0].lower()
    login = f"{primeiro_nome}{adjetivo}"

    # Limita o login a no máximo 16 caracteres
    if len(login) > 16:
        login = login[:16]

    return login

# Função para gerar um CPF aleatório (apenas números, sem validação)
def gerar_cpf():
    return ''.join([str(random.randint(0, 9)) for _ in range(11)])

# Testando geração de nomes e logins
if __name__ == "__main__":
    for _ in range(5):
        nome = gerar_nome()
        login = gerar_login(nome)
        print(f"Nome Gerado: {nome}, Login Gerado: {login}")
