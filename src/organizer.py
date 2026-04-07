import time
import shutil
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .config_loader import load_config
from .logger_setup import setup_logger
from .security import safe_move, sanitize_path

class DownloadHandler(FileSystemEventHandler):
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def on_created(self, event):
        if not event.is_directory:
            self.process_file(Path(event.src_path))

    def process_file(self, file_path: Path):
        ext = file_path.suffix.lower().lstrip('.')
        # Buscar regla
        rule = next((r for r in self.config['rules'] if r['extension'] == ext), None)
        if not rule:
            self.logger.info(f"No rule for {ext}, ignoring {file_path.name}")
            return
        
        dest_folder = Path(self.config['destination_base']) / rule['folder']
        if rule.get('subfolder_by_date', False):
            date_str = datetime.now().strftime("%Y-%m-%d")
            dest_folder = dest_folder / date_str
        
        dest_folder = sanitize_path(self.config['destination_base'], str(dest_folder))
        dest_path = dest_folder / file_path.name
        
        # Seguridad: cifrar si es sensible y está configurado
        if (self.config.get('encrypt_sensitive') and 
            ext in self.config.get('sensitive_extensions', [])):
            # Llamar a función de cifrado (implementar con cryptography)
            self.logger.info(f"Encryption requested for {file_path.name} - not implemented here")
        
        safe_move(file_path, dest_path, self.logger)

def run_once(config, logger):
    handler = DownloadHandler(config, logger)
    watch_dir = Path(config['watch_folder'])
    for item in watch_dir.iterdir():
        if item.is_file():
            handler.process_file(item)

def run_daemon(config, logger):
    event_handler = DownloadHandler(config, logger)
    observer = Observer()
    observer.schedule(event_handler, str(config['watch_folder']), recursive=False)
    observer.start()
    logger.info(f"Watching {config['watch_folder']}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/settings.json")
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()
    
    cfg = load_config(args.config)
    logger = setup_logger(cfg['log_file'])
    if args.once or cfg.get('run_once'):
        run_once(cfg, logger)
    else:
        run_daemon(cfg, logger)