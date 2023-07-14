from flask import Blueprint, render_template, request, redirect, url_for
import db

product_bp = Blueprint('product', __name__, url_prefix='/product')

@product_bp.route('/list')
def show_products():
    product_list = db.show_products()
    return render_template('products.html', products=product_list)

@product_bp.route('/products')
def show_item():
    product_item = db.show_item()
    return render_template('item.html', productes=product_item)

@product_bp.route('/develop')
def product_develop():
    return render_template('develop.html')

@product_bp.route('/develop_exe', methods=['POST'])
def develop_exe():
    name = request.form.get('name')
    types = request.form.get('types')
    price = request.form.get('price')
    stock = request.form.get('stock')
    comments = request.form.get('comments')
    size = request.form.get('size')
    
    db.insert_product(name, types, price, stock, comments, size)
    
    product_list = db.show_products()
    product_item = db.show_item()
    return render_template('products.html', products=product_list, productes=product_item)
