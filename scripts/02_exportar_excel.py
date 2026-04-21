import pandas as pd
import json
import h3

# ========================
# SOPORTES (desde JSON)
# ========================
with open("data/soportes_final.json") as f:
    soportes = pd.DataFrame(json.load(f))

# ------------------------
# NORMALIZAR COLUMNAS
# ------------------------
soportes.columns = [c.lower().strip() for c in soportes.columns]

# ------------------------
# CORREGIR COD_COMUNA (5 DÍGITOS)
# ------------------------
if "cod_comuna" in soportes.columns:
    soportes["cod_comuna"] = (
        pd.to_numeric(soportes["cod_comuna"], errors="coerce")
        .fillna(0)
        .astype(int)
        .astype(str)
        .str.zfill(5)
    )

# ------------------------
# CREAR TIPO SOPORTE
# ------------------------
def obtener_tipo(icon):
    if pd.isna(icon):
        return "otro"
    
    icon = str(icon).lower()

    if "billboard" in icon:
        return "billboard"
    elif "mall" in icon:
        return "mall"
    elif "bus" in icon:
        return "bus"
    elif "taxi" in icon:
        return "taxi"
    elif "subway" in icon:
        return "metro"
    elif "shelter" in icon:
        return "paradero"
    elif "digital" in icon:
        return "pantalla"
    elif "building" in icon:
        return "edificio"
    elif "supermarket" in icon:
        return "retail"
    else:
        return "otro"

if "icon" in soportes.columns:
    soportes["tipo_soporte"] = soportes["icon"].apply(obtener_tipo)
else:
    soportes["tipo_soporte"] = "otro"

# ------------------------
# CREAR CATEGORÍA
# ------------------------
def obtener_categoria(tipo):
    if tipo in ["bus", "taxi", "metro"]:
        return "transporte"
    elif tipo in ["mall", "retail"]:
        return "retail"
    elif tipo in ["pantalla"]:
        return "digital"
    elif tipo in ["billboard"]:
        return "tradicional"
    else:
        return "otros"

soportes["categoria"] = soportes["tipo_soporte"].apply(obtener_categoria)

# ------------------------
# OPCIONAL: ELIMINAR url/icon
# (DESCOMENTA SI QUIERES LIMPIAR)
# ------------------------
# soportes = soportes.loc[:, ~soportes.columns.str.lower().isin(["url", "icon"])]

# ------------------------
# ORDENAR COLUMNAS (SIN PERDER DATOS)
# ------------------------
columnas_inicio = [
    "lat", "lng", "comuna", "cod_comuna",
    "tipo_soporte", "categoria",
    "h3", "h6", "h8"
]

columnas_existentes = [c for c in columnas_inicio if c in soportes.columns]
otras = [c for c in soportes.columns if c not in columnas_existentes]

soportes = soportes[columnas_existentes + otras]

# ------------------------
# VALIDACIÓN
# ------------------------
print("\nColumnas finales soportes:")
print(soportes.columns.tolist())

if "cod_comuna" in soportes.columns:
    print("\nEjemplo cod_comuna:")
    print(soportes["cod_comuna"].drop_duplicates().head())

print("\nTipos de soporte:")
print(soportes["tipo_soporte"].value_counts())

print("\nCategorías:")
print(soportes["categoria"].value_counts())

# ------------------------
# EXPORTAR SOPORTES
# ------------------------
soportes.to_csv("data/soportes.csv", index=False)
soportes.to_excel("data/soportes.xlsx", index=False)

print(f"\n✅ Soportes exportados: {len(soportes)} registros")


# ========================
# TIENDAS (YA GEOCODIFICADAS)
# ========================
tiendas = pd.read_excel("data/tricot_tiendas_geo.xlsx")

# ------------------------
# NORMALIZAR COLUMNAS
# ------------------------
tiendas.columns = [c.lower().strip() for c in tiendas.columns]

# ------------------------
# DETECTAR LAT/LNG ROBUSTO
# ------------------------
posibles_lat = ["lat", "latitud", "latitude", "y"]
posibles_lng = ["lng", "lon", "longitud", "longitude", "x"]

lat_col = next((c for c in tiendas.columns if any(p in c for p in posibles_lat)), None)
lng_col = next((c for c in tiendas.columns if any(p in c for p in posibles_lng)), None)

if not lat_col or not lng_col:
    raise ValueError(f"No se encontraron columnas de coordenadas. Columnas disponibles: {tiendas.columns.tolist()}")

# ------------------------
# LIMPIAR COORDENADAS
# ------------------------
tiendas["lat"] = pd.to_numeric(tiendas[lat_col], errors="coerce")
tiendas["lng"] = pd.to_numeric(tiendas[lng_col], errors="coerce")

tiendas = tiendas.dropna(subset=["lat", "lng"])

# ------------------------
# GENERAR H3
# ------------------------
tiendas["h3"] = tiendas.apply(lambda x: h3.latlng_to_cell(x["lat"], x["lng"], 3), axis=1)
tiendas["h6"] = tiendas.apply(lambda x: h3.latlng_to_cell(x["lat"], x["lng"], 6), axis=1)
tiendas["h8"] = tiendas.apply(lambda x: h3.latlng_to_cell(x["lat"], x["lng"], 8), axis=1)

# ------------------------
# EXPORTAR TIENDAS
# ------------------------
tiendas.to_csv("data/tiendas.csv", index=False)
tiendas.to_excel("data/tiendas.xlsx", index=False)

print(f"✅ Tiendas exportadas: {len(tiendas)} registros")