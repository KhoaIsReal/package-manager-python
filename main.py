from fastapi import FastAPI, UploadFile, File
import os
import shutil
import mysql.connector

app = FastAPI()

def connect_to_database(host, user, password, database):
    """Establish a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            print("Connection to MySQL database was successful.")
            return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def close_connection(connection):
    """Close the database connection."""
    if connection and connection.is_connected():
        connection.close()
        print("MySQL connection is closed.")

def insert_data(connection, id, _description, file_name):
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO file_information(id, _description, file_name) VALUES (%s, %s, %s)",
        (id, _description, file_name)
    )
    connection.commit()
    cursor.close()

connection = connect_to_database(
    host="host.docker.internal",
    user="root",
    password="your_password",
    database="pm_db"
)

@app.get("/")
async def root():
    return {"message": "hello world!"}

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload(file: UploadFile = File(...), _description: str = "", id: int = 0):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Ghi vào database
    insert_data(connection, id, _description, file.filename)

    return {
        "filename": file.filename,
        "_description": _description,
        "id": id
    }

@app.on_event("shutdown")
def shutdown_event():
    close_connection(connection)
