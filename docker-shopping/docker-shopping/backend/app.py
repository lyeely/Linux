from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)
CORS(app)

# 数据库连接
def get_db():
    return psycopg2.connect(os.environ['DATABASE_URL'])

# 获取商品列表
@app.route('/api/products')
def get_products():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(products)

# 简易推荐（MCP风格）：根据商品ID推荐同品类
@app.route('/api/recommend/<int:product_id>')
def recommend(product_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # 获取当前商品名称
    cur.execute("SELECT name FROM products WHERE id = %s", (product_id,))
    current = cur.fetchone()
    
    # 推荐其他商品（简单规则：ID不同就行，模拟"看了还看"）
    cur.execute("SELECT * FROM products WHERE id != %s LIMIT 3", (product_id,))
    recs = cur.fetchall()
    
    cur.close()
    conn.close()
    return jsonify({
        'current': current['name'] if current else '',
        'recommendations': recs
    })

# 热门推荐（MCP风格）：销量/随机推荐
@app.route('/api/hot')
def hot():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM products ORDER BY RANDOM() LIMIT 3")
    recs = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(recs)

# 模拟购物车（用内存存储，简单演示）
cart = []

@app.route('/api/cart', methods=['GET', 'POST', 'DELETE'])
def handle_cart():
    global cart
    if request.method == 'GET':
        return jsonify(cart)
    
    if request.method == 'POST':
        item = request.json
        cart.append(item)
        return jsonify({'success': True})
    
    if request.method == 'DELETE':
        cart = []
        return jsonify({'success': True})

if __name__ == '__main__':
    # 初始化数据库
    from init_db import init_db
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)