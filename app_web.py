import streamlit as st
import pandas as pd
import random
from streamlit_gsheets import GSheetsConnection

# Configuración de la página para móvil
st.set_page_config(page_title="Elección de pasodobles", page_icon="🎵")

# --- CONEXIÓN A GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

# Creamos una función con caché de 10 segundos
@st.cache_data(ttl=10)
def cargar_datos_sheet():
    return conn.read()

# Llamamos a la función
df = cargar_datos_sheet()

# Convertimos a diccionario asegurando limpieza total de datos
PASODOBLES = {}
# Eliminamos filas que tengan el nombre vacío para evitar errores
df_limpio = df.dropna(subset=['Nombre'])

for index, row in df_limpio.iterrows():
    try:
        idx = int(row['ID'])
        nombre = str(row['Nombre']).strip() # .strip() quita espacios invisibles
        tags_raw = str(row['Tags']) if pd.notna(row['Tags']) else ""
        
        # Guardamos todo en minúsculas y sin espacios extra
        lista_tags = [t.strip().lower() for t in tags_raw.split(',') if t.strip()]
        
        PASODOBLES[idx] = {
            "nombre": nombre,
            "tags": lista_tags
        }
    except:
        continue # Si una fila da error (ej. ID no es número), la salta y sigue

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
# --- PANEL DE GESTIÓN MUSICAL (ADMIN) ---
st.divider()

with st.expander("🛠️ PANEL DE ADMINISTRACIÓN"):
    # Inicializamos el estado del login si no existe
    if 'admin_autenticado' not in st.session_state:
        st.session_state.admin_autenticado = False

    if not st.session_state.admin_autenticado:
        # Formulario de entrada
        password = st.text_input("Introduce la clave de Archivero:", type="password")
        if st.button("🔓 ACCEDER"):
            if password == "Daimus2026":
                st.session_state.admin_autenticado = True
                st.rerun() # Recargamos para mostrar el panel
            else:
                st.error("Contraseña incorrecta")
    else:
        # Si ya está autenticado, mostramos el panel elegante
        st.success("**¡Hola, Administrador!** Acceso concedido.")
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown("""
            ### Gestión de Pasodobles
            Puedes editar, añadir o corregir piezas directamente en la base de datos de Google.
            """)
            if st.button("🔒 CERRAR SESIÓN"):
                st.session_state.admin_autenticado = False
                st.rerun()
        
        with c2:
            st.write("##")
            url_excel = st.secrets["connections"]["gsheets"]["spreadsheet"]
            st.link_button("📂 ABRIR ARCHIVO MAESTRO", url_excel, use_container_width=True, type="primary")
