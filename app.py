from flask import Flask, request, render_template
from pymongo import MongoClient
import logging
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize the database
def init_db():
    try:
        client = MongoClient(os.getenv('MONGODB_URI'))
        db = client[os.getenv('DB_NAME')]
        db.queries.create_index('email', unique=True)
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
        client = MongoClient(os.getenv('MONGODB_URI'))
        db = client[os.getenv('DB_NAME')]
        db.queries.insert_one({
            'name': name,
            'email': email,
            'phone': phone,
            'query': query
        })
    except Exception as e:
        logging.error("Error occurred while submitting query from %s: %s", email, e, exc_info=True)
        return "An error occurred while submitting your query.", 500

    return 'Query submitted successfully!'

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
