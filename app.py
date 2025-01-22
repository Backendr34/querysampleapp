from flask import Flask, request, render_template
import sqlite3
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Initialize the database
def init_db():
    conn = sqlite3.connect('queries.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS queries (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        query TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

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
        conn = sqlite3.connect('queries.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO queries (name, email, phone, query)
        VALUES (?, ?, ?, ?)
        ''', (name, email, phone, query))
        conn.commit()
    except Exception as e:
        logging.error("Error occurred: %s", e)
        return "An error occurred while submitting your query.", 500
    finally:
        conn.close()

    return 'Query submitted successfully!'

if __name__ == '__main__':
    init_db()
    

   
