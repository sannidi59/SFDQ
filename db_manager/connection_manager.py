import mysql.connector
import snowflake.connector
import configparser
from typing import Union, Optional
from .credential_handler import CredentialHandler
from .exceptions import ConnectionError

class ConnectionManager:

    def __init__(self, db_type: str):
        """
        Initialize the Connection Manager based on the database type.
        """
        self.db_type = db_type.lower()
        self.config = self._load_config()

        if self.db_type not in ['snowflake', 'mysql']:
            raise ValueError(f"Unsupported database type: {db_type}")

    def _load_config(self) -> configparser.ConfigParser:
        """
        Load configurations from config.ini file.
        """
        config = configparser.ConfigParser()
        config.read('config/config.ini')
        return config

    def _get_credentials(self) -> dict:
        """
        Fetch credentials either from the config, environment variables, or AWS Secrets Manager.
        """
        credential_handler = CredentialHandler(self.db_type)
        return credential_handler.get_credentials()

    def connect(self) -> Union[snowflake.connector.SnowflakeConnection, mysql.connector.MySQLConnection]:
        """
        Establish a connection to the specified database.
        """
        try:
            if self.db_type == "snowflake":
                credentials = self._get_credentials()
                conn = snowflake.connector.connect(
                    user=credentials["user"],
                    password=credentials["password"],
                    account=self.config['SNOWFLAKE']['account'],
                    warehouse=self.config['SNOWFLAKE']['warehouse'],
                    database=self.config['SNOWFLAKE']['database'],
                    schema=self.config['SNOWFLAKE']['schema']
                )
            elif self.db_type == "mysql":
                credentials = self._get_credentials()
                conn = mysql.connector.connect(
                    host=self.config['MYSQL']['host'],
                    port=int(self.config['MYSQL']['port']),  # convert port to int
                    user=credentials["user"],
                    password=credentials["password"],
                    database=self.config['MYSQL']['database']
                )
            return conn

        except Exception as e:
            raise ConnectionError(f"Failed to connect to {self.db_type} database. Reason: {str(e)}") from e

    def close(self, conn: Optional[Union[snowflake.connector.SnowflakeConnection, mysql.connector.MySQLConnection]]):
        """
        Close the provided database connection.
        """
        if conn:
            conn.close()
