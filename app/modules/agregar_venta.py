from flask import render_template, request, flash, redirect, jsonify
import json
import db_config

def get_productos():
    conn = db_config.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, precio, stock FROM productos WHERE activo = 1")
    prods = cursor.fetchall()
    conn.close()
    return prods

def register_routes(app):
    @app.route('/agregar-venta', methods=['GET', 'POST'])
    def agregar_venta():
        if request.method == 'POST':
            try:
                producto_id = int(request.form['producto'])
                cantidad = float(request.form['cantidad'])
                unidad_medida = request.form['unidad_medida']

                conn = db_config.get_db_connection()
                cursor = conn.cursor()

                cursor.execute("SELECT nombre, precio, stock FROM productos WHERE id = ?", (producto_id,))
                producto = cursor.fetchone()
                
                if not producto:
                    conn.close()
                    flash("Producto no encontrado.", 'error')
                    return redirect('/agregar-venta')

                precio_unitario = producto[1]
                stock_actual = producto[2]

                if unidad_medida == 'gramo':
                    cantidad = cantidad / 1000
                elif unidad_medida == 'unidad':
                    # No es necesario realizar conversiones para unidades
                    pass

                precio_total = precio_unitario * cantidad

                if cantidad > stock_actual:
                    conn.close()
                    flash("No hay suficiente stock disponible para el producto seleccionado.", 'error')
                    return redirect('/agregar-venta')

                if cantidad <= 0:
                    conn.close()
                    flash("Seleccione una cantidad válida.", 'error')
                    return redirect('/agregar-venta')

                # Note: This logic only inserts into DB but doesn't seem to persist a "basket" unless client side handles it.
                # The original code inserted a new 'ventas' record with 0 total for EVERY item added?
                # That creates a new Order # for every item?
                # "INSERT INTO ventas (fecha, total) VALUES (NOW(), 0)"
                # Yes, original code seems to create a new sale per item addition in the form POST (maybe unused flow if JS handles it?).
                # Let's preserve original logic.

                cursor.execute("INSERT INTO ventas (fecha, total) VALUES (CURRENT_TIMESTAMP, 0)")
                venta_id = cursor.lastrowid

                cursor.execute("INSERT INTO ventas_productos (venta_id, producto_id, cantidad, precio_total) VALUES (?, ?, ?, ?)",
                            (venta_id, producto_id, cantidad, precio_total))
                conn.commit()

                cursor.execute("UPDATE productos SET stock = stock - ? WHERE id = ?", (cantidad, producto_id))
                conn.commit()
                conn.close()

                flash("Producto agregado a la venta.", 'success')
                return redirect('/agregar-venta')
            except Exception as e:
                flash(f"Error: {e}", 'error')
                return redirect('/agregar-venta')

        productos = get_productos()
        return render_template('agregar_venta.html', productos=productos)
    
    
    @app.route('/guardar-venta', methods=['POST'])
    def guardar_venta():
        conn = None
        try:
            conn = db_config.get_db_connection()
            cursor = conn.cursor()
            
            productos_agregados = json.loads(request.data)
            total_venta = sum(producto['cantidad'] * producto['precio_unitario'] for producto in productos_agregados)

            cursor.execute("INSERT INTO ventas (fecha, total) VALUES (CURRENT_TIMESTAMP, ?)", (total_venta,))
            venta_id = cursor.lastrowid

            for producto in productos_agregados:
                producto_id = producto['producto_id']
                cantidad = producto['cantidad']
                precio_unitario = producto['precio_unitario']

                cursor.execute("INSERT INTO ventas_productos (venta_id, producto_id, cantidad, precio_total) VALUES (?, ?, ?, ?)",
                            (venta_id, producto_id, cantidad, cantidad * precio_unitario))
                
                cursor.execute("UPDATE productos SET stock = stock - ? WHERE id = ?", (cantidad, producto_id))
            
            conn.commit()
            return jsonify({"success": True})
        except Exception as e:
            if conn:
                conn.rollback()
            print("Error al guardar la venta:", str(e))
            return jsonify({"success": False})
        finally:
            if conn:
                conn.close()
