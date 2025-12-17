from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MAPS_DIR = DATA_DIR / "maps"
MEXICO_DIR = DATA_DIR / "mexico"


class Config:
    MEXICO_SHAPEFILE = MEXICO_DIR / "00ent.shp"
