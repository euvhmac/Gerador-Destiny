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
                nome TEXT NOT NULL,
                genero TEXT NOT NULL
            )
        ''')

        # Lista de nomes masculinos e femininos
        nomes_masculinos = [
            "João Silva", "Carlos Eduardo", "Pedro Henrique", "Luiz Fernando",
            "Gabriel Lima", "Lucas Souza", "Felipe Almeida", "Ricardo Fernandes",
            "Roberto Vieira", "Vinícius Moreira", "Diego Azevedo", "Tiago Costa",
            "Guilherme Pinto", "Renato Castro", "César Oliveira", "Bruno Fonseca",
            "Hugo Santana", "Marcelo Antunes", "Vitor Barreto", "Leonardo Mendes"
        ]

        nomes_femininos = [
            "Maria Oliveira", "Ana Paula", "Fernanda Costa", "Mariana Alves",
            "Rafaela Pereira", "Juliana Mendes", "Isabela Martins", "Renata Rocha",
            "Beatriz Freitas", "Larissa Gonçalves", "Camila Ribeiro", "Patrícia Ferreira",
            "Viviane Duarte", "Elaine Moura", "Simone Cardoso", "Natália Braga",
            "Letícia Mendes", "Tatiana Correia", "Adriana Campos", "Carolina Machado"
        ]

        # Inserindo nomes masculinos
        cursor.executemany('INSERT INTO nomes (nome, genero) VALUES (?, "M")', [(nome,) for nome in nomes_masculinos])
        # Inserindo nomes femininos
        cursor.executemany('INSERT INTO nomes (nome, genero) VALUES (?, "F")', [(nome,) for nome in nomes_femininos])
        conn.commit()
        print(f"{len(nomes_masculinos) + len(nomes_femininos)} nomes inseridos no banco de dados.")

        # Criação da tabela de adjetivos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS adjetivos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                adjetivo TEXT NOT NULL,
                categoria TEXT NOT NULL
            )
        ''')

        # Lista de adjetivos categorizados
        adjetivos = [
            ("delas", "personalidade"), ("slots", "profissional"), ("acordeon", "musical"),
            ("junior", "status"), ("safadinha", "personalidade"), ("cheirosa", "característica"),
            ("oficial", "status"), ("cassino", "profissional"), ("xpto", "aleatório"),
            ("topzera", "personalidade"), ("coringa", "característica"), ("patroa", "status"),
            ("vip", "status"), ("feliz", "personalidade"), ("loira", "característica"),
            ("expert", "profissional"), ("gold", "status"), ("insano", "personalidade"),
            ("king", "status"), ("queen", "status"), ("brabo", "personalidade"),
            ("star", "status"), ("doida", "personalidade"), ("plus", "status")
        ]

        # Inserindo adjetivos com categorias
        cursor.executemany('INSERT INTO adjetivos (adjetivo, categoria) VALUES (?, ?)', adjetivos)
        conn.commit()
        print(f"{len(adjetivos)} adjetivos inseridos no banco de dados.")

        # Criação da tabela de DDDs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ddd (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL
            )
        ''')

        # Lista de DDDs válidos
        ddds_validos = [
            "11", "21", "31", "41", "51", "61", "71", "81", "91",
            "12", "22", "32", "42", "52", "62", "72", "82", "92",
            "13", "23", "33", "43", "53", "63", "73", "83", "93",
            "14", "24", "34", "44", "54", "64", "74", "84", "94",
            "15", "25", "35", "45", "55", "65", "75", "85", "95",
            "16", "26", "36", "46", "56", "66", "76", "86", "96",
            "17", "27", "37", "47", "57", "67", "77", "87", "97",
            "18", "28", "38", "48", "58", "68", "78", "88", "98",
            "19", "29", "39", "49", "59", "69", "79", "89", "99"
        ]

        # Inserindo DDDs no banco de dados
        cursor.executemany('INSERT INTO ddd (codigo) VALUES (?)', [(ddd,) for ddd in ddds_validos])
        conn.commit()
        print(f"{len(ddds_validos)} DDDs inseridos no banco de dados.")

        # Verifica se os dados foram inseridos corretamente
        cursor.execute('SELECT COUNT(*) FROM nomes')
        count_nomes = cursor.fetchone()[0]
        print(f"Nomes no banco de dados: {count_nomes}")

        cursor.execute('SELECT COUNT(*) FROM adjetivos')
        count_adjetivos = cursor.fetchone()[0]
        print(f"Adjetivos no banco de dados: {count_adjetivos}")

        cursor.execute('SELECT COUNT(*) FROM ddd')
        count_ddds = cursor.fetchone()[0]
        print(f"DDDs no banco de dados: {count_ddds}")

    except Exception as e:
        print(f"Erro ao criar o banco de dados: {e}")
    
    finally:
        conn.close()
        print("Conexão com o banco de dados encerrada.")

if __name__ == "__main__":
    criar_banco_de_dados()
