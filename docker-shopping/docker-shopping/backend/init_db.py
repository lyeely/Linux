import psycopg2
import time

def init_db():
    # 等待数据库启动
    for i in range(10):
        try:
            conn = psycopg2.connect(
                host='db',
                database='shop',
                user='shop_user',
                password='123456'
            )
            break
        except:
            print(f"等待数据库... {i+1}/10")
            time.sleep(2)
    
    cur = conn.cursor()
    
    # 创建商品表
    cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name TEXT,
            price INTEGER,
            image TEXT
        )
    ''')
    
    # 插入示例数据
    cur.execute("SELECT COUNT(*) FROM products")
    if cur.fetchone()[0] == 0:
        products = [
            ("机械键盘", 299, "https://picsum.photos/id/0/200/200"),
            ("无线鼠标", 89, "https://picsum.photos/id/20/200/200"),
            ("电竞耳机", 399, "https://picsum.photos/id/1/200/200"),
            ("显示器", 1899, "https://picsum.photos/id/26/200/200"),
        ]
        for p in products:
            cur.execute("INSERT INTO products (name, price, image) VALUES (%s, %s, %s)", p)
    
    conn.commit()
    cur.close()
    conn.close()
    print("数据库初始化完成！")

if __name__ == '__main__':
    init_db()