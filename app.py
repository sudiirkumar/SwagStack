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
    cur.close()
    if user:
        a = jsonify({'message': 'Login successful!', 'name': user, 'is_admin': isAdmin})
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
if __name__ == '__main__':
    app.run(debug=True)