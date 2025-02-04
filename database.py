import sqlite3

def conectar():
    return sqlite3.connect('encomendas.db')

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS encomendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        codigo TEXT NOT NULL UNIQUE,
        apartamento TEXT NOT NULL,
        bloco TEXT NOT NULL,
        status TEXT DEFAULT 'pendente',
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

def inserir(nome, codigo, apartamento, bloco):
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        INSERT INTO encomendas (nome, codigo, apartamento, bloco)
        VALUES (?, ?, ?, ?)
        ''', (nome, codigo, apartamento, bloco))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def listar_todos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM encomendas ORDER BY data DESC')
    registros = cursor.fetchall()
    conn.close()
    return registros

def buscar_por_id(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM encomendas WHERE id = ?', (id,))
    registro = cursor.fetchone()
    conn.close()
    return registro

def atualizar(id, nome, codigo, apartamento, bloco):
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        UPDATE encomendas
        SET nome = ?, codigo = ?, apartamento = ?, bloco = ?
        WHERE id = ?
        ''', (nome, codigo, apartamento, bloco, id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def excluir(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM encomendas WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def confirmar_entrega(codigo, apartamento, bloco):
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        UPDATE encomendas
        SET status = 'entregue'
        WHERE codigo = ? 
        AND apartamento = ?
        AND bloco = ?
        AND status = 'pendente'
        ''', (codigo, apartamento, bloco))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()