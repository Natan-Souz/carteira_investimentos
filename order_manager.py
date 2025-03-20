import sqlite3

def inserir_ordem(ativo, tipo, quantidade, preco, data):
    """
    Insere uma nova ordem de compra ou venda no banco de dados.
    
    Parâmetros:
    - ativo (str): Código do ativo (ex: PETR4)
    - tipo (str): 'compra' ou 'venda'
    - quantidade (int): Quantidade de ações
    - preco (float): Preço unitário
    - data (str): Data da transação no formato 'YYYY-MM-DD'
    """
    conexao = sqlite3.connect("carteira.db")
    cursor = conexao.cursor()
    
    try:
        cursor.execute('''
        INSERT INTO transacoes (ativo, tipo, quantidade, preco, data)
        VALUES (?, ?, ?, ?, ?)
        ''', (ativo.upper(), tipo.lower(), quantidade, preco, data))

        conexao.commit()
        print(f"✅ Ordem registrada: {tipo.upper()} {quantidade}x {ativo} a R$ {preco:.2f} em {data}")
    
    except sqlite3.Error as e:
        print(f"❌ Erro ao inserir ordem: {e}")

    finally:
        conexao.close()


def listar_transacoes():
    """
    Lista todas as transações registradas no banco de dados.
    """
    conexao = sqlite3.connect("carteira.db")
    cursor = conexao.cursor()
    
    cursor.execute("SELECT * FROM transacoes ORDER BY data DESC")
    transacoes = cursor.fetchall()
    
    conexao.close()
    return transacoes


def excluir_ordem(id_ordem):
    """
    Exclui uma ordem pelo ID.
    
    Parâmetros:
    - id_ordem (int): ID da ordem a ser excluída
    """
    conexao = sqlite3.connect("carteira.db")
    cursor = conexao.cursor()
    
    try:
        cursor.execute("DELETE FROM transacoes WHERE id = ?", (id_ordem,))
        conexao.commit()
        print(f"🗑️ Ordem {id_ordem} excluída com sucesso.")
    
    except sqlite3.Error as e:
        print(f"❌ Erro ao excluir ordem: {e}")
    
    finally:
        conexao.close()
