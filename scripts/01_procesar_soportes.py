import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import h3

# ========================
# ARCHIVOS
# ========================
INPUT = "data/soportes_vista_actual.csv"
COMUNAS = "data/comunas.geojson"

OUTPUT_JSON = "data/soportes_final.json"

# ========================
# CARGAR SOPORTES
# ========================
df = pd.read_csv(INPUT)

# Normalizar nombres (por si vienen distintos)
df.columns = [c.lower() for c in df.columns]

# Detectar columnas lat/lng automáticamente
lat_col = [c for c in df.columns if "lat" in c][0]
lng_col = [c for c in df.columns if "lon" in c or "lng" in c][0]

df["lat"] = pd.to_numeric(df[lat_col], errors="coerce")
df["lng"] = pd.to_numeric(df[lng_col], errors="coerce")

df = df.dropna(subset=["lat","lng"])

print(f"Registros válidos: {len(df)}")

# ========================
# GEO DATAFRAME
# ========================
geometry = [Point(xy) for xy in zip(df["lng"], df["lat"])]

gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# ========================
# COMUNAS
# ========================
comunas = gpd.read_file(COMUNAS)
comunas = comunas.to_crs(epsg=4326)

# ========================
# ASIGNAR COMUNA (ROBUSTO)
# ========================
gdf = gpd.sjoin_nearest(gdf, comunas, how="left")

# detectar campo comuna
campo = None
for c in gdf.columns:
    if "nom_com" in c.lower() or "comuna" in c.lower():
        campo = c
        break

if campo:
    gdf["comuna"] = gdf[campo]
else:
    gdf["comuna"] = "Sin comuna"

gdf["comuna"] = gdf["comuna"].fillna("Sin comuna")

# ========================
# H3
# ========================
gdf["h3"] = gdf.apply(lambda x: h3.latlng_to_cell(x["lat"], x["lng"], 3), axis=1)
gdf["h6"] = gdf.apply(lambda x: h3.latlng_to_cell(x["lat"], x["lng"], 6), axis=1)
gdf["h8"] = gdf.apply(lambda x: h3.latlng_to_cell(x["lat"], x["lng"], 8), axis=1)

# ========================
# LIMPIEZA
# ========================
gdf = gdf.drop(columns=["geometry"], errors="ignore")

# ========================
# EXPORTAR
# ========================
gdf.to_json(OUTPUT_JSON, orient="records", indent=2)

print("🔥 SOPORTES LISTOS → soportes_final.json")