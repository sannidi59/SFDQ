import pytest
from data_quality_framework.connection_manager import ConnectionManager
from data_quality_framework.exceptions import ConnectionError

class TestConnectionManager:

    @pytest.fixture
    def setup_config(self):
        """
        Fixture for loading configurations.
        """
        config = ConnectionManager._load_config()
        return config

    def test_load_config(self, setup_config):
        """
        Test loading configurations.
        """
        config = setup_config
        assert config is not None, "Config loading failed."
        assert 'SNOWFLAKE' in config, "Snowflake configurations missing."
        assert 'MYSQL' in config, "MySQL configurations missing."

    def test_get_credentials_snowflake(self):
        """
        Test retrieving Snowflake credentials.
        """
        cm = ConnectionManager(db_type="snowflake")
        credentials = cm._get_credentials()
        assert 'user' in credentials, "Snowflake user not retrieved."
        assert 'password' in credentials, "Snowflake password not retrieved."

    def test_get_credentials_mysql(self):
        """
        Test retrieving MySQL credentials.
        """
        cm = ConnectionManager(db_type="mysql")
        credentials = cm._get_credentials()
        assert 'user' in credentials, "MySQL user not retrieved."
        assert 'password' in credentials, "MySQL password not retrieved."

    def test_successful_connect_snowflake(self):
        """
        Test successful connection to Snowflake.
        """
        cm = ConnectionManager(db_type="snowflake")
        conn = cm.connect()
        assert conn is not None, "Snowflake connection failed."
        cm.close(conn)

    def test_successful_connect_mysql(self):
        """
        Test successful connection to MySQL.
        """
        cm = ConnectionManager(db_type="mysql")
        conn = cm.connect()
        assert conn is not None, "MySQL connection failed."
        cm.close(conn)

    def test_unsupported_database_type(self):
        """
        Test initialization with unsupported database type.
        """
        with pytest.raises(ValueError, match=r"Unsupported database type"):
            ConnectionManager(db_type="unknown_db")

    def test_failed_connection(self, mocker):
        """
        Test failed connection scenario.
        """
        mocker.patch('snowflake.connector.connect', side_effect=Exception('Mocked exception'))
        cm = ConnectionManager(db_type="snowflake")
        with pytest.raises(ConnectionError, match=r"Failed to connect"):
            cm.connect()

