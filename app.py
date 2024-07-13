from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__, template_folder="templates")

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'varsha@0506',
    'database': 'train_details_db'
}

# Function to initialize the database and create tables if they don't exist
def init_db():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS train_details (
            id INT AUTO_INCREMENT PRIMARY KEY,
            train_name VARCHAR(255) NOT NULL,
            departure_city VARCHAR(255) NOT NULL,
            arrival_city VARCHAR(255) NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            train_id INT,
            compartments INT NOT NULL,
            FOREIGN KEY (train_id) REFERENCES train_details(id)
        )
    ''')
    conn.commit()
    conn.close()

# Home route to render the HTML page and display joined data
@app.route("/")
# Home route to render the HTML page and display joined data
@app.route("/")
def home():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Joining train_details and orders tables on train_id
    cursor.execute('''
        SELECT train_details.id, train_details.train_name, train_details.departure_city, train_details.arrival_city, 
               orders.compartments AS compartments
        FROM train_details 
        LEFT JOIN orders ON train_details.id = orders.train_id
    ''')
    joined_data = cursor.fetchall()
    conn.close()

    return render_template("index.html", joined_data=joined_data)


# API endpoint to handle adding multiple trains at once
@app.route("/add_trains", methods=["POST"])
# API endpoint to handle adding a new train
@app.route("/add_train", methods=["POST"])
def add_train():
    try:
        # Access form data using request.form
        train_name = request.form.get("train_name")
        departure_city = request.form.get("departure_city")
        arrival_city = request.form.get("arrival_city")

        # Insert the values into the train_details table
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO train_details (train_name, departure_city, arrival_city) VALUES (%s, %s, %s)",
                       (train_name, departure_city, arrival_city))
        conn.commit()
        conn.close()

        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# API endpoint to handle updating train details
@app.route("/update_train", methods=["POST"])
def update_train():
    try:
        train_id = request.form.get("trainId")
        train_name = request.form.get("trainName")
        departure_city = request.form.get("departureCity")
        arrival_city = request.form.get("arrivalCity")
        compartments = request.form.get("compartments")  # Add this line to get compartments from the form

        # Use a transaction to update both tables
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        try:
            # Update train_details table
            cursor.execute("UPDATE train_details SET train_name = %s, departure_city = %s, arrival_city = %s WHERE id = %s",
                           (train_name, departure_city, arrival_city, train_id))

            # Update orders table
            cursor.execute("UPDATE orders SET compartments = %s WHERE train_id = %s",
                           (compartments, train_id))

            # Commit the transaction
            conn.commit()

        except Exception as e:
            # Rollback the transaction if an error occurs
            conn.rollback()
            raise e

        finally:
            conn.close()

        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
# API endpoint to handle adding an order for a train
@app.route("/add_order", methods=["POST"])
def add_order():
    try:
        train_id = request.form.get("trainId")
        product = request.form.get("product")

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (train_id, product) VALUES (%s, %s)",
                       (train_id, product))
        conn.commit()
        conn.close()

        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
