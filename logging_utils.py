import os
import logging
from datetime import datetime
from PyQt6.QtCore import QObject, pyqtSignal

class QtLogHandler(QObject, logging.Handler):
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        logging.Handler.__init__(self)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.setFormatter(formatter)

    def emit(self, record):
        msg = self.format(record)
        self.log_signal.emit(msg)


def setup_logging():
    # Create logs directory if it doesn't exist
    log_dir = r"C:\Users\jmasu\OneDrive\Documents\QA Files\logs"
    os.makedirs(log_dir, exist_ok=True)

    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f"qa_app_{timestamp}.log")

    # Set up logging configuration
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    # Add Qt handler for GUI logging if needed
    qt_handler = QtLogHandler()
    logging.getLogger().addHandler(qt_handler)

    return qt_handler


def log_exception(exc_type, exc_value, exc_traceback):
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))