import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

# Cargar tiendas
df = pd.read_excel("data/tricot_tiendas.xlsx")
df.columns = [c.lower() for c in df.columns]

# Construir dirección completa
df["direccion_full"] = df["dirección"].astype(str) + ", " + df["ciudad / comuna"].astype(str) + ", Chile"

# Geocoder (OpenStreetMap)
geolocator = Nominatim(user_agent="tiendas_app")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

latitudes = []
longitudes = []

print("🚀 Geocodificando... (puede tardar unos minutos)")

for i, row in df.iterrows():
    try:
        location = geocode(row["direccion_full"])
        if location:
            latitudes.append(location.latitude)
            longitudes.append(location.longitude)
        else:
            latitudes.append(None)
            longitudes.append(None)
    except:
        latitudes.append(None)
        longitudes.append(None)

df["lat"] = latitudes
df["lng"] = longitudes

# Guardar resultado
df.to_excel("data/tricot_tiendas_geo.xlsx", index=False)

print("✅ Geocodificación lista → tricot_tiendas_geo.xlsx")