from flask import Blueprint, render_template, request, redirect, url_for, session
import db

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/product/<int:product_id>')
def product(product_id):
    product = db.get_product_by_id(product_id)
    return render_template('item.html', product=product)

def get_product_quantity(product_id):
    cart_items = session.get('cart_items', [])
    return cart_items.count(str(product_id))

@cart_bp.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        try:
            product_id = int(request.form['product_id'])
        except (KeyError, ValueError):
            product_id = 0
        return add_to_cart(product_id)

    ecuser_id = get_user_id_from_session()
    cart_items = db.get_cart_items(ecuser_id)
    total_price = calculate_total_price(cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

def add_to_cart(product_id):
    product = db.get_product_by_id(product_id)
    if product is None:
        error_message = "商品が存在しません。"
        return render_template('error.html', error_message=error_message)

    # セッションからecuser_idを取得する
    ecuser_id = session.get('user_id', None)
    if ecuser_id is None:
        error_message = "ユーザーがログインしていません。"
        return render_template('error.html', error_message=error_message)

    # カート内に同じ商品がある場合は数量を増やす
    cart_items = session.get('cart_items', [])
    if str(product[0]) in cart_items:
        index = cart_items.index(str(product[0]))
        cart_quantity = int(cart_items[index + 1])
        cart_items[index + 1] = str(cart_quantity + 1)
    else:
        cart_items.append(str(product[0]))
        cart_items.append('1')
    
    session['cart_items'] = cart_items

    return redirect(url_for('cart.cart'))

def calculate_total_price(products):
    total_price = 0
    for product in products:
        total_price += product[2]
    return total_price

@cart_bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form['product_id']
    cart_items = session.get('cart_items', [])

    cart_items = [item for item in cart_items if item != product_id]

    session['cart_items'] = cart_items
    return redirect(url_for('cart.cart'))

def get_user_id_from_session():
    if 'user' in session and 'ecuser_id' in session['user']:
        return session['user']['ecuser_id']
    return None