import json
import logging
import os
import threading
import webbrowser
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse

from app import state, watcher

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config.json"
DASHBOARD_PATH = BASE_DIR / "dashboard" / "index.html"
LOG_DIR = BASE_DIR / "logs"


def _setup_logging() -> None:
    LOG_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        handlers=[
            logging.FileHandler(LOG_DIR / "activity.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def _load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {"watch_folder": str(BASE_DIR / "exports"), "server_host": "0.0.0.0", "server_port": 8080, "auto_open_browser": True}
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


@asynccontextmanager
async def lifespan(app: FastAPI):
    _setup_logging()
    config = _load_config()
    watch_folder = config.get("watch_folder", str(BASE_DIR / "exports"))

    watcher.process_latest_in_folder(watch_folder)
    observer = watcher.start_watcher(watch_folder)

    if config.get("auto_open_browser", True):
        port = config.get("server_port", 8080)
        threading.Timer(1.5, lambda: webbrowser.open(f"http://localhost:{port}")).start()

    yield

    observer.stop()
    observer.join()


app = FastAPI(title="Swimming Lesson Dashboard", lifespan=lifespan)


@app.get("/")
async def serve_dashboard():
    if not DASHBOARD_PATH.exists():
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return FileResponse(DASHBOARD_PATH, media_type="text/html")


@app.get("/api/data")
async def get_data():
    data = state.get_data()
    if data is None:
        return JSONResponse({"status": "waiting", "message": "No CSV processed yet."}, status_code=200)
    return JSONResponse(data)


@app.get("/api/status")
async def get_status():
    data = state.get_data()
    if data is None:
        return JSONResponse({"status": "waiting", "last_updated": None, "filename": None})
    return JSONResponse({
        "status": "ok",
        "last_updated": data.get("last_updated"),
        "filename": data.get("filename"),
    })
