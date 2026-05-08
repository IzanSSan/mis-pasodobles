import streamlit as st
import pandas as pd
import random
from streamlit_gsheets import GSheetsConnection

# Configuración de la página para móvil
st.set_page_config(page_title="Elección de pasodobles", page_icon="🎵")

# --- CONEXIÓN A GOOGLE SHEETS ---
# En lugar de la lista manual, leemos el Excel
conn = st.connection("gsheets", type=GSheetsConnection)

# Leemos los datos (indicando que queremos la hoja principal)
df = conn.read()

# Convertimos a diccionario para no romper el código del sorteo
PASODOBLES = {}
for index, row in df.iterrows():
    # Usamos .get para evitar errores si falta algún dato
    idx = int(row['ID'])
    nombre = str(row['Nombre'])
    tags_raw = str(row['Tags'])
    
    PASODOBLES[idx] = {
        "nombre": nombre,
        "tags": [t.strip().lower() for t in tags_raw.split(',')]
    }

# --- BASE DE DATOS COMPLETA REVISADA ---
# --- Desactivado -- PASODOBLES = {
#    1: {"nombre": "Alcalde i Músic", "tags": ["alegre", "pasacalle"]},
#    2: {"nombre": "Alegría Agostense", "tags": ["alegre", "facil"]},
#    3: {"nombre": "Alfara de Algimia", "tags": ["concierto"]},
#    4: {"nombre": "Amparito Roca", "tags": ["famoso", "alegre"]},
#    5: {"nombre": "Azcárraga", "tags": ["pasacalle", "clasico"]},
#    6: {"nombre": "Baidal", "tags": ["tradicional"]},
#    7: {"nombre": "Borosko", "tags": ["marchoso", "alegre"]},
#    8: {"nombre": "Campanera", "tags": ["popular", "alegre"]},
#    9: {"nombre": "Caridad Guardiola", "tags": ["torero"]},
#    10: {"nombre": "Churumbelerias", "tags": ["alegre", "concierto"]},
#    11: {"nombre": "Ecos Españoles", "tags": ["torero", "clasico"]},
#    12: {"nombre": "Eduardo Borrás", "tags": ["elegante"]},
#    13: {"nombre": "Educandos de Benejúzar", "tags": ["famoso", "facil", "alegre"]},
#    14: {"nombre": "El Abuelo", "tags": ["popular", "alegre"]},
#    15: {"nombre": "El Bequetero", "tags": ["fiesta", "alegre", "facil"]},
#    16: {"nombre": "El Gato Montés", "tags": ["famoso", "torero"]},
#    17: {"nombre": "El Tío Caniyitas", "tags": ["alegre"]},
#    18: {"nombre": "El Tío Ramón", "tags": ["popular", "alegre"]},
#    19: {"nombre": "El Tito", "tags": ["alegre", "facil"]},
#    20: {"nombre": "Farolero", "tags": ["torero"]},
#    21: {"nombre": "Febrer", "tags": ["concierto", "alegre"]},
#    22: {"nombre": "Fiesta en Benidorm", "tags": ["alegre", "popular"]},
#    23: {"nombre": "Jose Luis Valero", "tags": ["alegre"]},
#    24: {"nombre": "Juanito el Jarri", "tags": ["pasacalle"]},
#    25: {"nombre": "La Banda 2014", "tags": ["moderno", "alegre"]},
#    26: {"nombre": "La Vereda", "tags": ["alegre", "pasacalle"]},
#    27: {"nombre": "La Puerta Grande", "tags": ["torero", "famoso"]},
#    28: {"nombre": "L'Entrà", "tags": ["potente", "fiesta", "alegre"]},
#    29: {"nombre": "Martín García", "tags": ["elegante", "alegre"]},
#    30: {"nombre": "Miguel Crespo", "tags": ["tradicional", "elegante"]},
#    31: {"nombre": "Operador", "tags": ["facil", "alegre"]},
#    32: {"nombre": "Orgullo Santiaguista", "tags": ["fiesta", "alegre"]},
#    34: {"nombre": "Paquito el Chocolatero", "tags": ["fiesta", "famoso", "facil", "alegre"]},
#    35: {"nombre": "Pepe Antón", "tags": ["tradicional", "alegre"]},
#    36: {"nombre": "Pepe el Fester", "tags": ["fiesta", "alegre"]},
#    37: {"nombre": "Pérez Barceló", "tags": ["clasico", "alegre"]},
#    38: {"nombre": "Quelo", "tags": ["marchoso", "alegre"]},
#    39: {"nombre": "Ragón Falez", "tags": ["concierto", "alegre", "elegante"]},
#    40: {"nombre": "Tayo", "tags": ["pasacalle", "alegre"]},
#    41: {"nombre": "Tercio de Quites", "tags": ["torero", "elegante"]},
#    42: {"nombre": "Tomás Ferrús", "tags": ["potente", "alegre"]},
#    43: {"nombre": "Valencia", "tags": ["himno"]},
#    44: {"nombre": "Vicente Marín", "tags": ["marchoso", "alegre"]},
#    45: {"nombre": "Xàbia", "tags": ["famoso", "alegre"]},
#    46: {"nombre": "El Fallero", "tags": ["himno"]},
#    47: {"nombre": "Pepe Pons", "tags": ["pasacalle", "alegre"]}
# }

# Título visual
st.title("🎵 Generador de Repertorio")
# --- BOTÓN PARA CONSULTAR LA LISTA COMPLETA ---
with st.expander("📖 CONSULTAR ARCHIVO COMPLETO (47 Pasodobles)"):
    # Creamos dos columnas para que la lista no sea un "chorizo" infinito hacia abajo
    col1, col2 = st.columns(2)
    
    # Dividimos los pasodobles en dos grupos para mostrarlos
    mitad = len(PASODOBLES) // 2 + 1
    
    with col1:
        for i in range(1, mitad):
            if i in PASODOBLES:
                st.write(f"**{i}.** {PASODOBLES[i]['nombre']}")
                
    with col2:
        for i in range(mitad, 48):
            if i in PASODOBLES:
                st.write(f"**{i}.** {PASODOBLES[i]['nombre']}")
st.markdown("### Selección de Pasodobles")

# Filtros en la barra lateral o principal
modo = st.selectbox(
    "¿Qué tipo de acto es?",
    ["Todo el archivo", "Pasacalle Alegre (Sin himnos)", "Sólo Fáciles", "Estilo Torero", "Pasacalle Elegante"]
)

cantidad = st.number_input("¿Cuántos pasodobles necesitas?", min_value=1, max_value=10, value=4)

if st.button("🔀 GENERAR SORTEO", use_container_width=True):
    # Lógica de filtrado
    candidatos = []
    filtro_map = {
        "Pasacalle Alegre (Sin himnos)": "alegre",
        "Sólo Fáciles": "facil",
        "Estilo Torero": "torero",
        "Pasacalle Elegante": "elegante"
    }
    
    tag_buscado = filtro_map.get(modo)
    
    for id_p, info in PASODOBLES.items():
        if tag_buscado in ["alegre", "facil"] and "himno" in info["tags"]:
            continue
        if modo == "Todo el archivo" or tag_buscado in info["tags"]:
            candidatos.append(info["nombre"])

    if len(candidatos) >= cantidad:
        seleccion = random.sample(candidatos, cantidad)
        
        st.success(f"Selección para: {modo}")
        for i, nombre in enumerate(seleccion, 1):
            st.markdown(f"### {i}. {nombre}")
        
        st.info("💡 Recordatorio: 2 vueltas + redoble de descanso")
    else:
        st.error("No hay suficientes pasodobles con ese filtro.")
