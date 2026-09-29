import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configuración de la interfaz estilo Terminal Aduanera Profesional
st.set_page_config(page_title="Magaya Workspace Pro - BOG HUB", page_icon="⚙️", layout="wide")

# Estilos CSS avanzados para imitar el look corporativo de Magaya y etiquetas
st.markdown("""
    <style>
    .stButton>button {
        background-color: #1f3a60;
        color: white;
        font-weight: bold;
        border-radius: 4px;
        width: 100%;
        height: 40px;
        font-size: 13px;
        border: 1px solid #1a252f;
    }
    .stButton>button:hover { background-color: #2b579a; color: white; border-color: #2b579a; }
    .magaya-header { background-color: #141d26; color: white; padding: 18px; border-radius: 4px; margin-bottom: 5px; font-family: 'Courier New', monospace; border-bottom: 4px solid #2b579a; }
    .status-bar { background-color: #cbd5e1; padding: 8px; border-radius: 4px; border-left: 5px solid #1f3a60; font-size: 12px; font-family: monospace; margin-bottom: 15px; color: #0f172a; }
    .label-box {
        background-color: #ffffff;
        padding: 15px;
        border: 2px dashed #000000;
        border-radius: 4px;
        color: #000000;
        font-family: monospace;
        margin-top: 15px;
        max-width: 400px;
    }
    </style>
""", unsafe_allow_html=True)

# Cabecera Corporativa de Magaya Workspace
st.markdown("""
    <div class="magaya-header">
        <h2 style='margin:0; color:white; font-size:22px;'>⚙️ MAGAYA ENTERPRISE SYSTEM v13.5 - IN-HOUSE HUB</h2>
        <span style='font-size:12px; color:#94a3b8;'>Ecosistema de Comercio Exterior y Almacenaje Aeronáutico | Terminal de Carga El Dorado</span>
    </div>
""", unsafe_allow_html=True)

fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
st.markdown(f"""
    <div class="status-bar">
        <strong>ESTADO NODE:</strong> CONECTADO MIGRACIÓN DIAN | <strong>PERFIL:</strong> OPERARIO_MASTER | <strong>FECHA SIMULACIÓN:</strong> {fecha_actual} | <strong>LICENCIAS:</strong> ILIMITADAS
    </div>
""", unsafe_allow_html=True)

# --- GENERADOR DEL MAPA DE LA BODEGA REAL ---
@st.cache_data
def generar_bodega_real():
    lista_ubicaciones = []
    lados = ["01", "02"]
    
    for pos in range(1, 10):      
        for nivel in range(1, 6): 
            for ld in lados:
                lista_ubicaciones.append({"Codigo_Ubicacion": f"A{pos:02d}{nivel:02d}{ld}", "Pasillo_Zona": "Alpha", "Nivel": f"Nivel {nivel}", "Profundidad": "Estándar", "Estado": "Libre"})
                
    for pos in range(1, 8):       
        for nivel in range(1, 6):
            for ld in lados:
                lista_ubicaciones.append({"Codigo_Ubicacion": f"B{pos:02d}{nivel:02d}{ld}", "Pasillo_Zona": "Bravo", "Nivel": f"Nivel {nivel}", "Profundidad": "Estándar", "Estado": "Libre"})
        lista_ubicaciones.append({"Codigo_Ubicacion": f"B{pos:02d}A", "Pasillo_Zona": "Bravo", "Nivel": "Intermedio (FR)", "Profundidad": "Doble (Frente)", "Estado": "Libre"})
        lista_ubicaciones.append({"Codigo_Ubicacion": f"B{pos:02d}B", "Pasillo_Zona": "Bravo", "Nivel": "Intermedio (FO)", "Profundidad": "Doble (Fondo)", "Estado": "Libre"})

    for pos in range(1, 8):       
        for nivel in range(1, 6):
            for ld in lados:
                lista_ubicaciones.append({"Codigo_Ubicacion": f"C{pos:02d}{nivel:02d}{ld}", "Pasillo_Zona": "Charlie", "Nivel": f"Nivel {nivel}", "Profundidad": "Estándar", "Estado": "Libre"})
        lista_ubicaciones.append({"Codigo_Ubicacion": f"C{pos:02d}A", "Pasillo_Zona": "Charlie", "Nivel": "Intermedio (FR)", "Profundidad": "Doble (Frente)", "Estado": "Libre"})
        lista_ubicaciones.append({"Codigo_Ubicacion": f"C{pos:02d}B", "Pasillo_Zona": "Charlie", "Nivel": "Intermedio (FO)", "Profundidad": "Doble (Fondo)", "Estado": "Libre"})

    for p_nombre, max_pos in [("Foxtrot", 7), ("Golfo", 7), ("November", 4)]:
        for pos in range(1, max_pos + 1):       
            for nivel in range(1, 6):
                for ld in lados:
                    lista_ubicaciones.append({"Codigo_Ubicacion": f"{p_nombre}{pos:02d}{nivel:02d}{ld}-FR", "Pasillo_Zona": p_nombre, "Nivel": f"Nivel {nivel}", "Profundidad": "Doble (Frente)", "Estado": "Libre"})
                    lista_ubicaciones.append({"Codigo_Ubicacion": f"{p_nombre}{pos:02d}{nivel:02d}{ld}-FO", "Pasillo_Zona": p_nombre, "Nivel": f"Nivel {nivel}", "Profundidad": "Doble (Fondo)", "Estado": "Libre"})

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

    for z_nombre, z_prefijo in [("Bodega 1 Piso", "B1-PISO"), ("Bodega 2 Piso", "B2-PISO"), ("Sótano", "SOTANO"), ("Cuarto Seguridad", "SEGURIDAD"), ("Cuarto Frío", "FRIO")]:
        for espacio in range(1, 11):
            lista_ubicaciones.append({"Codigo_Ubicacion": f"{z_prefijo}-{espacio:02d}", "Pasillo_Zona": z_nombre, "Nivel": "Piso", "Profundidad": "Estándar", "Estado": "Libre"})

    return pd.DataFrame(lista_ubicaciones)

# --- INICIALIZACIÓN PERMANENTE DE DATOS OPERATIVOS ---
if 'mapa_bodega' not in st.session_state:
    st.session_state.mapa_bodega = generar_bodega_real()

if 'tabla_carga' not in st.session_state:
    fecha_base = datetime.now()
    st.session_state.tabla_carga = pd.DataFrame([
        {"AWB": "020-98765432", "Cliente": "Importaciones de Colombia S.A.", "Piezas": 12, "Peso_Kg": 450.0, "Dimensiones": "120x100x160", "Ubicacion": "A010101", "Fecha_Ingreso": fecha_base - timedelta(days=8), "Tareas_Asignadas": "Aforo Aduanero DIAN", "Estado_Tarea": "En Inspección", "Retencion_DIAN": True},
        {"AWB": "134-55544431", "Cliente": "Farma Bogota Logistics", "Piezas": 5, "Peso_Kg": 85.5, "Dimensiones": "60x60x80", "Ubicacion": "FRIO-01", "Fecha_Ingreso": fecha_base - timedelta(days=3), "Tareas_Asignadas": "Sustitución de Hielo Seco", "Estado_Tarea": "Pendiente", "Retencion_DIAN": False}
    ])
    st.session_state.mapa_bodega.loc[st.session_state.mapa_bodega['Codigo_Ubicacion'].isin(["A010101", "FRIO-01"]), 'Estado'] = 'Ocupado'

if 'ultimo_qr_data' not in st.session_state:
    st.session_state.ultimo_qr_data = None

# --- PANEL LATERAL DE NAVEGACIÓN ---
st.sidebar.markdown("### 🖥 nighttime CONTROL DE MÓDULOS")
modulo = st.sidebar.radio("Navegación Magaya Workspace:", [
    "1. Warehouse Receipt (Ingreso)",
    "2. Control de Inventario & Traslados",
    "3. Operaciones DIAN & Tareas Especiales",
    "4. Liquidación & Facturación Comercial",
    "5. Cargo Release (Salida de Carga)"
])

# ===================================================
# MÓDULO 1: WAREHOUSE RECEIPT (INGRESO DE CARGA & QR)
# ===================================================
if "1." in modulo:
    st.subheader("📥 MÓDULO: Warehouse Receipt (Ingreso de Carga & Impresión de QR)")
    df_libres = st.session_state.mapa_bodega[st.session_state.mapa_bodega['Estado'] == 'Libre']
    
    col_x, col_y = st.columns(2)
    with col_x:
        awb = st.text_input("Air Waybill Number (Guía AWB):", placeholder="000-00000000")
        cliente = st.text_input("Consignee Name (Cliente / Importador):")
        piezas = st.number_input("Total Pieces (Bultos):", min_value=1, value=1)
        ret_dian = st.checkbox("¿Registra Alerta / Inspección DIAN?", value=False)
    with col_y:
        peso = st.number_input("Gross Weight (Peso Bruto Kg):", min_value=0.1, value=50.0)
        dims = st.text_input("Dimensions (Largo x Ancho x Alto cm):", placeholder="120x80x100")
        ubicacion = st.selectbox("Assign Storage Location (Ubicaciones Libres):", df_libres['Codigo_Ubicacion'])
        dias_atras = st.slider("Antigüedad simulada (Días en bodega):", 0, 15, 0)

    if st.button("💾 SAVE TRANSACTION & GENERATE LABELS"):
        if awb and cliente:
            fecha_ingreso = datetime.now() - timedelta(days=dias_atras)
            nueva_carga = {"AWB": awb, "Cliente": cliente, "Piezas": piezas, "Peso_Kg": peso, "Dimensiones": dims, "Ubicacion": ubicacion, "Fecha_Ingreso": fecha_ingreso, "Tareas_Asignadas": "Ninguna", "Estado_Tarea": "N/A", "Retencion_DIAN": ret_dian}
            st.session_state.tabla_carga = pd.concat([st.session_state.tabla_carga, pd.DataFrame([nueva_carga])], ignore_index=True)
