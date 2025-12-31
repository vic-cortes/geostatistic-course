import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from libpysal.weights import KNN, DistanceBand, Queen, Rook
from shapely.geometry import LineString

from utils import MapColors, create_map_dataframe

mapa = create_map_dataframe()

NORMALIZE_BY_ROWS = "r"


# Cálculo de matriz
W = Queen.from_dataframe(mapa, ids="CVE_ENT")
W.transform = NORMALIZE_BY_ROWS


# Tower method
# Cálculo de matriz

W = Rook.from_dataframe(mapa, ids="CVE_ENT")
W.transform = NORMALIZE_BY_ROWS


# Matriz completa

W_dense, ids = W.full()
print("Dimensión de W:", W_dense.shape)
W_dense

# Re calcular la matriz sin ids

W_rook = Rook.from_dataframe(mapa)

# Normalizar filas

W_rook.transform = "r"

## Visualización del mapa

fig, ax = plt.subplots(1, 1, figsize=(10, 5), dpi=500)

# Poligonos
mapa.plot(ax=ax, color="white", edgecolor="black")

# Conexiones reina
W_rook.plot(
    mapa, edge_kws=dict(linewidth=1, color="red"), node_kws=dict(marker="*"), ax=ax
)
plt.figtext(
    0.4,
    0.95,
    "mapa de pesos espaciales de México\npor entidad federativa",
    fontweight="bold",
    color=MapColors.GRAY,
    ha="center",
    fontsize=14,
)  # Titulo
plt.figtext(
    0.4,
    0.87,
    "Método: Contigüedad - Torre",
    style="italic",
    color=MapColors.GRAY,
    ha="center",
    fontsize=12,
)  # Subtitulo
plt.figtext(
    0.0,
    0.05,
    "Fuente: Elaborado por SciData con datos de INEGI.",
    color=MapColors.GRAY,
    fontsize=10,
)  # Pie de gráfico
ax.set_axis_off()
ax = plt.gca()
plt.grid(False)
plt.tight_layout(rect=[0, 0.05, 0.85, 0.95])
