from flask import Blueprint, render_template, request, redirect, url_for, session
import db

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/product/<int:product_id>')
def product(product_id):
    product = db.get_product_by_id(product_id)
    return render_template('item.html', product=product)

@cart_bp.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        try:
            product_id = int(request.form['product_id'])
        except (KeyError, ValueError):
            product_id = 0
        add_to_cart(product_id)
        return redirect(url_for('cart.cart'))

    cart_items = session.get('cart_items', [])
    cart_products = [db.get_product_by_id(int(product_id)) for product_id in cart_items]
    total_price = calculate_total_price(cart_products)
    return render_template('cart.html', products=cart_products, total_price=total_price)

@cart_bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form['product_id']
    cart_items = session.get('cart_items', [])

    cart_items = [item for item in cart_items if item != product_id]

    session['cart_items'] = cart_items
    return redirect(url_for('cart.cart'))

def calculate_total_price(products):
    total_price = 0
    for product in products:
        total_price += product[2]
    return total_price

def add_to_cart(product_id):
    product = db.get_product_by_id(product_id)
    if product is None:
        return redirect(url_for('cart.cart'))

    session.permanent = True
    if 'cart_items' not in session:
        session['cart_items'] = []
    cart_list = session['cart_items']
    cart_list.append(str(product[0]))
    session['cart_items'] = cart_list
    return redirect("/")