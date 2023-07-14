from flask import Blueprint, render_template, request, redirect, url_for, session
import db

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/product/<int:product_id>')
def product(product_id):
    product = get_product_by_id(product_id)
    return render_template('item.html', product=product)

@cart_bp.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        product = get_product_by_id(product_id)
        add_to_cart(product)
        return redirect(url_for('cart.cart'))

    cart_items = session.get('cart', [])
    cart_products = [get_product_by_id(product_id) for product_id in cart_items]
    return render_template('cart.html', products=cart_products)

def get_product_by_id(product_id):
    for product in db.show_item():
        if product['id'] == product_id:
            return product
    return None

def add_to_cart(product):
    cart = session.get('cart', [])
    cart.append(product['id'])
    session['cart'] = cart