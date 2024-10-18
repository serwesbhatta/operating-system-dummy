def Show_tables(self, raw=True):
        """Show all tables in the database."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        results = self.cursor.fetchall()
        return self.__formatted_results(results) if not raw else self.__raw_results(results)