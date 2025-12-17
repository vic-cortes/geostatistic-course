import geopandas as gpd
import matplotlib.pyplot as plt
from geopandas.geodataframe import GeoDataFrame

from config import Config

map_: GeoDataFrame = gpd.read_file(Config.MEXICO_SHAPEFILE)
print(map_.head())


plt.figure(figsize=(15, 11), dpi=500)
map_.plot(facecolor="white", edgecolor="black")
plt.title("Proyección cartográfica de México\nDivisión política por entidad federativa")
plt.xlabel("Longitud")
plt.ylabel("Latitud")
plt.grid(True, alpha=0.3)
plt.show()
