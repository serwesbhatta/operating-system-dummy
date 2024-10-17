import sqlite3

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