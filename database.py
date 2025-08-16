import psycopg2
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.create_table()
    
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS nota_dinas (
            id SERIAL PRIMARY KEY,
            tanggal DATE,
            pengirim VARCHAR(100),
            tempat VARCHAR(100),
            petugas VARCHAR(100)
        );
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            self.conn.commit()
    
    def insert_data(self, data):
        query = """
        INSERT INTO nota_dinas (tanggal, pengirim, tempat, petugas)
        VALUES (%s, %s, %s, %s)
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query, (
                data["tanggal"],
                data["pengirim"],
                data["tempat"],
                data["petugas"]
            ))
            self.conn.commit()
    
    def get_all_data(self):
        query = "SELECT id, tanggal, pengirim, tempat, petugas FROM nota_dinas"
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    
    def delete_data(self, id):
        query = "DELETE FROM nota_dinas WHERE id = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (id,))
            self.conn.commit()