from flask import Blueprint, render_template, session
import db

orders_bp = Blueprint('order', __name__, url_prefix='/order')

@orders_bp.route('/history')
def orders():
    ecuser_id = session.get('ecuser_id')
    orders = get_orders(ecuser_id)
    return render_template('orders.html', orders=orders)

def get_orders(total_price, ecuser_id):
    # データベースから特定のユーザーの注文履歴を取得する処理に置き換える
    orders = db.get_order(total_price, ecuser_id)
    return orders