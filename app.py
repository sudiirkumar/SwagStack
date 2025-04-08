from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '&udhir2Kum#r' 
app.config['MYSQL_DB'] = 'swagstack'

mysql = MySQL(app)

user_id_int = int()
@app.route('/login', methods=['POST'])
def login():
    username_or_email = request.json.get('username_or_email')
    password = request.json.get('password')
    if not username_or_email or not password:  # Check for missing credentials
        return jsonify({'message': 'Email/Username and password are required!'}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT name FROM users WHERE (email=%s OR username=%s) AND password=%s", (username_or_email, username_or_email, password))
    user = cur.fetchone()
    cur.execute("SELECT isAdmin FROM users WHERE (email=%s OR username=%s) AND password=%s", (username_or_email, username_or_email, password))
    isAdmin = cur.fetchone()
    cur.execute("SELECT id FROM users WHERE (email=%s OR username=%s) AND password=%s", (username_or_email, username_or_email, password))
    user_id = cur.fetchone()
    cur.execute("DELETE FROM current_session_user")
    cur.execute("INSERT INTO current_session_user(user_id) VALUES (%s)", (user_id,))
    mysql.connection.commit()
    cur.close()
    if user:
        a = jsonify({'message': 'Login successful!', 'name': user, 'is_admin': isAdmin, 'user_id': user_id})
        return a, 200
    else:
        return jsonify({'message': 'Invalid credentials!'}), 401

@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')
    name = request.json.get('name')
    username = request.json.get('username')
    security_question = request.json.get('security_question')
    security_answer = request.json.get('security_answer')
        
    if not email or not password or not name or not username or not security_question or not security_answer:
        return jsonify({'message': 'All fields are required!'}), 400
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(email,password,name,username,security_question,security_answer) VALUES(%s,%s,%s,%s,%s,%s)", (email, password, name, username, security_question, security_answer))
        print("User registered successfully!")
        mysql.connection.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except Exception as e:
        mysql.connection.rollback()
        print(e)
        return jsonify({f'message': 'Error: User could not be registered.'}), 500
    finally:
        cur.close()

@app.route('/validate', methods=['POST'])
def validate():
    username_or_email = request.json.get('username_or_email')
    security_question = request.json.get('security_question')
    security_answer = request.json.get('security_answer')
    
    if not username_or_email or not security_question or not security_answer:
        return jsonify({'message':'All fields are required!'}), 400
    cur = mysql.connection.cursor()
    cur.execute("SELECT username FROM users WHERE (email = %s OR username = %s) AND security_question = %s AND security_answer = %s",(username_or_email, username_or_email, security_question, security_answer))
    user = cur.fetchone()
    cur.close()
    if user:
        return jsonify({'message':'Account found','username':user}), 200
    else:
        return jsonify({'message': 'Invalid credentials!'}), 401
    
@app.route('/reset', methods=['POST'])
def reset():
    password = request.json.get('password')
    username = request.json.get('username')
    if not password:
        return jsonify({'message':'All fields are required!'}), 400
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET password = %s WHERE username = %s",(password, username))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message':'Password reset successfully!'}), 200

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()

        # for p in products:
        #     print(p)
        # print(str(jsonify(products)))
        
        return jsonify(products), 200

    except mysql.connector.Error as err:
        print("Database error:", err)
        return jsonify({'error': 'Database connection failed'}), 500

    finally:
        if cursor:
            cursor.close()
            
@app.route('/api/deleteProduct/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        cursor = mysql.connection.cursor()

        cursor.execute("DELETE FROM product WHERE product_id = %s", (product_id,))
        mysql.connection.commit()

        return jsonify({'message': 'Deleted successfully'}), 200

    except mysql.connector.Error as err:
        print("Database error:", err)
        return jsonify({'error': 'Database connection failed'}), 500

    finally:
        if cursor:
            cursor.close()

@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM product WHERE product_id = %s", (product_id,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            # Manually map the row to dict since flask_mysqldb doesn't support dictionary=True
            product = {
                'product_id': row[0],
                'product_name': row[1],
                'category': row[2],
                'price': row[3],
                'stock_quantity': row[4],
                'last_stock_update': str(row[5]),
                'last_modify': str(row[6])
            }
            return jsonify(product), 200
        else:
            return jsonify({'error': 'Product not found'}), 404

    except Exception as e:
        print("Error fetching product:", e)
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/updateProduct/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("""
            UPDATE product 
            SET product_name = %s, category = %s, price = %s, stock_quantity = %s, last_modify = NOW() 
            WHERE product_id = %s
        """, (data['product_name'], data['category'], data['price'], data['stock_quantity'], product_id))
        mysql.connection.commit()
        return jsonify({'message': 'Product updated successfully'})
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to update product'}), 500
    finally:
        cursor.close()

@app.route('/api/addProduct', methods=['POST'])  # ✅ Changed PUT to POST
def add_product():
    data = request.get_json()
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO product (product_name, category, price, stock_quantity, last_modify)
            VALUES (%s, %s, %s, %s, NOW())
        """, (data['product_name'], data['category'], data['price'], data['stock_quantity']))
        mysql.connection.commit()
        return jsonify({'message': 'Product added successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to add product'}), 500  # ✅ corrected error message
    finally:
        cursor.close()
        
@app.route('/api/transaction_log')
def get_transaction_log():
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM transaction_log ORDER BY timestamp DESC")
    logs = cursor.fetchall()

    cursor.close()
    return jsonify(logs)

@app.route('/api/get_users')
def get_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, email, name, isAdmin FROM users")
    rows = cur.fetchall()
    users = []
    for row in rows:
        users.append({
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "name": row[3],
            "isAdmin": bool(row[4])
        })
    return jsonify(users)

@app.route('/api/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    mysql.connection.commit()
    return jsonify({"message": "User deleted"})

@app.route('/api/toggle_admin/<int:user_id>', methods=['PUT'])
def toggle_admin(user_id):
    data = request.get_json()
    isAdmin = data.get("isAdmin", 0)
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET isAdmin = %s WHERE id = %s", (isAdmin, user_id))
    mysql.connection.commit()
    return jsonify({"message": "Admin status updated"})


@app.route('/api/create_order', methods=['POST'])
def create_order():
    data = request.get_json()
    product_id = data['product_id']
    customer_id = data['customer_id']
    quantity = int(data['quantity'])

    cursor = mysql.connection.cursor()

    try:
        # Step 1: Get current logged-in user_id from current_user table
        cursor.execute("SELECT user_id FROM current_session_user LIMIT 1")
        user = cursor.fetchone()
        if not user:
            return jsonify({'error': 'No active user session'}), 403
        user_id = user[0]

        # Step 2: Get price and stock for product
        cursor.execute("SELECT price, stock_quantity FROM product WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        price, available_stock = product
        if quantity > available_stock:
            return jsonify({'error': 'Not enough stock available'}), 400

        total_amount = quantity * price

        # Step 3: Insert into sales_order
        cursor.execute("""
            INSERT INTO sales_order (customer_id, user_id, total_amount)
            VALUES (%s, %s, %s)
        """, (customer_id, user_id, total_amount))
        order_id = cursor.lastrowid

        # Step 4: Insert into order_item
        cursor.execute("""
            INSERT INTO order_item (order_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, (order_id, product_id, quantity, price))

        # Step 5: Update product stock
        cursor.execute("""
            UPDATE product
            SET stock_quantity = stock_quantity - %s
            WHERE product_id = %s
        """, (quantity, product_id))

        # Step 6: Commit transaction
        mysql.connection.commit()
        return jsonify({'msg': 'Order created successfully'}), 201

    except Exception as e:
        mysql.connection.rollback()
        print("Order creation failed:", str(e))
        return jsonify({'error': 'Failed to create order'}), 500

    finally:
        cursor.close()

@app.route('/api/get_orders', methods=['GET'])
def get_orders():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM sales_order ORDER BY order_date DESC")
    orders = cursor.fetchall()
    cursor.close()
    return jsonify(orders)

@app.route('/api/toggle_order_status', methods=['POST'])
def toggle_status():
    data = request.json
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE sales_order SET is_completed = %s WHERE order_id = %s", (data['is_completed'], data['order_id']))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'msg': 'Status updated'})
if __name__ == '__main__':
    app.run(debug=True)