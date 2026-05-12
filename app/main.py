import json
import logging
import threading
import webbrowser
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse

from app import state, watcher

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config.json"
TEACHERS_PATH = BASE_DIR / "teachers.json"
DASHBOARD_DIR = BASE_DIR / "dashboard"
LOG_DIR = BASE_DIR / "logs"

logger = logging.getLogger(__name__)


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


def _save_config(data: dict) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


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


# ── Pages ────────────────────────────────────────────────────────────────────

@app.get("/")
async def serve_dashboard():
    path = DASHBOARD_DIR / "index.html"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return FileResponse(path, media_type="text/html")


@app.get("/manage")
async def serve_manage():
    path = DASHBOARD_DIR / "manage.html"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Manage page not found")
    return FileResponse(path, media_type="text/html")


@app.get("/setup")
async def serve_setup():
    path = DASHBOARD_DIR / "setup.html"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Setup page not found")
    return FileResponse(path, media_type="text/html")


# ── Data APIs ─────────────────────────────────────────────────────────────────

@app.get("/api/data")
async def get_data():
    data = state.get_data()
    if data is None:
        return JSONResponse({"status": "waiting", "message": "No CSV processed yet."})
    return JSONResponse(data)


@app.get("/api/status")
async def get_status():
    data = state.get_data()
    config = _load_config()
    folder = config.get("watch_folder", "")
    folder_ok = Path(folder).exists()
    if data is None:
        return JSONResponse({"status": "waiting", "last_updated": None, "filename": None, "folder_ok": folder_ok, "watch_folder": folder})
    return JSONResponse({
        "status": "ok",
        "last_updated": data.get("last_updated"),
        "filename": data.get("filename"),
        "folder_ok": folder_ok,
        "watch_folder": folder,
    })


# ── Teacher management APIs ───────────────────────────────────────────────────

@app.get("/api/teachers")
async def get_teachers():
    if not TEACHERS_PATH.exists():
        return JSONResponse([])
    with open(TEACHERS_PATH, encoding="utf-8") as f:
        return JSONResponse(json.load(f))


@app.post("/api/teachers")
async def save_teachers(assignments: list[dict[str, Any]] = Body(...)):
    with open(TEACHERS_PATH, "w", encoding="utf-8") as f:
        json.dump(assignments, f, indent=2, ensure_ascii=False)
    logger.info(f"teachers.json updated: {len(assignments)} assignments saved")
    return JSONResponse({"status": "ok"})


# ── Config APIs ───────────────────────────────────────────────────────────────

@app.get("/api/config")
async def get_config():
    return JSONResponse(_load_config())


@app.post("/api/config")
async def save_config_endpoint(body: dict[str, Any] = Body(...)):
    config = _load_config()
    config.update(body)
    _save_config(config)
    logger.info(f"config.json updated: {body}")
    return JSONResponse({"status": "ok", "message": "Saved. Restart the server to apply changes."})


@app.post("/api/config/test")
async def test_folder(body: dict[str, Any] = Body(...)):
    folder = body.get("watch_folder", "").strip()
    exists = Path(folder).exists() if folder else False
    return JSONResponse({"exists": exists, "folder": folder})
