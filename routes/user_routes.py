from flask import Blueprint, request, jsonify
from entities.user_crud import create_user, get_all_users, update_user, delete_user

# Criando um Blueprint para as rotas de usuário
user_bp = Blueprint('user', __name__)

@user_bp.route('/user/test')
def test_route():
    return "Acesso à rota de teste de usuario bem-sucedido!"

# Rota para criar um usuário
@user_bp.route('/user', methods=['POST'])
def create_new_user():
    if request.is_json:
        # Requisição via JSON (como de uma API)
        data = request.get_json()
    else:
        # Requisição via formulário HTML
        data = {
            'name': request.form['name'],
            'dateofbirth': request.form['dateofbirth'],
            'email': request.form['email'],
            'password': request.form['password'],
            'institutionName': request.form['institutionName']
        }
    return create_user(data)


# Rota para listar todos os usuários
@user_bp.route('/users', methods=['GET'])
def list_users():
    return jsonify(get_all_users())

# Rota para atualizar um usuário
@user_bp.route('/user/<int:id>', methods=['PUT'])
def update_existing_user(id):
    data = request.get_json()
    return update_user(id, data)

# Rota para deletar um usuário
@user_bp.route('/user/<int:id>', methods=['DELETE'])
def delete_existing_user(id):
    return delete_user(id)
