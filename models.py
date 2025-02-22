from database import db

class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Pessoa {self.nome}>'

    @staticmethod
    def criar(nome, idade): #CRIA E ADICIONA UMA NOVA PESSOA NO DB
        try:
            nova_pessoa = Pessoa(nome=nome, idade=idade)
            db.session.add(nova_pessoa)
            db.session.commit()
            return nova_pessoa
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao criar pessoa: {e}")
            return None

    @staticmethod
    def listar():#RETORNA PESSOAS CADASTRADAS
        return Pessoa.query.all()

    @staticmethod
    def deletar(pessoa_id): #EXCLUI UMA PESSOA DO DB
        pessoa = Pessoa.query.get(pessoa_id)
        if pessoa:
            db.session.delete(pessoa)
            db.session.commit()
            return True
        return False


class Transacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'), nullable=False) #ASSOCIA ID_PESSOA COM A TRANSACAO
    pessoa = db.relationship('Pessoa', backref=db.backref('transacoes', lazy=True, cascade='all, delete'))

    def __repr__(self):
        return f'<Transacao {self.descricao} - {self.valor}>'

    @staticmethod
    def criar(descricao, valor, tipo, pessoa_id):
        nova_transacao = Transacao(descricao=descricao, valor=valor, tipo=tipo, pessoa_id=pessoa_id)
        db.session.add(nova_transacao)
        db.session.commit()
        return nova_transacao

    @staticmethod
    def listar(): #RETORNA TODAS AS TRASACOES DO BANCO
        return Transacao.query.all()


class ConsultaDeTotais:
    @staticmethod
    def listar_totais(): #CALCULA OS TOTAIS PESSOAIS E GERAIS
        pessoas = Pessoa.query.all()
        resultado = []
        total_receitas = 0
        total_despesas = 0

        for pessoa in pessoas:#PERCORRER LISTA DE CADASTRADOS
            receitas = sum(t.valor for t in pessoa.transacoes if t.tipo.lower() == 'receita')
            despesas = sum(t.valor for t in pessoa.transacoes if t.tipo.lower() == 'despesa')
            saldo = receitas - despesas

            total_receitas += receitas
            total_despesas += despesas

            resultado.append({
                'pessoa': pessoa.nome,
                'receitas': receitas,
                'despesas': despesas,
                'saldo': saldo
            })

        saldo_liquido = total_receitas - total_despesas
        totais_gerais = {
            'total_receitas': total_receitas,
            'total_despesas': total_despesas,
            'saldo_liquido': saldo_liquido
        }

        return resultado, totais_gerais
