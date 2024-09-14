import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import json
from languages import get_labels

# 방사성 동위원소 데이터 읽기
def load_isotope_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # 데이터에서 방사성 동위원소와 반감기 추출
    isotope_data = []
    for entry in data:  # 데이터의 각 항목을 순회합니다.
        isotope_name = entry.get('Isotope')
        half_life = entry.get('Half Life')
        
        if isotope_name and half_life:
            isotope_data.append((isotope_name, float(half_life)))
    
    return isotope_data

# 방사성 동위원소 데이터 불러오기
isotope_data = load_isotope_data('Radioactive-Isotope-Half-Lives.json')

# 언어 선택
language = st.selectbox('Select language:', ['English', '한국어'])
labels = get_labels(language)

# 입력 연대
input_age = st.number_input(labels['input_age'], min_value=1, value=1)

# 반감기 값을 추출
half_lives = [item[1] for item in isotope_data]
isotope_names = [item[0] for item in isotope_data]

# 가장 1에 가까운 반감기 찾기
diffs = [abs(half_life - input_age) for half_life in half_lives]
nearest_idx = np.argmin(diffs)
nearest_isotope = isotope_names[nearest_idx]

# 방사성 동위원소 선택
selected_isotope = st.selectbox(labels['select_isotope'], isotope_names)
selected_idx = isotope_names.index(selected_isotope)
selected_half_life = half_lives[selected_idx]

# 기본 산포도 그리기
fig, ax = plt.subplots(figsize=(15, 6))
ax.scatter(range(len(half_lives)), half_lives, color='blue', label='Half-life')

# 1에 가장 가까운 동위원소에 화살표 추가
ax.annotate(f'{labels["annotate_closest"]} : {nearest_isotope}', xy=(nearest_idx, half_lives[nearest_idx]),
            xytext=(nearest_idx, half_lives[nearest_idx] * 1.5),
            arrowprops=dict(facecolor='green', shrink=0.05))

# 선택된 동위원소의 반감기 강조
ax.scatter(selected_idx, selected_half_life, color='orange', label=f'{labels["annotate_selected"]} {selected_isotope}')
ax.axhline(y=input_age, color='gray', linestyle='--', label=f'{labels["input_age_label"]} {input_age}')

# 반감기 값은 로그 스케일로 표시
ax.set_yscale('log')

# 그래프 라벨 추가
ax.set_xlabel(labels['isotope_index'])
ax.set_ylabel(labels['half_life'])
ax.set_title(labels['scatter_plot_title'])

# 범례 추가
ax.legend()

# 기본 그래프 출력
st.pyplot(fig)

# 더보기 버튼 생성 후 선택된 동위원소와 가장 가까운 동위원소만 그리기
if st.button('더보기'):
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # 선택된 동위원소와 가장 가까운 동위원소만 표시
    ax.scatter([nearest_idx, selected_idx], [half_lives[nearest_idx], selected_half_life], color=['green', 'orange'], label=[nearest_isotope, selected_isotope])
    
    # 주석 추가
    ax.annotate(f'{labels["annotate_closest"]}: {nearest_isotope}', xy=(nearest_idx, half_lives[nearest_idx]), xytext=(nearest_idx, half_lives[nearest_idx] * 1.5),
                arrowprops=dict(facecolor='green', shrink=0.05))
    ax.annotate(f'{labels["annotate_selected"]}: {selected_isotope}', xy=(selected_idx, selected_half_life), xytext=(selected_idx, selected_half_life * 0.5),
                arrowprops=dict(facecolor='orange', shrink=0.05))
    
    # 반감기 값 로그 스케일 설정
    ax.set_yscale('log')

    # 라벨 및 제목 추가
    ax.set_xlabel(labels['isotope_index'])
    ax.set_ylabel(labels['half_life'])
    ax.set_title(f'{selected_isotope} vs {nearest_isotope}')
    
    # 그래프 출력
    st.pyplot(fig)

# 결과 표시
st.write(f"{labels['closest']} : **{nearest_isotope}**")
st.write(f"{labels['selected']} **{selected_isotope}**")
st.write(f"**{labels['half_life_of_selected_isotope']}: {selected_half_life}**")
