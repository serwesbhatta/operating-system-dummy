import sqlite3

def Table_exists(self, table_name):
        """Check if a table exists."""
        try:
            self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
            return self.cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return False