import urllib.request
import re

ORIGEN = "https://romaxa55.github.io/world_ip_tv/output/index.m3u"
SALIDA = "canales_por_pais.m3u"

MAPEO = {
    # Brasil
    "Brazil": "Brazil",
    "Roraima": "Brazil",
    "Goias": "Brazil",
    "Sao Paulo": "Brazil",
    "Rio de Janeiro": "Brazil",
    "Santa Catarina": "Brazil",
    "Rio Grande do Sul": "Brazil",
    "Rio Grande do Norte": "Brazil",
    "Minas Gerais": "Brazil",
    "Parana": "Brazil",
    "Espirito Santo": "Brazil",
    "Rondonia": "Brazil",
    "Ceara": "Brazil",
    "Bahia": "Brazil",
    "Alagoas": "Brazil",
    "Amazonas": "Brazil",
    "Distrito Federal": "Brazil",
    "Paraiba": "Brazil",
    "Para": "Brazil",
    "Maranhao": "Brazil",
    "Mato Grosso": "Brazil",
    "Pernambuco": "Brazil",

    # Argentina
    "Argentina": "Argentina",
    "Buenos Aires": "Argentina",
    "Mendoza": "Argentina",
    "Rio Negro": "Argentina",
    "Santa Fe": "Argentina",
    "Cordoba": "Argentina",
    "Chaco": "Argentina",
    "Misiones": "Argentina",
    "Salta": "Argentina",
    "Jujuy": "Argentina",
    "Neuquen": "Argentina",
    "Chubut": "Argentina",
    "San Juan": "Argentina",
    "San Luis": "Argentina",
    "Santiago del Estero": "Argentina",
    "Tucuman": "Argentina",
    "Entre Rios": "Argentina",
    "Formosa": "Argentina",
    "Catamarca": "Argentina",
    "La Pampa": "Argentina",
    "Ciudad Autonoma de Buenos Aires": "Argentina",
    "Corrientes": "Argentina",

    # Colombia
    "Colombia": "Colombia",
    "Cundinamarca": "Colombia",
    "Risaralda": "Colombia",
    "Quindio": "Colombia",
    "Caldas": "Colombia",
    "Magdalena": "Colombia",
    "Valle del Cauca": "Colombia",
    "Antioquia": "Colombia",
    "Huila": "Colombia",
    "Tolima": "Colombia",
    "Atlantico": "Colombia",
    "Cauca": "Colombia",
    "Choco": "Colombia",
    "Narino": "Colombia",
    "Norte de Santander": "Colombia",
    "San Andres, Providencia y Santa Catalina": "Colombia",

    # España
    "Spain": "Spain",
    "Asturias, Principado de": "Spain",
    "Castilla y Leon": "Spain",
    "Extremadura": "Spain",
    "Ceuta": "Spain",
    "La Rioja": "Spain",
    "Andalucia": "Spain",
    "Valenciana, Comunidad": "Spain",
    "Catalunya": "Spain",
    "Pais Vasco": "Spain",
    "Canarias": "Spain",
    "Castilla-La Mancha": "Spain",
    "Madrid, Comunidad de": "Spain",
    "Galicia": "Spain",
    "Illes Balears": "Spain",
    "Murcia, Region de": "Spain",
    "Navarra, Comunidad Foral de": "Spain",
    "Aragon": "Spain",

    # México
    "Mexico": "Mexico",
    "Tamaulipas": "Mexico",
    "Jalisco": "Mexico",
    "Guerrero": "Mexico",
    "Veracruz de Ignacio de la Llave": "Mexico",
    "Guanajuato": "Mexico",
    "Sinaloa": "Mexico",
    "Zacatecas": "Mexico",
    "Sonora": "Mexico",
    "Chihuahua": "Mexico",
    "Yucatan": "Mexico",
    "San Luis Potosi": "Mexico",
    "Ciudad de Mexico": "Mexico",
    "Coahuila de Zaragoza": "Mexico",
    "Baja California": "Mexico",
    "Aguascalientes": "Mexico",
    "Nuevo Leon": "Mexico",
    "Morelos": "Mexico",
    "Puebla": "Mexico",
    "Quintana Roo": "Mexico",
    "Queretaro": "Mexico",
    "Durango": "Mexico",

    # Chile
    "Chile": "Chile",
    "Los Lagos": "Chile",
    "Nuble": "Chile",
    "Coquimbo": "Chile",
    "Valparaiso": "Chile",
    "Biobio": "Chile",
    "Atacama": "Chile",
    "Maule": "Chile",
    "La Araucania": "Chile",
    "Libertador General Bernardo O'Higgins": "Chile",
    "Santiago": "Chile",

    # Perú
    "Peru": "Peru",
    "Ancash": "Peru",
    "Junin": "Peru",
    "Lima": "Peru",
    "Ucayali": "Peru",
    "Apurimac": "Peru",
    "Arequipa": "Peru",
    "Cusco": "Peru",
    "Ayacucho": "Peru",
    "Puno": "Peru",
    "Moquegua": "Peru",
    "Loreto": "Peru",

    # Venezuela
    "Venezuela": "Venezuela",
    "Aragua": "Venezuela",
    "Bolivar": "Venezuela",
    "Lara": "Venezuela",

    # República Dominicana
    "Dominican Republic": "Dominican Republic",
    "Distrito Nacional (Santo Domingo)": "Dominican Republic",
    "La Altagracia": "Dominican Republic",
    "Puerto Plata": "Dominican Republic",
    "Valverde": "Dominican Republic",
    "Monsenor Nouel": "Dominican Republic",
    "La Vega": "Dominican Republic",

    # Estados Unidos
    "United States": "United States",
    "California": "United States",
    "Florida": "United States",
    "Texas": "United States",
    "New York": "United States",
    "Arizona": "United States",
    "Nevada": "United States",
    "Pennsylvania": "United States",
    "Massachusetts": "United States",
    "Illinois": "United States",
    "Connecticut": "United States",
    "Hawaii": "United States",
    "New Jersey": "United States",
    "Maryland": "United States",
    "Michigan": "United States",
    "Wisconsin": "United States",
    "Kentucky": "United States",
    "Oregon": "United States",
    "Missouri": "United States",
    "North Carolina": "United States",
    "Ohio": "United States",
    "South Carolina": "United States",
    "Louisiana": "United States",
    "Washington": "United States",
    "Tennessee": "United States",
    "Delaware": "United States",
    "Oklahoma": "United States",
    "North Dakota": "United States",
    "Alaska": "United States",
    "Mississippi": "United States",
    "Kansas": "United States",
    "Arkansas": "United States",
    "Virginia": "United States",
    "Utah": "United States",
    "Rhode Island": "United States",
    "Indiana": "United States",
    "Idaho": "United States",
    "Alabama": "United States",
    "New Mexico": "United States",
    "Nebraska": "United States",
    "Iowa": "United States",
    "Maine": "United States",
    "Montana": "United States",
    "Minnesota": "United States",
    "New Hampshire": "United States",
    "District of Columbia": "United States"
}

PAISES_PERMITIDOS = {
    "Brazil",
    "Venezuela",
    "Colombia",
    "Argentina",
    "Chile",
    "Peru",
    "Mexico",
    "Ecuador",
    "Bolivia",
    "Paraguay",
    "Uruguay",
    "Costa Rica",
    "Panama",
    "Guatemala",
    "Honduras",
    "El Salvador",
    "Nicaragua",
    "Dominican Republic",
    "Puerto Rico",
    "Cuba",
    "Spain",
    "Russia",
}

PATRONES_DEPORTIVOS = [
    "espn",
    "fox sports",
    "tnt sports",
    "tyc sports",
    "dsports",
    "directv sports",
    "win sports",
    "win+ futbol",
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
]

EXCLUSIONES_DEPORTES = [
    "cine premiere",
    "paris premiere",
    "viju+ premiere",
]

def es_deportivo(nombre):
    nombre_limpio = nombre.lower()

    nombre_limpio = re.sub(r'\([^)]*\)', '', nombre_limpio)
    nombre_limpio = re.sub(r'\[[^\]]*\]', '', nombre_limpio)
    nombre_limpio = nombre_limpio.strip()

    if any(exclusion in nombre_limpio for exclusion in EXCLUSIONES_DEPORTES):
        return False

    return any(
        patron in nombre_limpio
        for patron in PATRONES_DEPORTIVOS
    )

print("Descargando lista original...")

with urllib.request.urlopen(ORIGEN) as respuesta:
    contenido = respuesta.read().decode("utf-8", errors="ignore")

lineas = contenido.splitlines()

salida = ["#EXTM3U"]

for i, linea in enumerate(lineas):
    if not linea.startswith("#EXTINF"):
        continue

    match = re.search(r'group-title="([^"]*)"', linea)

    if not match:
        continue

    grupo_original = match.group(1)
    nuevo_grupo = MAPEO.get(grupo_original, grupo_original)

    if nuevo_grupo not in PAISES_PERMITIDOS:
        continue

    nombre_canal = linea.split(",", 1)[-1].strip()

    if es_deportivo(nombre_canal):
    nuevo_grupo = "⚽ Deportes"

    linea_nueva = re.sub(
        r'group-title="[^"]*"',
        f'group-title="{nuevo_grupo}"',
        linea
    )

    salida.append(linea_nueva)

    if i + 1 < len(lineas):
        salida.append(lineas[i + 1])

with open(SALIDA, "w", encoding="utf-8") as f:
    f.write("\n".join(salida) + "\n")

print(f"Lista generada: {SALIDA}")
