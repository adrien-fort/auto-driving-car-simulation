import os
import logging
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configure logging, nothing fancy, just date/time and log level
def configure_logging():
    current_date = datetime.now().strftime("%Y%m%d")
    log_folder = os.path.join(PROJECT_ROOT, 'logs')
    log_file = f'simulator_{current_date}.log'
    log_path = os.path.join(log_folder, log_file)

    # Create the logs folder if it doesn't exist
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_path),  # Output to a log file (one per day)
        ]
    )


if __name__ == "__main__":
    configure_logging()
