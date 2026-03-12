from database.connection import get_connection

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY(role_id) REFERENCES roles(id)
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    address TEXT
);

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    manufacturer TEXT, 
    category_id INTEGER,
    prescription_required INTEGER NOT NULL DEFAULT 0,
    retail_price REAL NOT NULL,
    FOREIGN KEY(category_id) REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_id INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL,
    batch_number TEXT NOT NULL,
    manufacture_date TEXT NOT NULL,
    expiration_date TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity >= 0),
    purchase_price REAL NOT NULL CHECK(purchase_price >= 0),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY(medicine_id) REFERENCES medicines(id),
    FOREIGN KEY(supplier_id) REFERENCES suppliers(id),
    UNIQUE(medicine_id, batch_number)
);

CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    customer_id INTEGER,
    sale_date TEXT NOT NULL DEFAULT (datetime('now')),
    total_amount REAL NOT NULL DEFAULT 0 CHECK(total_amount >= 0),
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(customer_id) REFERENCES customers(id)
);

CREATE TABLE IF NOT EXISTS sale_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER NOT NULL,
    batch_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    price REAL NOT NULL CHECK(price >= 0),
    FOREIGN KEY(sale_id) REFERENCES sales(id) ON DELETE CASCADE,
    FOREIGN KEY(batch_id) REFERENCES batches(id)
);

CREATE INDEX IF NOT EXISTS idx_batches_medicine_exp
    ON batches(medicine_id, expiration_date);

CREATE INDEX IF NOT EXISTS idx_sale_items_sale
    ON sale_items(sale_id);

CREATE INDEX IF NOT EXISTS idx_sales_user_date
    ON sales(user_id, sale_date);
"""

SEED_SQL = """
INSERT OR IGNORE INTO roles(name) VALUES ('admin');
INSERT OR IGNORE INTO roles(name) VALUES ('pharmacist');

-- тестовий користувач (поки без хешування, зробимо пізніше в auth_service)
INSERT OR IGNORE INTO users(username, password_hash, role_id)
VALUES ('admin', 'admin', (SELECT id FROM roles WHERE name='admin'));
"""

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.executescript(SCHEMA_SQL)
    cur.executescript(SEED_SQL)
    conn.commit()
    conn.close()