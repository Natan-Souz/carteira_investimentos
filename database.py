import sqlite3

def criar_banco():
    conexao = sqlite3.connect('carteira.db')
    cursor = conexao.cursor()

    #Tabela de ativos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ativos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE NOT NULL,
        nome TEXT
    )
    """)

    #Tabela de transações
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ativo TEXT NOT NULL,
        tipo TEXT NOT NULL,  -- Compra ou Venda
        quantidade INTEGER NOT NULL,
        preco REAL NOT NULL,
        data TEXT NOT NULL
    )
    ''')

    conexao.commit()
    conexao.close()

if __name__ == "__main__":
    criar_banco()