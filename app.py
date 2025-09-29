import os
import psycopg2
import numpy as np
from pgvector.psycopg2 import register_vector
from PIL import Image
from sentence_transformers import SentenceTransformer
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)


DB_NAME = "VectorSearch"
DB_USER = "postgres"
DB_PASSWORD = "DB_PASSWORD"  
DB_HOST = "localhost"
DB_PORT = "5432"


print("Loading CLIP model...")
model = SentenceTransformer('clip-ViT-B-32')
print("Model loaded.")


def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    register_vector(conn)
    return conn


@app.route('/api/search', methods=['POST'])
def search():
    try:
        query_embedding = None
        
        
        image_file = request.files.get('image_query')
        text_query = request.form.get('text_query')

        
        if image_file and image_file.filename:
            print(f"Performing image search for file: '{image_file.filename}'")
            img = Image.open(image_file.stream)
            query_embedding = model.encode(img)
            
        
        elif text_query:
            print(f"Performing text search for: '{text_query}'")
            query_embedding = model.encode(text_query)
            
        else:
            return jsonify({'error': 'No query provided. Please enter text or upload an image.'}), 400

        
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT filename FROM images ORDER BY embedding <=> %s LIMIT 12",
            (query_embedding,)
        )
        results = cur.fetchall()
        
        cur.close()
        conn.close()

        filenames = [row[0] for row in results]
        
        return jsonify({'results': filenames})

    except Exception as e:
        print(f"An error occurred during search: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500


@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    
    app.run(debug=True)