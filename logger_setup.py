import logging
import os


def setup_logger(log_level: str = "INFO", log_file: str = None) -> None:
    """
    Configure the logging settings for the application.

    Args:
    - log_level (str): The logging level (e.g., "INFO", "DEBUG", "ERROR").
    - log_file (str): Path to the file where logs should be written.
                      If None, logs will be displayed in the console.
    """
    log_format = "%(asctime)s — %(levelname)s — %(message)s"
    log_datefmt = "%Y-%m-%d %H:%M:%S"

    # Configure logging to the console
    logging.basicConfig(level=log_level, format=log_format, datefmt=log_datefmt)

    # If a log file path is provided, add a file handler to log to the file as well
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(log_format, datefmt=log_datefmt))
        logging.getLogger().addHandler(file_handler)

    logging.info("Logger initialized successfully.")
