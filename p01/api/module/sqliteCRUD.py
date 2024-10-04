import sqlite3
from prettytable import PrettyTable


class SqliteCRUD:
    """
    A class to perform CRUD operations on a SQLite database.
    """

    def __init__(self, db_path):
        """Initialize the database connection and cursor."""
        self.db_path = db_path
        # Enable thread-safe mode by adding check_same_thread=False
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def __raw_results(self, results):
        """Convert raw results to a list of table names."""
        return [row[0] for row in results]

    def __formatted_results(self, results):
        """Format results as a PrettyTable."""
        table = PrettyTable()
        table.field_names = [desc[0] for desc in self.cursor.description]
        table.add_rows(results)
        return table

    def create_table(self, table_name, columns):
        """Create a new table with specified columns."""
        try:
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print(f"Table '{table_name}' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def drop_table(self, table_name):
        """Drop a table by name."""
        try:
            drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
            self.cursor.execute(drop_table_query)
            self.conn.commit()
            print(f"Dropped table '{table_name}' successfully.")
        except sqlite3.Error as e:
            print(f"Error dropping table: {e}")

    def show_tables(self, raw=True):
        """Show all tables in the database."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        results = self.cursor.fetchall()
        return self.__formatted_results(results) if not raw else self.__raw_results(results)

    def describe_table(self, table_name, raw=False):
        """Describe the structure of a table."""
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        results = self.cursor.fetchall()
        if raw:
            return [{ "column_name": row[1], "data_type": row[2], "isnull": "NULL" if row[3] == 0 else "NOT NULL" } for row in results]
        return self.__formatted_results(results)

    def insert_data(self, table_name, data):
        """Insert data into a table."""
        try:
            placeholders = ", ".join("?" * len(data))
            insert_query = f"INSERT INTO {table_name} VALUES ({placeholders});"
            self.cursor.execute(insert_query, data)
            self.conn.commit()
            print("Data inserted successfully.")
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")

    def read_data(self, table_name, filters=None):
        """
        Read data from a table, with optional filtering.
    
        Args:
            table_name (str): The name of the table to query.
            filters (dict, optional): A dictionary of filters to apply to the query (e.g., {"name": "filename"}).
                                    If None, all rows will be returned.

        Returns:
            list: The query results as a list of rows, or an empty list if no results.
        """
        try:
            select_query = f"SELECT * FROM {table_name}"

             # If filters are provided, add a WHERE clause
            if filters:
                conditions = [f"{key} = ?" for key in filters.keys()]
                where_clause = " WHERE " + " AND ".join(conditions)
                select_query += where_clause

            self.cursor.execute(select_query, tuple(filters.values()) if filters else ())
            results = self.cursor.fetchall()

            if results:
                print(results)
                return results
            else:
                print("No data found in the table.")
                return []
        except sqlite3.Error as e:
            print(f"Error reading data: {e}")

    def update_data(self, table_name, column, new_value, condition_column, condition_value):
        """Update data in a table based on a condition."""
        try:
            update_query = f"UPDATE {table_name} SET {column} = ? WHERE {condition_column} = ?;"
            self.cursor.execute(update_query, (new_value, condition_value))
            self.conn.commit()
            print("Data updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")

    def delete_data(self, table_name, condition_column, condition_value):
        """Delete data from a table based on a condition."""
        try:
            delete_query = f"DELETE FROM {table_name} WHERE {condition_column} = ?;"
            self.cursor.execute(delete_query, (condition_value,))
            self.conn.commit()
            print("Data deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()
        print("Database connection closed.")

    def formatted_print(self, table_name):
        """Print the contents of a table in a formatted manner."""
        self.cursor.execute(f"SELECT * FROM {table_name};")
        table_info = self.cursor.fetchall()
        table = PrettyTable()
        table.field_names = [desc[0] for desc in self.cursor.description]
        table.add_rows(table_info)
        return table

    def table_exists(self, table_name):
        """Check if a table exists."""
        try:
            self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
            return self.cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False


# Example usage:
if __name__ == "__main__":
    db_name = "../data/students.sqlite"
    conn = SqliteCRUD(db_name)

    # Define table schema
    table_name = "students"
    columns = ["id TEXT PRIMARY KEY", "name TEXT", "age INTEGER"]

    # Create table
    conn.create_table(table_name, columns)

    # Insert data
    conn.insert_data(table_name, ("1", "Alice", 25))
    conn.insert_data(table_name, ("2", "Bob", 23))
    conn.insert_data(table_name, ("3", "Charlie", 11))

    # Read data
    conn.read_data(table_name)

    # Update data
    conn.update_data(table_name, "age", 26, "name", "Alice")

    # Delete data
    conn.delete_data(table_name, "name", "Alice")

    # Close the database connection
    conn.close_connection()
