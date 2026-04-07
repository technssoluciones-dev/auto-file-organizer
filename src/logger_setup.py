import logging
import logging.handlers
import sys

def setup_logger(log_file_path: str, level=logging.INFO):
    logger = logging.getLogger("FileOrganizer")
    logger.setLevel(level)
    
    # Rotación: 5 MB por archivo, 3 backups
    file_handler = logging.handlers.RotatingFileHandler(
        log_file_path, maxBytes=5*1024*1024, backupCount=3
    )
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger