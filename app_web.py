import streamlit as st
import random

# Configuración de la página para móvil
st.set_page_config(page_title="Elección de pasodobles", page_icon="🎵")

# --- BASE DE DATOS COMPLETA REVISADA ---
PASODOBLES = {
    1: {"nombre": "Alcalde i Músic", "tags": ["alegre", "pasacalle"]},
    2: {"nombre": "Alegría Agostense", "tags": ["alegre", "facil"]},
    3: {"nombre": "Alfara de Algimia", "tags": ["concierto"]},
    4: {"nombre": "Amparito Roca", "tags": ["famoso", "alegre"]},
    5: {"nombre": "Azcárraga", "tags": ["pasacalle", "clasico"]},
    6: {"nombre": "Baidal", "tags": ["tradicional"]},
    7: {"nombre": "Borosko", "tags": ["marchoso", "alegre"]},
    8: {"nombre": "Campanera", "tags": ["popular", "alegre"]},
    9: {"nombre": "Caridad Guardiola", "tags": ["torero"]},
    10: {"nombre": "Churumbelerias", "tags": ["alegre", "concierto"]},
    11: {"nombre": "Ecos Españoles", "tags": ["torero", "clasico"]},
    12: {"nombre": "Eduardo Borrás", "tags": ["elegante"]},
    13: {"nombre": "Educandos de Benejúzar", "tags": ["famoso", "facil", "alegre"]},
    14: {"nombre": "El Abuelo", "tags": ["popular"]},
    15: {"nombre": "El Bequetero", "tags": ["fiesta", "alegre", "facil"]},
    16: {"nombre": "El Gato Montés", "tags": ["famoso", "torero"]},
    17: {"nombre": "El Tío Caniyitas", "tags": ["alegre"]},
    18: {"nombre": "El Tío Ramón", "tags": ["popular", "alegre"]},
    19: {"nombre": "El Tito", "tags": ["alegre", "facil"]},
    20: {"nombre": "Farolero", "tags": ["torero"]},
    21: {"nombre": "Febrer", "tags": ["concierto"]},
    22: {"nombre": "Fiesta en Benidorm", "tags": ["alegre", "popular"]},
    23: {"nombre": "Jose Luis Valero", "tags": ["elegante"]},
    24: {"nombre": "Juanito el Jarri", "tags": ["pasacalle"]},
    25: {"nombre": "La Banda 2014", "tags": ["moderno", "alegre"]},
    26: {"nombre": "La Vereda", "tags": ["alegre", "pasacalle"]},
    27: {"nombre": "La Puerta Grande", "tags": ["torero", "famoso"]},
    28: {"nombre": "L'Entrà", "tags": ["potente", "fiesta", "alegre"]},
    29: {"nombre": "Martín García", "tags": ["elegante"]},
    30: {"nombre": "Miguel Crespo", "tags": ["tradicional"]},
    31: {"nombre": "Operador", "tags": ["facil", "alegre"]},
    32: {"nombre": "Orgullo Santiaguista", "tags": ["fiesta", "alegre"]},
    34: {"nombre": "Paquito el Chocolatero", "tags": ["fiesta", "famoso", "facil", "alegre"]},
    35: {"nombre": "Pepe Antón", "tags": ["tradicional"]},
    36: {"nombre": "Pepe el Fester", "tags": ["fiesta", "alegre"]},
    37: {"nombre": "Pérez Barceló", "tags": ["clasico"]},
    38: {"nombre": "Quelo", "tags": ["marchoso", "alegre"]},
    39: {"nombre": "Ragón Falez", "tags": ["concierto"]},
    40: {"nombre": "Tayo", "tags": ["pasacalle", "alegre"]},
    41: {"nombre": "Tercio de Quites", "tags": ["torero", "elegante"]},
    42: {"nombre": "Tomás Ferrús", "tags": ["potente", "alegre"]},
    43: {"nombre": "Valencia", "tags": ["himno"]},
    44: {"nombre": "Vicente Marín", "tags": ["marchoso", "alegre"]},
    45: {"nombre": "Xàbia", "tags": ["famoso", "alegre"]},
    46: {"nombre": "El Fallero", "tags": ["himno"]},
    47: {"nombre": "Pepe Pons", "tags": ["pasacalle", "alegre"]}
}

# Título visual
st.title("🎵 Generador de Repertorio")
st.markdown("### Selección de Pasodobles")

# Filtros en la barra lateral o principal
modo = st.selectbox(
    "¿Qué tipo de acto es?",
    ["Todo el archivo", "Pasacalle Alegre (Sin himnos)", "Sólo Fáciles", "Estilo Torero"]
)

cantidad = st.number_input("¿Cuántos pasodobles necesitas?", min_value=1, max_value=10, value=4)

if st.button("🔀 GENERAR SORTEO", use_container_width=True):
    # Lógica de filtrado
    candidatos = []
    filtro_map = {
        "Pasacalle Alegre (Sin himnos)": "alegre",
        "Sólo Fáciles": "facil",
        "Estilo Torero": "torero"
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
