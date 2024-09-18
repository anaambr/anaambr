from flask import Flask, session, request, render_template, url_for, redirect
import sqlite3

app = Flask(__name__)

# chave para critografia de cookies na sessão
app.config['SECRET_KEY'] = 'superdificil'

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dash():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', nome=session['user'])

@app.route('/login', methods=['POST', 'GET'])
def login():
    # se já tá logado
    if 'user' in session:
        return redirect(url_for('dash')) #vai pra o dashboard

    if request.method == 'GET':
        return render_template('login.html')
    else:
        nome = request.form['nome']
        senha = request.form['senha']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE nome = ? AND senha = ?', (nome, senha)).fetchone()
        conn.close()

        if user:
            session['user'] = nome
            return redirect(url_for('dash'))
        else:
            return "SENHA INCORRETA ou não está cadastrado"

@app.route('/register', methods=['GET', 'POST'])
def register():
    # se já tá logado
    if 'user' in session:
        return redirect(url_for('dash')) #vai pra o dashboard

    if request.method == 'GET':
        return render_template('register.html')
    else:
        nome = request.form['nome']
        senha = request.form['senha']

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (nome, senha) VALUES (?, ?)', (nome, senha))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return redirect(url_for('login'))
        
        conn.close()
        session['user'] = nome
        return redirect(url_for('dash'))

@app.route('/logout', methods=['POST'])
def logout():
    if 'user' in session:
        session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
