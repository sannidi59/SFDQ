from logger_setup import setup_logger
from data_quality_framework.connection_manager import ConnectionManager
from data_quality_framework.query_manager import QueryManager

def main():
    # Initialize logging
    setup_logger(log_level="INFO", log_file="dqf_log.txt")

    # Create an instance of the ConnectionManager
    conn_manager = ConnectionManager()

    # Establish connections to Snowflake and MySQL
    sf_conn = conn_manager.get_snowflake_connection()
    mysql_conn = conn_manager.get_mysql_connection()

    # Create an instance of the QueryManager with established connections
    query_manager = QueryManager(sf_conn=sf_conn, mysql_conn=mysql_conn)

    # Fetch DDL for 'customer' table from both databases
    sf_customer_ddl = query_manager.fetch_ddl_from_snowflake(table_name="customer")
    mysql_customer_ddl = query_manager.fetch_ddl_from_mysql(table_name="customer")

    # Compare the DDLs
    if sf_customer_ddl == mysql_customer_ddl:
        print("DDLs for the 'customer' table in Snowflake and MySQL match!")
    else:
        print("DDLs for the 'customer' table in Snowflake and MySQL differ!")

    # Close the database connections
    sf_conn.close()
    mysql_conn.close()

if __name__ == "__main__":
    main()
