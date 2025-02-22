from flask import Flask, render_template, request, redirect, url_for
from models import db, Pessoa, Transacao, ConsultaDeTotais

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
db.init_app(app)

#ROTA - PÁGINA INICIAL
@app.route('/')
def index():
    pessoas = Pessoa.listar()
    return render_template('index.html', pessoas=pessoas)

#ROTA - CADASTRAR PESSOA
@app.route('/pessoa/novo', methods=['GET', 'POST'])
def nova_pessoa():
    if request.method == 'POST':
        nome = request.form['nome'] #RECUPERA DADOS
        idade = request.form['idade']
        Pessoa.criar(nome, idade)
        return redirect(url_for('index'))
    return render_template('pessoa_form.html')

#ROTA - CADASTRAR TRANSAÇÃO
@app.route('/transacao/novo', methods=['GET', 'POST'])
def nova_transacao():
    pessoas = Pessoa.listar() #RECUPERA LISTA DE PESSOAS CADASTRADAS
    if request.method == 'POST':
        descricao = request.form['descricao']
        valor = request.form['valor']
        tipo = request.form['tipo']
        pessoa_id = request.form['pessoa_id']
        Transacao.criar(descricao, valor, tipo, pessoa_id) #CRIA UMA NOVA TRANSACAO NO BANCO DE DADOS
        return redirect(url_for('index'))
    return render_template('transacao_form.html', pessoas=pessoas)

#ROTA - CONSULTAS GERAIS
@app.route('/consultas', methods=['GET'])
def consultas():
    totais, totais_gerais = ConsultaDeTotais.listar_totais()
    return render_template('consultas.html', totais=totais, totais_gerais=totais_gerais)

#ROTA - DELETAR USUÁRIO
@app.route('/pessoas/deletar/<int:pessoa_id>', methods=['POST'])
def deletar_pessoa(pessoa_id):
        if Pessoa.deletar(pessoa_id):
            return redirect(url_for('index'))
        return "Erro ao deletar pessoa", 400  #CASO NÃO SEJA POSSÍVEL DELETAR



if __name__ == '__main__':
    app.run(debug=True)
