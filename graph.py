import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import matplotlib.font_manager as fm

import seaborn as sns

from folium.plugins import MarkerCluster
import folium
from streamlit_folium import st_folium

#한글폰트 지정
plt.rcParams['font.family'] ='Malgun Gothic'

df_fish = pd.read_csv('C:\workspace\FisherySalesView\data\해양수산부_위판장별위탁판매현황.CSV', encoding='cp949')
df_shop = pd.read_csv('C:\workspace\FisherySalesView\data\산지위판장.csv', encoding='cp949')
df = pd.DataFrame(df_fish)
def date_amount(selected_fishes):
    #위판일자 데이터를 문자열이아닌 데이트타임타입으로 변경
    df['위판일자'] = pd.to_datetime(df['위판일자'])
    # 사용자가 여러 수산물 종류를 선택할 수 있도록 multiselect 사용


    # 위판일자별, 수산물 종류별로 위판수량 합계 계산
    summed_df = df.groupby(['위판일자', '수산물표준코드명'])['위판수량'].sum().reset_index()

    # 맷플롯립을 이용한 꺾은선 그래프 그리기
    #사이즈 설정
    plt.figure(figsize=(20, 10))

    # 선택된 수산물 종류별로 그래프 그리기
    for fish in selected_fishes:
        fish_df = summed_df[summed_df['수산물표준코드명'] == fish]
        fish_df['위판일자']
        plt.plot(np.array(fish_df['위판일자']),np.array(fish_df['위판수량']), label=fish, marker='o')

    plt.title('선택된 수산물 종류별 위판량 추이')
    plt.xlabel('위판일자')
    plt.ylabel('위판수량')
    plt.xticks(rotation=60)
    plt.legend()
    plt.tight_layout()

    # 스트림릿을 통해 그래프 보여주기
    return st.pyplot(plt)
def date_height(selected_fishes):


    # 위판일자별, 수산물 종류별로 위판수량 합계 계산
    summed_df = df.groupby(['위판일자', '수산물표준코드명'])['위판중량'].mean().reset_index()

    # 맷플롯립을 이용한 막대그래프 그리기
    # 크기조정
    plt.figure(figsize=(20, 10))
    # 바의 너비 설정
    bar_width = 0.35

    # 선택된 수산물 종류별로 그래프 그리기
    for fish in selected_fishes:
        fish_df = summed_df[summed_df['수산물표준코드명'] == fish]

        plt.bar(np.array(fish_df['위판일자']),np.array(fish_df['위판중량']), label=fish, alpha=0.7)

    plt.title('선택된 수산물 종류별 평균중량 추이')
    plt.xlabel('위판일자')
    plt.ylabel('위판중량')
    plt.xticks(rotation=60)
    plt.legend()
    plt.tight_layout()

    # 스트림릿을 통해 그래프 보여주기
    return st.pyplot(plt)
#-------------------------
def map_maker():
    # Streamlit 애플리케이션 제목
    st.title('전국 위판장 위치')
    # 위도와 경도에서 NaN 값이 있는 행 제거
    df_shop.dropna(subset=['위도', '경도'], inplace=True)

    # 지도 생성 및 마커 추가
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=7)
    marker_cluster = MarkerCluster().add_to(m)

    for idx, row in df_shop.iterrows():
        folium.Marker(location=[row['위도'], row['경도']], tooltip=row['조합명']).add_to(marker_cluster)

    # 스트림릿에서 지도 표시
    return st_folium(m, width=725)
    pass
def hitmap(filtered_df):
    # 히트맵에 사용할 데이터 준비
    pivot_table = filtered_df.pivot_table(index='산지조합명', columns='어종상태명', values='위판수량', aggfunc='mean')

    # 히트맵 생성을 위한 Figure와 Axes 객체 생성
    fig, ax = plt.subplots(figsize=(10, 11))
    sns.heatmap(pivot_table, annot=True, fmt=".1f", cmap="YlGnBu", ax=ax ,yticklabels=True)
    plt.yticks(rotation=0)
    # 스트림릿에서 Figure 객체 전달
    return st.pyplot(fig)
    
    pass
def round(association_data,toggle_merge):

    if toggle_merge:
        # 어종별 위판수량 집계
        species_counts = association_data.groupby('수산물표준코드명')['위판수량'].mean()
        # 수량 크기대로 내림차순 정리
        df_sorted = species_counts.sort_values(ascending=False)
        # 퍼센트 게이지 범위 설정, 너무 작은 것들 합치기
        threshold = 0.028 
        other = df_sorted[df_sorted / df_sorted.sum() < threshold].sum()
        df_filtered = df_sorted[df_sorted / df_sorted.sum() >= threshold]
        df_filtered['기타'] = other  # 너무 작은 값들을 '기타'로 합침
    else:
        # 어종별 위판수량 집계만 진행
        species_counts = association_data.groupby('수산물표준코드명')['위판수량'].mean()
        df_filtered = species_counts.sort_values(ascending=False)

    # 원그래프 그리기
    fig, ax = plt.subplots(figsize=(10, 8.5))
    wedges, texts, autotexts = ax.pie(df_filtered, 
                                      labels=df_filtered.index, 
                                      autopct='%1.1f%%', 
                                      textprops={'fontsize': 10})

    ax.axis('equal')  # 동그란 원 형태 유지
    #어종따로 표시
    ax.legend(wedges, df_filtered.index,
              title="어종",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    # 스트림릿에서 그래프 출력
    st.pyplot(fig)
#-------------------------