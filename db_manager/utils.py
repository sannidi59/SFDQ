import logging
from datetime import datetime

def setup_logging(log_level: str = "INFO", log_file: str = "dqf_log.txt") -> None:
    """
    Set up logging for the application.

    Args:
    - log_level (str, optional): The logging level. Defaults to "INFO".
    - log_file (str, optional): File to write logs to. Defaults to "dqf_log.txt".
    """
    logging.basicConfig(level=log_level,
                        format='[%(asctime)s] [%(levelname)s] - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[logging.FileHandler(log_file), logging.StreamHandler()])
    logging.info("Logging initialized")

def current_timestamp() -> str:
    """
    Returns the current timestamp as a string in the format 'YYYY-MM-DD HH:MM:SS'.

    Returns:
    - str: The timestamp.
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Other utility functions can be added as required
