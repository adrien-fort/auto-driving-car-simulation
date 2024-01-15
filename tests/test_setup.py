import os
import logging
from datetime import datetime
import pytest
from src.setup import configure_logging, PROJECT_ROOT

@pytest.fixture
def setup_logging():
    configure_logging()

def test_configure_logging(setup_logging):
    # Ensure the logs folder and log file are created
    configure_logging()

    current_date = datetime.now().strftime("%Y%m%d")
    log_folder = os.path.join(PROJECT_ROOT, 'logs')
    log_file = f'simulator_{current_date}.log'
    log_path = os.path.join(log_folder, log_file)

    assert os.path.exists(log_folder)
    assert os.path.exists(log_path)