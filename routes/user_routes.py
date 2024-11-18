from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from entities.user_crud import create_user, get_all_users, update_user, delete_user, get_user_by_email_and_password, get_user_by_id
from entities.admin_crud import get_admin_by_email_and_password

# Criando um Blueprint para as rotas de usuário
user_bp = Blueprint('user', __name__)

#Teste de funcionamento
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

# Rota para o login
@user_bp.route('/login', methods=['POST'])
def login_user():
    if request.is_json:
        data = request.get_json()  # Obtém os dados em JSON
    else:
        return jsonify({"error": "Formato de mídia não suportado. Envie os dados em JSON."}), 415
    
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400
    
    # Tenta encontrar o usuário na tabela de admin
    admin = get_admin_by_email_and_password(email, password)
    if admin:
        session['user_id'] = admin['id']
        session['role'] = 'admin'
        return jsonify({"message": f"Login bem-sucedido, Olá, {admin['username']}! Você é um administrador."}), 200
    
    # Tenta encontrar o usuário na tabela de user
    user = get_user_by_email_and_password(email, password)
    if user:
        session['user_id'] = user['id']
        session['role'] = 'user'
        return jsonify({"message": f"Login bem-sucedido, Olá, {user['name']}! Você é um usuário."}), 200
    
    return jsonify({"error": "Email ou senha incorretos"}), 401



#Rota para Logout
@user_bp.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove o user_id da sessão
    return redirect(url_for('app.login'))  # Redireciona





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



# Rota para o dashboard
@user_bp.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    user_role = session.get('role')

    if not user_id or not user_role:
        return redirect(url_for('app.login'))  # Redireciona para o login se não estiver logado

    if user_role == 'admin':
        return redirect(url_for('app.admin_dashboard'))
    elif user_role == 'user':
        return redirect(url_for('app.dashboard'))
    else:
        return redirect(url_for('app.login'))  # Em caso de erro, retorna ao login


@user_bp.route('/admin_dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('app.login'))
    return render_template('admin_dashboard.html')  # Renderiza o dashboard do admin


@user_bp.route('/dashboard')
def user_dashboard():
    if session.get('role') != 'user':
        return redirect(url_for('app.login'))
    return render_template('dashboard.html')  # Renderiza o dashboard do usuário


