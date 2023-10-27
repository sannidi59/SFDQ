from connection_manager import ConnectionManager
from typing import List, Dict, Union

class QueryManager:
    def __init__(self, db_type: str):
        """
        Initialize the QueryManager with a specific database type.
        """
        self.db_type = db_type.lower()
        self.connection_manager = ConnectionManager(db_type)

    def get_ddl(self, table_name: str) -> str:
        """
        Retrieves the DDL of a specified table.
        """
        conn = self.connection_manager.connect()
        cursor = conn.cursor()

        if self.db_type == "snowflake":
            # Snowflake specific way to get DDL
            query = f"SHOW CREATE TABLE {table_name};"
            cursor.execute(query)
            result = cursor.fetchone()  # Assuming result is a single row
            return result[0] if result else ""

        elif self.db_type == "mysql":
            # MySQL specific way to get DDL
            query = f"SHOW CREATE TABLE {table_name};"
            cursor.execute(query)
            result = cursor.fetchone()  # Result is in the form (table_name, create_statement)
            return result[1] if result else ""

        cursor.close()
        self.connection_manager.close(conn)

        return ""

    def get_records(self, table_name: str) -> List[Dict[str, Union[str, int, float]]]:
        """
        Retrieves all records from a specified table.
        """
        conn = self.connection_manager.connect()
        cursor = conn.cursor(dictionary=True)  # Assuming MySQL; for Snowflake adjust accordingly

        query = f"SELECT * FROM {table_name};"
        cursor.execute(query)
        records = cursor.fetchall()

        cursor.close()
        self.connection_manager.close(conn)

        return records

    def get_record_count(self, table_name: str) -> int:
        """
        Returns the number of records in a specified table.
        """
        conn = self.connection_manager.connect()
        cursor = conn.cursor()

        query = f"SELECT COUNT(*) FROM {table_name};"
        cursor.execute(query)
        count = cursor.fetchone()[0]

        cursor.close()
        self.connection_manager.close(conn)

        return count
