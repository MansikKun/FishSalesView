import streamlit as st
from page import *



if 'page' not in st.session_state:
    st.session_state['page'] = 'HOME'

menus={'날짜별':home,"장소별":mapping}

with st.sidebar:
    for menu in menus.keys():
        if st.button(menu, use_container_width=True, type='primary' if st.session_state['page']==menu else 'secondary'):
            st.session_state['page']=menu
            st.rerun()

for menu in menus.keys():
    if st.session_state['page']==menu:
        menus[menu]()