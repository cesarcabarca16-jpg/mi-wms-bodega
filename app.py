import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configuración de pantalla estilo Sistema Corporativo Aduanero
st.set_page_config(page_title="Custom Enterprise WMS - Magaya Alternative", page_icon="⚙️", layout="wide")

# Estilos visuales grises y corporativos de terminal de carga
st.markdown("""
    <style>
    .stButton>button { background-color: #1f3a60; color: white; font-weight: bold; border-radius: 4px; width: 100%; height: 45px; }
    .stButton>button:hover { background-color: #2b579a; color: white; }
    .magaya-header { background-color: #1a252f; color: white; padding: 15px; border-radius: 4px; margin-bottom: 15px; font-family: monospace; }
    .status-bar { background-color: #e2e8f0; padding: 10px; border-radius: 4px; border-left: 5px solid #1f3a60; font-size: 13px; font-family: monospace; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="magaya-header">
        <h2 style='margin:0; color:white;'>⚙️ ADVANCED WORKSPACE - CARGO & LOGISTICS SYSTEM</h2>
        <span style='font-size:12px;'>Módulos Integrados de Recibo, Inventario, Tareas, Facturación y Despacho | Usuarios: Ilimitados</span>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="status-bar">
        <strong>SISTEMA:</strong> CORPORATIVO | <strong>SEDE:</strong> BOG_HUB_CARGO | <strong>CONEXIÓN:</strong> CLOUD_SECURE
    </div>
""", unsafe_allow_html=True)

# --- MAPA DE LA BODEGA REAL (RACKS, PISOS Y CUARTOS) ---
@st.cache_data
def generar_bodega_real():
    lista_ubicaciones = []
    lados = ["01", "02"]
    
    # Pasillo Alpha (A)
    for pos in range(1, 10):      
        for nivel in range(1, 6): 
            for ld in lados:
                lista_ubicaciones.append({"Codigo_Ubicacion": f"A{pos:02d}{nivel:02d}{ld}", "Pasillo_Zona": "Alpha", "Nivel": f"Nivel {nivel}", "Profundidad": "Estándar", "Estado": "Libre"})
                
    # Pasillo Bravo (B) con dobles posiciones
    for pos in range(1, 9):       
        for nivel in range(1, 6):
            for ld in lados:
                lista_ubicaciones.append({"Codigo_Ubicacion": f"B{pos:02d}{nivel:02d}{ld}", "Pasillo_Zona": "Bravo", "Nivel": f"Nivel {nivel}", "Profundidad": "Estándar", "Estado": "Libre"})
        lista_ubicaciones.append({"Codigo_Ubicacion": f"B{pos:02d}A", "Pasillo_Zona": "Bravo", "Nivel": "Intermedio (FR)", "Profundidad": "Doble (Frente)", "Estado": "Libre"})
        lista_ubicaciones.append({"Codigo_Ubicacion": f"B{pos:02d}B", "Pasillo_Zona": "Bravo", "Nivel": "Intermedio (FO)", "Profundidad": "Doble (Fondo)", "Estado": "Libre"})

    # Pasillo Charlie (C)
    for pos in range(1, 8):       
        for nivel in range(1, 6):
            for ld in lados:
                lista_ubicaciones.append({"Codigo_Ubicacion": f"C{pos:02d}{nivel:02d}{ld}", "Pasillo_Zona": "Charlie", "Nivel": f"Nivel {nivel}", "Profundidad": "Estándar", "Estado": "Libre"})
        lista_ubicaciones.append({"Codigo_Ubicacion": f"C{pos:02d}A", "Pasillo_Zona": "Charlie", "Nivel": "Intermedio (FR)", "Profundidad": "Doble (Frente)", "Estado": "Libre"})
        lista_ubicaciones.append({"Codigo_Ubicacion": f"C{pos:02d}B", "Pasillo_Zona": "Charlie", "Nivel": "Intermedio (FO)", "Profundidad": "Doble (Fondo)", "Estado": "Libre"})

    # Pasillos Dobles (Foxtrot, Golfo, November)
    for p_nombre, max_pos in [("Foxtrot", 7), ("Golfo", 7), ("November", 4)]:
        for pos in range(1, max_pos + 1):       
            for nivel in range(1, 6):
                for ld in lados:
                    lista_ubicaciones.append({"Codigo_Ubicacion": f"{p_nombre[0]}{pos:02d}{nivel:02d}{ld}-FR", "Pasillo_Zona": p_nombre, "Nivel": f"Nivel {nivel}", "Profundidad": "Doble (Frente)", "Estado": "Libre"})
                    lista_ubicaciones.append({"Codigo_Ubicacion": f"{p_nombre[0]}{pos:02d}{nivel:02d}{ld}-FO", "Pasillo_Zona": p_nombre, "Nivel": f"Nivel {nivel}", "Profundidad": "Doble (Fondo)", "Estado": "Libre"})

    # Pasillo Hotel, Mike, Kilo, India
    for pos in range(1, 4):
        for nivel in range(1, 6):
            for ld in lados: lista_ubicaciones.append({"Codigo_Ubicacion": f"H{pos:02d}{nivel:02d}{ld}", "Pasillo_Zona": "Hotel", "Nivel": f"Nivel {nivel}", "Profundidad": "Estándar", "Estado": "Libre"})
    for nivel in range(1, 6):
        for ld in lados:
            lista_ubicaciones.append({"Codigo_Ubicacion": f"M1-01{nivel:02d}{ld}-FR", "Pasillo_Zona": "Mike 1", "Nivel": f"Nivel {nivel}", "Profundidad": "Doble (Frente)", "Estado": "Libre"})
            lista_ubicaciones.append({"Codigo_Ubicacion": f"M1-01{nivel:02d}{ld}-FO", "Pasillo_Zona": "Mike 1", "Nivel": f"Nivel {nivel}", "Profundidad": "Doble (Fondo)", "Estado": "Libre"})
            lista_ubicaciones.append({"Codigo_Ubicacion": f"M2-01{nivel:02d}{ld}", "Pasillo_Zona": "Mike 2", "Nivel": f"Nivel {nivel}", "Profundidad": "Estándar", "Estado": "Libre"})
    for pos in range(1, 8):
        for nivel in range(1, 6):
            for ld in lados:
                if pos == 1: lista_ubicaciones.append({"Codigo_Ubicacion": f"K{pos:02d}{nivel:02d}{ld}", "Pasillo_Zona": "Kilo", "Nivel": f"Nivel {nivel}", "Profundidad": "Estándar", "Estado": "Libre"})
                else:
                    lista_ubicaciones.append({"Codigo_Ubicacion": f"K{pos:02d}{nivel:02d}{ld}-FR", "Pasillo_Zona": "Kilo", "Nivel": f"Nivel {nivel}", "Profundidad": "Doble (Frente)", "Estado": "Libre"})
                    lista_ubicaciones.append({"Codigo_Ubicacion": f"K{pos:02d}{nivel:02d}{ld}-FO", "Pasillo_Zona": "Kilo", "Nivel": f"Nivel {nivel}", "Profundidad": "Doble (Fondo)", "Estado": "Libre"})
    for pos in range(1, 3):
        for nivel in range(1, 7): 
            for ld in lados: lista_ubicaciones.append({"Codigo_Ubicacion": f"I{pos:02d}{nivel:02d}{ld}", "Pasillo_Zona": "India", "Nivel": f"Nivel {nivel}", "Profundidad": "Estándar", "Estado": "Libre"})

    # Pisos y cuartos
    for z_nombre, z_prefijo in [("Bodega 1 Piso", "B1-PISO"), ("Bodega 2 Piso", "B2-PISO"), ("Sótano", "SOTANO"), ("Cuarto Seguridad", "SEGURIDAD"), ("Cuarto Frío", "FRIO")]:
        for espacio in range(1, 11):
            lista_ubicaciones.append({"Codigo_Ubicacion": f"{z_prefijo}-{espacio:02d}", "Pasillo_Zona": z_nombre, "Nivel": "Piso", "Profundidad": "Estándar", "Estado": "Libre"})

    return pd.DataFrame(lista_ubicaciones)

# --- INICIALIZACIÓN DE BASES DE DATOS EN MEMORIA PERSISTENTE ---
if 'mapa_bodega' not in st.session_state:
    st.session_state.mapa_bodega = generar_bodega_real()

if 'tabla_carga' not in st.session_state:
    st.session_state.tabla_carga = pd.DataFrame(columns=[
        "AWB", "Cliente", "Piezas", "Peso_Kg", "Dimensiones", "Ubicacion", "Fecha_Ingreso", "Tareas_Asignadas", "Estado_Tarea"
    ])

# --- MENÚ PRINCIPAL OPERATIVO ---
modulo = st.sidebar.selectbox("📂 SELECCIONE MÓDULO WMS:", [
    "1. Warehouse Receipt (Ingreso)",
    "2. Control de Inventario & Traslados",
    "3. Operaciones & Tareas Especiales",
    "4. Liquidación & Facturación",
    "5. Cargo Release (Salida Carga)"
])

# ==========================================
# MÓDULO 1: WAREHOUSE RECEIPT (INGRESO)
# ==========================================
if "1." in modulo:
    st.subheader("📥 MÓDULO: Warehouse Receipt (Ingreso e Inspección de Carga)")
    df_libres = st.session_state.mapa_bodega[st.session_state.mapa_bodega['Estado'] == 'Libre']
    
    with st.form("form_registro_ingreso"):
        col1, col2 = st.columns(2)
        with col1:
            awb = st.text_input("Número de Guía (AWB):", placeholder="Ej: 020-12345678")
            cliente = st.text_input("Consignee / Cliente:")
            piezas = st.number_input("Número de Piezas (Bultos):", min_value=1, value=1)
        with col2:
            peso = st.number_input("Gross Weight (Peso en Kg):", min_value=0.1, value=10.0)
            dims = st.text_input("Dimensions (L x A x Al en cm):", placeholder="Ej: 120x80x100")
            ubicacion = st.selectbox("Assign Initial Storage (Ubicación Libre):", df_libres['Codigo_Ubicacion'])
            
        dias_atras = st.slider("Simular días de ingreso hacia atrás (Para pruebas de facturación):", 0, 15, 0)
        fecha_ingreso = datetime.now() - timedelta(days=dias_atras)

        btn_ingreso = st.form_submit_button("💾 Guardar Transacción & Emitir Recibo")
        
        if btn_ingreso and awb:
            if awb in st.session_state.tabla_carga['AWB'].values:
                st.error("❌ ERROR: Esa AWB ya se encuentra registrada en la bodega.")
            else:
                nueva_carga = {
                    "AWB": awb, "Cliente": cliente, "Piezas": piezas, "Peso_Kg": peso,
                    "Dimensiones": dims, "Ubicacion": ubicacion, "Fecha_Ingreso": fecha_ingreso,
                    "Tareas_Asignadas": "Ninguna", "Estado_Tarea": "N/A"
                }
                st.session_state.tabla_carga = pd.concat([st.session_state.tabla_carga, pd.DataFrame([nueva_carga])], ignore_index=True)
                st.session_state.mapa_bodega.loc[st.session_state.mapa_bodega['Codigo_Ubicacion'] == ubicacion, 'Estado'] = 'Ocupado'
                st.success(f"✔️ RECEPTiON SUCCESSFUL: Carga {awb} almacenada en {ubicacion}.")
                st.rerun()

# ==========================================
# MÓDULO 2: CONTROL DE INVENTARIO & TRASLADOS
# ==========================================
elif "2." in modulo:
    st.subheader("📦 MÓDULO: Almacenamiento, Control de Inventarios & Traslados Internos")
    
    tab_inv, tab_traslado = st.tabs(["📋 Listado General de Stock", "🔄 Traslado de Ubicación (Movimiento Montacargas)"])
    
    with tab_inv:
        if st.session_state.tabla_carga.empty:
            st.info("La bodega se encuentra totalmente vacía en este momento.")
        else:
            st.dataframe(st.session_state.tabla_carga, use_container_width=True)
            
    with tab_traslado:
        if st.session_state.tabla_carga.empty:
