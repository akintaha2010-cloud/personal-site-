from flask import Flask, jsonify, redirect, render_template, request, url_for
import sqlite3
app = Flask(__name__)
DB_PATH = "lost_found.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            location TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
def get_items():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()
    return items
def add_user(item_name, location):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
    'INSERT INTO items (name, location) VALUES (?, ?)',
    (item_name, location)
)
    conn.commit()
    conn.close()
def uptade_user(item_id, item_name, location):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
    'UPDATE items SET name = ?, location = ? WHERE id = ?',
    (item_name, location, item_id)
)
    conn.commit()
    conn.close()
def delete_item(item_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'DELETE FROM items WHERE id = ?',
        (item_id,)
    )
    conn.commit()
    conn.close()
@app.route('/users', methods=['GET'])
def list_items():
    items = get_items()
    return jsonify(items)
@app.route('/')
def  index():
    items = get_items()
    return render_template('index.html', items=items)
@app.route('/add_user', methods=['POST'])
def add_user_route():
    item_name = request.form['item_name']
    location = request.form['location']
    add_user(item_name, location)
    return redirect(url_for('index'))
@app.route('/update_user/<int:user_id>', methods=['GET','POST'])
def update_user_route(user_id):
    if request.method == 'POST':
        item_name = request.form['item_name']
        location = request.form['location']
        uptade_user(user_id, item_name, location)
        return redirect(url_for('index'))
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM items WHERE id = ?',
        (user_id,)
    )

    item = cursor.fetchone()
    conn.close()
    return render_template(
        'update_user.html',
        item=item
    )
@app.route('/delete_user/<int:id>',methods=['GET'])
def delete_user_route(id):
    delete_item(id)
    return redirect(url_for('index'))
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
if __name__ == '__main__':
    import threading
    import webview
    init_db()
    def run_flask():
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=False,
            use_reloader=False,
        )
flask_thread = threading.Thread(
    target=run_flask,
    daemon=True
)
flask_thread.start()
webview.create_window(
    'FoundDesk'
    'http://127.0.0.1:5000',
    width=1000,
    height=700
)
webview.start()