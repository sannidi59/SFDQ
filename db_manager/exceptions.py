class DataQualityFrameworkError(Exception):
    """
    Base exception class for the Data Quality Framework.
    """
    pass

class ConnectionError(DataQualityFrameworkError):
    """
    Raised when there's an error connecting to the database.
    """
    pass

class CredentialError(DataQualityFrameworkError):
    """
    Raised when there's an issue with retrieving or using credentials.
    """
    pass

class QueryExecutionError(DataQualityFrameworkError):
    """
    Raised when there's an error executing a query.
    """
    pass

class ConfigurationError(DataQualityFrameworkError):
    """
    Raised when there's a problem with the configuration settings.
    """
    pass

# You can continue adding more specific exception classes as needed.
