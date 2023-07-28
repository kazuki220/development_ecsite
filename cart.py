from flask import Blueprint, render_template, request, redirect, url_for, session
import db

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    ecuser_id = session.get('ecuser_id')
    if ecuser_id is None:
        return redirect(url_for('login'))

    product_id = int(request.form['product_id'])
    quantity = int(request.form['quantity'])

    cart_id = db.get_user_cart_id(ecuser_id)
    if cart_id is None:
        cart_id = db.create_user_cart(ecuser_id)

    existing_item = db.get_cart_item(cart_id, product_id)

    if existing_item:
        db.update_cart_item(cart_id, product_id, existing_item['quantity'] + quantity)
    else:
        db.insert_cart_item(cart_id, product_id, quantity)

    return redirect(url_for('cart.show_cart'))

@cart_bp.route('/cart')
def show_cart():
    ecuser_id = session.get('ecuser_id')
    if ecuser_id is None:
        return redirect(url_for('login'))

    cart_id = db.get_user_cart_id(ecuser_id)

    if cart_id is None:
        return render_template('cart.html', cart_items=[])

    cart_items = db.get_user_cart_items(cart_id)
    return render_template('cart.html', cart_items=cart_items)

@cart_bp.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    ecuser_id = session.get('ecuser_id')
    if ecuser_id is None:
        return redirect(url_for('login'))

    cart_id = db.get_user_cart_id(ecuser_id)

    if cart_id is not None:
        db.remove_from_cart(product_id, cart_id)

    return redirect(url_for('cart.show_cart'))

@cart_bp.route('/view', methods=['GET', 'POST'])
def view_cart():
    ecuser_id = session.get('ecuser_id')
    if ecuser_id:
        cart_items = db.get_cart_items(ecuser_id)
        total_price = db.calculate_cart_total(ecuser_id)
        return render_template('cart.html', cart_items=cart_items, total_price=total_price)
    else:
        return render_template('error.html', error_message='ログインしていません。')