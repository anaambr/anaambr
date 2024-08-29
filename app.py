from flask import Flask, url_for, request, render_template, flash, redirect
import sqlite3

app= Flask(__name__)

def get_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_connection()
    users = conn.execute('SELECT id, email FROM users').fetchall()
    return render_template('pages/index.html', users=users)

@app.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['password']
        if not email:
            flash('Email é obrigatorio')

        else:
            conn = get_connection()
            conn.execute("INSERT INTO users (email, senha) VALUES(?,?)",(email, senha))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
   
    return render_template('pages/create.html')

@app.route('/<int:id>/edit', methods= ['GET', 'POST'])
def edit(id):

    SELECT = "SELECT * FROM users WHERE id=?"
    conn = get_connection()
    user = conn.execute(SELECT, (str(id),)).fetchone()
    
    if user == None:
        return 'Não existe'
    
    if request.method == 'POST':
        email = request.form['email']
        UPDATE = "UPDATE users SET email=? WHERE id=?"
        conn.execute(UPDATE, (email, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))


    return render_template('pages/edit.html', user = user)

    
    
    #if request.method == 'POST':
    #   return 'oi'
    # conn= get_connection()
    # pdate ="UPDATE users SET email=? WHERE ID =?"
    # return str(id)
