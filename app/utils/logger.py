import logging
from logging import FileHandler


def init_logger(app):
    """Initializes the logger for the Flask application using settings from config.py."""
    
    # Remove the default loggers
    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)
    
    # Retrieve logging configuration from the app's config
    log_level = app.config['LOG_LEVEL']
    log_format = app.config['LOG_FORMAT']
    log_file = app.config['LOG_FILE']

    # define the log format
    formatter = logging.Formatter(log_format)  # Log format from config.py

    # FileHandler for logging (writes to a file)
    file_handler = FileHandler(log_file)  # Log file specified in config.py
    file_handler.setLevel(log_level)  # Set the logging level from config.py
    file_handler.setFormatter(formatter)

    # Add the FileHandler to Flask's logger
    app.logger.addHandler(file_handler)

    # Optional: Console handler for logging to the terminal as well
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)  # Set the logging level from config.py
    console_handler.setFormatter(formatter)
    
    # Add the ConsoleHandler to Flask's logger
    app.logger.addHandler(console_handler)
