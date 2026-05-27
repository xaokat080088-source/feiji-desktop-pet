import sys
import os
from pathlib import Path


def app_root() -> Path:
    if getattr(sys, "frozen", False):
        # PyInstaller 6.x 把资源放在 _internal/（sys._MEIPASS），不是 exe 同级目录
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


def user_data_dir() -> Path:
    base = Path(os.environ.get("APPDATA", Path.home())) / "Feiji"
    base.mkdir(parents=True, exist_ok=True)
    return base


APP_ROOT   = app_root()
USER_DATA  = user_data_dir()
FRAMES_DIR = APP_ROOT / "frames_nobg"
MUSIK_DIR  = APP_ROOT / "musik"
ASSETS_DIR = APP_ROOT / "assets"
ICON_PATH  = ASSETS_DIR / "look-1.ico"
STATE_FILE = USER_DATA / "pet_state.json"
CACHE_DIR  = USER_DATA / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
