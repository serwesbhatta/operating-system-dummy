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
        Create_table(self.cursor, self.conn, table_name, columns)

    def drop_table(self, table_name):
        Drop_table(self.cursor, self.conn, table_name)

    def show_tables(self, raw=True):
        return Show_tables(self.cursor, raw)

    def describe_table(self, table_name, raw=False):
        return Describe_table(self.cursor, table_name, raw)

    def insert_data(self, table_name, data):
        Insert_data(self.cursor, self.conn, table_name, data)

    def read_data(self, table_name, filters=None):
        return Read_data(self.cursor, table_name, filters)

    def update_data(self, table_name, column, new_value, condition_column, condition_value):
        return Update_data(self.cursor, self.conn, table_name, column, new_value, condition_column, condition_value)

    def delete_data(self, table_name, condition_column, condition_value):
        Delete_data(self.cursor, self.conn, table_name, condition_column, condition_value)

    def table_exists(self, table_name):
        return Table_exists(self.cursor, table_name)

    def get_file_content(self, filename, oid):
        filters = {"name": filename, "oid" : oid}
        return Get_file_content(self.cursor, filters)
    
    def close_connection(self):
        """Close the database connection."""
        self.conn.close()
        print("Database connection closed.")
