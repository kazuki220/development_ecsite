from flask import Blueprint, render_template, request, redirect, url_for
import db

product_bp = Blueprint('product', __name__, url_prefix='/product')

@product_bp.route('/products')
def show_product():
    return render_template('products.html')

@product_bp.route('/register')
def develop_register():
    return render_template('register.html')

@product_bp.route('/register_exe', methods=['POST'])
def register_exe():
    name = request.form.get('name')
    types = request.form.get('types')
    price = request.form.get('price')
    stock = request.form.get('stock')
    comments = request.form.get('comments')
    size = request.form.get('size')
    
    db.insert_product(name, types, price, stock, comments, size)
    
    return redirect(url_for('product_bp.product_list'))

@product_bp.route('/list', methods=['GET'])
def product_list():
    product_list = db.show_product()
    return render_template('product.html', products=product_list)