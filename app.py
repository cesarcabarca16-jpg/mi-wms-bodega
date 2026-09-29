import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de pantalla estilo Terminal Corporativa (Magaya Look)
st.set_page_config(page_title="Magaya Custom WMS Interface", page_icon="⚙️", layout="wide")

# --- ESTILOS CSS PARA IMITAR EL LOOK GRIS DE MAGAYA ---
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f5; }
    .stButton>button {
        background-color: #2b579a;
        color: white;
        font-weight: bold;
        border-radius: 4px;
        width: 100%;
        height: 45px;
    }
    .stButton>button:hover { background-color: #1e3d73; color: white; }
    .magaya-header {
        background-color: #1f3a60;
        color: white;
        padding: 12px;
        border-radius: 4px;
        margin-bottom: 15px;
        font-family: 'Courier New', Courier, monospace;
    }
    .status-bar {
        background-color: #e2e8f0;
        padding: 8px;
        border-radius: 4px;
        border-left: 5px solid #2b579a;
        font-size: 13px;
        font-family: monospace;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABECERA ESTILO MAGAYA ECOSYSTEM ---
st.markdown("""
    <div class="magaya-header">
        <h2 style='margin:0; color:white;'>⚙️ MAGAYA WORKSPACE - IN-HOUSE EXTENSION</h2>
        <span style='font-size:12px;'>Subsistema de Operación de Bodega Local | Licencias Operarios: ILIMITADAS</span>
    </div>
""", unsafe_allow_html=True)

# Barra de estado del sistema en tiempo real
fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
st.markdown(f"""
    <div class="status-bar">
        <strong>ESTADO:</strong> ONLINE | <strong>ESTACIÓN:</strong> BODEGA_BOGOTA_01 | <strong>FECHA/HORA:</strong> {fecha_actual} | <strong>CONEXIÓN:</strong> SERVIDOR_LOCAL
    </div>
""", unsafe_allow_html=True)

# --- GENERADOR ROBUSTO DEL MAPA DE TU BODEGA ---
@st.cache_data
def generar_bodega_real():
    lista_ubicaciones = []
    lados = ["01", "02"]
    
    # 1. PASILLO ALPHA (A)
    for pos in range(1, 10):      
        for nivel in range(1, 6): 
            for ld in lados:
                cod = f"A{pos:02d}{nivel:02d}{ld}"
                lista_ubicaciones.append({"Codigo_Ubicacion": cod, "Pasillo_Zona": "Alpha", "Nivel": f"Nivel {nivel}", "Profundidad": "Estándar", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})
                
    # 2. PASILLO BRAVO (B)
    for pos in range(1, 9):       
        for nivel in range(1, 6):
            for ld in lados:
                cod = f"B{pos:02d}{nivel:02d}{ld}"
                lista_ubicaciones.append({"Codigo_Ubicacion": cod, "Pasillo_Zona": "Bravo", "Nivel": f"Nivel {nivel}", "Profundidad": "Estándar", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})
        lista_ubicaciones.append({"Codigo_Ubicacion": f"B{pos:02d}A", "Pasillo_Zona": "Bravo", "Nivel": "Intermedio (Frente)", "Profundidad": "Doble (Frente)", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})
        lista_ubicaciones.append({"Codigo_Ubicacion": f"B{pos:02d}B", "Pasillo_Zona": "Bravo", "Nivel": "Intermedio (Fondo)", "Profundidad": "Doble (Fondo)", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})

    # 3. PASILLO CHARLIE (C)
    for pos in range(1, 8):       
        for nivel in range(1, 6):
            for ld in lados:
                cod = f"C{pos:02d}{nivel:02d}{ld}"
                lista_ubicaciones.append({"Codigo_Ubicacion": cod, "Pasillo_Zona": "Charlie", "Nivel": f"Nivel {nivel}", "Profundidad": "Estándar", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})
        lista_ubicaciones.append({"Codigo_Ubicacion": f"C{pos:02d}A", "Pasillo_Zona": "Charlie", "Nivel": "Intermedio (Frente)", "Profundidad": "Doble (Frente)", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})
        lista_ubicaciones.append({"Codigo_Ubicacion": f"C{pos:02d}B", "Pasillo_Zona": "Charlie", "Nivel": "Intermedio (Fondo)", "Profundidad": "Doble (Fondo)", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})

    # 4. PASILLOS CON DOBLE PROFUNDIDAD ESTÁNDAR (Foxtrot, Golfo, November)
    pasillos_dobles = [("Foxtrot", 7), ("Golfo", 7), ("November", 4)]
    for p_nombre, max_pos in pasillos_dobles:
        p_letra = p_nombre[0]
        for pos in range(1, max_pos + 1):       
            for nivel in range(1, 6):
                for ld in lados:
                    lista_ubicaciones.append({"Codigo_Ubicacion": f"{p_letra}{pos:02d}{nivel:02d}{ld}-FR", "Pasillo_Zona": p_nombre, "Nivel": f"Nivel {nivel}", "Profundidad": "Doble (Frente)", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})
                    lista_ubicaciones.append({"Codigo_Ubicacion": f"{p_letra}{pos:02d}{nivel:02d}{ld}-FO", "Pasillo_Zona": p_nombre, "Nivel": f"Nivel {nivel}", "Profundidad": "Doble (Fondo)", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})

    # 5. PASILLO HOTEL (H)
    for pos in range(1, 4):
        for nivel in range(1, 6):
            for ld in lados:
                lista_ubicaciones.append({"Codigo_Ubicacion": f"H{pos:02d}{nivel:02d}{ld}", "Pasillo_Zona": "Hotel", "Nivel": f"Nivel {nivel}", "Profundidad": "Estándar", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})

    # 6. PASILLOS MIKE (M1 y M2)
    for nivel in range(1, 6):
        for ld in lados:
            lista_ubicaciones.append({"Codigo_Ubicacion": f"M1-01{nivel:02d}{ld}-FR", "Pasillo_Zona": "Mike 1", "Nivel": f"Nivel {nivel}", "Profundidad": "Doble (Frente)", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})
            lista_ubicaciones.append({"Codigo_Ubicacion": f"M1-01{nivel:02d}{ld}-FO", "Pasillo_Zona": "Mike 1", "Nivel": f"Nivel {nivel}", "Profundidad": "Doble (Fondo)", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})
            lista_ubicaciones.append({"Codigo_Ubicacion": f"M2-01{nivel:02d}{ld}", "Pasillo_Zona": "Mike 2", "Nivel": f"Nivel {nivel}", "Profundidad": "Estándar", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})

    # 7. PASILLO KILO (K)
    for pos in range(1, 8):
        for nivel in range(1, 6):
            for ld in lados:
                if pos == 1:
                    lista_ubicaciones.append({"Codigo_Ubicacion": f"K{pos:02d}{nivel:02d}{ld}", "Pasillo_Zona": "Kilo", "Nivel": f"Nivel {nivel}", "Profundidad": "Estándar", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})
                else:
                    lista_ubicaciones.append({"Codigo_Ubicacion": f"K{pos:02d}{nivel:02d}{ld}-FR", "Pasillo_Zona": "Kilo", "Nivel": f"Nivel {nivel}", "Profundidad": "Doble (Frente)", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})
                    lista_ubicaciones.append({"Codigo_Ubicacion": f"K{pos:02d}{nivel:02d}{ld}-FO", "Pasillo_Zona": "Kilo", "Nivel": f"Nivel {nivel}", "Profundidad": "Doble (Fondo)", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})

    # 8. PASILLO INDIA (I)
    for pos in range(1, 3):
        for nivel in range(1, 7): 
            for ld in lados:
                lista_ubicaciones.append({"Codigo_Ubicacion": f"I{pos:02d}{nivel:02d}{ld}", "Pasillo_Zona": "India", "Nivel": f"Nivel {nivel}", "Profundidad": "Estándar", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})

    # 9. ZONAS DE PISO, SÓTANO, CUARTOS ESPECIALES
    zonas_especiales = [("Bodega 1 Piso", "B1-PISO"), ("Bodega 2 Piso", "B2-PISO"), ("Sótano", "SOTANO"), ("Cuarto Seguridad", "SEGURIDAD"), ("Cuarto Frío", "FRIO")]
    for z_nombre, z_prefijo in zonas_especiales:
        for espacio in range(1, 11):
            lista_ubicaciones.append({"Codigo_Ubicacion": f"{z_prefijo}-{espacio:02d}", "Pasillo_Zona": z_nombre, "Nivel": "Piso / N/A", "Profundidad": "Estándar", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})

    return pd.DataFrame(lista_ubicaciones)

if 'inventario' not in st.session_state:
    st.session_state.inventario = generar_bodega_real()

# --- MENÚ LATERAL: CONTROL DE VISTA ---
st.sidebar.markdown("### 🖥️ CONTROL DE MÓDULOS")
rol = st.sidebar.selectbox("Seleccione Modo de Interfaz:", ["Operaciones de Bodega (Móvil)", "Live Map & Control Gerencial"])

# --- MODULO 1: OPERACIONES DE BODEGA ---
if "Operaciones de Bodega" in rol:
    # Emulando los submódulos clásicos del menú lateral de Magaya
    opcion_bodega = st.sidebar.radio("Documentos de Almacén:", ["📥 Warehouse Receipt (Recibo)", "📤 Cargo Release (Salida/Picking)", "🔍 Location Finder (Buscador)"])
    
    # MÓDULO RECIBO (Warehouse Receipt)
    if "Warehouse Receipt" in opcion_bodega:
        st.subheader("📝 COMPONENT: Warehouse Receipt (Ingreso de Carga)")
        df_libres = st.session_state.inventario[st.session_state.inventario['Estado'] == 'Libre']
        
        with st.form("magaya_wr_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                sku = st.text_input("Commodity Name / SKU / Paleta ID:", placeholder="Ej: Paleta Repuestos ABC")
                cant = st.number_input("Quantity (Unidades/Paletas):", min_value=1, value=1)
            with col_b:
                ubicacion = st.selectbox("Assign Location (Ubicaciones Libres):", df_libres['Codigo_Ubicacion'])
                shipper = st.text_input("Shipper / Cliente Ospitante:", value="Cliente Genérico S.A.")
            
            # Validaciones lógicas de doble profundidad
            cod_fondo = ""
            if ubicacion.endswith("A"): cod_fondo = ubicacion.replace("A", "B")
            elif ubicacion.endswith("-FR"): cod_fondo = ubicacion.replace("-FR", "-FO")
                
            if cod_fondo:
                fila_fondo = st.session_state.inventario[st.session_state.inventario['Codigo_Ubicacion'] == cod_fondo]
                if not fila_fondo.empty and (fila_fondo['Estado'].values == "Libre"):
                    st.warning(f"⚠️ LOGISTIC ALERT (LIFO): Está intentando ubicar en el Frente ({ubicacion}) pero el Fondo ({cod_fondo}) está vacío. Se sugiere reubicar primero al Fondo.")
            
