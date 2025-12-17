import geopandas as gpd

from config import Config

map = gpd.read_file(Config.MEXICO_SHAPEFILE)

print(map.head())
