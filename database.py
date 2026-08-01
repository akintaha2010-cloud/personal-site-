import sqlite3

DB_PATH = "lost_found.db"

#Functions for database managing
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            report_type TEXT NOT NULL DEFAULT 'Lost',
            user_id INTEGER,
            category TEXT,
            description TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("PRAGMA table_info(items)")
    columns = cursor.fetchall()

    column_names = []

    for column in columns:
        column_names.append(column[1])

    if "user_id" not in column_names:
        cursor.execute("""
            ALTER TABLE items
            ADD COLUMN user_id INTEGER
        """)

    if "category" not in column_names:
        cursor.execute("""
            ALTER TABLE items
            ADD COLUMN category TEXT
        """)

    if "description" not in column_names:
        cursor.execute("""
            ALTER TABLE items
            ADD COLUMN description TEXT
        """)

    if "created_at" not in column_names:
        cursor.execute("""
            ALTER TABLE items
            ADD COLUMN created_at TEXT
        """)

        cursor.execute("""
            UPDATE items
            SET created_at = datetime('now', 'localtime')
            WHERE created_at IS NULL
        """)

    conn.commit()
    conn.close()


def get_items():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            items.id,
            items.report_type,
            items.name,
            items.location,
            items.category,
            items.description,
            users.full_name,
            items.user_id,
            items.created_at
        FROM items
        LEFT JOIN users
            ON items.user_id = users.id
        ORDER BY items.id DESC
    """)

    items = cursor.fetchall()

    conn.close()
    return items


def get_items_by_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            items.id,
            items.report_type,
            items.name,
            items.location,
            items.category,
            items.description,
            users.full_name,
            items.user_id,
            items.created_at
        FROM items
        LEFT JOIN users
            ON items.user_id = users.id
        WHERE items.user_id = ?
        ORDER BY items.id DESC
    """, (user_id,))

    items = cursor.fetchall()

    conn.close()
    return items


def add_item( report_type, item_name, location, category, description, user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO items (
            report_type,
            name,
            location,
            category,
            description,
            user_id,
            created_at
        )
        VALUES (
            ?, ?, ?, ?, ?, ?,
            datetime('now', 'localtime')
        )
    """, (
        report_type,
        item_name,
        location,
        category,
        description,
        user_id
    ))

    conn.commit()
    conn.close()


def delete_item(item_id, user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM items
        WHERE id = ? AND user_id = ?
    """, (
        item_id,
        user_id
    ))

    deleted_count = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted_count


def add_user(full_name, email, hashed_password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (
            full_name,
            email,
            password
        )
        VALUES (?, ?, ?)
    """, (
        full_name,
        email,
        hashed_password
    ))

    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            full_name,
            email,
            password
        FROM users
        WHERE LOWER(email) = LOWER(?)
    """, (email,))

    user = cursor.fetchone()

    conn.close()
    return user