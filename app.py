from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, session
import sqlite3
app = Flask(__name__)
app.secret_key = 'Senha@12345'

#Primeiro passo é puxar o banco de dados com a aplicação, e inicializa-lo

def init_db():
    conn = sqlite3.connect('database.db')
    cursor_da_aplicacao = conn.cursor()
    cursor_da_aplicacao.execute('''CREATE TABLE IF NOT EXISTS usuarios(id INTERGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)
                                ''')

    cursor_da_aplicacao.execute('''
    CREATE TABLE IF NOT EXIST client(
    id INTERGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL, 
    cpf TEXT NOT NULL (LENGTH(cpf) = 11), 
    email TEXT NOT NULL)
''')
    conn.commit()  
    conn.close()

#Após encerramento do banco de dados iniciamos a aplicação web

@app.route("/")
def index():
    if 'usuario' in session: #checagem se o usuário já esta logado 
        conn = sqlite3.connect('cadastro.db')
        cursor_da_aplicacao = conn.cursor()
        cursor_da_aplicacao.execute("SELECT * FROM clientes")
        clientes = cursor_da_aplicacao.fetchall()
        conn.close()
        return render_template('index.html', clientes=clientes)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():#metodo para puxar o login do usuário
    if request.method == 'POST': 
        usuario = request.form['username']
        senha = request.form['password']
        conn = sqlite3.connect('cadastro.db')
        cursor_da_aplicacao = conn.cursor()
        cursor_da_aplicacao.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (usuario, senha))
        user = cursor_da_aplicacao.fetchone()
        conn.close()
        if user:
            session['usuario'] = usuario
            return redirect(url_for('index'))
        return "Usuário ou senha inválidos."
    return render_template('login.html')

#encerramento do usuário e retorna para página de login
@app.route('/logout')
def logout():
    session.pop('usuario', None) 
    return redirect(url_for('login'))

#rota para adicionar novos usuários 
@app.route('/add', methods=['POST'])
def add():
    if 'usuario' in session:
        nome = request.form['nome']
        cpf = request.form['cpf'][:11]  # Limita a 11 caracteres
        email = request.form['email']
        conn = sqlite3.connect('cadastro.db')
        cursor_da_aplicacao = conn.cursor()
        cursor_da_aplicacao.execute("INSERT INTO clientes (nome, cpf, email) VALUES (?, ?, ?)", (nome, cpf, email))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return redirect(url_for('login'))

#rota para exclusão de usuários
@app.route('/delete/<int:id>')
def delete(id):
    if 'usuario' in session:
        conn = sqlite3.connect('cadastro.db')
        cursor_da_aplicacao = conn.cursor()
        cursor_da_aplicacao.execute("DELETE FROM clientes WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 
