import sqlite3

def delete_data(self, table_name, condition_column, condition_value):
        """Delete data from a table based on a condition."""
        try:
            delete_query = f"DELETE FROM {table_name} WHERE {condition_column} = ?;"
            self.cursor.execute(delete_query, (condition_value,))
            self.conn.commit()
            print("Data deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")