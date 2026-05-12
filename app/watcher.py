import logging
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from app import processor, state

logger = logging.getLogger(__name__)


class CSVHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix.lower() == ".csv":
            logger.info(f"New CSV detected: {path.name}")
            _process_file(str(path))

    def on_moved(self, event):
        if event.is_directory:
            return
        path = Path(event.dest_path)
        if path.suffix.lower() == ".csv":
            logger.info(f"CSV moved into folder: {path.name}")
            _process_file(str(path))


def _process_file(filepath: str) -> None:
    try:
        data = processor.process_csv(filepath)
        state.set_data(data)
        logger.info(f"Processed {Path(filepath).name}: {data['summary']['total_lessons']} lessons loaded")
    except Exception as exc:
        logger.error(f"Failed to process {filepath}: {exc}")


def process_latest_in_folder(folder: str) -> None:
    folder_path = Path(folder)
    if not folder_path.exists():
        logger.warning(f"Watch folder does not exist: {folder}")
        return
    csvs = sorted(folder_path.glob("*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
    if csvs:
        logger.info(f"Loading most recent CSV on startup: {csvs[0].name}")
        _process_file(str(csvs[0]))
    else:
        logger.info("No CSV files found in watch folder — waiting for first export.")


def start_watcher(folder: str) -> Observer:
    folder_path = Path(folder)
    if not folder_path.exists():
        logger.warning(f"Watch folder does not exist — watcher not started: {folder}")
        observer = Observer()
        observer.start()
        return observer

    handler = CSVHandler()
    observer = Observer()
    observer.schedule(handler, str(folder_path), recursive=False)
    observer.start()
    logger.info(f"Watching folder: {folder_path}")
    return observer
