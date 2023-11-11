import streamlit as st
import re
import time
import pandas as pd
import pymysql
import streamlit.components.v1 as components
from sqlalchemy import create_engine 
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode, AgGridTheme

st.set_page_config(layout="wide")


#-----------------------------------------------------------------------------#
# Filtro de clientes
#-----------------------------------------------------------------------------#
@st.cache_data
def dataclientes():
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')        
    st.session_state.dataorigen_modulo_clientes      = pd.read_sql_query(f"""SELECT * FROM {schema}.modulo_clientes WHERE available=1""" , engine)
    st.session_state.data_modulo_clientes            = st.session_state.dataorigen_modulo_clientes.copy()
    st.session_state.lista_clientes_modulo_clientes  = ['Todos'] + sorted(list(st.session_state.dataorigen_modulo_clientes[st.session_state.dataorigen_modulo_clientes['nombre_completo'].notnull()]['nombre_completo'].unique()))
    st.session_state.lista_identificacion_modulo_clientes  = ['Todos'] + sorted(list(st.session_state.dataorigen_modulo_clientes[st.session_state.dataorigen_modulo_clientes['identificacion'].notnull()]['identificacion'].unique()))
    lista                            = list(st.session_state.dataorigen_modulo_clientes[st.session_state.dataorigen_modulo_clientes['telefono1'].notnull()]['telefono1'].unique()) + list(st.session_state.dataorigen_modulo_clientes[st.session_state.dataorigen_modulo_clientes['telefono2'].notnull()]['telefono2'].unique())
    st.session_state.lista_telefonos_modulo_clientes = ['Todos'] + lista
    st.session_state.cliente_modulo_clientes         = 'Todos'
    st.session_state.identificacion_modulo_clientes  = 'Todos'
    st.session_state.telefono_modulo_clientes        = 'Todos'
    engine.dispose()


def reset_todos_modulo_clientes():
    st.session_state.data_modulo_clientes            = st.session_state.dataorigen_modulo_clientes.copy()
    st.session_state.lista_clientes_modulo_clientes  = ['Todos'] + sorted(list(st.session_state.dataorigen_modulo_clientes[st.session_state.dataorigen_modulo_clientes['nombre_completo'].notnull()]['nombre_completo'].unique()))
    st.session_state.lista_identificacion_modulo_clientes  = ['Todos'] + sorted(list(st.session_state.dataorigen_modulo_clientes[st.session_state.dataorigen_modulo_clientes['identificacion'].notnull()]['identificacion'].unique()))
    lista                            = list(st.session_state.dataorigen_modulo_clientes[st.session_state.dataorigen_modulo_clientes['telefono1'].notnull()]['telefono1'].unique()) + list(st.session_state.dataorigen_modulo_clientes[st.session_state.dataorigen_modulo_clientes['telefono2'].notnull()]['telefono2'].unique())
    st.session_state.lista_telefonos_modulo_clientes = ['Todos'] + lista
    st.session_state.cliente_modulo_clientes         = 'Todos'
    st.session_state.identificacion_modulo_clientes  = 'Todos'
    st.session_state.telefono_modulo_clientes        = 'Todos'    
    
def clientechange_modulo_clientes():
    if st.session_state.cliente_modulo_clientes=='Todos':
        reset_todos_modulo_clientes()
    else:
        idd = st.session_state.data_modulo_clientes['nombre_completo']==st.session_state.cliente_modulo_clientes
        st.session_state.data_modulo_clientes = st.session_state.data_modulo_clientes[idd]
        st.session_state.lista_clientes_modulo_clientes  = ['Todos'] + sorted(list(st.session_state.data_modulo_clientes[st.session_state.data_modulo_clientes['nombre_completo'].notnull()]['nombre_completo'].unique()))
        st.session_state.lista_identificacion_modulo_clientes  = ['Todos'] + sorted(list(st.session_state.data_modulo_clientes[st.session_state.data_modulo_clientes['identificacion'].notnull()]['identificacion'].unique()))
        lista                            = list(st.session_state.data_modulo_clientes[st.session_state.data_modulo_clientes['telefono1'].notnull()]['telefono1'].unique()) + list(st.session_state.data_modulo_clientes[st.session_state.data_modulo_clientes['telefono2'].notnull()]['telefono2'].unique())
        st.session_state.lista_telefonos_modulo_clientes = ['Todos'] + lista
        st.session_state.cliente_modulo_clientes         = st.session_state.cliente_modulo_clientes
        st.session_state.identificacion_modulo_clientes  = st.session_state.identificacion_modulo_clientes
        st.session_state.telefono_modulo_clientes        = st.session_state.telefono_modulo_clientes
        
def identificacionchange_modulo_clientes():
    if st.session_state.identificacion_modulo_clientes=='Todos':
        reset_todos_modulo_clientes()
    else:
        idd = st.session_state.data_modulo_clientes['identificacion']==st.session_state.identificacion_modulo_clientes
        st.session_state.data_modulo_clientes = st.session_state.data_modulo_clientes[idd]
        st.session_state.lista_clientes_modulo_clientes  = ['Todos'] + sorted(list(st.session_state.data_modulo_clientes[st.session_state.data_modulo_clientes['nombre_completo'].notnull()]['nombre_completo'].unique()))
        st.session_state.lista_identificacion_modulo_clientes  = ['Todos'] + sorted(list(st.session_state.data_modulo_clientes[st.session_state.data_modulo_clientes['identificacion'].notnull()]['identificacion'].unique()))
        lista                            = list(st.session_state.data_modulo_clientes[st.session_state.data_modulo_clientes['telefono1'].notnull()]['telefono1'].unique()) + list(st.session_state.data_modulo_clientes[st.session_state.data_modulo_clientes['telefono2'].notnull()]['telefono2'].unique())
        st.session_state.lista_telefonos_modulo_clientes = ['Todos'] + lista
        st.session_state.cliente_modulo_clientes         = st.session_state.cliente_modulo_clientes
        st.session_state.identificacion_modulo_clientes  = st.session_state.identificacion_modulo_clientes
        st.session_state.telefono_modulo_clientes        = st.session_state.telefono_modulo_clientes
        
def telefonochange_modulo_clientes():
    if st.session_state.telefono_modulo_clientes=='Todos':
        reset_todos_modulo_clientes()
    else:
        idd = (st.session_state.data_modulo_clientes['telefono1']==st.session_state.telefono_modulo_clientes) | (st.session_state.data_modulo_clientes['telefono2']==st.session_state.telefono_modulo_clientes)
        st.session_state.data_modulo_clientes = st.session_state.data_modulo_clientes[idd]
        st.session_state.lista_clientes_modulo_clientes  = ['Todos'] + sorted(list(st.session_state.data_modulo_clientes[st.session_state.data_modulo_clientes['nombre_completo'].notnull()]['nombre_completo'].unique()))
        st.session_state.lista_identificacion_modulo_clientes  = ['Todos'] + sorted(list(st.session_state.data_modulo_clientes[st.session_state.data_modulo_clientes['identificacion'].notnull()]['identificacion'].unique()))
        lista                            = list(st.session_state.data_modulo_clientes[st.session_state.data_modulo_clientes['telefono1'].notnull()]['telefono1'].unique()) + list(st.session_state.data_modulo_clientes[st.session_state.data_modulo_clientes['telefono2'].notnull()]['telefono2'].unique())
        st.session_state.lista_telefonos_modulo_clientes = ['Todos'] + lista   
        st.session_state.lista_telefonos_modulo_clientes = st.session_state.lista_telefonos_modulo_clientes
        st.session_state.cliente_modulo_clientes         = st.session_state.cliente_modulo_clientes
        st.session_state.identificacion_modulo_clientes  = st.session_state.identificacion_modulo_clientes
        st.session_state.telefono_modulo_clientes        = st.session_state.telefono_modulo_clientes
        
        
#-----------------------------------------------------------------------------#
# Crear
def crear_cliente():

    st.write('---')
    col1,col2,col3 = st.columns([3,1,2])
    with col1:
        nombre = st.text_input('Nombre del cliente',value='')
    with col2:
        tipoid = st.selectbox('Tipo de identificación', options=['CC','CE','NIT','Pasaporte'])
    with col3:
        numerodid = st.text_input('Identificación',value='')

    col1,col2,col3 = st.columns([1,1,2])
    with col1:
        telefono1 = st.text_input('Telefono de contacto (1)',value='')
    with col2:
        telefono2 = st.text_input('Telefono de contacto (2)',value='')
    with col3:
        email = st.text_input('Email',value='')
        
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Guardar'):
            with st.spinner('Guardando cliente'):
                if nombre!='':
                    nombre    = re.sub('\s+',' ',nombre).title()
                    engine    = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')        
                    datastock = pd.read_sql_query(f"""SELECT id FROM {schema}.modulo_clientes WHERE (nombre_completo='{nombre}' OR identificacion='{numerodid}') AND available=1""" , engine)
                    if datastock.empty:
                        dataexport = pd.DataFrame([{'fecha_registro': datetime.now().strftime('%Y-%m-%d'),'nombre_completo':nombre,'tipo_identificacion':tipoid,'identificacion':numerodid,'telefono1':telefono1,'telefono2':telefono2,'email':email,'available':1}])
                        dataexport = dataexport.replace('', None)
                        dataexport.to_sql('modulo_clientes', engine, if_exists='append', index=False, chunksize=1)
                        st.success('Cliente guardado exitosamente')
                    else:
                        st.error('Nombre y/o identificación ya existe en la base de datos')
                    engine.dispose()
                    time.sleep(5)
                    st.cache_data.clear()
                    st.session_state.tipo_clientes = True
                    st.session_state.tipo_crear    = False
                    st.rerun()
                else: st.error('Debe poner un nombre del cliente')
            
            
#-----------------------------------------------------------------------------#
# Clientes  
def clientes():       

    dataclientes()
    
    st.write('---')
    st.write('Filtros')
    col1,col2,col3 = st.columns(3)
    with col1: 
        st.selectbox('Por cliente', options=st.session_state.lista_clientes_modulo_clientes,key='cliente_modulo_clientes',on_change=clientechange_modulo_clientes)
    with col2: 
        st.selectbox('Por identificacion', options=st.session_state.lista_identificacion_modulo_clientes,key='identificacion_modulo_clientes',on_change=identificacionchange_modulo_clientes)
    with col3: 
        st.selectbox('Por telefono', options=st.session_state.lista_telefonos_modulo_clientes,key='telefono_modulo_clientes',on_change=telefonochange_modulo_clientes)

    datastockagrid = st.session_state.data_modulo_clientes.copy()
    variables = [x for x in ['id','nombre_completo','tipo_identificacion','identificacion','telefono1', 'telefono2','email'] if x in datastockagrid]
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
    
    if response['selected_rows']:
        datastockagridfilter = datastockagrid[datastockagrid['id']==response['selected_rows'][0]['id']]
        datastockagridfilter = datastockagridfilter.iloc[[0]]
        datastockagridfilter.index = range(len(datastockagridfilter))
        datastockedit              = datastockagridfilter.copy()
        
        st.write('---')
        st.write('Información del Cliente')
        
        col1,col2,col3 = st.columns([3,1,2])
        with col1:
            nombre = st.text_input('Nombre del cliente',value=datastockedit['nombre_completo'].iloc[0])
            datastockedit.loc[0,'nombre_completo'] = re.sub('\s+',' ',nombre).title()
        with col2:
            lista  = ['CC','CE','NIT','Pasaporte']
            try:    
                if datastockedit['tipo_identificacion'].iloc[0] in lista: 
                    indice = lista.index(datastockedit['tipo_identificacion'].iloc[0])
                else:
                    indice = 0
            except: indice = 0
            tipoid = st.selectbox('Tipo de identificación', options=lista,index=indice)
            datastockedit.loc[0,'tipo_identificacion'] = tipoid
        with col3:
            numerodid = st.text_input('Identificación',value=datastockedit['identificacion'].iloc[0])
            datastockedit.loc[0,'identificacion'] = numerodid
    
        col1,col2,col3 = st.columns([1,1,2])
        with col1:
            telefono1 = st.text_input('Telefono de contacto (1)',value=datastockedit['telefono1'].iloc[0])
            datastockedit.loc[0,'telefono1'] = telefono1
        with col2:
            telefono2 = st.text_input('Telefono de contacto (2)',value=datastockedit['telefono2'].iloc[0])
            datastockedit.loc[0,'telefono2'] = telefono2
        with col3:
            email = st.text_input('Email',value=datastockedit['email'].iloc[0])
            datastockedit.loc[0,'email'] = email
            
        col1, col2 = st.columns(2)
        with col1:
            if st.button('Guardar'):
                st.session_state.editar        = True
                st.session_state.borrar        = False
                st.session_state.borrarconfirm = False
                
        with col2:
            if st.button('Borrar cliente'):
                st.session_state.editar        = False
                st.session_state.borrar        = True
                st.session_state.borrarconfirm = False
    
        if st.session_state.editar:
            editar_cliente(datastockedit)                
                
        if st.session_state.borrar:
            with col2:
                if st.button('Seguro quiere borrar el cliente?'):
                    st.session_state.borrarconfirm = True

        if st.session_state.borrarconfirm and st.session_state.borrar:
            borrar_cliente(datastockedit)
            

def editar_cliente(datastock):
    with st.spinner('Guardando cliente'):
        datastock = datastock.replace('', None)
        vardrop   = [x for x in ['fecha_registro'] if x in list(datastock)]
        if vardrop!=[]: datastock.drop(columns=vardrop,inplace=True)
        variables = list(datastock)
        variables.remove('id')
        condicion = '`'+'`=%s,`'.join(variables)+'`=%s'
        variables.append('id')
        datastock = datastock[variables]
        conn = pymysql.connect(host=host,
                       user=user,
                       password=password,
                       db=schema)
        with conn.cursor() as cursor:
            sql = f"UPDATE modulo_clientes SET {condicion} WHERE `id` = %s"
            list_of_tuples = datastock.to_records(index=False).tolist()
            cursor.executemany(sql, list_of_tuples)
        st.success('Cliente guardado exitosamente')
        conn.commit()
        conn.close()
        time.sleep(5)
        st.cache_data.clear()
        for i in ['editar','borrar','borrarconfirm']:
            if i in st.session_state:
                del st.session_state[i]
            if i not in st.session_state: 
                st.session_state[i] = False
        st.rerun()

def borrar_cliente(datastock):
    with st.spinner('Borrando cliente'):
        datastock = datastock[['id']]
        conn      = pymysql.connect(host=host,
                       user=user,
                       password=password,
                       db=schema)
        with conn.cursor() as cursor:
            #sql = "DELETE FROM modulo_clientes WHERE id = %s"
            sql = "UPDATE modulo_clientes SET available=0 WHERE `id` = %s"
            list_of_tuples = datastock.to_records(index=False).tolist()
            cursor.executemany(sql, list_of_tuples)
        st.success('Cliente borrado exitosamente')
        conn.commit()
        conn.close()
        time.sleep(5)
        st.cache_data.clear()
        for i in ['editar','borrar','borrarconfirm']:
            if i in st.session_state:
                del st.session_state[i]
            if i not in st.session_state: 
                st.session_state[i] = False
        st.rerun()
#-----------------------------------------------------------------------------#


user     = st.secrets["user_bigdata"]
password = st.secrets["password_bigdata"]
host     = st.secrets["host_bigdata"]
schema   = 'partyplum'

formato = {'tipo_crear':False,
           'tipo_clientes':False,
           'editar':False,
           'borrar':False,
           'borrarconfirm':False,
           'cliente_modulo_clientes':'',
           'lista_clientes_modulo_clientes':[],
           'identificacion_modulo_clientes':'',
           'lista_identificacion_modulo_clientes':[],
           'telefono_modulo_clientes':'',
           'lista_telefonos_modulo_clientes':[],
           'dataorigen_modulo_clientes':pd.DataFrame(),
           'data_modulo_clientes':pd.DataFrame()
}

for key,value in formato.items():
    if key not in st.session_state: 
        st.session_state[key] = value
        
col1,col2 = st.columns(2) 
with col1:
    if st.button('Crear'):
        st.session_state.tipo_crear    = True
        st.session_state.tipo_clientes = False
        
with col2:
    if st.button('Clientes'):
        st.session_state.tipo_clientes = True
        st.session_state.tipo_crear    = False
 
if st.session_state.tipo_crear:
    crear_cliente()
    
if st.session_state.tipo_clientes:
    clientes()
                   
components.html(
    """
<script>
const elements = window.parent.document.querySelectorAll('.stButton button')
elements[0].style.backgroundColor = '#cc7076';
elements[0].style.fontWeight = 'bold';
elements[0].style.color = 'white';
elements[0].style.width = '100%';
elements[1].style.backgroundColor = '#cc7076';
elements[1].style.fontWeight = 'bold';
elements[1].style.color = 'white';
elements[1].style.width = '100%';
elements[2].style.backgroundColor = '#cc7076';
elements[2].style.fontWeight = 'bold';
elements[2].style.color = 'white';
elements[2].style.width = '100%';
elements[3].style.backgroundColor = '#cc7076';
elements[3].style.fontWeight = 'bold';
elements[3].style.color = 'white';
elements[3].style.width = '100%'
elements[4].style.backgroundColor = '#cc7076';
elements[4].style.fontWeight = 'bold';
elements[4].style.color = 'white';
elements[4].style.width = '100%'
elements[5].style.backgroundColor = '#cc7076';
elements[5].style.fontWeight = 'bold';
elements[5].style.color = 'white';
elements[5].style.width = '100%'
elements[6].style.backgroundColor = '#cc7076';
elements[6].style.fontWeight = 'bold';
elements[6].style.color = 'white';
elements[6].style.width = '100%'
elements[7].style.backgroundColor = '#cc7076';
elements[7].style.fontWeight = 'bold';
elements[7].style.color = 'white';
elements[7].style.width = '100%'
elements[8].style.backgroundColor = '#cc7076';
elements[8].style.fontWeight = 'bold';
elements[8].style.color = 'white';
elements[8].style.width = '100%'
elements[9].style.backgroundColor = '#cc7076';
elements[9].style.fontWeight = 'bold';
elements[9].style.color = 'white';
elements[9].style.width = '100%'
</script>
"""
)