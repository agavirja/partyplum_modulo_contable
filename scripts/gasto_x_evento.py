import streamlit as st
import re
import time
import pandas as pd
import pymysql
import streamlit.components.v1 as components
from bs4 import BeautifulSoup
from sqlalchemy import create_engine 
from datetime import datetime

user     = st.secrets["user_bigdata"]
password = st.secrets["password_bigdata"]
host     = st.secrets["host_bigdata"]
schema   = 'partyplum'

lista_categorias = ['Aguas', 'Alquileres', 'Cajas', 'Domicilios', 'Flores', 'Impresiones', 'Personal', 'Postres', 'Reposteria', 'Transporte']

@st.cache_data
def dataproveedores():
    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')        
    st.session_state.dataorigen_gastos_evento = pd.read_sql_query(f"""SELECT * FROM {schema}.modulo_proveedores WHERE available=1""" , engine)
    st.session_state.data_gastos_evento       = st.session_state.dataorigen_gastos_evento.copy()
    st.session_state.lista_proveedores  = ['Todos'] + sorted(list(st.session_state.dataorigen_gastos_evento[st.session_state.dataorigen_gastos_evento['nombre_razon_social'].notnull()]['nombre_razon_social'].unique()))
    st.session_state.lista_contactos    = ['Todos'] + sorted(list(st.session_state.dataorigen_gastos_evento[st.session_state.dataorigen_gastos_evento['nombre_contacto'].notnull()]['nombre_contacto'].unique()))
    st.session_state.proveedores        = 'Todos'
    st.session_state.contactos          = 'Todos'
    engine.dispose()
    
def reset_todos():
    st.session_state.data_gastos_evento = st.session_state.dataorigen_gastos_evento.copy()
    st.session_state.lista_proveedores = ['Todos'] + sorted(list(st.session_state.dataorigen_gastos_evento[st.session_state.dataorigen_gastos_evento['nombre_razon_social'].notnull()]['nombre_razon_social'].unique()))
    st.session_state.lista_contactos   = ['Todos'] + sorted(list(st.session_state.dataorigen_gastos_evento[st.session_state.dataorigen_gastos_evento['nombre_contacto'].notnull()]['nombre_contacto'].unique()))
    st.session_state.proveedores       = 'Todos'
    st.session_state.contactos         = 'Todos'

def proveedorchange():
    if st.session_state.proveedores=='Todos':
        reset_todos()
    else:
        idd = st.session_state.data_gastos_evento['nombre_razon_social']==st.session_state.proveedores
        st.session_state.data_gastos_evento = st.session_state.data_gastos_evento[idd]
        st.session_state.lista_proveedores  = ['Todos'] + sorted(list(st.session_state.data_gastos_evento[st.session_state.data_gastos_evento['nombre_razon_social'].notnull()]['nombre_razon_social'].unique()))
        st.session_state.lista_contactos    = ['Todos'] + sorted(list(st.session_state.data_gastos_evento[st.session_state.data_gastos_evento['nombre_contacto'].notnull()]['nombre_contacto'].unique()))
        st.session_state.proveedores  = st.session_state.proveedores
        st.session_state.contactos    = st.session_state.contactos

def contactochange():
    if st.session_state.contactos=='Todos':
        reset_todos()
    else:
        idd = st.session_state.data_gastos_evento['nombre_contacto']==st.session_state.contactos
        st.session_state.data_gastos_evento = st.session_state.data_gastos_evento[idd]
        st.session_state.lista_proveedores  = ['Todos'] + sorted(list(st.session_state.data_gastos_evento[st.session_state.data_gastos_evento['nombre_razon_social'].notnull()]['nombre_razon_social'].unique()))
        st.session_state.lista_contactos    = ['Todos'] + sorted(list(st.session_state.data_gastos_evento[st.session_state.data_gastos_evento['nombre_contacto'].notnull()]['nombre_contacto'].unique()))
        st.session_state.proveedores  = st.session_state.proveedores
        st.session_state.contactos    = st.session_state.contactos
        
def crear_gasto_evento(id_modulo_eventos):

    formato = {'click':0,
               'editar_gasto':False,
               'borrar_gasto':False,
               'borrar_gastoconfirm':False,
               'proveedores':'',
               'lista_proveedores':[],
               'contactos':'',
               'lista_contactos':[],
               'dataorigen_gastos_evento':pd.DataFrame(),
               'data_gastos_evento':pd.DataFrame(),
    }

    for key,value in formato.items():
        if key not in st.session_state: 
            st.session_state[key] = value
            
    dataproveedores()
    st.write('---')
    st.write('Añadir Gasto')
    col1,col2= st.columns(2)
    with col1: 
        st.selectbox('Por Nombre o razon social del proveedor', options=st.session_state.lista_proveedores,key='proveedores',on_change=proveedorchange)
    with col2: 
        st.selectbox('Por Contacto', options=st.session_state.lista_contactos,key='contactos',on_change=contactochange)

    datastockgastoevento       = st.session_state.data_gastos_evento.copy()
    datastockgastoevento       = datastockgastoevento.iloc[[0]]
    datastockgastoevento.index = range(len(datastockgastoevento))
    
    id_modulo_proveedores = int(datastockgastoevento['id'].iloc[0])
    nombre_razon_social   = datastockgastoevento['nombre_razon_social'].iloc[0]
    nombre_comercial      = datastockgastoevento['nombre_comercial'].iloc[0]
    tipo_identificacion   = datastockgastoevento['tipo_identificacion'].iloc[0]
    identificacion        = datastockgastoevento['identificacion'].iloc[0]
    
    col1,col2,col3 = st.columns(3)
    with col1:
        valor = st.number_input('Valor proveedor',min_value=0,value=0)
    with col2:
        iva = st.number_input('IVA',min_value=0,value=0)
    with col3:
        categoria = st.selectbox('Categoria', options=lista_categorias)

    dataexportgastoevento = pd.DataFrame([{'id_modulo_eventos':id_modulo_eventos,
                                'id_modulo_proveedores':id_modulo_proveedores,
                                'fecha_registro':datetime.now().strftime('%Y-%m-%d'),
                                'nombre_razon_social':nombre_razon_social,
                                'nombre_comercial':nombre_comercial,
                                'tipo_identificacion':tipo_identificacion,
                                'identificacion':identificacion,
                                'valor':valor,
                                'iva':iva,
                                'categoria':categoria,
                                'available':1
                                }])
    
    if st.button('Guardar Gasto'):
        with st.spinner('Guardando Gasto'):
            engine     = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')        
            dataexportgastoevento = dataexportgastoevento.replace('', None)
            dataexportgastoevento.to_sql('modulo_gastos_evento', engine, if_exists='append', index=False, chunksize=1)
            st.success('Gasto guardado exitosamente')
            engine.dispose()
            #st.cache_data.clear()
            st.session_state.click += 1
            st.session_state.anadirgasto = False
            st.rerun()
    
    
def editar_gasto_evento(datagastos,id_gasto):

    formato = {'click':0,
               'editar_gasto':False,
               'borrar_gasto':False,
               'borrar_gastoconfirm':False,
               'proveedores':'',
               'lista_proveedores':[],
               'contactos':'',
               'lista_contactos':[],
               'dataorigen_gastos_evento':pd.DataFrame(),
               'data_gastos_evento':pd.DataFrame(),
    }

    for key,value in formato.items():
        if key not in st.session_state: 
            st.session_state[key] = value
            
    editdatagasto = datagastos[datagastos['id']==id_gasto]
    
    col1,col2,col3,col4 = st.columns([3,2,1,2])
    with col1:
        st.text_input('Nombre o razon social',value=editdatagasto['nombre_razon_social'].iloc[0],disabled=True)
    with col2:
        st.text_input('Nombre comercial',value=editdatagasto['nombre_comercial'].iloc[0],disabled=True)
    with col3:
        st.text_input('Tipo de identificacion',value=editdatagasto['tipo_identificacion'].iloc[0],disabled=True)
    with col4:
        st.text_input('Identificacion',value=editdatagasto['identificacion'].iloc[0],disabled=True)

    col1,col2,col3 = st.columns(3)
    with col1:
        valor = st.number_input('Valor proveedor',min_value=0,value=int(float(editdatagasto['valor'].iloc[0])))
    with col2:
        iva = st.number_input('IVA',min_value=0,value=int(float(editdatagasto['iva'].iloc[0])))
    with col3:
        try:    
            if editdatagasto['categoria'].iloc[0] in lista_categorias: 
                indice = lista_categorias.index(editdatagasto['categoria'].iloc[0])
            else:
                indice = 0
        except: indice = 0
        categoria = st.selectbox('Categoria', options=lista_categorias,index=indice)

    dataeditgastoevento = pd.DataFrame([{'id':id_gasto,
                                'valor':valor,
                                'iva':iva,
                                'categoria':categoria,
                                'available':1
                                }])

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Guardar Gasto'):
            st.session_state.editar_gasto        = True
            st.session_state.borrar_gasto        = False
            st.session_state.borrar_gastoconfirm = False
            
    with col2:
        if st.button('Borrar Gasto'):
            st.session_state.editar_gasto        = False
            st.session_state.borrar_gasto        = True
            st.session_state.borrar_gastoconfirm = False

    if st.session_state.editar_gasto:
        editar_gasto(dataeditgastoevento)              
            
    if st.session_state.borrar_gasto:
        with col2:
            if st.button('Seguro quiere borrar el gasto?'):
                st.session_state.borrar_gastoconfirm = True

    if st.session_state.borrar_gastoconfirm and st.session_state.borrar_gasto:
        borrar_proveedor(dataeditgastoevento) 
    
    
def editar_gasto(dataeditgastoevento): 
    with st.spinner('Guardando gasto'):
        dataeditgastoevento = dataeditgastoevento.replace('', None)
        
        variables = list(dataeditgastoevento)
        variables.remove('id')
        condicion = '`'+'`=%s,`'.join(variables)+'`=%s'
        variables.append('id')
        dataeditgastoevento = dataeditgastoevento[variables]
        conn = pymysql.connect(host=host,
                       user=user,
                       password=password,
                       db=schema)
        with conn.cursor() as cursor:
            sql = f"UPDATE modulo_gastos_evento SET {condicion} WHERE `id` = %s"
            list_of_tuples = dataeditgastoevento.to_records(index=False).tolist()
            cursor.executemany(sql, list_of_tuples)
        st.success('Gasto guardado exitosamente')
        conn.commit()
        conn.close()
        time.sleep(5)
        #st.cache_data.clear()
        for i in ['editar_gasto','borrar_gasto','borrar_gastoconfirm']:
            if i in st.session_state:
                del st.session_state[i]
            if i not in st.session_state: 
                st.session_state[i] = False
        st.session_state.click += 1
        st.rerun()
             
def borrar_proveedor(dataeditgastoevento):
    with st.spinner('Borrando gasto'):
        dataeditgastoevento = dataeditgastoevento[['id']]
        conn = pymysql.connect(host=host,
                       user=user,
                       password=password,
                       db=schema)
        with conn.cursor() as cursor:
            # sql = "DELETE FROM modulo_gastos_evento WHERE id = %s"
            sql = "UPDATE modulo_gastos_evento SET available=0 WHERE `id` = %s"
            list_of_tuples = dataeditgastoevento.to_records(index=False).tolist()
            cursor.executemany(sql, list_of_tuples)
        st.success('Gasto borrado exitosamente')
        conn.commit()
        conn.close()
        time.sleep(5)
        st.session_state.borrar_gasto = False
        #st.cache_data.clear()
        for i in ['editar_gasto','borrar_gasto','borrar_gastoconfirm']:
            if i in st.session_state:
                del st.session_state[i]
            if i not in st.session_state: 
                st.session_state[i] = False
        st.session_state.click += 1
        st.rerun()
#-----------------------------------------------------------------------------#s        