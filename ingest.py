import os
import psycopg2
import shutil
import numpy as np
from pgvector.psycopg2 import register_vector
from PIL import Image
from sentence_transformers import SentenceTransformer


DB_NAME = "VectorSearch"  
DB_USER = "postgres"
DB_PASSWORD = "DB_PASSWORD"  
DB_HOST = "localhost"
DB_PORT = "5432"


IMAGE_FOLDER = 'C:/Users/Abhinav Gusain/Downloads/101_ObjectCategories/101_ObjectCategories' 

STATIC_IMAGE_FOLDER = 'C:/Users/Abhinav Gusain/Documents/VectorSearchDB/static/images'
os.makedirs(STATIC_IMAGE_FOLDER, exist_ok=True)


print("Loading CLIP model...")

model = SentenceTransformer('clip-ViT-B-32')
print("Model loaded.")



conn = None
cur = None 
try:
    print("Connecting to the database...")
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    register_vector(conn)
    print("Database connection successful.")

    
    print(f"--- STARTING INGESTION ---") 
    print(f"Reading images from SOURCE folder: {IMAGE_FOLDER}") 
    print(f"Copying images to DESTINATION folder: {STATIC_IMAGE_FOLDER}") 

    category_folders = [d for d in os.listdir(IMAGE_FOLDER) if os.path.isdir(os.path.join(IMAGE_FOLDER, d))]
    print(f"Found {len(category_folders)} category folders.") 

    if len(category_folders) == 0:
        print("!!! WARNING: No category folders found in the source directory. Make sure IMAGE_FOLDER is correct.") 

    for category_name in category_folders:
        category_path = os.path.join(IMAGE_FOLDER, category_name)
        image_files = [f for f in os.listdir(category_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

        for filename in image_files:
            new_filename = f"{category_name}_{filename}"
            original_image_path = os.path.join(category_path, filename)
            destination_image_path = os.path.join(STATIC_IMAGE_FOLDER, new_filename)

            
            print(f"COPYING FROM: {original_image_path}") 
            print(f"COPYING TO:   {destination_image_path}")

            try:
                
                img = Image.open(original_image_path)

                
                embedding = model.encode(img)

                
                cur.execute(
                    "INSERT INTO images (filename, embedding) VALUES (%s, %s) ON CONFLICT (filename) DO NOTHING",
                    (new_filename, embedding)
                )

                
                shutil.copy2(original_image_path, destination_image_path)

            except Exception as e:
                print(f"!!! ERROR processing {filename}: {e}") 

    
    conn.commit()
    print("--- INGESTION COMPLETE ---") 

except Exception as e:
    
    print(f"A critical error occurred: {e}")

finally:
    
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
    print("Database connection closed.")