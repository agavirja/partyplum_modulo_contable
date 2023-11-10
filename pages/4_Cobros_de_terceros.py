import streamlit as st
import time
import pandas as pd
import pymysql
import boto3
import random
import string
import requests
import streamlit.components.v1 as components
import mimetypes
from sqlalchemy import create_engine 
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode, AgGridTheme
from urllib.parse import urlsplit

user     = st.secrets["user_bigdata"]
password = st.secrets["password_bigdata"]
host     = st.secrets["host_bigdata"]
schema   = 'partyplum'

#-----------------------------------------------------------------------------#
# Crear cobro de terceros
@st.cache_data
def dataproveedores():
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')        
    st.session_state.dataorigen_modulo_cobro_terceros = pd.read_sql_query(f"""SELECT * FROM {schema}.modulo_proveedores WHERE available=1""" , engine)
    st.session_state.data_modulo_cobro_terceros       = st.session_state.dataorigen_modulo_cobro_terceros.copy()
    st.session_state.lista_proveedores_modulo_cobro_terceros  = ['Todos'] + sorted(list(st.session_state.dataorigen_modulo_cobro_terceros[st.session_state.dataorigen_modulo_cobro_terceros['nombre_razon_social'].notnull()]['nombre_razon_social'].unique()))
    st.session_state.lista_contactos_modulo_cobro_terceros    = ['Todos'] + sorted(list(st.session_state.dataorigen_modulo_cobro_terceros[st.session_state.dataorigen_modulo_cobro_terceros['nombre_contacto'].notnull()]['nombre_contacto'].unique()))
    st.session_state.proveedores_modulo_cobro_terceros        = 'Todos'
    st.session_state.contactos_modulo_cobro_terceros          = 'Todos'
    engine.dispose()
    
def reset_todos_modulo_cobro_terceros():
    st.session_state.data_modulo_cobro_terceros = st.session_state.dataorigen_modulo_cobro_terceros.copy()
    st.session_state.lista_proveedores_modulo_cobro_terceros = ['Todos'] + sorted(list(st.session_state.dataorigen_modulo_cobro_terceros[st.session_state.dataorigen_modulo_cobro_terceros['nombre_razon_social'].notnull()]['nombre_razon_social'].unique()))
    st.session_state.lista_contactos_modulo_cobro_terceros   = ['Todos'] + sorted(list(st.session_state.dataorigen_modulo_cobro_terceros[st.session_state.dataorigen_modulo_cobro_terceros['nombre_contacto'].notnull()]['nombre_contacto'].unique()))
    st.session_state.proveedores_modulo_cobro_terceros       = 'Todos'
    st.session_state.contactos_modulo_cobro_terceros         = 'Todos'

def proveedorchange_modulo_cobro_terceros():
    if st.session_state.proveedores_modulo_cobro_terceros=='Todos':
        reset_todos_modulo_cobro_terceros()
    else:
        idd = st.session_state.data_modulo_cobro_terceros['nombre_razon_social']==st.session_state.proveedores_modulo_cobro_terceros
        st.session_state.data_modulo_cobro_terceros = st.session_state.data_modulo_cobro_terceros[idd]
        st.session_state.lista_proveedores_modulo_cobro_terceros  = ['Todos'] + sorted(list(st.session_state.data_modulo_cobro_terceros[st.session_state.data_modulo_cobro_terceros['nombre_razon_social'].notnull()]['nombre_razon_social'].unique()))
        st.session_state.lista_contactos_modulo_cobro_terceros    = ['Todos'] + sorted(list(st.session_state.data_modulo_cobro_terceros[st.session_state.data_modulo_cobro_terceros['nombre_contacto'].notnull()]['nombre_contacto'].unique()))
        st.session_state.proveedores_modulo_cobro_terceros  = st.session_state.proveedores_modulo_cobro_terceros
        st.session_state.contactos_modulo_cobro_terceros    = st.session_state.contactos_modulo_cobro_terceros

def contactochange_modulo_cobro_terceros():
    if st.session_state.contactos_modulo_cobro_terceros=='Todos':
        reset_todos_modulo_cobro_terceros()
    else:
        idd = st.session_state.data_modulo_cobro_terceros['nombre_contacto']==st.session_state.contactos_modulo_cobro_terceros
        st.session_state.data_modulo_cobro_terceros = st.session_state.data_modulo_cobro_terceros[idd]
        st.session_state.lista_proveedores_modulo_cobro_terceros  = ['Todos'] + sorted(list(st.session_state.data_modulo_cobro_terceros[st.session_state.data_modulo_cobro_terceros['nombre_razon_social'].notnull()]['nombre_razon_social'].unique()))
        st.session_state.lista_contactos_modulo_cobro_terceros    = ['Todos'] + sorted(list(st.session_state.data_modulo_cobro_terceros[st.session_state.data_modulo_cobro_terceros['nombre_contacto'].notnull()]['nombre_contacto'].unique()))
        st.session_state.proveedores_modulo_cobro_terceros  = st.session_state.proveedores_modulo_cobro_terceros
        st.session_state.contactos_modulo_cobro_terceros    = st.session_state.contactos_modulo_cobro_terceros
        
        
#-----------------------------------------------------------------------------#
# Editar cobro de terceros
@st.cache_data
def datagastosterceros(click):
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')        
    st.session_state.dataorigen_terceros_edit           = pd.read_sql_query(f"""SELECT * FROM {schema}.modulo_gastos_terceros WHERE available=1""" , engine)
    st.session_state.data_terceros_edit                 = st.session_state.dataorigen_terceros_edit.copy()
    st.session_state.lista_proveedores_terceros_edit    = ['Todos'] + sorted(list(st.session_state.dataorigen_terceros_edit[st.session_state.dataorigen_terceros_edit['nombre_razon_social'].notnull()]['nombre_razon_social'].unique()))
    st.session_state.lista_identificacion_terceros_edit = ['Todos'] + sorted(list(st.session_state.dataorigen_terceros_edit[st.session_state.dataorigen_terceros_edit['identificacion'].notnull()]['identificacion'].unique()))
    st.session_state.lista_pagado_terceros_edit         = ['Todos'] + sorted(list(st.session_state.dataorigen_terceros_edit[st.session_state.dataorigen_terceros_edit['pagada'].notnull()]['pagada'].unique()))
    st.session_state.proveedores_terceros_edit          = 'Todos'
    st.session_state.identificacion_terceros_edit       = 'Todos'
    st.session_state.pagado_terceros_edit               = 'Todos'
    engine.dispose()

def reset_todos_terceros_edit():
    st.session_state.data_terceros_edit                 = st.session_state.dataorigen_terceros_edit.copy()
    st.session_state.lista_proveedores_terceros_edit    = ['Todos'] + sorted(list(st.session_state.dataorigen_terceros_edit[st.session_state.dataorigen_terceros_edit['nombre_razon_social'].notnull()]['nombre_razon_social'].unique()))
    st.session_state.lista_identificacion_terceros_edit = ['Todos'] + sorted(list(st.session_state.dataorigen_terceros_edit[st.session_state.dataorigen_terceros_edit['identificacion'].notnull()]['identificacion'].unique()))
    st.session_state.lista_pagado_terceros_edit         = ['Todos'] + sorted(list(st.session_state.dataorigen_terceros_edit[st.session_state.dataorigen_terceros_edit['pagada'].notnull()]['pagada'].unique()))
    st.session_state.proveedores_terceros_edit          = 'Todos'
    st.session_state.identificacion_terceros_edit       = 'Todos'
    st.session_state.pagado_terceros_edit               = 'Todos'

def proveedorchange_edit():
    if st.session_state.proveedores_terceros_edit == 'Todos':
        reset_todos_terceros_edit()
    else:
        idd = st.session_state.data_terceros_edit['nombre_razon_social'] == st.session_state.proveedores_terceros_edit
        st.session_state.data_terceros_edit                 = st.session_state.data_terceros_edit[idd]
        st.session_state.lista_proveedores_terceros_edit    = ['Todos'] + sorted(list(st.session_state.data_terceros_edit[st.session_state.data_terceros_edit['nombre_razon_social'].notnull()]['nombre_razon_social'].unique()))
        st.session_state.lista_identificacion_terceros_edit = ['Todos'] + sorted(list(st.session_state.data_terceros_edit[st.session_state.data_terceros_edit['identificacion'].notnull()]['identificacion'].unique()))
        st.session_state.lista_pagado_terceros_edit         = ['Todos'] + sorted(list(st.session_state.data_terceros_edit[st.session_state.data_terceros_edit['pagada'].notnull()]['pagada'].unique()))
        st.session_state.proveedores_terceros_edit          = st.session_state.proveedores_terceros_edit
        st.session_state.identificacion_terceros_edit       = st.session_state.identificacion_terceros_edit
        st.session_state.pagado_terceros_edit               = st.session_state.pagado_terceros_edit
        
def identificacionchange_edit():
    if st.session_state.identificacion_terceros_edit == 'Todos':
        reset_todos_terceros_edit()
    else:
        idd = st.session_state.data_terceros_edit['identificacion'] == st.session_state.identificacion_terceros_edit
        st.session_state.data_terceros_edit                 = st.session_state.data_terceros_edit[idd]
        st.session_state.lista_proveedores_terceros_edit    = ['Todos'] + sorted(list(st.session_state.data_terceros_edit[st.session_state.data_terceros_edit['nombre_razon_social'].notnull()]['nombre_razon_social'].unique()))
        st.session_state.lista_identificacion_terceros_edit = ['Todos'] + sorted(list(st.session_state.data_terceros_edit[st.session_state.data_terceros_edit['identificacion'].notnull()]['identificacion'].unique()))
        st.session_state.lista_pagado_terceros_edit         = ['Todos'] + sorted(list(st.session_state.data_terceros_edit[st.session_state.data_terceros_edit['pagada'].notnull()]['pagada'].unique()))
        st.session_state.proveedores_terceros_edit          = st.session_state.proveedores_terceros_edit
        st.session_state.identificacion_terceros_edit       = st.session_state.identificacion_terceros_edit
        st.session_state.pagado_terceros_edit               = st.session_state.pagado_terceros_edit

def pagadochange_edit():
    if st.session_state.pagado_terceros_edit == 'Todos':
        reset_todos_terceros_edit()
    else:
        idd = st.session_state.data_terceros_edit['pagada'] == st.session_state.pagado_terceros_edit
        st.session_state.data_terceros_edit                 = st.session_state.data_terceros_edit[idd]
        st.session_state.lista_proveedores_terceros_edit    = ['Todos'] + sorted(list(st.session_state.data_terceros_edit[st.session_state.data_terceros_edit['nombre_razon_social'].notnull()]['nombre_razon_social'].unique()))
        st.session_state.lista_identificacion_terceros_edit = ['Todos'] + sorted(list(st.session_state.data_terceros_edit[st.session_state.data_terceros_edit['identificacion'].notnull()]['identificacion'].unique()))
        st.session_state.lista_pagado_terceros_edit         = ['Todos'] + sorted(list(st.session_state.data_terceros_edit[st.session_state.data_terceros_edit['pagada'].notnull()]['pagada'].unique()))
        st.session_state.proveedores_terceros_edit          = st.session_state.proveedores_terceros_edit
        st.session_state.identificacion_terceros_edit       = st.session_state.identificacion_terceros_edit
        st.session_state.pagado_terceros_edit               = st.session_state.pagado_terceros_edit

#-----------------------------------------------------------------------------#
def descargar_archivo(url, nombre_archivo):
    response = requests.get(url)
    with open(nombre_archivo, 'wb') as f:
        f.write(response.content)
        
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
def crear_cobro():
    dataproveedores()
    st.write('---')
    col1,col2 = st.columns(2)
    with col1: 
        st.selectbox('Por Nombre o razon social del proveedor', options=st.session_state.lista_proveedores_modulo_cobro_terceros,key='proveedores_modulo_cobro_terceros',on_change=proveedorchange_modulo_cobro_terceros)
    with col2: 
        st.selectbox('Por Contacto', options=st.session_state.lista_contactos_modulo_cobro_terceros,key='contactos_modulo_cobro_terceros',on_change=contactochange_modulo_cobro_terceros)

    dataproveedorfiltro       = st.session_state.data_modulo_cobro_terceros.copy()
    dataproveedorfiltro       = dataproveedorfiltro.iloc[[0]]
    dataproveedorfiltro.index = range(len(dataproveedorfiltro))
    
    if any([x for x in [st.session_state.proveedores_modulo_cobro_terceros,st.session_state.contactos_modulo_cobro_terceros] if x!='Todos']):

        st.write('---')
        st.write('Información del proveedor')
        
        col1,col2,col3,col4 = st.columns([3,3,1,2])
        with col1:
            st.text_input('Nombre o razon social',value=dataproveedorfiltro['nombre_razon_social'].iloc[0],disabled=True)
        with col2:
            st.text_input('Nombre comercial',value=dataproveedorfiltro['nombre_comercial'].iloc[0],disabled=True)
        with col3:
            st.text_input('Tipo',value=dataproveedorfiltro['tipo_identificacion'].iloc[0],disabled=True)
        with col4:
            st.text_input('Identificacion',value=dataproveedorfiltro['identificacion'].iloc[0],disabled=True)
        
        st.write('---')
        st.write('Información del cobro')
        col1,col2,col3 = st.columns(3)                
        with col1:
            fecha_factura = st.date_input('Fecha de la factura',value="today")
        with col2:
            valor_factura = st.number_input('Valor de la factura',min_value=0,value=0)
        with col3:
            iva = st.number_input('IVA',min_value=0,value=0)
            
        with col1:
            retencion_fuente = st.number_input('Retencion en la fuente',min_value=0,value=0)       
        with col2:
            retencion_ica = st.number_input('Retencion ICA',min_value=0,value=0)
        with col3:
            tipo_gasto = st.selectbox('Tipo de gasto',options=['Proveedor','Compras para la empresa','Empleados','Otros'])
            
        with col1:
            pagada = st.selectbox('Factura pagada?',options=['No','Si'])
        with col2:
            if pagada=='Si':
                lista_medios_pago = ['Transferencia bancaria','Consignacion','Efectivo','Tarjeta de credito','PSE','Nequi','Daviplata']
            else:
                lista_medios_pago = ['']
            forma_pago = st.selectbox('Forma de pago',options=lista_medios_pago)
        with col3:
            if pagada=='Si':
                fecha_pago = st.date_input('Fecha de pago',value="today")            
            else:
                fecha_pago = st.date_input('Fecha de pago',value=None)
        with col1:
            documento1 = st.file_uploader('Factura')
            if documento1 is not None:
                documento1 = img2s3(documento1)
                
        with col2:
            documento2 = st.file_uploader('Documento (1) (adicional)')
            if documento2 is not None:
                documento2 = img2s3(documento2)
                
        with col3:
            documento3 = st.file_uploader('Documento (2) (adicional)')
            if documento3 is not None:
                documento3 = img2s3(documento3)
                
        with col1:
            comprobante_pago = st.file_uploader('Comprobante de pago')
            if comprobante_pago is not None:
                comprobante_pago = img2s3(comprobante_pago)
        with col2:
            comentarios = st.text_area('Comentarios',value='')
    
        datamatch = pd.DataFrame([{'fecha_registro':datetime.now().strftime('%Y-%m-%d'),'fecha_factura':fecha_factura,'tipo_gasto':tipo_gasto,'documento1':documento1,'documento2':documento2,'documento3':documento3,'valor_factura':valor_factura,'iva':iva,'retencion_fuente':retencion_fuente,  'retencion_ica':retencion_ica,'pagada':pagada,'forma_pago':forma_pago,'fecha_pago':fecha_pago,'comprobante_pago':comprobante_pago,'comentarios':comentarios,'available':1}])
        datamatch.index = range(len(datamatch))
        dataproveedor2export = dataproveedorfiltro[['id','nombre_razon_social','nombre_comercial','tipo_identificacion','identificacion']]
        dataproveedor2export.rename(columns={'id':'id_modulo_proveedor'},inplace=True)
        dataexport = dataproveedor2export.merge(datamatch,left_index=True, right_index=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button('Crear cobro de terceros'):
                with st.spinner('Creando cobro de terceros'):
                    engine     = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')        
                    dataexport = dataexport.replace('', None)
                    dataexport.to_sql('modulo_gastos_terceros', engine, if_exists='append', index=False, chunksize=1)
                    st.success('Cobro de terceros creado exitosamente')
                    engine.dispose()
                    time.sleep(5)
                    st.cache_data.clear()
                    st.session_state.tipo_cuenta = True
                    st.session_state.tipo_crear  = False
                    st.rerun()
                    
#-----------------------------------------------------------------------------#
# Cuentas generales
def cuentas_generales():

    datagastosterceros(st.session_state.click)
    st.write('---')
    st.write('Filtro por factura')

    col1,col2,col3 = st.columns([2,2,1])
    with col1: 
        st.selectbox('Por Nombre o razon social del proveedor', options=st.session_state.lista_proveedores_terceros_edit,key='proveedores_terceros_edit',on_change=proveedorchange_edit)
    with col2:
        st.selectbox('Por Identificacion', options=st.session_state.lista_identificacion_terceros_edit,key='identificacion_terceros_edit',on_change=identificacionchange_edit)
    with col3: 
        st.selectbox('Por pago', options=st.session_state.lista_pagado_terceros_edit,key='pagado_terceros_edit',on_change=pagadochange_edit)

    datastockagrid = st.session_state.data_terceros_edit.copy()
    variables      = [x for x in ['id','fecha_factura', 'tipo_gasto', 'nombre_razon_social', 'nombre_comercial', 'tipo_identificacion', 'identificacion', 'valor_factura', 'iva', 'retencion_fuente', 'retencion_ica', 'pagada', 'forma_pago', 'fecha_pago'] if x in datastockagrid]

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
        datastockagridfilter       = datastockagridfilter.fillna(value='')
        datastockedit              = datastockagridfilter.copy()
        
        st.write('---')
        st.write('Información del Proveedor')
        col1,col2,col3,col4 = st.columns([3,3,1,2])
        with col1:
            st.text_input('Nombre o razon social',value=datastockedit['nombre_razon_social'].iloc[0],disabled=True)
        with col2:
            st.text_input('Nombre comercial',value=datastockedit['nombre_comercial'].iloc[0],disabled=True)
        with col3:
            st.text_input('Tipo',value=datastockedit['tipo_identificacion'].iloc[0],disabled=True)
        with col4:
            st.text_input('Identificacion',value=datastockedit['identificacion'].iloc[0],disabled=True)
        
        for i in ['fecha_factura','fecha_pago']:
            datastockedit[i] = pd.to_datetime(datastockedit[i],errors='coerce')

        st.write('---')
        st.write('Información del cobro')
        col1,col2,col3 = st.columns(3)    
        with col1:
            try:    fecha_factura = st.date_input('Fecha de la factura',value=datastockedit['fecha_factura'].iloc[0])
            except: fecha_factura = st.date_input('Fecha de la factura',value=None)
            datastockedit.loc[0,'fecha_factura'] = fecha_factura
        with col2:
            valor_factura = st.number_input('Valor de la factura',min_value=0,value=int(float(datastockedit['valor_factura'].iloc[0])))
            datastockedit.loc[0,'valor_factura'] = valor_factura
        with col3:
            iva = st.number_input('IVA',min_value=0,value=int(float(datastockedit['iva'].iloc[0])))
            datastockedit.loc[0,'iva'] = iva            
        with col1:
            retencion_fuente = st.number_input('Retencion en la fuente',min_value=0,value=int(float(datastockedit['retencion_fuente'].iloc[0])))       
            datastockedit.loc[0,'retencion_fuente'] = retencion_fuente            
        with col2:
            retencion_ica = st.number_input('Retencion ICA',min_value=0,value=int(float(datastockedit['retencion_ica'].iloc[0])))
            datastockedit.loc[0,'retencion_ica'] = retencion_ica     
        with col3:
            lista  = ['Proveedor','Compras para la empresa','Empleados','Otros']
            try:    
                if datastockedit['tipo_gasto'].iloc[0] in lista: 
                    indice = lista.index(datastockedit['tipo_gasto'].iloc[0])
                else:
                    indice = 0
            except: indice = 0
            tipo_gasto = st.selectbox('Tipo de gasto',options=lista,index=indice)
            datastockedit.loc[0,'tipo_gasto'] = tipo_gasto
        with col1:
            lista  = ['No','Si']
            try:    
                if datastockedit['pagada'].iloc[0] in lista: 
                    indice = lista.index(datastockedit['pagada'].iloc[0])
                else:
                    indice = 0
            except: indice = 0
            pagada = st.selectbox('Factura pagada?',options=lista,index=indice)
            datastockedit.loc[0,'pagada'] = pagada
        with col2:
            
            if pagada=='Si':
                lista = ['Transferencia bancaria','Consignacion','Efectivo','Tarjeta de credito','PSE','Nequi','Daviplata']
                try:    
                    if datastockedit['forma_pago'].iloc[0] in lista: 
                        indice = lista.index(datastockedit['forma_pago'].iloc[0])
                    else:
                        indice = 0
                except: indice = 0
            else:
                lista  = ['']
                indice = 0
            forma_pago = st.selectbox('Forma de pago',options=lista,index=indice)
            datastockedit.loc[0,'forma_pago'] = forma_pago
        with col3:
            try:    fecha_pago = st.date_input('Fecha de pago',value=datastockedit['fecha_pago'].iloc[0])
            except: fecha_pago = st.date_input('Fecha de pago',value=None)
            datastockedit.loc[0,'fecha_pago'] = fecha_pago
        with col1:
            documento1 = st.file_uploader('Factura')
            if documento1 is not None:
                documento1 = img2s3(documento1)
                datastockedit.loc[0,'documento1'] = documento1
            else:
                if es_url(datastockedit['documento1'].iloc[0]):
                    st.write(datastockedit['documento1'].iloc[0])
        with col2:
            documento2 = st.file_uploader('Documento (1) (adicional)')
            if documento2 is not None:
                documento2 = img2s3(documento2)
                datastockedit.loc[0,'documento2'] = documento2
            else:
                if es_url(datastockedit['documento2'].iloc[0]):
                    st.write(datastockedit['documento2'].iloc[0])
        with col3:
            documento3 = st.file_uploader('Documento (2) (adicional)')
            if documento3 is not None:
                documento3 = img2s3(documento3)
                datastockedit.loc[0,'documento3'] = documento3
            else:
                if es_url(datastockedit['documento3'].iloc[0]):
                    st.write(datastockedit['documento3'].iloc[0])
                    
        with col1:
            comprobante_pago = st.file_uploader('Comprobante de pago')
            if comprobante_pago is not None:
                comprobante_pago = img2s3(comprobante_pago)
                datastockedit.loc[0,'comprobante_pago'] = comprobante_pago
            else:
                if es_url(datastockedit['comprobante_pago'].iloc[0]):
                    st.write(datastockedit['comprobante_pago'].iloc[0])
        with col2:
            comentarios = st.text_area('Comentarios',value=datastockedit['comentarios'].iloc[0])     
            datastockedit.loc[0,'comentarios'] = comentarios

        col1, col2 = st.columns(2)
        with col1:
            if st.button('Guardar gasto de terceros'):
                st.session_state.editar        = True
                st.session_state.borrar        = False
                st.session_state.borrarconfirm = False
                
        with col2:
            if st.button('Borrar gasto'):
                st.session_state.editar        = False
                st.session_state.borrar        = True
                st.session_state.borrarconfirm = False
    
        if st.session_state.editar:
            editar_gastos_terceros(datastockedit)                
                
        if st.session_state.borrar:
            with col2:
                if st.button('Seguro de borrar gasto?'):
                    st.session_state.borrarconfirm = True

        if st.session_state.borrarconfirm and st.session_state.borrar:
            borrar_gastos_terceros(datastockedit)
            
def editar_gastos_terceros(datastock):     
    with st.spinner('Guardando gasto de terceros'):
        datastock.loc[0,'available'] = 1
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
            sql = f"UPDATE modulo_gastos_terceros SET {condicion} WHERE `id` = %s"
            list_of_tuples = datastock.to_records(index=False).tolist()
            cursor.executemany(sql, list_of_tuples)
        st.success('Gasto de terceros guardado exitosamente')
        conn.commit()
        conn.close()
        time.sleep(5)
        st.cache_data.clear()
        for i in ['editar','borrar','borrarconfirm']:
            if i in st.session_state:
                del st.session_state[i]
            if i not in st.session_state: 
                st.session_state[i] = False
        st.session_state.click += 1
        st.rerun()

def borrar_gastos_terceros(datastock):
    with st.spinner('Borrando gasto'):
        datastock = datastock.replace('', None)
        datastock = datastock[['id']]
        conn      = pymysql.connect(host=host,
                       user=user,
                       password=password,
                       db=schema)
        with conn.cursor() as cursor:
            #sql = "DELETE FROM modulo_proveedores WHERE id = %s"
            sql = "UPDATE modulo_gastos_terceros SET available=0 WHERE `id` = %s"
            list_of_tuples = datastock.to_records(index=False).tolist()
            cursor.executemany(sql, list_of_tuples)
        st.success('Gasto borrado exitosamente')
        conn.commit()
        conn.close()
        time.sleep(5)
        st.cache_data.clear()
        for i in ['editar','borrar','borrarconfirm']:
            if i in st.session_state:
                del st.session_state[i]
            if i not in st.session_state: 
                st.session_state[i] = False
        st.session_state.click += 1
        st.rerun()       

#-----------------------------------------------------------------------------#

formato = {'tipo_cuenta':False,
           'tipo_crear':False,
           'borrar':False,
           'editar':False,
           'borrarconfirm':False,
           'click':1,
           'proveedores_modulo_cobro_terceros': '',
           'lista_proveedores_modulo_cobro_terceros': [],
           'contactos_modulo_cobro_terceros': '',
           'lista_contactos_modulo_cobro_terceros': [],
           'dataorigen_gastos_evento': pd.DataFrame(),
           'data_gastos_evento': pd.DataFrame(),
           'dataorigen_terceros_edit': pd.DataFrame(),
           'data_terceros_edit': pd.DataFrame(),
           'lista_proveedores_terceros_edit': [],
           'lista_identificacion_terceros_edit': [],
           'lista_pagado_terceros_edit': [],
           'proveedores_terceros_edit': '',
           'identificacion_terceros_edit': '',
           'pagado_terceros_edit': ''
           }

for key,value in formato.items():
    if key not in st.session_state: 
        st.session_state[key] = value

col1,col2 = st.columns(2) 
with col1:
    if st.button('Crear'):
        st.session_state.tipo_crear  = True
        st.session_state.tipo_cuenta = False
        
with col2:
    if st.button('Cuentas generales'):
        st.session_state.tipo_crear  = False
        st.session_state.tipo_cuenta = True
 
if st.session_state.tipo_crear:
    crear_cobro()
    
if st.session_state.tipo_cuenta:
    cuentas_generales()
    
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
elements[10].style.backgroundColor = '#cc7076';
elements[10].style.fontWeight = 'bold';
elements[10].style.color = 'white';
elements[10].style.width = '100%'
elements[11].style.backgroundColor = '#cc7076';
elements[11].style.fontWeight = 'bold';
elements[11].style.color = 'white';
elements[11].style.width = '100%'
</script>
"""
)