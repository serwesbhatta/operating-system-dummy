def Describe_table(self, table_name, raw=False):
        """Describe the structure of a table."""
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        results = self.cursor.fetchall()
        if raw:
            return [{ "column_name": row[1], "data_type": row[2], "isnull": "NULL" if row[3] == 0 else "NOT NULL" } for row in results]
        return self.__formatted_results(results)