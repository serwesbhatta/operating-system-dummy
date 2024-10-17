import sqlite3
from prettytable import PrettyTable
from .operations import *

class SqliteCRUD:
    """A class to perform CRUD operations on a SQLite database."""

    def __init__(self, db_path):
        """Initialize the database connection and cursor."""
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        create_table(self.cursor, table_name, columns)

    def drop_table(self, table_name):
        drop_table(self.cursor, self.conn, table_name)

    def show_tables(self, raw=True):
        return show_tables(self.cursor, raw)

    def describe_table(self, table_name, raw=False):
        return describe_table(self.cursor, table_name, raw)

    def insert_data(self, table_name, data):
        insert_data(self.cursor, self.conn, table_name, data)

    def read_data(self, table_name, filters=None):
        return read_data(self.cursor, table_name, filters)

    def update_data(self, table_name, column, new_value, condition_column, condition_value):
        return update_data(self.cursor, self.conn, table_name, column, new_value, condition_column, condition_value)

    def delete_data(self, table_name, condition_column, condition_value):
        delete_data(self.cursor, self.conn, table_name, condition_column, condition_value)

    def table_exists(self, table_name):
        return table_exists(self.cursor, table_name)

    def get_file_content(self, filename, user_id):
        filters = {"name": filename}
        return get_file_content(self.cursor, "files", filters)
    
    def close_connection(self):
        """Close the database connection."""
        self.conn.close()
        print("Database connection closed.")
