import streamlit as st
import pandas as pd

# Configuración de la página de la Demo
st.set_page_config(page_title="WMS Personalizado - Demo Gerencial", page_icon="📦", layout="wide")

st.title("📦 Sistema WMS In-House - Prototipo Real")
st.markdown("### Control de Operación de Bodega con Usuarios Ilimitados")

# --- GENERADOR AUTOMÁTICO DEL MAPA DE TU BODEGA REAL ---
@st.cache_data
def generar_bodega_real():
    lista_ubicaciones = []
    
    # 1. PASILLO ALPHA (A) -> Posiciones 1 a 9, Niveles 1 a 5, Sin doble profundidad
    for pos in range(1, 10):      
        for nivel in range(1, 6): 
            for lado_num in range(1, 3):   
                cod = f"A{pos:02d}{nivel:02d}{lado_num:02d}"
                lista_ubicaciones.append({
                    "Codigo_Ubicacion": cod, "Pasillo_Zona": "Alpha", "Nivel": f"Nivel {nivel}",
                    "Profundidad": "Estándar", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0
                })
                
    # 2. PASILLO BRAVO (B) -> Posiciones 1 a 8, Niveles 1 a 5 + Intermedios Doble Profundidad
    for pos in range(1, 9):       
        for nivel in range(1, 6):
            for lado_num in range(1, 3):
                cod = f"B{pos:02d}{nivel:02d}{lado_num:02d}"
                lista_ubicaciones.append({
                    "Codigo_Ubicacion": cod, "Pasillo_Zona": "Bravo", "Nivel": f"Nivel {nivel}",
                    "Profundidad": "Estándar", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0
                })
        lista_ubicaciones.append({"Codigo_Ubicacion": f"B{pos:02d}A", "Pasillo_Zona": "Bravo", "Nivel": "Intermedio (Frente)", "Profundidad": "Doble (Frente)", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})
        lista_ubicaciones.append({"Codigo_Ubicacion": f"B{pos:02d}B", "Pasillo_Zona": "Bravo", "Nivel": "Intermedio (Fondo)", "Profundidad": "Doble (Fondo)", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})

    # 3. PASILLO CHARLIE (C) -> Posiciones 1 a 7, Niveles 1 a 5 + Intermedios Doble Profundidad
    for pos in range(1, 8):       
        for nivel in range(1, 6):
            for lado_num in range(1, 3):
                cod = f"C{pos:02d}{nivel:02d}{lado_num:02d}"
                lista_ubicaciones.append({
                    "Codigo_Ubicacion": cod, "Pasillo_Zona": "Charlie", "Nivel": f"Nivel {nivel}",
                    "Profundidad": "Estándar", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0
                })
        lista_ubicaciones.append({"Codigo_Ubicacion": f"C{pos:02d}A", "Pasillo_Zona": "Charlie", "Nivel": "Intermedio (Frente)", "Profundidad": "Doble (Frente)", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})
        lista_ubicaciones.append({"Codigo_Ubicacion": f"C{pos:02d}B", "Pasillo_Zona": "Charlie", "Nivel": "Intermedio (Fondo)", "Profundidad": "Doble (Fondo)", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})

    # 4. PASILLOS CON DOBLE PROFUNDIDAD ESTÁNDAR (Foxtrot, Golfo, November)
    pasillos_dobles = [("Foxtrot", 7), ("Golfo", 7), ("November", 4)]
    for p_nombre, max_pos in pasillos_dobles:
        p_letra = p_nombre[0]  # F, G, N
        for pos in range(1, max_pos + 1):       
            for nivel in range(1, 6):
                for lado_num in range(1, 3):
                    lista_ubicaciones.append({"Codigo_Ubicacion": f"{p_letra}{pos:02d}{nivel:02d}{lado_num:02d}-FR", "Pasillo_Zona": p_nombre, "Nivel": f"Nivel {nivel}", "Profundidad": "Doble (Frente)", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})
                    lista_ubicaciones.append({"Codigo_Ubicacion": f"{p_letra}{pos:02d}{nivel:02d}{lado_num:02d}-FO", "Pasillo_Zona": p_nombre, "Nivel": f"Nivel {nivel}", "Profundidad": "Doble (Fondo)", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})

    # 5. PASILLO HOTEL (H) -> Posiciones 1 a 3, Niveles 1 a 5, Sin profundidad
    for pos in range(1, 4):
        for nivel in range(1, 6):
            for lado_num in range(1, 3):
                lista_ubicaciones.append({"Codigo_Ubicacion": f"H{pos:02d}{nivel:02d}{lado_num:02d}", "Pasillo_Zona": "Hotel", "Nivel": f"Nivel {nivel}", "Profundidad": "Estándar", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})

    # 6. PASILLOS MIKE (M1 Doble y M2 Sencillo) -> Posición 1, Niveles 1 a 5
    for nivel in range(1, 6):
        for lado_num in range(1, 3):
            lista_ubicaciones.append({"Codigo_Ubicacion": f"M1-01{nivel:02d}{lado_num:02d}-FR", "Pasillo_Zona": "Mike 1", "Nivel": f"Nivel {nivel}", "Profundidad": "Doble (Frente)", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})
            lista_ubicaciones.append({"Codigo_Ubicacion": f"M1-01{nivel:02d}{lado_num:02d}-FO", "Pasillo_Zona": "Mike 1", "Nivel": f"Nivel {nivel}", "Profundidad": "Doble (Fondo)", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})
            lista_ubicaciones.append({"Codigo_Ubicacion": f"M2-01{nivel:02d}{lado_num:02d}", "Pasillo_Zona": "Mike 2", "Nivel": f"Nivel {nivel}", "Profundidad": "Estándar", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})

    # 7. PASILLO KILO (K) -> K01 Sencillo, K02 a K07 Doble Profundidad
    for pos in range(1, 8):
        for nivel in range(1, 6):
            for lado_num in range(1, 3):
                if pos == 1:
                    lista_ubicaciones.append({"Codigo_Ubicacion": f"K{pos:02d}{nivel:02d}{lado_num:02d}", "Pasillo_Zona": "Kilo", "Nivel": f"Nivel {nivel}", "Profundidad": "Estándar", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})
                else:
                    lista_ubicaciones.append({"Codigo_Ubicacion": f"K{pos:02d}{nivel:02d}{lado_num:02d}-FR", "Pasillo_Zona": "Kilo", "Nivel": f"Nivel {nivel}", "Profundidad": "Doble (Frente)", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})
                    lista_ubicaciones.append({"Codigo_Ubicacion": f"K{pos:02d}{nivel:02d}{lado_num:02d}-FO", "Pasillo_Zona": "Kilo", "Nivel": f"Nivel {nivel}", "Profundidad": "Doble (Fondo)", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})

    # 8. PASILLO INDIA (I) -> Posición 1 y 2, 6 Niveles de Altura, Sin profundidad
    for pos in range(1, 3):
        for nivel in range(1, 7): 
            for lado_num in range(1, 3):
                lista_ubicaciones.append({"Codigo_Ubicacion": f"I{pos:02d}{nivel:02d}{lado_num:02d}", "Pasillo_Zona": "India", "Nivel": f"Nivel {nivel}", "Profundidad": "Estándar", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})

    # 9. ZONAS DE PISO, SÓTANO, CUARTOS ESPECIALES
    zonas_especiales = [("Bodega 1 Piso", "B1-PISO"), ("Bodega 2 Piso", "B2-PISO"), ("Sótano", "SOTANO"), ("Cuarto Seguridad", "SEGURIDAD"), ("Cuarto Frío", "FRIO")]
    for z_nombre, z_prefijo in zonas_especiales:
        for espacio in range(1, 11):
            lista_ubicaciones.append({"Codigo_Ubicacion": f"{z_prefijo}-{espacio:02d}", "Pasillo_Zona": z_nombre, "Nivel": "Piso / N/A", "Profundidad": "Estándar", "Estado": "Libre", "Producto": "Ninguno", "Cantidad": 0})

    return pd.DataFrame(lista_ubicaciones)

if 'inventario' not in st.session_state:
    st.session_state.inventario = generar_bodega_real()

# --- INTERFAZ DE LA APLICACIÓN ---
st.sidebar.header("🕹️ Panel de Navegación")
rol = st.sidebar.selectbox("Seleccione el Rol:", ["Operario / Montacarguista", "Gerencia / Supervisor"])

if rol == "Operario / Montacarguista":
    st.header("📲 Interfaz Móvil para Equipos (Montacargas)")
    tab1, tab2 = st.tabs(["📥 Entrada / Almacenar", "🔍 Localizar Producto"])
    
    with tab1:
        st.subheader("Registrar movimiento de montacargas")
        df_libres = st.session_state.inventario[st.session_state.inventario['Estado'] == 'Libre']
        
        with st.form("guardar_paleta"):
            sku = st.text_input("Ingrese SKU o Nombre del Producto:", placeholder="Ej: Paleta Llantas 15")
            cant = st.number_input("Cantidad de Paletas / Cajas:", min_value=1, value=1)
            ubicacion = st.selectbox("Seleccione Código de Ubicación Destino:", df_libres['Codigo_Ubicacion'])
            
            # --- LÓGICA DE VALIDACIÓN PARA DOBLE PROFUNDIDAD Y CUARTOS ---
            cod_fondo = ""
            if ubicacion.endswith("A"): cod_fondo = ubicacion.replace("A", "B")
            elif ubicacion.endswith("-FR"): cod_fondo = ubicacion.replace("-FR", "-FO")
                
            if cod_fondo:
                fila_fondo = st.session_state.inventario[st.session_state.inventario['Codigo_Ubicacion'] == cod_fondo]
                if not fila_fondo.empty and fila_fondo['Estado'].values == "Libre":
                    st.warning(f"⚠️ **Alerta Logística:** Está guardando en el Frente ({ubicacion}) pero el Fondo ({cod_fondo}) está libre. Optimice el espacio usando primero el fondo.")
            
            if "SEGURIDAD" in ubicacion:
                st.info("🔒 **Control de Seguridad:** Esta ubicación requiere registro de precinto en bitácora manual.")
            elif "FRIO" in ubicacion:
                st.info("❄️ **Cadena de Frío:** Recuerde validar que el producto tolere refrigeración antes de confirmar.")

            btn_confirmar = st.form_submit_button("Confirmar Ubicación en Bodega")
            
            if btn_confirmar and sku:
                idx = st.session_state.inventario[st.session_state.inventario['Codigo_Ubicacion'] == ubicacion].index
                st.session_state.inventario.at[idx, 'Estado'] = 'Ocupado'
                st.session_state.inventario.at[idx, 'Producto'] = sku
                st.session_state.inventario.at[idx, 'Cantidad'] = cant
                st.success(f"✔️ Operación exitosa. Ubicación {ubicacion} actualizada a OCUPADA.")
                st.rerun()

    with tab2:
        st.subheader("Buscador rápido de posiciones")
        buscar = st.text_input("Escriba el producto que va a retirar:")
        if buscar:
            res = st.session_state.inventario[st.session_state.inventario['Producto'].str.contains(buscar, case=False)]
