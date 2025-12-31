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

# Método de vecinos - K vecinos

## Cálculo de la matriz con 4 vecinos por área
knn4 = KNN.from_dataframe(mapa, k=4, ids="CVE_ENT")
knn4.transform = NORMALIZE_BY_ROWS


# Re calcular la matriz sin ids
W_knn4 = KNN.from_dataframe(mapa, k=4)
W_knn4.transform = NORMALIZE_BY_ROWS

## Visualización del mapa
fig, ax = plt.subplots(1, 1, figsize=(10, 5), dpi=500)

# Poligonos
mapa.plot(ax=ax, color="white", edgecolor="black")
# Conexiones reina
W_knn4.plot(
    mapa, edge_kws=dict(linewidth=1, color="red"), node_kws=dict(marker="*"), ax=ax
)
plt.figtext(
    0.4,
    0.95,
    "Mapa de pesos espaciales de México\npor entidad federativa",
    fontweight="bold",
    color=MapColors.GRAY,
    ha="center",
    fontsize=14,
)  # Titulo
plt.figtext(
    0.4,
    0.87,
    "Método: Vecinos cercanos - 4 vecinos",
    style="italic",
    color=MapColors.GRAY,
    ha="center",
    fontsize=12,
)  # Subtitulo
plt.figtext(
    0.05,
    0.05,
    "Fuente: Elaborado por SciData con datos de INEGI.",
    color=MapColors.GRAY,
    fontsize=10,
)  # Pie de gráfico
ax.set_axis_off()
ax = plt.gca()
plt.grid(False)
plt.tight_layout(rect=[0, 0.05, 0.85, 0.95])


# Matriz inversa de distancias

# Cálculo de matriz inversa de la distancia

W_D_inv = DistanceBand.from_dataframe(
    mapa,
    threshold=9_000_000,
    binary=False,
    p=2,
    alpha=-2.0,
    ids="CVE_ENT",
)
W_D_inv.transform = NORMALIZE_BY_ROWS
# Matriz completa

W_D_inv_dense, ids = W_D_inv.full()

print("Dimensión de W:", W_D_inv_dense.shape)
W_D_inv_dense


# Re calcular la matriz sin ids

W_D_inv2 = DistanceBand.from_dataframe(
    mapa, threshold=9000000, binary=False, p=2, alpha=-2.0
)

# Normalizar filas

W_D_inv2.transform = "r"

## Visualización del mapa

fig, ax = plt.subplots(1, 1, figsize=(10, 5), dpi=500)
# Poligonos
mapa.plot(ax=ax, color="white", edgecolor="black")
# Conexiones reina
W_D_inv2.plot(
    mapa,
    edge_kws=dict(linewidth=1, color="red"),
    node_kws=dict(marker="*"),
    ax=ax,
)
plt.figtext(
    0.4,
    0.95,
    "Mapa de pesos espaciales de México\npor entidad federativa",
    fontweight="bold",
    color=MapColors.GRAY,
    ha="center",
    fontsize=14,
)  # Titulo
plt.figtext(
    0.4,
    0.87,
    "Método: Distancias - Distancia inversa",
    style="italic",
    color=MapColors.GRAY,
    ha="center",
    fontsize=12,
)  # Subtitulo
plt.figtext(
    0.05,
    0.05,
    "Fuente: Elaborado por SciData con datos de INEGI.",
    color=MapColors.GRAY,
    fontsize=10,
)  # Pie de gráfico
ax.set_axis_off()
ax = plt.gca()
plt.grid(False)
plt.tight_layout(rect=[0, 0.05, 0.85, 0.95])
