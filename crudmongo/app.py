from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Configuração do MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['meuBanco']  # Nome do banco de dados
collection = db['clientes']  # Nome da coleção (tabela)

# Página inicial: Listar clientes, permitir pesquisa e ordenação por botão
@app.route('/', methods=['GET', 'POST'])
def index():
    sort_by = request.args.get('sort_by', 'nome')  # Ordenar por padrão pelo nome
    order = request.args.get('order', 'asc')  # Ordem crescente por padrão

    # Definir direção de ordenação
    order_direction = 1 if order == 'asc' else -1

    # Pesquisa por nome
    query = {}
    if request.method == 'POST':
        nome_pesquisa = request.form['nome']
        query = {"nome": {"$regex": nome_pesquisa, "$options": "i"}}
    
    # Busca no MongoDB
    clientes = collection.find(query).sort(sort_by, order_direction)

    return render_template('index.html', clientes=clientes, sort_by=sort_by, order=order)

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
