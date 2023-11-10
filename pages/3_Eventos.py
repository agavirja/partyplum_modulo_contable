import streamlit as st
import time
import pandas as pd
import pymysql
import boto3
import random
import string
import streamlit.components.v1 as components
import mimetypes
from bs4 import BeautifulSoup
from sqlalchemy import create_engine 
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode, AgGridTheme
from urllib.parse import urlsplit

from scripts.gasto_x_evento import crear_gasto_evento,editar_gasto_evento
from scripts.ingresos_x_evento import ingresos

st.set_page_config(layout="wide")

#-----------------------------------------------------------------------------#
# Filtro para editar eventos
#-----------------------------------------------------------------------------#
@st.cache_data
def dataeventos():
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')        
    st.session_state.dataorigen_modulo_eventos      = pd.read_sql_query(f"""SELECT * FROM {schema}.modulo_eventos WHERE available=1""" , engine)
    st.session_state.data_modulo_eventos            = st.session_state.dataorigen_modulo_eventos.copy()
    st.session_state.lista_clientes_modulo_eventos  = ['Todos'] + sorted(list(st.session_state.dataorigen_modulo_eventos[st.session_state.dataorigen_modulo_eventos['nombre_completo'].notnull()]['nombre_completo'].unique()))
    st.session_state.lista_tematica_modulo_eventos  = ['Todos'] + sorted(list(st.session_state.dataorigen_modulo_eventos[st.session_state.dataorigen_modulo_eventos['tema_evento'].notnull()]['tema_evento'].unique()))
    lista                            = list(st.session_state.dataorigen_modulo_eventos[st.session_state.dataorigen_modulo_eventos['telefono1'].notnull()]['telefono1'].unique()) + list(st.session_state.dataorigen_modulo_eventos[st.session_state.dataorigen_modulo_eventos['telefono2'].notnull()]['telefono2'].unique())
    st.session_state.lista_telefonos_modulo_eventos = ['Todos'] + lista
    st.session_state.cliente_modulo_eventos         = 'Todos'
    st.session_state.tematica_modulo_eventos        = 'Todos'
    st.session_state.telefono_modulo_eventos        = 'Todos'
    engine.dispose()
    
@st.cache_data
def getdatagastoseventos(id_evento,click):
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')        
    data   = pd.read_sql_query(f"""SELECT * FROM {schema}.modulo_gastos_evento WHERE id_modulo_eventos={id_evento} AND available=1""" , engine)
    engine.dispose()
    return data
    
def reset_todos_modulo_eventos():
    st.session_state.data_modulo_eventos            = st.session_state.dataorigen_modulo_eventos.copy()
    st.session_state.lista_clientes_modulo_eventos  = ['Todos'] + sorted(list(st.session_state.dataorigen_modulo_eventos[st.session_state.dataorigen_modulo_eventos['nombre_completo'].notnull()]['nombre_completo'].unique()))
    st.session_state.lista_tematica_modulo_eventos  = ['Todos'] + sorted(list(st.session_state.dataorigen_modulo_eventos[st.session_state.dataorigen_modulo_eventos['tema_evento'].notnull()]['tema_evento'].unique()))
    lista                            = list(st.session_state.dataorigen_modulo_eventos[st.session_state.dataorigen_modulo_eventos['telefono1'].notnull()]['telefono1'].unique()) + list(st.session_state.dataorigen_modulo_eventos[st.session_state.dataorigen_modulo_eventos['telefono2'].notnull()]['telefono2'].unique())
    st.session_state.lista_telefonos_modulo_eventos = ['Todos'] + lista
    st.session_state.cliente_modulo_eventos         = 'Todos'
    st.session_state.tematica_modulo_eventos        = 'Todos'
    st.session_state.telefono_modulo_eventos        = 'Todos'    
    
def clientechange_modulo_eventos():
    if st.session_state.cliente_modulo_eventos=='Todos':
        reset_todos_modulo_eventos()
    else:
        idd = st.session_state.data_modulo_eventos['nombre_completo']==st.session_state.cliente_modulo_eventos
        st.session_state.data_modulo_eventos = st.session_state.data_modulo_eventos[idd]
        st.session_state.lista_clientes_modulo_eventos  = ['Todos'] + sorted(list(st.session_state.data_modulo_eventos[st.session_state.data_modulo_eventos['nombre_completo'].notnull()]['nombre_completo'].unique()))
        st.session_state.lista_tematica_modulo_eventos  = ['Todos'] + sorted(list(st.session_state.data_modulo_eventos[st.session_state.data_modulo_eventos['tema_evento'].notnull()]['tema_evento'].unique()))
        lista                            = list(st.session_state.data_modulo_eventos[st.session_state.data_modulo_eventos['telefono1'].notnull()]['telefono1'].unique()) + list(st.session_state.data_modulo_eventos[st.session_state.data_modulo_eventos['telefono2'].notnull()]['telefono2'].unique())
        st.session_state.lista_telefonos_modulo_eventos = ['Todos'] + lista
        st.session_state.cliente_modulo_eventos  = st.session_state.cliente_modulo_eventos
        st.session_state.tematica_modulo_eventos = st.session_state.tematica_modulo_eventos
        st.session_state.telefono_modulo_eventos = st.session_state.telefono_modulo_eventos
        
def tematicachange_modulo_eventos():
    if st.session_state.tematica_modulo_eventos=='Todos':
        reset_todos_modulo_eventos()
    else:
        idd = st.session_state.data_modulo_eventos['tema_evento']==st.session_state.tematica_modulo_eventos
        st.session_state.data_modulo_eventos = st.session_state.data_modulo_eventos[idd]
        st.session_state.lista_clientes_modulo_eventos  = ['Todos'] + sorted(list(st.session_state.data_modulo_eventos[st.session_state.data_modulo_eventos['nombre_completo'].notnull()]['nombre_completo'].unique()))
        st.session_state.lista_tematica_modulo_eventos  = ['Todos'] + sorted(list(st.session_state.data_modulo_eventos[st.session_state.data_modulo_eventos['tema_evento'].notnull()]['tema_evento'].unique()))
        lista                            = list(st.session_state.data_modulo_eventos[st.session_state.data_modulo_eventos['telefono1'].notnull()]['telefono1'].unique()) + list(st.session_state.data_modulo_eventos[st.session_state.data_modulo_eventos['telefono2'].notnull()]['telefono2'].unique())
        st.session_state.lista_telefonos_modulo_eventos = ['Todos'] + lista
        st.session_state.cliente_modulo_eventos  = st.session_state.cliente_modulo_eventos
        st.session_state.tematica_modulo_eventos = st.session_state.tematica_modulo_eventos
        st.session_state.telefono_modulo_eventos = st.session_state.telefono_modulo_eventos
        
def telefonochange_modulo_eventos():
    if st.session_state.telefono_modulo_eventos=='Todos':
        reset_todos_modulo_eventos()
    else:
        idd = (st.session_state.data_modulo_eventos['telefono1']==st.session_state.telefono_modulo_eventos) | (st.session_state.data_modulo_eventos['telefono2']==st.session_state.telefono_modulo_eventos)
        st.session_state.data_modulo_eventos = st.session_state.data_modulo_eventos[idd]
        st.session_state.lista_clientes_modulo_eventos  = ['Todos'] + sorted(list(st.session_state.data_modulo_eventos[st.session_state.data_modulo_eventos['nombre_completo'].notnull()]['nombre_completo'].unique()))
        st.session_state.lista_tematica_modulo_eventos  = ['Todos'] + sorted(list(st.session_state.data_modulo_eventos[st.session_state.data_modulo_eventos['tema_evento'].notnull()]['tema_evento'].unique()))
        lista                            = list(st.session_state.data_modulo_eventos[st.session_state.data_modulo_eventos['telefono1'].notnull()]['telefono1'].unique()) + list(st.session_state.data_modulo_eventos[st.session_state.data_modulo_eventos['telefono2'].notnull()]['telefono2'].unique())
        st.session_state.lista_telefonos_modulo_eventos = ['Todos'] + lista   
        st.session_state.lista_telefonos_modulo_eventos = st.session_state.lista_telefonos_modulo_eventos
        st.session_state.cliente_modulo_eventos  = st.session_state.cliente_modulo_eventos
        st.session_state.tematica_modulo_eventos = st.session_state.tematica_modulo_eventos
        st.session_state.telefono_modulo_eventos = st.session_state.telefono_modulo_eventos
    
#-----------------------------------------------------------------------------#
# Filtro de clientes
#-----------------------------------------------------------------------------#
@st.cache_data
def dataclientes():
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')        
    st.session_state.dataorigen_filtro_clientes_modulo_eventos = pd.read_sql_query(f"""SELECT * FROM {schema}.modulo_clientes WHERE available=1""" , engine)
    st.session_state.data_filtro_clientes_modulo_eventos       = st.session_state.dataorigen_filtro_clientes_modulo_eventos.copy()
    st.session_state.lista_filtros_clientes_modulo_eventos    = ['Todos'] + sorted(list(st.session_state.dataorigen_filtro_clientes_modulo_eventos[st.session_state.dataorigen_filtro_clientes_modulo_eventos['nombre_completo'].notnull()]['nombre_completo'].unique()))
    lista                                       = list(st.session_state.dataorigen_filtro_clientes_modulo_eventos[st.session_state.dataorigen_filtro_clientes_modulo_eventos['telefono1'].notnull()]['telefono1'].unique()) + list(st.session_state.dataorigen_filtro_clientes_modulo_eventos[st.session_state.dataorigen_filtro_clientes_modulo_eventos['telefono2'].notnull()]['telefono2'].unique())
    st.session_state.lista_filtros_telefonos_modulo_eventos    = ['Todos'] + list(set(lista))   
    st.session_state.filtroclientes_modulo_eventos             = 'Todos'
    st.session_state.filtrotelefono_modulo_eventos             = 'Todos'
    engine.dispose()
    
def reset_todos_modulo_eventos_clientes():
    st.session_state.data_filtro_clientes_modulo_eventos    = st.session_state.dataorigen_filtro_clientes_modulo_eventos.copy()
    st.session_state.lista_filtros_clientes_modulo_eventos  = ['Todos'] + sorted(list(st.session_state.dataorigen_filtro_clientes_modulo_eventos[st.session_state.dataorigen_filtro_clientes_modulo_eventos['nombre_completo'].notnull()]['nombre_completo'].unique()))
    lista                                    = list(st.session_state.dataorigen_filtro_clientes_modulo_eventos[st.session_state.dataorigen_filtro_clientes_modulo_eventos['telefono1'].notnull()]['telefono1'].unique()) + list(st.session_state.dataorigen_filtro_clientes_modulo_eventos[st.session_state.dataorigen_filtro_clientes_modulo_eventos['telefono2'].notnull()]['telefono2'].unique())
    st.session_state.lista_filtros_telefonos_modulo_eventos = ['Todos'] + list(set(lista))   
    st.session_state.filtroclientes_modulo_eventos          = 'Todos'
    st.session_state.filtrotelefono_modulo_eventos          = 'Todos'


def filtroclienteschange_modulo_eventos():
    if st.session_state.filtroclientes_modulo_eventos=='Todos':
        reset_todos_modulo_eventos_clientes()
    else:
        idd = st.session_state.data_filtro_clientes_modulo_eventos['nombre_completo']==st.session_state.filtroclientes_modulo_eventos
        st.session_state.data_filtro_clientes_modulo_eventos    = st.session_state.data_filtro_clientes_modulo_eventos[idd]
        st.session_state.lista_filtros_clientes_modulo_eventos  = ['Todos'] + sorted(list(st.session_state.data_filtro_clientes_modulo_eventos[st.session_state.data_filtro_clientes_modulo_eventos['nombre_completo'].notnull()]['nombre_completo'].unique()))
        lista                                    = list(st.session_state.data_filtro_clientes_modulo_eventos[st.session_state.data_filtro_clientes_modulo_eventos['telefono1'].notnull()]['telefono1'].unique()) + list(st.session_state.data_filtro_clientes_modulo_eventos[st.session_state.data_filtro_clientes_modulo_eventos['telefono2'].notnull()]['telefono2'].unique())
        st.session_state.lista_filtros_telefonos_modulo_eventos = ['Todos'] + list(set(lista))   
        st.session_state.filtroclientes_modulo_eventos          = st.session_state.filtroclientes_modulo_eventos
        st.session_state.filtrotelefono_modulo_eventos          = st.session_state.filtrotelefono_modulo_eventos

def filtrotelefonochange_modulo_eventos():
    if st.session_state.filtrotelefono_modulo_eventos=='Todos':
        reset_todos_modulo_eventos_clientes()
    else:
        idd = (st.session_state.data_filtro_clientes_modulo_eventos['telefono1']==st.session_state.filtrotelefono_modulo_eventos) | (st.session_state.data_filtro_clientes_modulo_eventos['telefono2']==st.session_state.filtrotelefono_modulo_eventos)
        st.session_state.data_filtro_clientes_modulo_eventos    = st.session_state.data_filtro_clientes_modulo_eventos[idd]
        st.session_state.lista_filtros_clientes_modulo_eventos  = ['Todos'] + sorted(list(st.session_state.data_filtro_clientes_modulo_eventos[st.session_state.data_filtro_clientes_modulo_eventos['nombre_completo'].notnull()]['nombre_completo'].unique()))
        lista                                    = list(st.session_state.data_filtro_clientes_modulo_eventos[st.session_state.data_filtro_clientes_modulo_eventos['telefono1'].notnull()]['telefono1'].unique()) + list(st.session_state.data_filtro_clientes_modulo_eventos[st.session_state.data_filtro_clientes_modulo_eventos['telefono2'].notnull()]['telefono2'].unique())
        st.session_state.lista_filtros_telefonos_modulo_eventos = ['Todos'] + list(set(lista))   
        st.session_state.filtroclientes_modulo_eventos          = st.session_state.filtroclientes_modulo_eventos
        st.session_state.filtrotelefono_modulo_eventos          = st.session_state.filtrotelefono_modulo_eventos

@st.cache_data
def dataingresos(id_modulo_eventos,click):
    engine  = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')        
    st.session_state.dataingresos = pd.read_sql_query(f"""SELECT * FROM {schema}.modulo_facturacion_clientes WHERE id_modulo_eventos={id_modulo_eventos}""" , engine)
    engine.dispose()

def es_url(texto):
   try:
       resultado = urlsplit(texto)
       return all([resultado.scheme, resultado.netloc])
   except ValueError:
       return False
        
def get_content_type_and_extension(file_name):
    content_type, encoding = mimetypes.guess_type(file_name)
    if content_type:
        extension = mimetypes.guess_extension(content_type)
        return content_type, extension
    else:
        return None, None

def generate_random_code(file_name):
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    current_date = datetime.now().strftime('%y%m%d')
    name_without_extension = file_name.split('.')[0]
    code = f"{current_date}{random_part}{name_without_extension}"
    code = code[:10]
    return code

@st.cache_data
def img2s3(uploadfile):

    #session = boto3.Session(
    #    aws_access_key_id=st.secrets["aws_access_key_id"],
    #    aws_secret_access_key=st.secrets["aws_secret_access_key"],
    #    region_name=st.secrets["region_name"]
    #)
    session = boto3.Session(
        aws_access_key_id='AKIA3Y3AFA4CUR2JNR4K',
        aws_secret_access_key='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',
        region_name='us-east-2'
    )
    contentType,dotfile = get_content_type_and_extension(uploadfile.name)
    randomnumber        = generate_random_code(uploadfile.name)
    
    #s3 = boto3.client("s3")
    s3 = session.client('s3')
    images3name  = f'doc_{randomnumber}{dotfile}' 
    s3file       = f'matina_eventos/{images3name}'
    s3.upload_fileobj(
        uploadfile,
        'personal-data-bucket-online',
        s3file,
        ExtraArgs={
            "ContentType": contentType
        }
    )
    principal_img = f'https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/{s3file}'

    return principal_img

#-----------------------------------------------------------------------------#
# Crear
def crear_evento():
    
    dataclientes()
    
    st.write('---')
    st.write('Cliente')
    col1,col2 = st.columns(2)
    with col1: 
        st.selectbox('Por cliente', options=st.session_state.lista_filtros_clientes_modulo_eventos,key='filtroclientes_modulo_eventos',on_change=filtroclienteschange_modulo_eventos)
    with col2: 
        st.selectbox('Por telefono', options=st.session_state.lista_filtros_telefonos_modulo_eventos,key='filtrotelefono',on_change=filtrotelefonochange_modulo_eventos)

    datacliente       = st.session_state.data_filtro_clientes_modulo_eventos.copy()
    datacliente       = datacliente.iloc[[0]]
    datacliente.index = range(len(datacliente))
    
    col1,col2,col3,col4 = st.columns([3,1,2,2])
    with col1:
        st.text_input('Nombre del cliente',value=datacliente['nombre_completo'].iloc[0],disabled=True)
    with col2:
        st.text_input('Tipo',value=datacliente['tipo_identificacion'].iloc[0],disabled=True)
    with col3:
        st.text_input('Identificacion',value=datacliente['identificacion'].iloc[0],disabled=True)
    with col4:
        st.text_input('Telefono',value=datacliente['telefono1'].iloc[0],disabled=True)
                             
    variables  = [x for x in ['id', 'nombre_completo', 'tipo_identificacion', 'identificacion', 'telefono1', 'telefono2', 'email'] if x in datacliente]
    datacliente = datacliente[variables]
    datacliente.rename(columns={'id':'id_cliente'},inplace=True)
    
    st.write('---')
    st.write('Datos del evento')
    col1,col2,col3 = st.columns(3)
    with col1:
        fecha_evento = st.date_input('fecha del evento',value="today")
    with col2:
        tema_evento = st.text_input('Tema del evento',value='')
    with col3:
        nombre_homenajeado1 = st.text_input('Nombre del homenajeado (1)',value='')
    with col1:
        nombre_homenajeado2 = st.text_input('Nombre del homenajeado (2)',value='')
    with col2:
        ciudad_evento = st.selectbox('Ciudad del evento',options=['Bogota'])
    with col3:    
        direccion_evento = st.text_input('Dirección del evento',value='')
    with col1:
        hora_evento = st.text_input('Hora del evento',value='')
    with col2:
        codigo_paquete = st.selectbox('Código del paquete siigo',options=['P01-Decoracion mini table','P02-Decoracion mediano','P03-Decoracion Ecologico','P04-Decoracion deluxe'])
    with col3:
        nombre_paquete = st.selectbox('Nombre del paquete',options=['Decoracion mini table','Decoracion mediano','Decoracion Ecologico','Decoracion deluxe'])
    with col1:
        valor_paquete  = st.number_input('Valor total',min_value=0,value=1000000)

    datamatch = pd.DataFrame([{'fecha_registro':datetime.now().strftime('%Y-%m-%d'), 'fecha_evento':fecha_evento,'tema_evento':tema_evento,'nombre_homenajeado1':nombre_homenajeado1,'nombre_homenajeado2': nombre_homenajeado2,'ciudad_evento': ciudad_evento,'direccion_evento': direccion_evento,'hora_evento':  hora_evento,'codigo_paquete': codigo_paquete,'nombre_paquete': nombre_paquete,'valor_paquete':valor_paquete,'available':1}])
    datamatch.index = range(len(datamatch))
    dataexport = datacliente.merge(datamatch,left_index=True, right_index=True)
    
    if st.button('Crear evento'):
        with st.spinner('Creando evento'):
            engine     = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')        
            dataexport = dataexport.replace('', None)
            dataexport.to_sql('modulo_eventos', engine, if_exists='append', index=False, chunksize=1)
            st.success('Evento creado exitosamente')

            resultId = engine.execute('SELECT LAST_INSERT_ID() as last_id;')
            resultId = resultId.fetchone()['last_id']
            data_facturacion_clientes_evento = pd.DataFrame([{'id_modulo_eventos':resultId,'valor_paquete':valor_paquete}]) 
            data_facturacion_clientes_evento.to_sql('modulo_facturacion_clientes', engine, if_exists='append', index=False, chunksize=1)

            engine.dispose()
            time.sleep(5)
            st.cache_data.clear()
            st.session_state.tipo_eventos = True
            st.session_state.tipo_crear   = False
            st.rerun()
            
#-----------------------------------------------------------------------------#
# Eventos
def eventos():

    dataeventos()
    st.write('---')
    st.write('Filtros')
    
    col1,col2,col3 = st.columns(3)
    with col1: 
        st.selectbox('Por cliente', options=st.session_state.lista_clientes_modulo_eventos,key='cliente_modulo_eventos',on_change=clientechange_modulo_eventos)
    with col2: 
        st.selectbox('Por tematica', options=st.session_state.lista_tematica_modulo_eventos,key='tematica_modulo_eventos',on_change=tematicachange_modulo_eventos)
    with col3: 
        st.selectbox('Por telefono', options=st.session_state.lista_telefonos_modulo_eventos,key='telefono_modulo_eventos',on_change=telefonochange_modulo_eventos)
     
    datastockagrid = st.session_state.data_modulo_eventos.copy()
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
        datastockedit['fecha_evento'] = pd.to_datetime(datastockedit['fecha_evento'],errors='coerce')

        st.write('---')
        st.write('Información del Evento')        
     
        col1,col2,col3 = st.columns(3)
        with col1:
            try:    fecha_evento = st.date_input('fecha del evento',value=datastockedit['fecha_evento'].iloc[0])
            except: fecha_evento = st.date_input('fecha del evento',value=None)
            datastockedit.loc[0,'fecha_evento'] = fecha_evento
        with col2:
            tema_evento = st.text_input('Tema del evento',value=datastockedit['tema_evento'].iloc[0])
            datastockedit.loc[0,'tema_evento'] = tema_evento
        with col3:
            nombre_homenajeado1 = st.text_input('Nombre del homenajeado (1)',value=datastockedit['nombre_homenajeado1'].iloc[0])
            datastockedit.loc[0,'nombre_homenajeado1'] = nombre_homenajeado1
        with col1:
            nombre_homenajeado2 = st.text_input('Nombre del homenajeado (2)',value=datastockedit['nombre_homenajeado2'].iloc[0])
            datastockedit.loc[0,'nombre_homenajeado2'] = nombre_homenajeado2
        with col2:
            lista  = ['Bogota']
            try:    
                if datastockedit['ciudad_evento'].iloc[0] in lista: 
                    indice = lista.index(datastockedit['ciudad_evento'].iloc[0])
                else:
                    indice = 0
            except: indice = 0
            ciudad_evento = st.selectbox('Ciudad del evento', options=lista,index=indice)
            datastockedit.loc[0,'ciudad_evento'] = ciudad_evento
        with col3:    
            direccion_evento = st.text_input('Dirección del evento',value=datastockedit['direccion_evento'].iloc[0])
            datastockedit.loc[0,'direccion_evento'] = direccion_evento
        with col1:
            hora_evento = st.text_input('Hora del evento',value=datastockedit['hora_evento'].iloc[0])
            datastockedit.loc[0,'hora_evento'] = hora_evento
        with col2:
            lista  = ['P01-Decoracion mini table','P02-Decoracion mediano','P03-Decoracion Ecologico','P04-Decoracion deluxe']
            try:    
                if datastockedit['codigo_paquete'].iloc[0] in lista: 
                    indice = lista.index(datastockedit['codigo_paquete'].iloc[0])
                else:
                    indice = 0
            except: indice = 0
            codigo_paquete = st.selectbox('Código del paquete siigo', options=lista,index=indice)
            datastockedit.loc[0,'codigo_paquete'] = codigo_paquete
        with col3:
            lista  = ['Decoracion mini table','Decoracion mediano','Decoracion Ecologico','Decoracion deluxe']
            try:    
                if datastockedit['nombre_paquete'].iloc[0] in lista: 
                    indice = lista.index(datastockedit['nombre_paquete'].iloc[0])
                else:
                    indice = 0
            except: indice = 0
            nombre_paquete = st.selectbox('Nombre del paquete', options=lista,index=indice)
            datastockedit.loc[0,'nombre_paquete'] = nombre_paquete
        with col1:
            try:    valor = int(float(datastockedit['valor_paquete'].iloc[0]))
            except: valor = 2000000
            valor_paquete  = st.number_input('Valor total',min_value=0,value=valor)
            datastockedit.loc[0,'valor_paquete'] = valor_paquete 

        col1, col2 = st.columns(2)
        with col1:
            if st.button('Guardar'):
                st.session_state.editar        = True
                st.session_state.borrar        = False
                st.session_state.borrarconfirm = False
                
        with col2:
            if st.button('Borrar evento'):
                st.session_state.editar        = False
                st.session_state.borrar        = True
                st.session_state.borrarconfirm = False
    
        if st.session_state.editar:
            editar_evento(datastockedit)                
                
        if st.session_state.borrar:
            with col2:
                if st.button('Seguro quiere borrar el evento?'):
                    st.session_state.borrarconfirm = True

        if st.session_state.borrarconfirm and st.session_state.borrar:
            borrar_evento(datastockedit)

        # Anadir gasto
        anadir_gasto(int(response['selected_rows'][0]['id']))
        
        # Ingresos del evento
        ingresos(int(response['selected_rows'][0]['id']))
        
        # Resumen de cuentas
        resumen_cuentas(int(response['selected_rows'][0]['id']),datastockedit)
        
        # Facturacion
        cifras_facturacion(int(response['selected_rows'][0]['id']))
        
def editar_evento(datastock):     
    with st.spinner('Guardando evento'):
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
            sql = f"UPDATE modulo_eventos SET {condicion} WHERE `id` = %s"
            list_of_tuples = datastock.to_records(index=False).tolist()
            cursor.executemany(sql, list_of_tuples)
        st.success('Evento guardado exitosamente')
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

def borrar_evento(datastock):
    with st.spinner('Borrando evento'):
        datastock = datastock.replace('', None)
        datastock = datastock[['id']]
        conn      = pymysql.connect(host=host,
                       user=user,
                       password=password,
                       db=schema)
        with conn.cursor() as cursor:
            #sql = "DELETE FROM modulo_proveedores WHERE id = %s"
            sql = "UPDATE modulo_eventos SET available=0 WHERE `id` = %s"
            list_of_tuples = datastock.to_records(index=False).tolist()
            cursor.executemany(sql, list_of_tuples)
        st.success('Evento borrado exitosamente')
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
        
def anadir_gasto(id_evento):
    st.write('---')
    st.write('Información de proveedores por evento')

    datagastos = getdatagastoseventos(id_evento,st.session_state.click)
    variables  = [x for x in ['id','nombre_razon_social', 'nombre_comercial', 'tipo_identificacion', 'identificacion', 'valor', 'iva', 'categoria'] if x in datagastos]
    #st.dataframe(datagastos)
    
    gb = GridOptionsBuilder.from_dataframe(datagastos[variables])
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
    
    response_tabla_gasto = AgGrid(
        datagastos[variables],
        gridOptions=gridOptions,
        custom_css=custom_css,
        columns_auto_size_mode="FIT_CONTENTS",
        use_checkbox=True,
        theme=AgGridTheme.STREAMLIT,
        domLayout='autoHeight',
    ) 
    
    if response_tabla_gasto['selected_rows']:
        st.write('---')
        st.write('Editar información del gasto')
        st.session_state.anadirgasto = False
        editar_gasto_evento(datagastos,response_tabla_gasto['selected_rows'][0]['id'])
        
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button('Agregar gasto de proveedores de este evento'): 
                st.session_state.anadirgasto = True
        
    if st.session_state.anadirgasto:
        crear_gasto_evento(id_evento)
        
def resumen_cuentas(id_evento,datastock):
    
    #---------------------------------------------------------------------#
    # Cuentas general
    st.write('---')
    
    # dataingresosxevento = dataingresos(id_evento,st.session_state.click)
    dataingresos(id_evento,st.session_state.click)
    dataingresosxevento = st.session_state.dataingresos.copy()
    
    IVA             = 0.19
    datagastos      = getdatagastoseventos(id_evento,st.session_state.click)
    recaudoterceros = datagastos['valor'].sum()+datagastos['iva'].sum()
    valorpaquete    = datastock['valor_paquete'].iloc[0]
    ganancia        = (valorpaquete-recaudoterceros)/(1+IVA)
    IVA_paquete     = ganancia*IVA
    
    valor_ingreso = 0
    for i in ['valor_pago1','valor_pago2','valor_pago3','valor_pago4']:
        try:
            valor_ingreso += dataingresosxevento[i].iloc[0]
        except: pass
    saldo_pendiente = valorpaquete-valor_ingreso
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <link href="https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/css/nucleo-icons.css" rel="stylesheet">
      <link href="https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/css/nucleo-svg.css" rel="stylesheet">
      <link id="pagestyle" href="https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/css/soft-ui-dashboard.css?v=1.0.7" rel="stylesheet">
    </head>
    <body>
    <div class="container-fluid py-4">
      <div class="row">
        <div class="col-xl-12 col-sm-12 mb-xl-0 mb-2">
          <div class="card h-100">
            <div class="card-body p-3">
              <div class="container-fluid py-4">
                <div class="row" style="margin-bottom: -30px;">
                  <div class="card-body p-3">
                    <div class="row">
                      <div class="numbers">
                        <h3 class="font-weight-bolder mb-0" style="text-align: center; font-size: 1.5rem;border-bottom: 0.5px solid #ccc; padding-bottom: 8px;">Resumen de cuentas</h3>
                      </div>
                    </div>
                  </div>
                </div>
              </div> 
              
            <div class="container-fluid py-4">
              <div class="row">
                <div class="col-xl-2 col-sm-3 mb-xl-0 mb-2">
                  <div class="card">
                    <div class="card-body p-3">
                      <div class="row">
                        <div class="numbers">
                          <h3 class="font-weight-bolder mb-0" style="text-align: center;font-size: 1.5rem;">${valorpaquete:,.0f}</h3>
                          <p class="mb-0 text-capitalize" style="font-weight: 300;font-size: 1rem;text-align: center;">Valor del paquete</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="col-xl-2 col-sm-3 mb-xl-0 mb-2">
                  <div class="card">
                    <div class="card-body p-3">
                      <div class="row">
                        <div class="numbers">
                          <h3 class="font-weight-bolder mb-0" style="text-align: center;font-size: 1.5rem;">${recaudoterceros:,.0f}</h3>
                          <p class="mb-0 text-capitalize" style="font-weight: 300;font-size: 1rem;text-align: center;">Recaudo a Terceros</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="col-xl-2 col-sm-3 mb-xl-0 mb-2">
                  <div class="card">
                    <div class="card-body p-3">
                      <div class="row">
                        <div class="numbers">
                          <h3 class="font-weight-bolder mb-0" style="text-align: center;font-size: 1.5rem;">${ganancia:,.2f}</h3>
                          <p class="mb-0 text-capitalize" style="font-weight: 300;font-size: 1rem;text-align: center;">Ganancia neta</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="col-xl-2 col-sm-3 mb-xl-0 mb-2">
                  <div class="card">
                    <div class="card-body p-3">
                      <div class="row">
                        <div class="numbers">
                          <h3 class="font-weight-bolder mb-0" style="text-align: center;font-size: 1.5rem;">${IVA_paquete:,.2f}</h3>
                          <p class="mb-0 text-capitalize" style="font-weight: 300;font-size: 1rem;text-align: center;">IVA del paquete</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div> 
               
                <div class="col-xl-2 col-sm-3 mb-xl-0 mb-2">
                  <div class="card">
                    <div class="card-body p-3">
                      <div class="row">
                        <div class="numbers">
                          <h3 class="font-weight-bolder mb-0" style="text-align: center;font-size: 1.5rem;">${valor_ingreso:,.0f}</h3>
                          <p class="mb-0 text-capitalize" style="font-weight: 300;font-size: 1rem;text-align: center;">Pagos del cliente</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div> 

                <div class="col-xl-2 col-sm-3 mb-xl-0 mb-2">
                  <div class="card">
                    <div class="card-body p-3">
                      <div class="row">
                        <div class="numbers">
                          <h3 class="font-weight-bolder mb-0" style="text-align: center;font-size: 1.5rem;">${saldo_pendiente:,.0f}</h3>
                          <p class="mb-0 text-capitalize" style="font-weight: 300;font-size: 1rem;text-align: center;">Saldo pendiente por pagar</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div> 
                
              </div>
            </div>
      </div>
    </div>         
    </body>
    </html>
    """     
    texto = BeautifulSoup(html, 'html.parser')
    st.markdown(texto, unsafe_allow_html=True)
        
    


def cifras_facturacion(id_evento):
    
    st.write('---')
    st.write('Información de facturacion')
    
    dataingresos(id_evento,st.session_state.click)
    datacifrasfacturacion = st.session_state.dataingresos.copy()
    variables = [x for x in ['id','id_modulo_eventos','fecha_factura','valor_factura','factura','valor_paquete','valor_recaudo_terceros','iva','ganancia'] if x in datacifrasfacturacion]
    datacifrasfacturacion = datacifrasfacturacion[variables]

    try: datacifrasfacturacion['fecha_factura'] = pd.to_datetime(datacifrasfacturacion['fecha_factura'],errors='coerce')
    except: pass

    col1,col2,col3 = st.columns(3)    
    with col1:
        try:    fecha_factura = st.date_input('Fecha de emision de la factura',value=datacifrasfacturacion['fecha_factura'].iloc[0])
        except: fecha_factura = st.date_input('Fecha de emision de la factura',value=None)
        datacifrasfacturacion.loc[0,'fecha_factura'] = fecha_factura
    with col2:
        try:    valor_factura = st.number_input('Valor de la factura al cliente',min_value=0,value=int(float(datacifrasfacturacion['valor_factura'].iloc[0])))
        except: valor_factura = st.number_input('Valor de la factura al cliente',min_value=0,value=0)
        datacifrasfacturacion.loc[0,'valor_factura'] = valor_factura
    with col3:
        try:    iva = st.number_input('IVA',min_value=0,value=int(float(datacifrasfacturacion['iva'].iloc[0])))
        except: iva = st.number_input('IVA',min_value=0,value=0)
        datacifrasfacturacion.loc[0,'iva'] = iva 

    with col1:
        try:    valor_paquete = st.number_input('Valor del paquete',min_value=0,value=int(float(datacifrasfacturacion['valor_paquete'].iloc[0])))
        except: valor_paquete = st.number_input('Valor del paquete',min_value=0,value=0)
        datacifrasfacturacion.loc[0,'valor_paquete'] = valor_paquete
    with col2:
        try: valor_recaudo_terceros = st.number_input('Recaudo de terceros',min_value=0,value=int(float(datacifrasfacturacion['valor_recaudo_terceros'].iloc[0])))
        except: valor_recaudo_terceros = st.number_input('Recaudo de terceros',min_value=0,value=0)
        datacifrasfacturacion.loc[0,'valor_recaudo_terceros'] = valor_recaudo_terceros 
    with col3:
        try:    ganancia = st.number_input('Ganancia',min_value=0,value=int(float(datacifrasfacturacion['ganancia'].iloc[0])))
        except: ganancia = st.number_input('Ganancia',min_value=0,value=0)
        datacifrasfacturacion.loc[0,'ganancia'] = ganancia 

    with col1:
        factura = st.file_uploader('Factura')
        if factura is not None:
            factura = img2s3(factura)
            datacifrasfacturacion.loc[0,'factura'] = factura
        else:
            try:
                if es_url(datacifrasfacturacion['factura'].iloc[0]):
                    st.write(datacifrasfacturacion['factura'].iloc[0])
            except: pass
      
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Guardar facturacion'):
            with st.spinner('Guardando facturacion'):
                
                datacifrasfacturacion = datacifrasfacturacion.replace('', None)
                vardrop   = [x for x in ['fecha_registro'] if x in list(datacifrasfacturacion)]
                if vardrop!=[]: datacifrasfacturacion.drop(columns=vardrop,inplace=True)
                variables = list(datacifrasfacturacion)
                variables.remove('id')
                condicion = '`'+'`=%s,`'.join(variables)+'`=%s'
                variables.append('id')
                datacifrasfacturacion = datacifrasfacturacion[variables]
                conn = pymysql.connect(host=host,
                               user=user,
                               password=password,
                               db=schema)
                with conn.cursor() as cursor:
                    sql = f"UPDATE modulo_facturacion_clientes SET {condicion} WHERE `id` = %s"
                    list_of_tuples = datacifrasfacturacion.to_records(index=False).tolist()
                    cursor.executemany(sql, list_of_tuples)
                st.success('Facturacion guardado exitosamente')
                conn.commit()
                conn.close()
                time.sleep(5)
                st.cache_data.clear()
                st.session_state.click += 1
                st.rerun()
        
#-----------------------------------------------------------------------------#
        
user     = st.secrets["user_bigdata"]
password = st.secrets["password_bigdata"]
host     = st.secrets["host_bigdata"]
schema   = 'partyplum'

formato = {'tipo_crear':False,
           'tipo_eventos':False,
           'editar':False,
           'borrar':False,
           'borrarconfirm':False,
           'anadirgasto':False, 
           'click':0,
           'cliente_modulo_eventos':'',
           'lista_clientes_modulo_eventos':[],
           'tematica_modulo_eventos':'',
           'lista_tematica_modulo_eventos':[],
           'telefono_modulo_eventos':'',
           'lista_telefonos_modulo_eventos':[],
           'dataorigen_modulo_eventos':pd.DataFrame(),
           'data_modulo_eventos':pd.DataFrame(),
           'filtroclientes_modulo_eventos':'',
           'lista_filtros_clientes_modulo_eventos':[],
           'filtrotelefono_modulo_eventos':'',
           'lista_filtros_telefonos_modulo_eventos':[],
           'dataingresos':pd.DataFrame(),
}

for key,value in formato.items():
    if key not in st.session_state: 
        st.session_state[key] = value
        
col1,col2 = st.columns(2) 
with col1:
    if st.button('Crear'):
        st.session_state.tipo_crear   = True
        st.session_state.tipo_eventos = False
        
with col2:
    if st.button('Eventos'):
        st.session_state.tipo_eventos = True
        st.session_state.tipo_crear   = False
 
if st.session_state.tipo_crear:
    crear_evento()
    
if st.session_state.tipo_eventos:
    eventos()

 
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
elements[4].style.width = '100%';
elements[5].style.backgroundColor = '#cc7076';
elements[5].style.fontWeight = 'bold';
elements[5].style.color = 'white';
elements[5].style.width = '100%';
elements[6].style.backgroundColor = '#cc7076';
elements[6].style.fontWeight = 'bold';
elements[6].style.color = 'white';
elements[6].style.width = '100%';
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
