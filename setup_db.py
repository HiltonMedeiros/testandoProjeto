from database import app, db

# Criação das tabelas no banco de dados:
with app.app_context():
    db.create_all()
    print("Banco de Dados criado!")
