from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Configuração do MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['clientes']  # Nome do banco de dados
collection = db['client']  # Nome da coleção (tabela)

# Página inicial: Listar clientes e permitir pesquisa
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome_pesquisa = request.form['nome']
        clientes = collection.find({"nome": {"$regex": nome_pesquisa, "$options": "i"}})
    else:
        clientes = collection.find()
    return render_template('index.html', clientes=clientes)

# Criar cliente
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        collection.insert_one({'nome': nome, 'email': email})
        return redirect(url_for('index'))
    return render_template('create.html')

# Editar cliente
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    cliente = collection.find_one({"_id": ObjectId(id)})
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        collection.update_one({"_id": ObjectId(id)}, {"$set": {'nome': nome, 'email': email}})
        return redirect(url_for('index'))
    return render_template('edit.html', cliente=cliente)

# Excluir cliente
@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
