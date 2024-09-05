import logging
import sys
import os
from logging.handlers import RotatingFileHandler

# Define a Standard log formatter
class StandardLogFormatter(logging.Formatter):
    def format(self, record):
        # Adjust the level name to include a colon and ensure padding
        levelname_with_colon = f"{record.levelname}:".ljust(9, " ")  # Add colon and pad to 8 + 1 characters

        # Replace the level name in the record with the padded version
        record.levelname = levelname_with_colon

        # Create the log format with the padded and colon-added level name
        log_format = "%(levelname)s %(message)s"
        formatter = logging.Formatter(log_format, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a handler for stdout (DEBUG and below)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)

    # Create a handler for stderr (WARNING and above)
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)

    # Apply the StandardLogFormatter to both handlers
    log_formatter = StandardLogFormatter()
    stdout_handler.setFormatter(log_formatter)
    stderr_handler.setFormatter(log_formatter)

    # Add the handlers to the logger
    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)

    # Add a file handler for INFO and above
    # Get the directory where the script is running
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    log_file_path = os.path.join(script_directory, "app.log")

    # Create a rotating file handler (log file size: 5MB, keeps 5 backups)
    file_handler = RotatingFileHandler(log_file_path, maxBytes=5*1024*1024, backupCount=5)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger

logga = setup_logger()