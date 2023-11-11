import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from sqlalchemy import create_engine 
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode, AgGridTheme

st.set_page_config(layout="wide")

#-----------------------------------------------------------------------------#
# Filtro para editar eventos
#-----------------------------------------------------------------------------#
@st.cache_data
def datacontable():
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')        
    st.session_state.data_facturacion_clientes = pd.read_sql_query(f"""SELECT * FROM {schema}.modulo_facturacion_clientes """ , engine)
    st.session_state.data_facturacion_terceros = pd.read_sql_query(f"""SELECT * FROM {schema}.modulo_gastos_terceros WHERE available=1""" , engine)
    
    for i in ['fecha_pago','fecha_factura']:
        if i in st.session_state.data_facturacion_clientes:
            try: st.session_state.data_facturacion_clientes[i] = pd.to_datetime(st.session_state.data_facturacion_clientes[i],errors='coerce')
            except: pass
        
    for i in ['fecha_pago','fecha_factura']:
        if i in st.session_state.data_facturacion_terceros:
            try: st.session_state.data_facturacion_terceros[i] = pd.to_datetime(st.session_state.data_facturacion_terceros[i],errors='coerce')
            except: pass
    engine.dispose()
    
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')
#-----------------------------------------------------------------------------#


user     = st.secrets["user_bigdata"]
password = st.secrets["password_bigdata"]
host     = st.secrets["host_bigdata"]
schema   = 'partyplum'

formato = {
           'data_facturacion_clientes':pd.DataFrame(),
           'data_facturacion_terceros':pd.DataFrame()
}

for key,value in formato.items():
    if key not in st.session_state: 
        st.session_state[key] = value
        
datacontable()

#-----------------------------------------------------------------------------#
# Facturacion de terceros
#-----------------------------------------------------------------------------#
col1, col2 = st.columns(2)
with col1:
    fecha_inicial = st.date_input('Fecha inicial',value=None)
with col2:
    if fecha_inicial is not None:
        fecha_maxima  = st.date_input('Fecha final',min_value=fecha_inicial)
    else: fecha_maxima  = st.date_input('Fecha final', value=None)

st.write('---')
st.write('Informacion gastos a terceros')
datastockagrid = st.session_state.data_facturacion_terceros.copy()


datastockagrid.index = range(len(datastockagrid))

idd = datastockagrid.index>=0
if fecha_inicial is not None:
    idd = (idd) & (datastockagrid['fecha_pago']>=fecha_inicial.strftime('%Y-%m-%d'))
if fecha_maxima is not None:
    idd = (idd) & (datastockagrid['fecha_pago']<=fecha_maxima.strftime('%Y-%m-%d'))
        
datastockagrid = datastockagrid[idd]
variables      = [x for x in ['id', 'fecha_factura', 'tipo_gasto', 'nombre_razon_social', 'nombre_comercial', 'tipo_identificacion', 'identificacion', 'documento1', 'documento2', 'documento3', 'valor_factura', 'iva', 'retencion_fuente', 'retencion_ica', 'pagada', 'forma_pago', 'fecha_pago', 'comprobante_pago'] if x in datastockagrid]
gb = GridOptionsBuilder.from_dataframe(datastockagrid[variables])
gb.configure_default_column(cellStyle={'color': 'grey', 'font-size': '20px'}, resizable=True, filterable=True, sortable=True, suppressMenu=True, wrapHeaderText=True, autoHeaderHeight=True)
gb.configure_selection(selection_mode="single", use_checkbox=True)

gridOptions = gb.build()

# Configurar las opciones de estilo personalizado
custom_css = {
    ".ag-header-cell-text": {
        "font-size": "20px",
        "text-overflow": "revert",
        "font-weight": 1000,
        "text-align": "center"
    },
    ".ag-theme-streamlit": {
        "transform": "scale(0.8)",
        "transform-origin": "0 0",
        "width": "100vw"
    }
}

response = AgGrid(
    datastockagrid[variables],
    gridOptions=gridOptions,
    custom_css=custom_css,
    columns_auto_size_mode="FIT_CONTENTS",
    use_checkbox=True,
    theme=AgGridTheme.STREAMLIT,
    domLayout='autoHeight',
)

col1,col2 = st.columns(2)
with col1:
    csv = convert_df(datastockagrid)     
    st.download_button(
       "Descargar facturacion gastos a terceros",
       csv,
       "data_facturacion_gastos_terceros.csv",
       "text/csv",
       key='data_facturacion_gastos_terceros_csv'
    )

components.html(
    """
<script>
const elements = window.parent.document.querySelectorAll('.stDownloadButton button')
elements[0].style.width = '100%';
elements[0].style.fontWeight = 'bold';
elements[0].style.backgroundColor = '#17e88f';
</script>
"""
)

#-----------------------------------------------------------------------------#
# Facturacion a clientes
#-----------------------------------------------------------------------------#
st.write('---')
st.write('Informacion facturacion a los clientes')

datastockagrid = st.session_state.data_facturacion_clientes.copy()
datastockagrid.index = range(len(datastockagrid))
idd = datastockagrid.index>=0
if fecha_inicial is not None:
    idd = (idd) & (datastockagrid['fecha_factura']>=fecha_inicial.strftime('%Y-%m-%d'))
if fecha_maxima is not None:
    idd = (idd) & (datastockagrid['fecha_factura']<=fecha_maxima.strftime('%Y-%m-%d'))

datastockagrid = datastockagrid[idd]
variables      = [x for x in ['id', 'fecha_factura', 'valor_factura', 'factura', 'valor_paquete', 'valor_recaudo_terceros', 'iva', 'ganancia', 'fecha_pago1', 'valor_pago1', 'pago1', 'fecha_pago2', 'valor_pago2', 'pago2', 'fecha_pago3', 'valor_pago3', 'pago3', 'fecha_pago4', 'valor_pago4', 'pago4'] if x in datastockagrid]
gb = GridOptionsBuilder.from_dataframe(datastockagrid[variables])
gb.configure_default_column(cellStyle={'color': 'grey', 'font-size': '20px'}, resizable=True, filterable=True, sortable=True, suppressMenu=True, wrapHeaderText=True, autoHeaderHeight=True)
gb.configure_selection(selection_mode="single", use_checkbox=True)

gridOptions = gb.build()

# Configurar las opciones de estilo personalizado
custom_css = {
    ".ag-header-cell-text": {
        "font-size": "20px",
        "text-overflow": "revert",
        "font-weight": 1000,
        "text-align": "center"
    },
    ".ag-theme-streamlit": {
        "transform": "scale(0.8)",
        "transform-origin": "0 0",
        "width": "100vw"
    }
}

response = AgGrid(
    datastockagrid[variables],
    gridOptions=gridOptions,
    custom_css=custom_css,
    columns_auto_size_mode="FIT_CONTENTS",
    use_checkbox=True,
    theme=AgGridTheme.STREAMLIT,
    domLayout='autoHeight',
)

col1,col2 = st.columns(2)
with col1:
    csv = convert_df(datastockagrid)     
    st.download_button(
       "Descargar facturacion a los clientes",
       csv,
       "data_facturacion_clientes.csv",
       "text/csv",
       key='data_facturacion_clientes_csv'
    )
    
components.html(
    """
<script>
const elements = window.parent.document.querySelectorAll('.stDownloadButton button')
elements[1].style.width = '100%';
elements[1].style.fontWeight = 'bold';
elements[1].style.backgroundColor = '#17e88f';
</script>
"""
)