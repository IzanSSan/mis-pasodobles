import streamlit as st
import random

# Configuración de la página para móvil
st.set_page_config(page_title="Sorteo Pasodobles 2025", page_icon="🎵")

# --- BASE DE DATOS (Misma que antes) ---
PASODOBLES = {
    1: {"nombre": "Alcalde i Músic", "tags": ["alegre", "pasacalle"]},
    2: {"nombre": "Alegría Agostense", "tags": ["alegre", "facil"]},
    3: {"nombre": "Alfara de Algimia", "tags": ["concierto"]},
    4: {"nombre": "Amparito Roca", "tags": ["famoso", "alegre"]},
    # ... (Aquí irían los 47, asegúrate de copiar el diccionario completo del código anterior)
}

# Título visual
st.title("🎵 Generador de Repertorio")
st.markdown("### Selección de Pasodobles 2025")

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