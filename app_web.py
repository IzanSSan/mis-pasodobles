import streamlit as st
import pandas as pd
import random
from streamlit_gsheets import GSheetsConnection

# Configuración de la página para móvil
st.set_page_config(page_title="Elección de pasodobles", page_icon="🎵")

# --- CONEXIÓN A GOOGLE SHEETS (DENTRO DE FUNCIÓN CON CACHÉ) ---
@st.cache_data(ttl=10)
def cargar_datos_sheet():
    # Creamos la conexión dentro para forzar el refresco
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn.read()

# Llamamos a la función
df = cargar_datos_sheet()

# Convertimos a diccionario asegurando limpieza total de datos
PASODOBLES = {}
df_limpio = df.dropna(subset=['Nombre'])

for index, row in df_limpio.iterrows():
    try:
        # Aseguramos que el ID sea entero
        idx = int(row['ID'])
        nombre = str(row['Nombre']).strip()
        tags_raw = str(row['Tags']) if pd.notna(row['Tags']) else ""
        
        # Guardamos todo en minúsculas y sin espacios extra
        lista_tags = [t.strip().lower() for t in tags_raw.split(',') if t.strip()]
        
        PASODOBLES[idx] = {
            "nombre": nombre,
            "tags": lista_tags
        }
    except:
        continue

# Título visual
st.title("🎵 Generador de Repertorio")

# --- BOTÓN PARA CONSULTAR LA LISTA COMPLETA ---
with st.expander("📖 CONSULTAR ARCHIVO COMPLETO"):
    col1, col2 = st.columns(2)
    items = list(PASODOBLES.items())
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
    ["Todo el archivo", "Pasacalle Alegre", "Sólo Fáciles", "Estilo Torero", "Entrada de bandas"]
)

cantidad = st.number_input("¿Cuántos pasodobles necesitas?", min_value=1, max_value=10, value=4)

if st.button("🔀 GENERAR SORTEO", use_container_width=True):
    candidatos = []
    filtro_map = {
        "Pasacalle Alegre": "alegre",
        "Sólo Fáciles": "facil",
        "Estilo Torero": "torero",
        "Entrada de bandas": "elegante"
    }
    
    tag_buscado = filtro_map.get(modo)
    
    for id_p, info in PASODOBLES.items():
        # Lógica: si buscamos alegre/fácil, excluimos himnos
        if tag_buscado in ["alegre", "facil"] and "himno" in info["tags"]:
            continue
        
        if modo == "Todo el archivo" or (tag_buscado and tag_buscado in info["tags"]):
            candidatos.append(info["nombre"])

    if len(candidatos) >= cantidad:
        seleccion = random.sample(candidatos, cantidad)
        st.success(f"Selección para: {modo}")
        for i, nombre in enumerate(seleccion, 1):
            st.markdown(f"### {i}. {nombre}")
        st.info("💡 Recordatorio: 2 vueltas + redoble de descanso")
    else:
        st.error(f"No hay suficientes pasodobles con el filtro '{tag_buscado}'. Revisa el Excel.")

# --- PANEL DE GESTIÓN MUSICAL (ADMIN) ---
st.divider()

with st.expander("🛠️ PANEL DE ADMINISTRACIÓN"):
    if 'admin_autenticado' not in st.session_state:
        st.session_state.admin_autenticado = False

    if not st.session_state.admin_autenticado:
        password = st.text_input("Introduce la clave de Archivero:", type="password")
        if st.button("🔓 ACCEDER"):
            if password == "Daimus2026":
                st.session_state.admin_autenticado = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
    else:
        st.success("**¡Hola, Administrador!** Acceso concedido.")
        
        # BOTÓN MAGICO DE REFRESCO DE DATOS
        if st.button("🔄 REFRESCAR BASE DE DATOS (Forzar lectura Excel)"):
            st.cache_data.clear()
            st.rerun()

        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown("Puedes editar el Excel y luego pulsar el botón de arriba.")
            if st.button("🔒 CERRAR SESIÓN"):
                st.session_state.admin_autenticado = False
                st.rerun()
        
        with c2:
            url_excel = st.secrets["connections"]["gsheets"]["spreadsheet"]
            st.link_button("📂 ABRIR EXCEL", url_excel, use_container_width=True, type="primary")
