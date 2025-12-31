import geopandas as gpd
from geopandas.geodataframe import GeoDataFrame

from config import Config

MONTHS = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]


def create_map_dataframe() -> GeoDataFrame:
    """
    Crea y devuelve un GeoDataFrame con el shapefile de México.
    """
    mapa: GeoDataFrame = gpd.read_file(Config.MEXICO_SHAPEFILE)
    return mapa


class MapColors:
    SALMON = "#FF6467"
    BLACK = "black"
    WHITE = "white"
    GRAY = "#525252"
