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

@product_bp.route('/delete', methods=['GET', 'POST'])
def delete_product():
    if request.method == 'POST':
        name = request.form.get('name')
        product = db.get_product_by_name(name)
        if product:
            db.delete_product(name)
            return redirect(url_for('product.show_products'))
        else:
            error_message = "商品が見つかりませんでした。"
            return render_template('delete.html', error_message=error_message)

    return render_template('delete.html')

@product_bp.route('/search', methods=['GET', 'POST'])
def search_results():
    if request.method == 'POST':
        pass
    else:
        query = request.args.get('query', '').strip()
        if query:
            search_results = db.search_products(query)
            return render_template('search_results.html', results=search_results, query=query)
        else:
            return render_template('search.html')
        
@product_bp.route('/product/<int:product_id>')
def product(product_id):
    product = db.get_product_by_id(product_id)
    return render_template('item.html', product=product)  
