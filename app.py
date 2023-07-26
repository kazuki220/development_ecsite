from flask import Flask, render_template, request, redirect, url_for, session
import db
from product import product_bp
from cart import cart_bp
from orders import orders_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key' 
app.register_blueprint(product_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(orders_bp)

@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')

    if msg == None:
        return render_template('index.html')
    else:
        return render_template('index.html', msg=msg)
    
@app.route('/', methods=['POST'])
def login():
    user_name = request.form.get('user_name')
    password = request.form.get('password')
    user_type = request.form.get('user_type')

    if user_type == 'admin':
        if db.admin_login(user_name, password):
            session['user'] = {'user_name': user_name, 'user_type': user_type}
            return redirect(url_for('admin_page'))
    elif user_type == 'user':
        if db.user_login(user_name, password):
            session['user'] = {'user_name': user_name, 'user_type': user_type}
            return redirect(url_for('user_page'))

    error = 'ユーザ名またはパスワードが違います。'
    return render_template('index.html', error=error)

@app.route('/admin', methods=['GET'])
def admin_page():
    if 'user' in session and session['user']['user_type'] == 'admin':
        return render_template('admin.html')
    else:
        return redirect(url_for('index'))

@app.route('/user', methods=['GET'])
def user_page():
    if 'user' in session and session['user']['user_type'] == 'user':
        return render_template('user.html')
    else:
        return redirect(url_for('index'))


@app.route('/registers')
def registers_form():
    return render_template('registers.html')

@app.route('/registers_exe', methods=['POST'])
def registers_exe():
    user_name = request.form.get('user_name')
    password = request.form.get('password')
    user_type = request.form.get('user_type')

    if user_name == '':
        error = 'ユーザ名が未入力です'
        return render_template('registers.html', error=error)

    if password == '':
        error = 'パスワードが未入力です'
        return render_template('registers.html', error=error)
    
    if user_type == 'admin':
        count = db.insert_user(user_name, password, user_type='admin')
    elif user_type == 'user':
        count = db.insert_user(user_name, password, user_type='user')
    else:
        error = '無効なユーザタイプです'
        return render_template('registers.html', error=error)

    count = db.insert_user(user_name, password, user_type)

    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('index', msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('registers.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.template_filter('calculate_total_price')
def calculate_total_price(products):
    total_price = 0
    for product in products:
        total_price += product[2]
    return total_price

if __name__ == '__main__':
    app.run(debug=True)