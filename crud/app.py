# aula Aula 14 - CRUD em Flask com SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientes.sqlite3'

db = SQLAlchemy(app)
class Cliente(db.Model):
    id = db.Column('id', db.Integer, primary_key = True, autoincrement=True)
    nome = db.Column(db.String(150))
    idade = db.Column(db.Integer)
    telefone = db.Column(db.String(11))
    endereco = db.Column(db.String(150))
    
    def __init__(self, nome, idade, telefone, endereco):
        self.nome = nome
        self.idade = idade
        self.telefone = telefone
        self.endereco = endereco

@app.route('/')
def index():
    clientes = Cliente.query.all()
    print(clientes)
    return render_template('index.html', clientes = clientes)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        cliente = Cliente(request.form['nome'], request.form['idade'], request.form['telefone'], request.form['endereco'])
        #o ideal seria um try catch
        db.session.add(cliente)
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete(id):
    cliente = Cliente.query.get(id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('index'))
    
@app.route('/edit/<int:id>', methods = ['GET', 'POST'])
def edit(id):
    cliente = Cliente.query.get(id)
    if request.method == 'POST':
        cliente.nome = request.form['nome']
        cliente.idade = request.form['idade']
        #o ideal seria um try catch
        db.session.commit()
    
        return redirect(url_for('index'))
    return render_template('edit.html', cliente=cliente)
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=3000)