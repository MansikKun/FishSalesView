import streamlit as st
from page import *

st.set_page_config(layout="wide")

if 'page' not in st.session_state:
    st.session_state['page'] = 'HOME'

menus={'HOME':home,"Map":map}

with st.sidebar:
    for menu in menus.keys():
        if st.button(menu, use_container_width=True, type='primary' if st.session_state['page']==menu else 'secondary'):
            st.session_state['page']=menu
            st.rerun()

for menu in menus.keys():
    if st.session_state['page']==menu:
        menus[menu]()