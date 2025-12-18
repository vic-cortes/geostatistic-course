import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
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


class TypeOfCrime:
    HOMICIDIO_DOLOSO = "Homicidio doloso"


class Columns:
    SUBTYPE_OF_CRIME = "Subtipo de delito"


data = pd.read_csv(Config.IDFC, encoding="cp1252")
map_: GeoDataFrame = gpd.read_file(Config.MEXICO_SHAPEFILE)


data["Total"] = data[MONTHS].sum(axis=1)
data.head(5)

# Filtrar por delitos de homicidio doloso
data_filter = data.copy()
data_filter = data_filter[
    data_filter[Columns.SUBTYPE_OF_CRIME] == TypeOfCrime.HOMICIDIO_DOLOSO
]
data_filter.head(5)
