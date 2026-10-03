import urllib.request
import re
import unicodedata

ORIGEN = "https://romaxa55.github.io/world_ip_tv/output/index.m3u"
SALIDA = "canales_por_pais.m3u"

# =========================================================
# MAPEO DE REGIONES / ESTADOS / PROVINCIAS A PAÍS
# =========================================================

MAPEO = {
    # Brasil
    "Brazil": "Brazil",
    "Acre": "Brazil",
    "Alagoas": "Brazil",
    "Amapa": "Brazil",
    "Amazonas": "Brazil",
    "Bahia": "Brazil",
    "Ceara": "Brazil",
    "Distrito Federal": "Brazil",
    "Espirito Santo": "Brazil",
    "Goias": "Brazil",
    "Maranhao": "Brazil",
    "Mato Grosso": "Brazil",
    "Mato Grosso do Sul": "Brazil",
    "Minas Gerais": "Brazil",
    "Para": "Brazil",
    "Paraiba": "Brazil",
    "Parana": "Brazil",
    "Pernambuco": "Brazil",
    "Piaui": "Brazil",
    "Rio de Janeiro": "Brazil",
    "Rio Grande do Norte": "Brazil",
    "Rio Grande do Sul": "Brazil",
    "Rondonia": "Brazil",
    "Roraima": "Brazil",
    "Santa Catarina": "Brazil",
    "Sao Paulo": "Brazil",
    "Sergipe": "Brazil",
    "Tocantins": "Brazil",

    # Argentina
    "Argentina": "Argentina",
    "Buenos Aires": "Argentina",
    "Catamarca": "Argentina",
    "Chaco": "Argentina",
    "Chubut": "Argentina",
    "Ciudad Autonoma de Buenos Aires": "Argentina",
    "Cordoba": "Argentina",
    "Corrientes": "Argentina",
    "Entre Rios": "Argentina",
    "Formosa": "Argentina",
    "Jujuy": "Argentina",
    "La Pampa": "Argentina",
    "La Rioja": "Argentina",
    "Mendoza": "Argentina",
    "Misiones": "Argentina",
    "Neuquen": "Argentina",
    "Rio Negro": "Argentina",
    "Salta": "Argentina",
    "San Juan": "Argentina",
    "San Luis": "Argentina",
    "Santa Cruz": "Argentina",
    "Santa Fe": "Argentina",
    "Santiago del Estero": "Argentina",
    "Tierra del Fuego": "Argentina",
    "Tucuman": "Argentina",

    # Colombia
    "Colombia": "Colombia",
    "Amazonas": "Colombia",
    "Antioquia": "Colombia",
    "Arauca": "Colombia",
    "Atlantico": "Colombia",
    "Bolivar": "Colombia",
    "Boyaca": "Colombia",
    "Caldas": "Colombia",
    "Caqueta": "Colombia",
    "Casanare": "Colombia",
    "Cauca": "Colombia",
    "Cesar": "Colombia",
    "Choco": "Colombia",
    "Cordoba": "Colombia",
    "Cundinamarca": "Colombia",
    "Guainia": "Colombia",
    "Guaviare": "Colombia",
    "Huila": "Colombia",
    "La Guajira": "Colombia",
    "Magdalena": "Colombia",
    "Meta": "Colombia",
    "Narino": "Colombia",
    "Norte de Santander": "Colombia",
    "Putumayo": "Colombia",
    "Quindio": "Colombia",
    "Risaralda": "Colombia",
    "San Andres, Providencia y Santa Catalina": "Colombia",
    "Santander": "Colombia",
    "Sucre": "Colombia",
    "Tolima": "Colombia",
    "Valle del Cauca": "Colombia",
    "Vaupes": "Colombia",
    "Vichada": "Colombia",

    # España
    "Spain": "Spain",
    "Andalucia": "Spain",
    "Aragon": "Spain",
    "Asturias, Principado de": "Spain",
    "Canarias": "Spain",
    "Cantabria": "Spain",
    "Castilla-La Mancha": "Spain",
    "Castilla y Leon": "Spain",
    "Catalunya": "Spain",
    "Ceuta": "Spain",
    "Extremadura": "Spain",
    "Galicia": "Spain",
    "Illes Balears": "Spain",
    "La Rioja": "Spain",
    "Madrid, Comunidad de": "Spain",
    "Melilla": "Spain",
    "Murcia, Region de": "Spain",
    "Navarra, Comunidad Foral de": "Spain",
    "Pais Vasco": "Spain",
    "Valenciana, Comunidad": "Spain",

    # México
    "Mexico": "Mexico",
    "Aguascalientes": "Mexico",
    "Baja California": "Mexico",
    "Baja California Sur": "Mexico",
    "Campeche": "Mexico",
    "Chiapas": "Mexico",
    "Chihuahua": "Mexico",
    "Ciudad de Mexico": "Mexico",
    "Coahuila de Zaragoza": "Mexico",
    "Colima": "Mexico",
    "Durango": "Mexico",
    "Guanajuato": "Mexico",
    "Guerrero": "Mexico",
    "Hidalgo": "Mexico",
    "Jalisco": "Mexico",
    "Mexico State": "Mexico",
    "Michoacan de Ocampo": "Mexico",
    "Morelos": "Mexico",
    "Nayarit": "Mexico",
    "Nuevo Leon": "Mexico",
    "Oaxaca": "Mexico",
    "Puebla": "Mexico",
    "Queretaro": "Mexico",
    "Quintana Roo": "Mexico",
    "San Luis Potosi": "Mexico",
    "Sinaloa": "Mexico",
    "Sonora": "Mexico",
    "Tabasco": "Mexico",
    "Tamaulipas": "Mexico",
    "Tlaxcala": "Mexico",
    "Veracruz de Ignacio de la Llave": "Mexico",
    "Yucatan": "Mexico",
    "Zacatecas": "Mexico",

    # Chile
    "Chile": "Chile",
    "Antofagasta": "Chile",
    "Atacama": "Chile",
    "Aysen": "Chile",
    "Biobio": "Chile",
    "Coquimbo": "Chile",
    "La Araucania": "Chile",
    "Libertador General Bernardo O'Higgins": "Chile",
    "Los Lagos": "Chile",
    "Los Rios": "Chile",
    "Magallanes": "Chile",
    "Maule": "Chile",
    "Nuble": "Chile",
    "Santiago": "Chile",
    "Tarapaca": "Chile",
    "Valparaiso": "Chile",

    # Perú
    "Peru": "Peru",
    "Amazonas": "Peru",
    "Ancash": "Peru",
    "Apurimac": "Peru",
    "Arequipa": "Peru",
    "Ayacucho": "Peru",
    "Cajamarca": "Peru",
    "Callao": "Peru",
    "Cusco": "Peru",
    "Huancavelica": "Peru",
    "Huanuco": "Peru",
    "Ica": "Peru",
    "Junin": "Peru",
    "La Libertad": "Peru",
    "Lambayeque": "Peru",
    "Lima": "Peru",
    "Loreto": "Peru",
    "Madre de Dios": "Peru",
    "Moquegua": "Peru",
    "Pasco": "Peru",
    "Piura": "Peru",
    "Puno": "Peru",
    "San Martin": "Peru",
    "Tacna": "Peru",
    "Tumbes": "Peru",
    "Ucayali": "Peru",

    # Venezuela
    "Venezuela": "Venezuela",
    "Amazonas": "Venezuela",
    "Anzoategui": "Venezuela",
    "Apure": "Venezuela",
    "Aragua": "Venezuela",
    "Barinas": "Venezuela",
    "Bolivar": "Venezuela",
    "Carabobo": "Venezuela",
    "Cojedes": "Venezuela",
    "Delta Amacuro": "Venezuela",
    "Distrito Capital": "Venezuela",
    "Falcon": "Venezuela",
    "Guarico": "Venezuela",
    "Lara": "Venezuela",
    "Merida": "Venezuela",
    "Miranda": "Venezuela",
    "Monagas": "Venezuela",
    "Nueva Esparta": "Venezuela",
    "Portuguesa": "Venezuela",
    "Sucre": "Venezuela",
    "Tachira": "Venezuela",
    "Trujillo": "Venezuela",
    "Vargas": "Venezuela",
    "Yaracuy": "Venezuela",
    "Zulia": "Venezuela",

    # Ecuador
    "Ecuador": "Ecuador",
    "Azuay": "Ecuador",
    "Bolivar": "Ecuador",
    "Canar": "Ecuador",
    "Carchi": "Ecuador",
    "Chimborazo": "Ecuador",
    "Cotopaxi": "Ecuador",
    "El Oro": "Ecuador",
    "Esmeraldas": "Ecuador",
    "Galapagos": "Ecuador",
    "Guayas": "Ecuador",
    "Imbabura": "Ecuador",
    "Loja": "Ecuador",
    "Los Rios": "Ecuador",
    "Manabi": "Ecuador",
    "Morona Santiago": "Ecuador",
    "Napo": "Ecuador",
    "Orellana": "Ecuador",
    "Pastaza": "Ecuador",
    "Pichincha": "Ecuador",
    "Santa Elena": "Ecuador",
    "Santo Domingo de los Tsachilas": "Ecuador",
    "Sucumbios": "Ecuador",
    "Tungurahua": "Ecuador",
    "Zamora Chinchipe": "Ecuador",

    # Bolivia
    "Bolivia": "Bolivia",
    "Beni": "Bolivia",
    "Chuquisaca": "Bolivia",
    "Cochabamba": "Bolivia",
    "La Paz": "Bolivia",
    "Oruro": "Bolivia",
    "Pando": "Bolivia",
    "Potosi": "Bolivia",
    "Santa Cruz": "Bolivia",
    "Tarija": "Bolivia",

    # Paraguay
    "Paraguay": "Paraguay",
    "Alto Parana": "Paraguay",
    "Boqueron": "Paraguay",
    "Caaguazu": "Paraguay",
    "Central": "Paraguay",
    "Itapua": "Paraguay",
    "Presidente Hayes": "Paraguay",

    # Uruguay
    "Uruguay": "Uruguay",

    # Costa Rica
    "Costa Rica": "Costa Rica",
    "Puntarenas": "Costa Rica",
    "San Jose": "Costa Rica",

    # Panamá
    "Panama": "Panama",

    # Guatemala
    "Guatemala": "Guatemala",
    "Escuintla": "Guatemala",
    "Huehuetenango": "Guatemala",
    "Izabal": "Guatemala",
    "Quiche": "Guatemala",
    "Sacatepequez": "Guatemala",
    "San Marcos": "Guatemala",
    "Santa Rosa": "Guatemala",
    "Solola": "Guatemala",
    "Totonicapan": "Guatemala",

    # Honduras
    "Honduras": "Honduras",

    # El Salvador
    "El Salvador": "El Salvador",

    # Nicaragua
    "Nicaragua": "Nicaragua",

    # República Dominicana
    "Dominican Republic": "Dominican Republic",
    "Distrito Nacional (Santo Domingo)": "Dominican Republic",
    "La Altagracia": "Dominican Republic",
    "La Vega": "Dominican Republic",
    "Monsenor Nouel": "Dominican Republic",
    "Puerto Plata": "Dominican Republic",
    "Valverde": "Dominican Republic",

    # Puerto Rico
    "Puerto Rico": "Puerto Rico",

    # Cuba
    "Cuba": "Cuba",

    # Rusia
    "Russia": "Russia",
}

PAISES_PERMITIDOS = {
    "Argentina",
    "Bolivia",
    "Brazil",
    "Chile",
    "Colombia",
    "Costa Rica",
    "Cuba",
    "Dominican Republic",
    "Ecuador",
    "El Salvador",
    "Guatemala",
    "Honduras",
    "Mexico",
    "Nicaragua",
    "Panama",
    "Paraguay",
    "Peru",
    "Puerto Rico",
    "Russia",
    "Spain",
    "Uruguay",
    "Venezuela",
}

# =========================================================
# DETECCIÓN DE CANALES DEPORTIVOS
# =========================================================

PATRONES_DEPORTIVOS = [
    "espn",
    "fox sports",
    "fox deportes",
    "tnt sports",
    "tyc sports",
    "dsports",
    "directv sports",
    "win sports",
    "win+",
    "tigo sports",
    "goltv",
    "gol tv",
    "sportv",
    "bandsports",
    "teledeporte",
    "claro sports",
    "aym sports",
    "azteca deportes",
    "itv deportes",
    "px sports",
    "n sports",
    "as3 sport",
    "setanta sports",
    "trace sport",
    "viju+ sport",
    "okko sport",
    "okko prajm sport",
    "okko futbol",
    "sportivnyy",
    "astrahan.ru sport",
    "mma-tv",
    "hard knocks fighting championship",
    "tna wrestling",
    "red bull tv",
    "futbol",
    "fútbol",
    "football",
    "soccer",
    "deportes",
    "sports",
    "tennis",
    "tenis",
    "golf",
    "basket",
    "nba",
    "nfl",
    "nhl",
    "mlb",
    "ufc",
    "mma",
    "wrestling",
    "boxing",
    "boxeo",
    "motorsport",
    "motor sport",
    "formula 1",
    "fórmula 1",
]

EXCLUSIONES_DEPORTES = [
    "cine premiere",
    "paris premiere",
    "viju+ premiere",
]

NOMBRES_DEPORTIVOS_EXACTOS = {
    "premiere",
    "premiere 2",
    "premiere 3",
    "premiere 4",
    "premiere 5",
    "premiere 6",
    "premiere 7",
    "premiere 8",
    "premiere clubes",
}

# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

def normalizar_texto(texto):
    texto = unicodedata.normalize("NFKD", texto or "")
    texto = "".join(
        c for c in texto
        if not unicodedata.combining(c)
    )
    return texto.casefold().strip()


def limpiar_nombre_tecnico(nombre):
    texto = normalizar_texto(nombre)

    # Quita notas entre () y [].
    texto = re.sub(r"\([^)]*\)", "", texto)
    texto = re.sub(r"\[[^\]]*\]", "", texto)

    # Quita etiquetas de calidad habituales.
    texto = re.sub(
        r"\b(8k|4k|uhd|fhd|full hd|hd|sd|2160p|1440p|1080p|720p|576p|540p|480p|360p)\b",
        "",
        texto,
    )

    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def extraer_nombre_canal(linea_extinf):
    # La coma que separa metadata del nombre debe estar fuera de comillas.
    partes = re.split(
        r',(?=(?:[^"]*"[^"]*")*[^"]*$)',
        linea_extinf,
        maxsplit=1,
    )

    if len(partes) == 2:
        return partes[1].strip()

    return ""


def es_deportivo(nombre):
    nombre_normalizado = limpiar_nombre_tecnico(nombre)

    if any(
        normalizar_texto(exclusion) in nombre_normalizado
        for exclusion in EXCLUSIONES_DEPORTES
    ):
        return False

    if nombre_normalizado in {
        normalizar_texto(x)
        for x in NOMBRES_DEPORTIVOS_EXACTOS
    }:
        return True

    return any(
        normalizar_texto(patron) in nombre_normalizado
        for patron in PATRONES_DEPORTIVOS
    )


def puntuacion_calidad(nombre):
    nombre = normalizar_texto(nombre)

    if "4320p" in nombre or "8k" in nombre:
        return 8
    if "2160p" in nombre or "4k" in nombre or "uhd" in nombre:
        return 7
    if "1440p" in nombre:
        return 6
    if "1080p" in nombre or "fhd" in nombre or "full hd" in nombre:
        return 5
    if "720p" in nombre or re.search(r"\bhd\b", nombre):
        return 4
    if "576p" in nombre:
        return 3
    if "540p" in nombre:
        return 2
    if "480p" in nombre:
        return 1

    return 0


def clave_orden(texto):
    return normalizar_texto(texto)


def orden_categoria(grupo):
    # Deportes arriba; luego países en orden alfabético.
    if grupo == "⚽ Deportes":
        return (0, "")
    return (1, clave_orden(grupo))


# =========================================================
# DESCARGAR FUENTE
# =========================================================

print("Descargando lista original...")

request = urllib.request.Request(
    ORIGEN,
    headers={"User-Agent": "Mozilla/5.0"},
)

with urllib.request.urlopen(request, timeout=60) as respuesta:
    contenido = respuesta.read().decode("utf-8", errors="ignore")

lineas = contenido.splitlines()

# =========================================================
# PROCESAR CANALES
# =========================================================

canales = []

for i, linea in enumerate(lineas):
    if not linea.startswith("#EXTINF"):
        continue

    match = re.search(r'group-title="([^"]*)"', linea)
    if not match:
        continue

    grupo_original = match.group(1)
    nuevo_grupo = MAPEO.get(grupo_original, grupo_original)

    # Filtrar antes de categorizar.
    if nuevo_grupo not in PAISES_PERMITIDOS:
        continue

    nombre_canal = extraer_nombre_canal(linea)
    if not nombre_canal:
        continue

    # La URL normalmente es la siguiente línea no vacía.
    url = ""
    j = i + 1

    while j < len(lineas):
        candidata = lineas[j].strip()

        if candidata and not candidata.startswith("#"):
            url = candidata
            break

        if candidata.startswith("#EXTINF"):
            break

        j += 1

    if not url:
        continue

    if es_deportivo(nombre_canal):
        nuevo_grupo = "⚽ Deportes"

    linea_nueva = re.sub(
        r'group-title="[^"]*"',
        f'group-title="{nuevo_grupo}"',
        linea,
    )

    canales.append({
        "grupo": nuevo_grupo,
        "nombre": nombre_canal,
        "linea": linea_nueva,
        "url": url,
        "calidad": puntuacion_calidad(nombre_canal),
    })

# =========================================================
# ELIMINAR DUPLICADOS
# =========================================================

canales_unicos = {}

for canal in canales:
    # La clave ignora resolución/calidad, pero respeta categoría y nombre base.
    clave = (
        normalizar_texto(canal["grupo"]),
        limpiar_nombre_tecnico(canal["nombre"]),
    )

    if clave not in canales_unicos:
        canales_unicos[clave] = canal
        continue

    actual = canales_unicos[clave]

    # Si hay varias versiones del mismo canal, conservar la de mayor calidad.
    if canal["calidad"] > actual["calidad"]:
        canales_unicos[clave] = canal

canales = list(canales_unicos.values())

# =========================================================
# ORDENAR
# =========================================================

canales.sort(
    key=lambda canal: (
        orden_categoria(canal["grupo"]),
        clave_orden(canal["nombre"]),
    )
)

# =========================================================
# GENERAR M3U
# =========================================================

salida = ["#EXTM3U"]

for canal in canales:
    salida.append(canal["linea"])
    salida.append(canal["url"])

with open(SALIDA, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(salida) + "\n")

# =========================================================
# ESTADÍSTICAS EN EL LOG DE GITHUB ACTIONS
# =========================================================

grupos = {}

for canal in canales:
    grupos[canal["grupo"]] = grupos.get(canal["grupo"], 0) + 1

print()
print("Lista generada correctamente.")
print(f"Archivo: {SALIDA}")
print(f"Canales finales: {len(canales)}")
print()
print("Canales por categoría:")

for grupo in sorted(grupos, key=orden_categoria):
    print(f"  {grupo}: {grupos[grupo]}")
