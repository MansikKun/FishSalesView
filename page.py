import streamlit as st
from graph import *
import time

def home():
    selected_fishes = st.multiselect('수산물 종류 선택', df['수산물표준코드명'].unique())
    col1, col2= st.columns([1,1])
    with col1:
        st.title('어종별 위판량 추이')
        date_amount(selected_fishes)
    with col2:
        st.title('어종별 평균중량 추이')
        date_height(selected_fishes)
def mapping():
    map_maker()
    selected_species = st.selectbox('어종상태명을 선택하세요.', options=(df_fish['어종상태명'].unique().tolist()))
    filtered_df = df_fish[df_fish['어종상태명'] == selected_species]
    
    col1, col2= st.columns([1,1])
    with col1:  
        
        hitmap(filtered_df)
    with col2:
        selected_association = st.selectbox('산지조합을 선택하세요.', options=(filtered_df['산지조합명'].unique().tolist()))
        association_data = filtered_df[filtered_df['산지조합명'] == selected_association]
        round(association_data)
        pass