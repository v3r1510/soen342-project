import sqlite3
import os

class Database:
    
    DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'Soen_342_initialized.db')
    
    @staticmethod
    def get_connection():
        """Get a database connection with foreign keys enabled"""
        conn = sqlite3.connect(Database.DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    
    @staticmethod
    def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            else:
                result = None
            
            conn.commit()
            return result
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    
    @staticmethod
    def execute_many(query, params_list):
        
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.executemany(query, params_list)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
