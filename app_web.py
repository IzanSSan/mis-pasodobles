import streamlit as st
import pandas as pd
import random
from streamlit_gsheets import GSheetsConnection

# Configuración de la página para móvil
st.set_page_config(page_title="Elección de pasodobles", page_icon="🎵")

# --- CONEXIÓN A GOOGLE SHEETS ---
@st.cache_data(ttl=10)
def cargar_datos_sheet():
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn.read()

df = cargar_datos_sheet()

# --- PROCESAMIENTO DE DATOS ---
PASODOBLES = {}
df_limpio = df.dropna(subset=['Nombre'])

for index, row in df_limpio.iterrows():
    try:
        idx = int(row['ID'])
        nombre = str(row['Nombre']).strip()
        tags_raw = str(row['Tags']) if pd.notna(row['Tags']) else ""
        
        # Leemos duración: si no existe la columna o está vacía, ponemos 3.5 min
        duracion = float(row['Duracion']) if 'Duracion' in row and pd.notna(row['Duracion']) else 3.5
        
        lista_tags = [t.strip().lower() for t in tags_raw.split(',') if t.strip()]
        
        PASODOBLES[idx] = {
            "nombre": nombre,
            "tags": lista_tags,
            "duracion": duracion
        }
    except:
        continue

# --- INTERFAZ VISUAL ---
st.title("🎵 Generador de Repertorio")

with st.expander("📖 CONSULTAR ARCHIVO COMPLETO"):
    items = list(PASODOBLES.items())
    col1, col2 = st.columns(2)
    mitad = len(items) // 2 + (len(items) % 2)
    with col1:
        for id_p, info in items[:mitad]:
            st.write(f"**{id_p}.** {info['nombre']}")
    with col2:
        for id_p, info in items[mitad:]:
            st.write(f"**{id_p}.** {info['nombre']}")

st.markdown("### Selección de Pasodobles")

modo = st.selectbox(
    "¿Qué tipo de acto es?",
    ["Todo el archivo", "Pasacalle Alegre (Sin himnos)", "Sólo Fáciles", "Estilo Torero", "Pasacalle Elegante"]
)

cantidad = st.number_input("¿Cuántos pasodobles necesitas?", min_value=1, max_value=15, value=4)

# --- LÓGICA DEL BOTÓN GENERAR ---
if st.button("🔀 GENERAR SORTEO", use_container_width=True):
    candidatos_ids = []
    filtro_map = {
        "Pasacalle Alegre (Sin himnos)": "alegre",
        "Sólo Fáciles": "facil",
        "Estilo Torero": "torero",
        "Pasacalle Elegante": "elegante"
    }
    
    tag_buscado = filtro_map.get(modo)
    
    for id_p, info in PASODOBLES.items():
        # Filtro de seguridad para himnos en pasacalles
        if tag_buscado in ["alegre", "facil"] and "himno" in info["tags"]:
            continue
        
        # Si coincide el tag o es "Todo el archivo"
        if modo == "Todo el archivo" or (tag_buscado and tag_buscado in info["tags"]):
            candidatos_ids.append(id_p)

    if len(candidatos_ids) >= cantidad:
        seleccion_ids = random.sample(candidatos_ids, cantidad)
        
        st.success(f"Selección para: {modo}")
        tiempo_total = 0.0
        
        for i, idx in enumerate(seleccion_ids, 1):
            p = PASODOBLES[idx]
            st.markdown(f"### {i}. {p['nombre']} ({p['duracion']} min)")
            tiempo_total += p['duracion']
        
        # Mostrar resumen de tiempo
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Música neta", f"{round(tiempo_total, 1)} min")
        with c2:
            # Calculamos tiempo con descansos (un 20% más)
            st.metric("Tiempo con pausas", f"{round(tiempo_total * 1.2, 1)} min")
        
        st.info("💡 Consejo: 2 vueltas por pasodoble + redoble de descanso.")
    else:
        st.error(f"No hay suficientes pasodobles con el filtro '{modo}'.")

# --- PANEL DE ADMINISTRACIÓN ---
st.divider()
with st.expander("🛠️ PANEL DE ADMINISTRACIÓN"):
    if 'admin_autenticado' not in st.session_state:
        st.session_state.admin_autenticado = False

    if not st.session_state.admin_autenticado:
        password = st.text_input("Clave de Archivero:", type="password")
        if st.button("🔓 ACCEDER"):
            if password == "Daimus2026":
                st.session_state.admin_autenticado = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
    else:
        st.success("Acceso de Administrador")
        
        if st.button("🔄 REFRESCAR BASE DE DATOS"):
            st.cache_data.clear()
            st.rerun()

        c1, c2 = st.columns([2, 1])
        with c1:
            st.write("Edita el Excel y pulsa el botón de arriba.")
            if st.button("🔒 CERRAR SESIÓN"):
                st.session_state.admin_autenticado = False
                st.rerun()
        with c2:
            url_excel = st.secrets["connections"]["gsheets"]["spreadsheet"]
            st.link_button("📂 ABRIR EXCEL", url_excel, use_container_width=True, type="primary")
