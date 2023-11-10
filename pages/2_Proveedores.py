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
# Filtro de proveedores
#-----------------------------------------------------------------------------#
@st.cache_data
def dataproveedores():
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')        
    st.session_state.dataorigen_modulo_proveedores      = pd.read_sql_query(f"""SELECT * FROM {schema}.modulo_proveedores WHERE available=1""" , engine)
    st.session_state.data_modulo_proveedores            = st.session_state.dataorigen_modulo_proveedores.copy()
    st.session_state.lista_proveedores_modulo_proveedores    = ['Todos'] + sorted(list(st.session_state.dataorigen_modulo_proveedores[st.session_state.dataorigen_modulo_proveedores['nombre_razon_social'].notnull()]['nombre_razon_social'].unique()))
    st.session_state.lista_identificacion_modulo_proveedores = ['Todos'] + sorted(list(st.session_state.dataorigen_modulo_proveedores[st.session_state.dataorigen_modulo_proveedores['identificacion'].notnull()]['identificacion'].unique()))
    st.session_state.lista_contacto_modulo_proveedores  = ['Todos'] + sorted(list(st.session_state.dataorigen_modulo_proveedores[st.session_state.dataorigen_modulo_proveedores['nombre_contacto'].notnull()]['nombre_contacto'].unique()))
    lista                            = list(st.session_state.dataorigen_modulo_proveedores[st.session_state.dataorigen_modulo_proveedores['telefono1'].notnull()]['telefono1'].unique()) + list(st.session_state.dataorigen_modulo_proveedores[st.session_state.dataorigen_modulo_proveedores['telefono2'].notnull()]['telefono2'].unique())
    st.session_state.lista_telefonos_modulo_proveedores = ['Todos'] + lista
    st.session_state.proveedor_modulo_proveedores       = 'Todos'
    st.session_state.identificacion_modulo_proveedores  = 'Todos'
    st.session_state.contacto_modulo_proveedores        = 'Todos'
    st.session_state.telefono_modulo_proveedores        = 'Todos'
    
    engine.dispose()
    
    
def reset_todos_modulo_proveedores():
    st.session_state.data_modulo_proveedores                 = st.session_state.dataorigen_modulo_proveedores.copy()
    st.session_state.lista_proveedores_modulo_proveedores    = ['Todos'] + sorted(list(st.session_state.dataorigen_modulo_proveedores[st.session_state.dataorigen_modulo_proveedores['nombre_razon_social'].notnull()]['nombre_razon_social'].unique()))
    st.session_state.lista_identificacion_modulo_proveedores = ['Todos'] + sorted(list(st.session_state.dataorigen_modulo_proveedores[st.session_state.dataorigen_modulo_proveedores['identificacion'].notnull()]['identificacion'].unique()))
    st.session_state.lista_contacto_modulo_proveedores  = ['Todos'] + sorted(list(st.session_state.dataorigen_modulo_proveedores[st.session_state.dataorigen_modulo_proveedores['nombre_contacto'].notnull()]['nombre_contacto'].unique()))
    lista                            = list(st.session_state.dataorigen_modulo_proveedores[st.session_state.dataorigen_modulo_proveedores['telefono1'].notnull()]['telefono1'].unique()) + list(st.session_state.dataorigen_modulo_proveedores[st.session_state.dataorigen_modulo_proveedores['telefono2'].notnull()]['telefono2'].unique())
    st.session_state.lista_telefonos_modulo_proveedores = ['Todos'] + lista
    st.session_state.proveedor_modulo_proveedores       = 'Todos'
    st.session_state.identificacion_modulo_proveedores  = 'Todos'
    st.session_state.contacto_modulo_proveedores        = 'Todos'
    st.session_state.telefono_modulo_proveedores        = 'Todos'    
    
def proveedorchange_modulo_proveedores():
    if st.session_state.proveedor_modulo_proveedores=='Todos':
        reset_todos_modulo_proveedores()
    else:
        idd = st.session_state.data_modulo_proveedores['nombre_razon_social']==st.session_state.proveedor_modulo_proveedores
        st.session_state.data_modulo_proveedores = st.session_state.data_modulo_proveedores[idd]
        st.session_state.lista_proveedores_modulo_proveedores    = ['Todos'] + sorted(list(st.session_state.data_modulo_proveedores[st.session_state.data_modulo_proveedores['nombre_razon_social'].notnull()]['nombre_razon_social'].unique()))
        st.session_state.lista_identificacion_modulo_proveedores = ['Todos'] + sorted(list(st.session_state.data_modulo_proveedores[st.session_state.data_modulo_proveedores['identificacion'].notnull()]['identificacion'].unique()))
        st.session_state.lista_contacto_modulo_proveedores  = ['Todos'] + sorted(list(st.session_state.data_modulo_proveedores[st.session_state.data_modulo_proveedores['nombre_contacto'].notnull()]['nombre_contacto'].unique()))
        lista                            = list(st.session_state.data_modulo_proveedores[st.session_state.data_modulo_proveedores['telefono1'].notnull()]['telefono1'].unique()) + list(st.session_state.data_modulo_proveedores[st.session_state.data_modulo_proveedores['telefono2'].notnull()]['telefono2'].unique())
        st.session_state.lista_telefonos_modulo_proveedores = ['Todos'] + lista
        st.session_state.proveedor_modulo_proveedores       = st.session_state.proveedor_modulo_proveedores
        st.session_state.identificacion_modulo_proveedores  = st.session_state.identificacion_modulo_proveedores
        st.session_state.contacto_modulo_proveedores        = st.session_state.contacto_modulo_proveedores
        st.session_state.telefono_modulo_proveedores        = st.session_state.telefono_modulo_proveedores
        
def identificacionchange_modulo_proveedores():
    if st.session_state.identificacion_modulo_proveedores=='Todos':
        reset_todos_modulo_proveedores()
    else:
        idd = st.session_state.data_modulo_proveedores['identificacion']==st.session_state.identificacion_modulo_proveedores
        st.session_state.data_modulo_proveedores = st.session_state.data_modulo_proveedores[idd]
        st.session_state.lista_proveedores_modulo_proveedores    = ['Todos'] + sorted(list(st.session_state.data_modulo_proveedores[st.session_state.data_modulo_proveedores['nombre_razon_social'].notnull()]['nombre_razon_social'].unique()))
        st.session_state.lista_identificacion_modulo_proveedores = ['Todos'] + sorted(list(st.session_state.data_modulo_proveedores[st.session_state.data_modulo_proveedores['identificacion'].notnull()]['identificacion'].unique()))
        st.session_state.lista_contacto_modulo_proveedores  = ['Todos'] + sorted(list(st.session_state.data_modulo_proveedores[st.session_state.data_modulo_proveedores['nombre_contacto'].notnull()]['nombre_contacto'].unique()))
        lista                            = list(st.session_state.data_modulo_proveedores[st.session_state.data_modulo_proveedores['telefono1'].notnull()]['telefono1'].unique()) + list(st.session_state.data_modulo_proveedores[st.session_state.data_modulo_proveedores['telefono2'].notnull()]['telefono2'].unique())
        st.session_state.lista_telefonos_modulo_proveedores = ['Todos'] + lista
        st.session_state.proveedor_modulo_proveedores       = st.session_state.proveedor_modulo_proveedores
        st.session_state.identificacion_modulo_proveedores  = st.session_state.identificacion_modulo_proveedores
        st.session_state.contacto_modulo_proveedores        = st.session_state.contacto_modulo_proveedores
        st.session_state.telefono_modulo_proveedores        = st.session_state.telefono_modulo_proveedores
        
def contactochange_modulo_proveedores():
    if st.session_state.contacto_modulo_proveedores=='Todos':
        reset_todos_modulo_proveedores()
    else:
        idd = st.session_state.data_modulo_proveedores['nombre_contacto']==st.session_state.contacto_modulo_proveedores
        st.session_state.data_modulo_proveedores = st.session_state.data_modulo_proveedores[idd]
        st.session_state.lista_proveedores_modulo_proveedores    = ['Todos'] + sorted(list(st.session_state.data_modulo_proveedores[st.session_state.data_modulo_proveedores['nombre_razon_social'].notnull()]['nombre_razon_social'].unique()))
        st.session_state.lista_identificacion_modulo_proveedores = ['Todos'] + sorted(list(st.session_state.data_modulo_proveedores[st.session_state.data_modulo_proveedores['identificacion'].notnull()]['identificacion'].unique()))
        st.session_state.lista_contacto_modulo_proveedores  = ['Todos'] + sorted(list(st.session_state.data_modulo_proveedores[st.session_state.data_modulo_proveedores['nombre_contacto'].notnull()]['nombre_contacto'].unique()))
        lista                            = list(st.session_state.data_modulo_proveedores[st.session_state.data_modulo_proveedores['telefono1'].notnull()]['telefono1'].unique()) + list(st.session_state.data_modulo_proveedores[st.session_state.data_modulo_proveedores['telefono2'].notnull()]['telefono2'].unique())
        st.session_state.lista_telefonos_modulo_proveedores = ['Todos'] + lista
        st.session_state.proveedor_modulo_proveedores       = st.session_state.proveedor_modulo_proveedores
        st.session_state.identificacion_modulo_proveedores  = st.session_state.identificacion_modulo_proveedores
        st.session_state.contacto_modulo_proveedores        = st.session_state.contacto_modulo_proveedores
        st.session_state.telefono_modulo_proveedores        = st.session_state.telefono_modulo_proveedores
        
def telefonochange_modulo_proveedores():
    if st.session_state.telefono_modulo_proveedores=='Todos':
        reset_todos_modulo_proveedores()
    else:
        idd = (st.session_state.data_modulo_proveedores['telefono1']==st.session_state.telefono_modulo_proveedores) | (st.session_state.data_modulo_proveedores['telefono2']==st.session_state.telefono_modulo_proveedores)
        st.session_state.data_modulo_proveedores = st.session_state.data_modulo_proveedores[idd]
        st.session_state.lista_proveedores_modulo_proveedores    = ['Todos'] + sorted(list(st.session_state.data_modulo_proveedores[st.session_state.data_modulo_proveedores['nombre_razon_social'].notnull()]['nombre_razon_social'].unique()))
        st.session_state.lista_identificacion_modulo_proveedores = ['Todos'] + sorted(list(st.session_state.data_modulo_proveedores[st.session_state.data_modulo_proveedores['identificacion'].notnull()]['identificacion'].unique()))
        st.session_state.lista_contacto_modulo_proveedores  = ['Todos'] + sorted(list(st.session_state.data_modulo_proveedores[st.session_state.data_modulo_proveedores['nombre_contacto'].notnull()]['nombre_contacto'].unique()))
        lista                            = list(st.session_state.data_modulo_proveedores[st.session_state.data_modulo_proveedores['telefono1'].notnull()]['telefono1'].unique()) + list(st.session_state.data_modulo_proveedores[st.session_state.data_modulo_proveedores['telefono2'].notnull()]['telefono2'].unique())
        st.session_state.lista_telefonos_modulo_proveedores = ['Todos'] + lista   
        st.session_state.lista_telefonos_modulo_proveedores = st.session_state.lista_telefonos_modulo_proveedores
        st.session_state.proveedor_modulo_proveedores       = st.session_state.proveedor_modulo_proveedores
        st.session_state.identificacion_modulo_proveedores  = st.session_state.identificacion_modulo_proveedores
        st.session_state.contacto_modulo_proveedores        = st.session_state.contacto_modulo_proveedores
        st.session_state.telefono_modulo_proveedores        = st.session_state.telefono_modulo_proveedores
        
        
#-----------------------------------------------------------------------------#
# Crear
def crear_proveedores():
    
    st.write('---')
    col1,col2,col3,col4 = st.columns([3,3,1,2])
    with col1:
        nombre = st.text_input('Nombre o razon social',value='')
    with col2:
        nombre_comercial = st.text_input('Nombre comercial',value='')
        nombre_comercial = re.sub('\s+',' ',nombre_comercial).title()
    with col3:
        tipoid = st.selectbox('Tipo', options=['CC','CE','NIT','Pasaporte'])
    with col4:
        numerodid = st.text_input('Identificación',value='')

    col1,col2,col3 = st.columns([3,2,2])
    with col1:
        contacto = st.text_input('Nombre de contacto',value='')
        contacto = re.sub('\s+',' ',contacto).title()
    with col2:
        telefono1 = st.text_input('Telefono de contacto (1)',value='')
    with col3:
        telefono2 = st.text_input('Telefono de contacto (2)',value='')
        
    with col1:
        email = st.text_input('Email',value='')
    with col2:
        ciudad = st.selectbox('Ciudad', options=['Bogota'])
    with col3:
        direccion = st.text_input('Dirección',value='')
        
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Guardar'):
            with st.spinner('Guardando proveedor'):
                if nombre!='' and numerodid!='':
                    nombre    = re.sub('\s+',' ',nombre).upper()
                    engine    = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')        
                    datastock = pd.read_sql_query(f"""SELECT id FROM {schema}.modulo_proveedores WHERE (nombre_razon_social='{nombre}' OR identificacion='{numerodid}') AND available=1""" , engine)
                    if datastock.empty:
                        dataexport = pd.DataFrame([{'fecha_registro': datetime.now().strftime('%Y-%m-%d'),'nombre_razon_social':nombre,'nombre_comercial':nombre_comercial,'tipo_identificacion':tipoid,'identificacion': numerodid,'nombre_contacto':contacto,'telefono1': telefono1,'telefono2':telefono2,'email': email,'ciudad':ciudad,'direccion':direccion,'available':1}])
                        dataexport = dataexport.replace('', None)
                        dataexport.to_sql('modulo_proveedores', engine, if_exists='append', index=False, chunksize=1)
                        st.success('Proveedor guardado exitosamente')
                    else:
                        st.error('Nombre o razon social y/o identificación ya existe en la base de datos')
                    engine.dispose()
                    time.sleep(5)
                    st.cache_data.clear()
                    st.session_state.tipo_proveedores = True
                    st.session_state.tipo_crear       = False
                    st.rerun()
                else: st.error('Debe poner un nombre del proveedor e identificación') 
        
#-----------------------------------------------------------------------------#
# Proveedores    
def proveedores():
    
    dataproveedores()
    st.write('---')
    st.write('Filtros')
    col1,col2,col3,col4 = st.columns(4)
    with col1: 
        st.selectbox('Por Proveedor', options=st.session_state.lista_proveedores_modulo_proveedores,key='proveedor_modulo_proveedores',on_change=proveedorchange_modulo_proveedores)
    with col2: 
        st.selectbox('Por Identificacion', options=st.session_state.lista_identificacion_modulo_proveedores,key='identificacion_modulo_proveedores',on_change=identificacionchange_modulo_proveedores)
    with col3: 
        st.selectbox('Por Telefono', options=st.session_state.lista_telefonos_modulo_proveedores,key='telefono_modulo_proveedores',on_change=telefonochange_modulo_proveedores)
    with col4: 
        st.selectbox('Por nombre de contacto', options=st.session_state.lista_contacto_modulo_proveedores,key='contacto_modulo_proveedores',on_change=contactochange_modulo_proveedores)

    datastockagrid = st.session_state.data_modulo_proveedores.copy()
    gb = GridOptionsBuilder.from_dataframe(datastockagrid)
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
        datastockagrid,
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
        datastockagridfilter       = datastockagridfilter.fillna(value='')
        datastockedit              = datastockagridfilter.copy()
        
        st.write('---')
        st.write('Información del Proveedor')

        col1,col2,col3,col4 = st.columns([3,3,1,2])
        with col1:
            nombre = st.text_input('Nombre o razon social',value=datastockedit['nombre_razon_social'].iloc[0])
            datastockedit.loc[0,'nombre_razon_social'] = re.sub('\s+',' ',nombre).upper()
        with col2:
            nombre_comercial = st.text_input('Nombre comercial',value=datastockedit['nombre_comercial'].iloc[0])
            nombre_comercial = re.sub('\s+',' ',nombre_comercial).title()
            datastockedit.loc[0,'nombre_comercial'] = nombre_comercial
        with col3:
            lista  = ['CC','CE','NIT','Pasaporte']
            try:    
                if datastockedit['tipo_identificacion'].iloc[0] in lista: 
                    indice = lista.index(datastockedit['tipo_identificacion'].iloc[0])
                else:
                    indice = 0
            except: indice = 0
            tipoid = st.selectbox('Tipo', options=lista,index=indice)
            datastockedit.loc[0,'tipo_identificacion'] = tipoid
        with col4:
            numerodid = st.text_input('Identificación',value=datastockedit['identificacion'].iloc[0])
            datastockedit.loc[0,'identificacion'] = numerodid
        col1,col2,col3 = st.columns([3,2,2])
        with col1:
            contacto = st.text_input('Nombre de contacto',value=datastockedit['nombre_contacto'].iloc[0])
            contacto = re.sub('\s+',' ',contacto).title()
            datastockedit.loc[0,'nombre_contacto'] = contacto
        with col2:
            telefono1 = st.text_input('Telefono de contacto (1)',value=datastockedit['telefono1'].iloc[0])
            datastockedit.loc[0,'telefono1'] = telefono1
        with col3:
            telefono2 = st.text_input('Telefono de contacto (2)',value=datastockedit['telefono2'].iloc[0])
            datastockedit.loc[0,'telefono2'] = telefono2
            
        with col1:
            email = st.text_input('Email',value=datastockedit['email'].iloc[0])
            datastockedit.loc[0,'email'] = email
        with col2:
            lista  = ['Bogota']
            try:    
                if datastockedit['ciudad'].iloc[0] in lista: 
                    indice = lista.index(datastockedit['ciudad'].iloc[0])
                else:
                    indice = 0
            except: indice = 0
            ciudad = st.selectbox('Ciudad', options=lista,index=indice)
            datastockedit.loc[0,'ciudad'] = ciudad
        with col3:
            direccion = st.text_input('Dirección',value=datastockedit['direccion'].iloc[0])
            datastockedit.loc[0,'direccion'] = direccion
            
            
        col1, col2 = st.columns(2)
        with col1:
            if st.button('Guardar'):
                st.session_state.editar        = True
                st.session_state.borrar        = False
                st.session_state.borrarconfirm = False
                
        with col2:
            if st.button('Borrar proveedor'):
                st.session_state.editar        = False
                st.session_state.borrar        = True
                st.session_state.borrarconfirm = False
    
        if st.session_state.editar:
            editar_proveedor(datastockedit)                
                
        if st.session_state.borrar:
            with col2:
                if st.button('Seguro quiere borrar el proveedor?'):
                    st.session_state.borrarconfirm = True

        if st.session_state.borrarconfirm and st.session_state.borrar:
            borrar_proveedor(datastockedit)
            
def editar_proveedor(datastock):     
    with st.spinner('Guardando proveedor'):
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
            sql = f"UPDATE modulo_proveedores SET {condicion} WHERE `id` = %s"
            list_of_tuples = datastock.to_records(index=False).tolist()
            cursor.executemany(sql, list_of_tuples)
        st.success('Proveedor guardado exitosamente')
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

def borrar_proveedor(datastock):
    with st.spinner('Borrando proveedor'):
        datastock = datastock.replace('', None)
        datastock = datastock[['id']]
        conn      = pymysql.connect(host=host,
                       user=user,
                       password=password,
                       db=schema)
        with conn.cursor() as cursor:
            #sql = "DELETE FROM modulo_proveedores WHERE id = %s"
            sql = "UPDATE modulo_proveedores SET available=0 WHERE `id` = %s"
            list_of_tuples = datastock.to_records(index=False).tolist()
            cursor.executemany(sql, list_of_tuples)
        st.success('Proveedor borrado exitosamente')
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
           'tipo_proveedores':False,
           'editar':False,
           'borrar':False,
           'borrarconfirm':False,
           'proveedor_modulo_proveedores':'',
           'lista_proveedores_modulo_proveedores':[],
           'identificacion_modulo_proveedores':'',
           'lista_identificacion_modulo_proveedores':[],
           'contacto_modulo_proveedores':'',
           'lista_contacto_modulo_proveedores':[],
           'telefono_modulo_proveedores':'',
           'lista_telefonos_modulo_proveedores':[],
           'dataorigen_modulo_proveedores':pd.DataFrame(),
           'data_modulo_proveedores':pd.DataFrame()
}

for key,value in formato.items():
    if key not in st.session_state: 
        st.session_state[key] = value
        
col1,col2 = st.columns(2) 
with col1:
    if st.button('Crear'):
        st.session_state.tipo_crear       = True
        st.session_state.tipo_proveedores = False
        
with col2:
    if st.button('Proveedores'):
        st.session_state.tipo_proveedores = True
        st.session_state.tipo_crear       = False
 
if st.session_state.tipo_crear:
    crear_proveedores()
    
if st.session_state.tipo_proveedores:
    proveedores()
                   
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