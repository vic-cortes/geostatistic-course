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
    YEAR = "Año"
    CLAVE_ENT = "Clave_Ent"
    ENTIDAD = "Entidad"
    TOTAL = "Total"


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

# Agrupar por año, clave de entidad y entidad, sumando el total de homicidios dolosos
data_total_hom = data_filter.copy()
data_total_hom = (
    data_total_hom.groupby([Columns.YEAR, Columns.CLAVE_ENT, Columns.ENTIDAD])[
        Columns.TOTAL
    ]
    .sum()
    .reset_index()
)
data_total_hom.head(32)

# Verificar columnas
map_[["CVE_ENT", "NOMGEO"]].dtypes
data_total_hom[[Columns.CLAVE_ENT, Columns.ENTIDAD]].dtypes

# Fix data type mismatch before merge
# Convert both columns to string type to ensure compatibility
map_["CVE_ENT"] = map_["CVE_ENT"].astype(str)
data_total_hom[Columns.CLAVE_ENT] = data_total_hom[Columns.CLAVE_ENT].astype(str)

# Filter for 2024 data
data_2024 = data_total_hom[data_total_hom[Columns.YEAR] == 2024]

map_ = map_.merge(
    data_2024,
    left_on=["CVE_ENT", "NOMGEO"],
    right_on=[Columns.CLAVE_ENT, Columns.ENTIDAD],
    how="left",
)


print(map_.head())
