from flask import Blueprint, render_template, request, redirect, url_for, session
import db

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_name = request.form.get('product_name')
    quantity = int(request.form.get('quantity'))

    product = db.get_product_name(product_name)

    if product:
        if 'cart_items' not in session:
            session['cart_items'] = []

        cart_item = {
            'product_name': product[0],
            'quantity': quantity,
            'price': product[2]
        }
        session['cart_items'].append(cart_item)
        return redirect(url_for('product.product', product_id=product[0]))
    else:
        return render_template('error.html', error_message='ログインしていません。')

@cart_bp.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart_items = session.get('cart_items', [])

    for item in cart_items:
        if item['product_id'] == product_id:
            cart_items.remove(item)
            break

    session['cart_items'] = cart_items

    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/view', methods=['GET', 'POST'])
def view_cart():
    ecuser_id = session.get('user_id')
    if ecuser_id:
        cart_items = db.get_cart_items(ecuser_id)
        total_price = db.calculate_cart_total(ecuser_id)
        return render_template('cart.html', cart_items=cart_items, total_price=total_price)
    else:
        return render_template('error.html', error_message='ログインしていません。')