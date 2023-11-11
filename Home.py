import streamlit as st
import streamlit.components.v1 as components


# streamlit run D:\Dropbox\Empresa\PartyPlum\app_matina_eventos\Home.py
# https://streamlit.io/
# pipreqs --encoding utf-8 "D:\Dropbox\Empresa\PartyPlum\app_matina_eventos"

#st.set_page_config(layout="wide")
st.set_page_config(layout="wide",page_icon ="https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/partyplum/favicon_party_plum.png")
st.image('https://personal-data-bucket-online.s3.us-east-2.amazonaws.com/partyplum_logosimbolo.png')


components.html(
    """
<script>
const elements = window.parent.document.querySelectorAll('.stDownloadButton button')
elements[0].style.width = '100%';
elements[0].style.fontWeight = 'bold';
elements[0].style.backgroundColor = '#17e88f';
elements[1].style.width = '100%';
elements[1].style.fontWeight = 'bold';
elements[1].style.backgroundColor = '#17e88f';
elements[2].style.width = '100%';
elements[2].style.fontWeight = 'bold';
elements[2].style.backgroundColor = '#17e88f';
</script>
"""
)
