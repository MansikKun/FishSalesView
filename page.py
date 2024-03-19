import streamlit as st
from graph import *


def home():
    with st.sidebar:
        selected_fishes = st.multiselect('수산물 종류 선택', df['수산물표준코드명'].unique())

    st.write('어종별 위판량 추이')
    date_amount(selected_fishes)
    st.write('어종별 평균중량 추이')
    date_height(selected_fishes)
def mapping():
    with st.sidebar:
        selected_species = st.selectbox('어종상태', options=(df_fish['어종상태명'].unique().tolist()))
        filtered_df = df_fish[df_fish['어종상태명'] == selected_species]
        selected_association = st.selectbox('산지조합', options=(filtered_df['산지조합명'].unique().tolist()))
    map_maker()
    hitmap(filtered_df)    

    toggle_merge = st.checkbox('작은 값들을 "기타"로 묶기',value=True)
    association_data = filtered_df[filtered_df['산지조합명'] == selected_association]
    round(association_data,toggle_merge)
    
    pass