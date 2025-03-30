from flask import Flask, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)

# Database connection
def connect_db():
    conn = sqlite3.connect('handbag_auctions.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return "Welcome to the Luxury Handbag Auction Analysis!"

# API Endpoint to fetch distinct brands
@app.route('/brands', methods=['GET'])
def get_brands():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT Brand FROM auction_data")
    brands = [row['Brand'] for row in cursor.fetchall()]
    conn.close()
    return jsonify(brands)

# Prevent running in interactive environments like Jupyter
if __name__ == '__main__':
    try:
        print("Starting Flask on port 5001...")
        app.run(debug=True, port=5001)
    except Exception as e:
        print(f"Error starting Flask: {e}")