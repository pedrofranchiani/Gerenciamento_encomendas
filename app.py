from flask import Flask, render_template, request, redirect, url_for, flash
from database import (
    criar_tabela, inserir, listar_todos, buscar_por_id,
    atualizar, excluir, confirmar_entrega
)

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Inicialização do banco
criar_tabela()

# Rotas principais
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome'].strip()
    codigo = request.form['codigo'].strip()
    apartamento = request.form['apartamento'].strip()
    bloco = request.form['bloco'].strip()
    
    if not all([nome, codigo, apartamento, bloco]):
        flash('Preencha todos os campos!', 'erro')
        return redirect(url_for('index'))
    
    if inserir(nome, codigo, apartamento, bloco):
        flash('Cadastro realizado com sucesso!', 'sucesso')
    else:
        flash('Erro: Código já cadastrado!', 'erro')
    
    return redirect(url_for('gerenciar'))

@app.route('/gerenciar')
def gerenciar():
    return render_template('gerenciar.html', registros=listar_todos())

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        nome = request.form['nome'].strip()
        codigo = request.form['codigo'].strip()
        apartamento = request.form['apartamento'].strip()
        bloco = request.form['bloco'].strip()
        
        if atualizar(id, nome, codigo, apartamento, bloco):
            flash('Registro atualizado!', 'sucesso')
        else:
            flash('Erro ao atualizar!', 'erro')
        
        return redirect(url_for('gerenciar'))
    
    registro = buscar_por_id(id)
    return render_template('editar.html', registro=registro) if registro else redirect(url_for('gerenciar'))

@app.route('/excluir/<int:id>')
def excluir_registro(id):
    excluir(id)
    flash('Registro excluído!', 'sucesso')
    return redirect(url_for('gerenciar'))

@app.route('/confirmar-entrega', methods=['GET', 'POST'])
def confirmar_entrega_route():
    if request.method == 'POST':
        codigo = request.form['codigo'].strip()
        apartamento = request.form['apartamento'].strip()
        bloco = request.form['bloco'].strip()
        
        if confirmar_entrega(codigo, apartamento, bloco):
            flash('Entrega confirmada com sucesso!', 'sucesso')
        else:
            flash('Encomenda não encontrada ou já entregue!', 'erro')
        
        return redirect(url_for('confirmar_entrega_route'))
    
    return render_template('confirmar_entrega.html')

@app.route('/entregas')
def entregas():
    return render_template('entregas.html', registros=listar_todos())

if __name__ == '__main__':
    app.run(debug=True)