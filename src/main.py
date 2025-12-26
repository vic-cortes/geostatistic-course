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

# Dataset source:
# https://drive.google.com/file/d/16oRu_xGKwuGoqwmKmz7A8mcVNFwb4Vt5/view


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


def create_map_by_crime(
    df: pd.DataFrame,
    mapa: GeoDataFrame,
    year: int = 2024,
    type_of_crime: TypeOfCrime | None = None,
) -> GeoDataFrame:
    """
    Crea un mapa temático de México basado en los datos de homicidios dolosos.
    """
    if type_of_crime is None:
        raise ValueError("type_of_crime no puede ser None")

    if not (2015 <= year <= 2024):
        raise ValueError("year debe estar entre 2015 y 2024")

    df_filtered = df.copy()
    df_filtered = df_filtered[
        df_filtered[IdfcColumns.SUBTYPE_OF_CRIME] == type_of_crime
    ]

    # Agrupar por año, clave de entidad y entidad, sumando el total de crimen
    GROUP_BY_COLUMNS = [
        IdfcColumns.YEAR,
        IdfcColumns.CLAVE_ENT,
        IdfcColumns.ENTIDAD,
    ]

    df_total_crime = df_filtered.copy()
    df_total_crime = (
        df_total_crime.groupby(GROUP_BY_COLUMNS)[IdfcColumns.TOTAL].sum().reset_index()
    )

    # Fix data type mismatch before merge
    # Convert both columns to string type to ensure compatibility
    mapa[MapColumns.CVE_ENT] = mapa[MapColumns.CVE_ENT].astype(str)
    df_total_crime[IdfcColumns.CLAVE_ENT] = df_total_crime[
        IdfcColumns.CLAVE_ENT
    ].astype(str)

    # Filter by year
    df_by_year = df_total_crime[df_total_crime[IdfcColumns.YEAR] == year]

    mapa = mapa.merge(
        df_by_year,
        left_on=[MapColumns.NOMGEO],
        right_on=[IdfcColumns.ENTIDAD],
        how="left",
    )

    return mapa


# Try reading with error handling and explicit parameters
sismos_df = pd.read_csv(
    Config.SISMO_DATA,
    skiprows=4,
    encoding="latin1",
)

sismos_df = sismos_df.dropna(subset=["Hora"])
sismos_df["Magnitud"] = pd.to_numeric(sismos_df["Magnitud"], errors="coerce")


# Convertir el df a GeoDataFrame
geometry = gpd.points_from_xy(sismos_df["Longitud"], sismos_df["Latitud"])
sismos_gdf = gpd.GeoDataFrame(sismos_df, geometry=geometry, crs="4326")


# Extraer la referencia de los kms
KMS_REGEX = r"(\d+(?:\.\d+)?)\s*km"
COLUMN_REF_KMS = "Referencia de localizacion"

sismos_gdf["km_epicentro"] = (
    sismos_df[COLUMN_REF_KMS].str.extract(KMS_REGEX)[0].astype(float)
)

# Sismos de magnitud 5.5 en adelante y menores a 200 kms de epicentro
sismos_gdf_ct = sismos_gdf[
    (sismos_gdf["Magnitud"] >= 5.5) & (sismos_gdf["km_epicentro"] <= 200)
].copy()

qt = sismos_gdf_ct["Magnitud"].quantile([0, 0.2, 0.4, 0.6, 0.8, 1]).values
# 2. Crear variable categórica
sismos_gdf_ct["Magnitud_qt"] = pd.cut(
    sismos_gdf_ct["Magnitud"], bins=qt, include_lowest=True
)
# 3. Generaer etiquetas
labels = [f"{qt[i]:.1f} - {qt[i+1]:.1f}" for i in range(5)]

# 4. Tamaños de puntos por quintil
size_map = dict(zip(sismos_gdf_ct["Magnitud_qt"].cat.categories, [20, 40, 60, 80, 100]))
sismos_gdf_ct["size"] = sismos_gdf_ct["Magnitud_qt"].map(size_map)
sismos_gdf_ct = sismos_gdf_ct.to_crs(mapa.crs)


import numpy as np
from matplotlib.lines import Line2D

fig, ax = plt.subplots(figsize=(10, 5), dpi=500)
# Capa de la cartografía por división política (estatal)
mapa.plot(ax=ax, color="white", edgecolor="black", linewidth=0.6)


class MapColors:
    SALMON = "#FF6467"
    BLACK = "black"
    GRAY = "#525252"


plot_params = {
    "ax": ax,
    "markersize": sismos_gdf_ct["size"],
    "color": MapColors.SALMON,
    "edgecolor": MapColors.BLACK,
    "linewidth": 0.5,
    "alpha": 0.85,
}


# Capa de sismos
sismos_gdf_ct.plot(**plot_params)
handles = [
    Line2D(
        xdata=[0],
        ydata=[0],
        marker="o",
        color=MapColors.SALMON,
        label=lab,
        markersize=np.sqrt(size),
        linestyle="None",
    )
    for lab, size in zip(labels, [20, 40, 60, 80, 100])
]
ax.legend(handles=handles, title="Magnitud", loc="lower left", frameon=True)

base_params = {
    "x": 0.4,
    "y": 0.95,
    "fontweight": "bold",
    "color": MapColors.GRAY,
    "ha": "center",
    "fontsize": 14,
}

plt.figtext(s="Sismos registrados del 2000 al 2025", **base_params)  # Titulo
plt.figtext(
    y=0.87,
    s="maginitudes 5.5 en adelante\nepicentros menores a 200 km",
    fontsize=12,
    **base_params,
)  # Subtitulo
plt.figtext(
    0.05,
    0.05,
    "Fuente: SMN. Catálogo de sismos.",
    color=MapColors.GRAY,
    fontsize=10,
)  # Pie de gráfico
ax.set_axis_off()
ax = plt.gca()
legend = ax.get_legend()

for text in legend.get_texts():
    text.set_color(MapColors.GRAY)

if legend is not None:
    legend.get_frame().set_linewidth(0)
    legend.get_frame().set_edgecolor("none")

plt.grid(False)
plt.tight_layout(rect=[0, 0.05, 0.85, 0.95])
