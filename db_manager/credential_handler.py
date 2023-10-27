import configparser
import os
import boto3
from typing import Dict
from .exceptions import CredentialError


class CredentialHandler:

    def __init__(self, db_type: str):
        """
        Initialize the Credential Handler with a specific database type.
        """
        self.db_type = db_type.lower()
        self.config = self._load_config()

    def _load_config(self) -> configparser.ConfigParser:
        """
        Load configurations from config.ini file.
        """
        config = configparser.ConfigParser()
        config.read('config/config.ini')
        return config

    def _get_from_config(self) -> Dict[str, str]:
        """
        Retrieve credentials from the config.ini file.
        """
        user = self.config[self.db_type]['user']
        password = self.config.get(self.db_type, 'password', fallback=None)
        return {"user": user, "password": password}

    def _get_from_env(self) -> Dict[str, str]:
        """
        Retrieve credentials from environment variables.
        """
        user = os.getenv(f"{self.db_type.upper()}_USER")
        password = os.getenv(f"{self.db_type.upper()}_PASSWORD")
        if not user or not password:
            raise CredentialError(f"Failed to retrieve {self.db_type} credentials from environment variables.")
        return {"user": user, "password": password}

    def _get_from_aws_secrets(self) -> Dict[str, str]:
        """
        Retrieve credentials from AWS Secrets Manager.
        """
        client = boto3.client('secretsmanager', region_name=self.config['AWS']['region'])

        try:
            response = client.get_secret_value(SecretId=f"{self.db_type}-credentials")
        except Exception as e:
            raise CredentialError(
                f"Failed to retrieve {self.db_type} credentials from AWS Secrets Manager. Reason: {str(e)}") from e

        secret = eval(response['SecretString'])  # converting string representation of dictionary to actual dictionary
        return {"user": secret['user'], "password": secret['password']}

    def get_credentials(self) -> Dict[str, str]:
        """
        Public method to fetch credentials based on the available methods.

        Current hierarchy:
        1. AWS Secrets Manager
        2. Environment Variables
        3. config.ini
        """
        try:
            # Try getting credentials from AWS Secrets Manager
            return self._get_from_aws_secrets()
        except CredentialError:
            pass

        try:
            # If AWS fails, try getting credentials from environment variables
            return self._get_from_env()
        except CredentialError:
            pass

        # If both AWS and environment variables fail, get from config
        return self._get_from_config()
