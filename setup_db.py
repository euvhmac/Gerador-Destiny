# src/setup_db.py

import sqlite3
import os

def criar_banco_de_dados():
    # Define o caminho absoluto para o banco de dados
    db_path = os.path.join(os.path.dirname(__file__), 'nomes.db')

    # Verifica se o banco de dados já existe e apaga o antigo
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Arquivo 'nomes.db' removido para recriação.")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Criação da tabela para armazenar os nomes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )
        ''')

        # Lista de 50 nomes a serem inseridos
        nomes = [
            "João Silva", "Maria Oliveira", "Carlos Eduardo", "Ana Paula",
            "Pedro Henrique", "Fernanda Costa", "Luiz Fernando", "Mariana Alves",
            "Gabriel Lima", "Rafaela Pereira", "Lucas Souza", "Juliana Mendes",
            "Felipe Almeida", "Isabela Martins", "Roberto Vieira", "Renata Rocha",
            "Ricardo Fernandes", "Beatriz Freitas", "Vinícius Moreira", "Larissa Gonçalves",
            "Diego Azevedo", "Camila Ribeiro", "Tiago Costa", "Patrícia Ferreira",
            "Guilherme Pinto", "Viviane Duarte", "Renato Castro", "Elaine Moura",
            "César Oliveira", "Simone Cardoso", "Bruno Fonseca", "Natália Braga",
            "Hugo Santana", "Letícia Mendes", "Marcelo Antunes", "Tatiana Correia",
            "Vitor Barreto", "Adriana Campos", "Leonardo Mendes", "Carolina Machado",
            "Rodrigo Moreira", "Aline Vasconcelos", "Daniel Pereira", "Priscila Martins",
            "Igor Sampaio", "Vanessa Neves", "Fábio Rocha", "Jéssica Fernandes",
            "Alexandre Almeida", "Luciana Ferreira"
        ]

        # Inserindo nomes no banco de dados
        cursor.executemany('INSERT INTO nomes (nome) VALUES (?)', [(nome,) for nome in nomes])
        conn.commit()
        print(f"{len(nomes)} nomes inseridos no banco de dados.")

        # Criação da tabela de adjetivos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS adjetivos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                adjetivo TEXT NOT NULL
            )
        ''')

        # Lista de 50 adjetivos a serem inseridos
        adjetivos = [
            "01", "delas", "slots", "acordeon", "junior", "safadinha",
            "cheirosa", "oficial", "cassino", "011", "021", "013", 
            "damidia", "daspaty", "delas", "xpto", "topzera", "zica",
            "coringa", "malvada", "patroa", "feliz", "vip", "loira",
            "branquela", "mister", "sedutora", "gangster", "bbb",
            "noob", "expert", "black", "pink", "gold", "silver",
            "brabo", "insano", "like", "quente", "frio", "bombom",
            "king", "queen", "doida", "boss", "star", "021", "013",
            "000", "plus"
        ]

        # Inserindo adjetivos no banco de dados
        cursor.executemany('INSERT INTO adjetivos (adjetivo) VALUES (?)', [(adj,) for adj in adjetivos])
        conn.commit()
        print(f"{len(adjetivos)} adjetivos inseridos no banco de dados.")

        # Verifica se os dados foram inseridos corretamente
        cursor.execute('SELECT COUNT(*) FROM nomes')
        count_nomes = cursor.fetchone()[0]
        print(f"Nomes no banco de dados: {count_nomes}")

        cursor.execute('SELECT COUNT(*) FROM adjetivos')
        count_adjetivos = cursor.fetchone()[0]
        print(f"Adjetivos no banco de dados: {count_adjetivos}")

    except Exception as e:
        print(f"Erro ao criar o banco de dados: {e}")
    
    finally:
        conn.close()
        print("Conexão com o banco de dados encerrada.")

if __name__ == "__main__":
    criar_banco_de_dados()
