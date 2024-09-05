import logging
import sys
from venv import logger


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

    # Create a handler for stdout (INFO and below)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)

    # Create a handler for stderr (ERROR and above)
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)

    # Apply the FastAPI log formatter to both handlers
    log_formatter = StandardLogFormatter()
    stdout_handler.setFormatter(log_formatter)
    stderr_handler.setFormatter(log_formatter)

    # Add the handlers to the logger
    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)

    return logger

logga = setup_logger()
