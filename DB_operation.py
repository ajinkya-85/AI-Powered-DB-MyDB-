import sqlite3
from typing import List, Union

class DBOperation:
    def __init__(self, db_name: str = 'MyDB.db'):
        self.db_name = db_name

    def execute_query(self, query: str) -> Union[tuple, str]:
        """
        Executes a SQL query and returns results or confirmation message
        """
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                
                if query.lower().strip().startswith('select'):
                    # For SELECT queries, return the results
                    results = cursor.fetchall()
                    columns = [description[0] for description in cursor.description]
                    return columns, results
                else:
                    # For other queries (INSERT, UPDATE, DELETE), commit and return message
                    conn.commit()
                    return "Query executed successfully"
                    
        except sqlite3.Error as e:
            return f"Database error: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"
    def get_table_columns(self, table_name: str) -> list:
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [info[1] for info in cursor.fetchall()]
                return columns
        except sqlite3.Error as e:
            raise Exception(f"Error getting table columns: {str(e)}")

    def get_table_data(self, table_name: str) -> tuple:
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                # Get columns first
                columns = self.get_table_columns(table_name)
                # Get data
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                return columns, rows
        except sqlite3.Error as e:
            raise Exception(f"Error getting table data: {str(e)}")

    def get_all_tables(self) -> List[str]:
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
                tables = [row[0] for row in cursor.fetchall()]
                return tables
        except sqlite3.Error as e:
            raise Exception(f"Error getting tables: {str(e)}")