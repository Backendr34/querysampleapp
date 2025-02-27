from flask import Flask, request, render_template
import psycopg2
import logging
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize the database
def init_db():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),  # This should be the host where your database is deployed
            port=os.getenv('DB_PORT', '5432')  # Default PostgreSQL port
        )
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            query TEXT NOT NULL
        )''')
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error("Error initializing database: %s", e)

# Route for the query form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the form submission
@app.route('/submit_query', methods=['POST'])
def submit_query():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    query = request.form['query']

    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),  # This should be the host where your database is deployed
            port=os.getenv('DB_PORT', '5432')  # Default PostgreSQL port
        )
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO queries (name, email, phone, query)
        VALUES (%s, %s, %s, %s)
        ''', (name, email, phone, query))
        conn.commit()
        cursor.close()
    except Exception as e:
        logging.error("Error occurred while submitting query from %s: %s", email, e, exc_info=True)
        return "An error occurred while submitting your query.", 500
    finally:
        conn.close()

    return 'Query submitted successfully!'

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
