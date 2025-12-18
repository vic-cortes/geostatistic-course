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


class IdfcColumns:
    SUBTYPE_OF_CRIME = "Subtipo de delito"
    YEAR = "Año"
    CLAVE_ENT = "Clave_Ent"
    ENTIDAD = "Entidad"
    TOTAL = "Total"


class MapColumns:
    CVE_ENT = "CVE_ENT"
    NOMGEO = "NOMGEO"


df = pd.read_csv(Config.IDFC, encoding="cp1252")
mapa: GeoDataFrame = gpd.read_file(Config.MEXICO_SHAPEFILE)


df[IdfcColumns.TOTAL] = df[MONTHS].sum(axis=1)
df.head(5)

# Filtrar por delitos de homicidio doloso
data_filter = df.copy()
data_filter = data_filter[
    data_filter[IdfcColumns.SUBTYPE_OF_CRIME] == TypeOfCrime.HOMICIDIO_DOLOSO
]
data_filter.head(5)

# Agrupar por año, clave de entidad y entidad, sumando el total de homicidios dolosos
data_total_hom = data_filter.copy()
data_total_hom = (
    data_total_hom.groupby(
        [IdfcColumns.YEAR, IdfcColumns.CLAVE_ENT, IdfcColumns.ENTIDAD]
    )[IdfcColumns.TOTAL]
    .sum()
    .reset_index()
)
data_total_hom.head(32)

# Verificar columnas
mapa[[MapColumns.CVE_ENT, MapColumns.NOMGEO]].dtypes
data_total_hom[[IdfcColumns.CLAVE_ENT, IdfcColumns.ENTIDAD]].dtypes

# Fix data type mismatch before merge
# Convert both columns to string type to ensure compatibility
mapa[MapColumns.CVE_ENT] = mapa[MapColumns.CVE_ENT].astype(str)
data_total_hom[IdfcColumns.CLAVE_ENT] = data_total_hom[IdfcColumns.CLAVE_ENT].astype(
    str
)

# Filter for 2024 data
data_2024 = data_total_hom[data_total_hom[IdfcColumns.YEAR] == 2024]

mapa = mapa.merge(
    data_2024,
    left_on=[MapColumns.NOMGEO],
    right_on=[IdfcColumns.ENTIDAD],
    how="left",
)

# Mapa temático con variable continua
plt.figure(figsize=(15, 12), dpi=500)
mapa.plot(
    column=IdfcColumns.TOTAL,
    legend=True,
    cmap="OrRd",
    legend_kwds={"label": "Escala Continua", "orientation": "horizontal"},
    edgecolor="black",
)
plt.title(
    "Distribución espacial de los homicidios doloso en México\nPor entidad federativa al cierre de 2024"
)
plt.grid(False)
plt.show()


plt.figure(figsize=(15, 12), dpi=500)
mapa.plot(
    column=IdfcColumns.TOTAL,
    scheme="Quantiles",
    k=5,
    legend=True,
    cmap="YlGnBu",
    legend_kwds={"loc": "lower left", "fmt": "{:.0f}"},
    edgecolor="black",
)
plt.title(
    "Distribución espacial de los homicidios doloso en México por quintiles\nPor entidad federativa al cierre de 2024"
)
plt.grid(False)
plt.tight_layout()

# plt.savefig(, dpi=500, bbox_inches="tight", facecolor="white")
