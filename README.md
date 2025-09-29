# VectorSearchDB

This project is a content-based image search engine built with Python, Flask, and PostgreSQL. It uses the pgvector extension to perform efficient, vector-based similarity searches. The application allows users to find images by submitting either a text description or by uploading a visually similar image.

Core Features

⚫ **Text-to-Image Search:** Find images based on a descriptive text query, like "a red car on a street".

⚫ **Image-to-Image Search:** Find images that are visually similar to an image uploaded by the user.

⚫ **Vector-Based:** The search is powered by AI-generated vector embeddings from a pre-trained CLIP model, enabling a deep, semantic understanding of image content.

## Technology Stack

⚫ **Backend:** Python, Flask

⚫ **Database:** PostgreSQL with the pgvector extension

⚫ **AI Model:** sentence-transformers (CLIP ViT-B-32)

⚫ **Frontend:** HTML, CSS, JavaScript

## Setup and Installation

Here's how to get the project running locally.

1.  **Clone the Repository**
    ```bash
    git clone <your-repository-url>
    cd VectorSearchDB
    ```

2.  **Set Up Environment**
    This project uses Conda for environment management. Make sure you have Anaconda or Miniconda installed. The required packages can be installed via `pip`.
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: To generate the requirements.txt file, run `pip freeze > requirements.txt` in your activated environment).*

3.  **Set Up PostgreSQL**
    ⚫ Make sure you have PostgreSQL (version 16 is recommended) installed.
    ⚫ Install the `pgvector` extension by copying the extension files into your PostgreSQL directory.
    ⚫ Create a new database, for example, named `VectorSearch`.

4.  **Configure Scripts**
    ⚫ In both `ingest.py` and `app.py`, update the `DB_PASSWORD` variable with your own PostgreSQL password.
    ⚫ In `ingest.py`, make sure the `IMAGE_FOLDER` variable points to the location of your chosen dataset (e.g., the Caltech-101 folder).

## How to Run

1.  **Populate the Database**
    Run the ingestion script. This will process your images, generate embeddings, populate the database, and copy the renamed images to the `static/images` folder.
    ```bash
    python ingest.py
    ```

2.  **Start the Backend Server**
    Run the Flask application to start the web server.
    ```bash
    python app.py
    ```

3.  **Use the Application**
    Open your web browser and go to `http://127.0.0.1:5000` to use the search engine.