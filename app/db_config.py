import sqlite3
import bcrypt
import os

DB_NAME = 'spv_dybj.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DB_NAME):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create Tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_usuario TEXT NOT NULL,
                contrasena TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                activo BOOLEAN DEFAULT 1
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                marca TEXT,
                precio REAL,
                stock REAL,
                categoria INTEGER,
                caducidad DATE,
                activo BOOLEAN DEFAULT 1,
                FOREIGN KEY (categoria) REFERENCES categorias (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                total REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas_productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venta_id INTEGER,
                producto_id INTEGER,
                cantidad REAL,
                precio_total REAL,
                FOREIGN KEY (venta_id) REFERENCES ventas (id),
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        ''')
        
        print("Tables created successfully.")
        
        # Seed Fake Data
        seed_data(cursor)
        
        conn.commit()
        conn.close()
        print("Database initialized and seeded.")

def seed_data(cursor):
    # Default User
    password = b"admin"
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    cursor.execute("INSERT INTO usuario (nombre_usuario, contrasena) VALUES (?, ?)", ('admin', hashed))
    
    # Categories
    categorias = ['Bebidas', 'Frituras', 'Galletas', 'Dulces', 'Lácteos']
    for cat in categorias:
        cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (cat,))
    
    # Products
    productos = [
        ('Coca Cola 600ml', 'Coca Cola', 18.00, 50, 1, '2025-12-31'),
        ('Pepsi 600ml', 'Pepsi', 17.00, 45, 1, '2025-12-31'),
        ('Doritos Nacho', 'Sabritas', 15.00, 30, 2, '2026-01-15'),
        ('Ruffles Queso', 'Sabritas', 16.00, 25, 2, '2026-01-20'),
        ('Emperador Chocolate', 'Gamesa', 14.00, 40, 3, '2025-11-20'),
        ('Oreo 10pz', 'Nabisco', 12.00, 60, 3, '2025-10-10'),
    ]
    
    for prod in productos:
        cursor.execute("INSERT INTO productos (nombre, marca, precio, stock, categoria, caducidad) VALUES (?, ?, ?, ?, ?, ?)", prod)

    print("Fake data inserted.")
