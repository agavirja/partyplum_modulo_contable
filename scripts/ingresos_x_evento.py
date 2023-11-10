import streamlit as st
import re
import time
import pandas as pd
import numpy as np
import pymysql
import boto3
import copy
import random
import string
import requests
import streamlit.components.v1 as components
import mimetypes
from bs4 import BeautifulSoup
from sqlalchemy import create_engine 
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode, AgGridTheme
from urllib.parse import urlsplit

user     = st.secrets["user_bigdata"]
password = st.secrets["password_bigdata"]
host     = st.secrets["host_bigdata"]
schema   = 'partyplum'

@st.cache_data
def dataingresos(id_modulo_eventos,click):
    engine       = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')        
    dataingresos = pd.read_sql_query(f"""SELECT * FROM {schema}.modulo_facturacion_clientes WHERE id_modulo_eventos={id_modulo_eventos}""" , engine)
    engine.dispose()
    return dataingresos
    
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


def ingresos(id_modulo_eventos):       

    formato = {'click_ingreso':1,
               'editar':False,
    }

    for key,value in formato.items():
        if key not in st.session_state: 
            st.session_state[key] = value
            
    dataexport = dataingresos(id_modulo_eventos,st.session_state.click)
    dataexport.loc[0,'id_modulo_eventos'] = id_modulo_eventos
    st.write('---')
    st.write('---')
    st.write('Ingresos del evento')
    
    for i in ['fecha_pago1','fecha_pago2','fecha_pago3','fecha_pago4']:
        try: dataexport[i] = pd.to_datetime(dataexport[i],errors='coerce')
        except: pass
        
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.write('Pago 1')
        try:    fecha_pago1 = st.date_input('Fecha pago inicial', value=dataexport['fecha_pago1'].iloc[0])
        except: fecha_pago1 = st.date_input('Fecha pago inicial', value=None)
        try:    valor_pago1 = st.number_input('Valor del pago inicial',min_value=0,value=int(float(dataexport['valor_pago1'].iloc[0])))
        except: valor_pago1 = st.number_input('Valor del pago inicial',min_value=0,value=0)
        pago1 = st.file_uploader('Comprobante de pago inicial')
        if pago1 is not None:
            pago1 = img2s3(pago1)
            dataexport.loc[0,'pago1'] = pago1
        else:
            try:
                if es_url(dataexport['pago1'].iloc[0]):
                    st.write(dataexport['pago1'].iloc[0])
            except: pass
        dataexport.loc[0,'fecha_pago1'] = fecha_pago1 
        dataexport.loc[0,'valor_pago1'] = valor_pago1

    with col2:
        st.write('Pago 2')
        try:    fecha_pago2 = st.date_input('Fecha segundo pago', value=dataexport['fecha_pago2'].iloc[0])
        except: fecha_pago2 = st.date_input('Fecha segundo pago', value=None)
        try:    valor_pago2 = st.number_input('Valor del segundo pago',min_value=0,value=int(float(dataexport['valor_pago2'].iloc[0])))
        except: valor_pago2 = st.number_input('Valor del segundo pago',min_value=0,value=0)
        pago2 = st.file_uploader('Comprobante de segundo pago')
        if pago2 is not None:
            pago2 = img2s3(pago2)
            dataexport.loc[0,'pago2'] = pago2
        else:
            try:
                if es_url(dataexport['pago2'].iloc[0]):
                    st.write(dataexport['pago2'].iloc[0])
            except: pass
        dataexport.loc[0,'fecha_pago2'] = fecha_pago2 
        dataexport.loc[0,'valor_pago2'] = valor_pago2
        
    with col3:
        st.write('Pago 3')
        try:    fecha_pago3 = st.date_input('Fecha tercer pago', value=dataexport['fecha_pago3'].iloc[0])
        except: fecha_pago3 = st.date_input('Fecha tercer pago', value=None)
        try:    valor_pago3 = st.number_input('Valor del tercer pago',min_value=0,value=int(float(dataexport['valor_pago3'].iloc[0])))
        except: valor_pago3 = st.number_input('Valor del tercer pago',min_value=0,value=0)
        pago3 = st.file_uploader('Comprobante de tercer pago')
        if pago3 is not None:
            pago3 = img2s3(pago3)
            dataexport.loc[0,'pago3'] = pago3
        else:
            try:
                if es_url(dataexport['pago3'].iloc[0]):
                    st.write(dataexport['pago3'].iloc[0])
            except: pass
        dataexport.loc[0,'fecha_pago3'] = fecha_pago3
        dataexport.loc[0,'valor_pago3'] = valor_pago3 
        
    with col4:
        st.write('Pago 4')
        try:    fecha_pago4 = st.date_input('Fecha cuarto pago', value=dataexport['fecha_pago4'].iloc[0])
        except: fecha_pago4 = st.date_input('Fecha cuarto pago', value=None)
        try:    valor_pago4 = st.number_input('Valor del cuarto pago',min_value=0,value=int(float(dataexport['valor_pago4'].iloc[0])))
        except: valor_pago4 = st.number_input('Valor del cuarto pago',min_value=0,value=0)
        pago4 = st.file_uploader('Comprobante de cuarto pago')
        if pago4 is not None:
            pago4 = img2s3(pago4)
            dataexport.loc[0,'pago4'] = pago4
        else:
            try:
                if es_url(dataexport['pago4'].iloc[0]):
                    st.write(dataexport['pago4'].iloc[0])
            except: pass
        dataexport.loc[0,'fecha_pago4'] = fecha_pago4
        dataexport.loc[0,'valor_pago4'] = valor_pago4 
        
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Guardar ingresos'):
            st.session_state.editar = True

    if st.session_state.editar:
        editar_ingresos(dataexport) 
        
def editar_ingresos(datastock):
    with st.spinner('Guardando ingresos'):
        if pd.isna(datastock['id'].iloc[0]) or pd.isna(datastock['id'].iloc[0]) or datastock['id'].iloc[0] is None:
            engine    = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{schema}')        
            datastock.to_sql('modulo_facturacion_clientes', engine, if_exists='append', index=False, chunksize=1)
            st.success('Ingresos guardados exitosamente')
            engine.dispose()
        else:
            datastock = datastock.replace('', None)
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
                sql = f"UPDATE modulo_facturacion_clientes SET {condicion} WHERE `id` = %s"
                list_of_tuples = datastock.to_records(index=False).tolist()
                cursor.executemany(sql, list_of_tuples)
            st.success('Ingresos guardados exitosamente')
            conn.commit()
            conn.close()
        time.sleep(5)
        st.cache_data.clear()
        for i in ['editar']:
            if i in st.session_state:
                del st.session_state[i]
            if i not in st.session_state: 
                st.session_state[i] = False
        st.session_state.click += 1
        st.rerun()