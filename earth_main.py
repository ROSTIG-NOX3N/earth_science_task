import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import json
from languages import get_labels

# 방사성 동위원소 데이터 읽기 및 파싱
def parse_isotope_data(data):
    isotope_data = []
    if isinstance(data, list) and data[0] == "Dataset":
        for entry in data[1]:
            if entry[0] == "Association":
                isotope_name = None
                half_life = None
                
                # 각 Association 내부의 Rule을 확인하여 Isotope와 Half Life 추출
                for rule in entry[1:]:
                    if rule[0] == "Rule":
                        key = rule[1].strip("'")  # 키에서 따옴표 제거
                        value = rule[2].strip("'") if isinstance(rule[2], str) else rule[2]  # 값에서 따옴표 제거
                        
                        if key == "Isotope":
                            isotope_name = value
                        elif key == "Half Life":
                            half_life = float(value)

                # Isotope와 Half Life가 모두 존재할 경우 리스트에 추가
                if isotope_name and half_life:
                    isotope_data.append((isotope_name, half_life))
                else:
                    st.warning(f"Missing 'Isotope' or 'Half Life' in entry: {entry}")
    return isotope_data

# 방사성 동위원소 데이터 불러오기
def load_isotope_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return parse_isotope_data(data)
    except Exception as e:
        st.error(f"Failed to load isotope data: {e}")
        return []

# 방사성 동위원소 데이터 불러오기
isotope_data = load_isotope_data('Formatted-Radioactive-Isotope-Half-Lives.json')

if not isotope_data:
    st.stop()  # 데이터 로드에 실패하면 앱 중지

# 언어 선택 (그래프는 무조건 영어로 표시되지만 인터페이스는 언어 선택 가능)
language = st.selectbox('Select language:', ['English', '한국어'])
labels = get_labels(language)

# 입력 연대
input_age = st.number_input(labels['input_age'], min_value=1, value=1)

# 반감기 값을 추출
half_lives = [item[1] for item in isotope_data]
isotope_names = [item[0] for item in isotope_data]

# 입력된 연대와 반감기 차이를 계산하여 가장 가까운 100개 선택
diffs = [abs(half_life - input_age) for half_life in half_lives]
sorted_indices = np.argsort(diffs)[:100]  # 차이가 가장 작은 100개의 인덱스

# 1. 산포도 그리기 (우상향으로 정렬)
sorted_half_lives = sorted([half_lives[i] for i in sorted_indices])  # 반감기 값을 오름차순 정렬
fig, ax = plt.subplots(figsize=(15, 6))
ax.scatter(range(len(sorted_half_lives)), sorted_half_lives, color='blue', label='Half-life')
ax.set_xlabel(labels['isotope_index'])
ax.set_ylabel(labels['half_life'])
ax.set_title(labels['scatter_plot_title'])  # 영어 고정 제목 사용
ax.set_yscale('log')  # 로그 스케일 설정
st.pyplot(fig)

# 2. 방사성 동위원소 선택
selected_isotope = st.selectbox(labels['select_isotope'], [isotope_names[i] for i in sorted_indices])
selected_idx = isotope_names.index(selected_isotope)
selected_half_life = half_lives[selected_idx]

# 3. "더보기" 버튼을 눌렀을 때 산포도 표시
if st.button('더보기'):
    # 선택된 동위원소 주변 100개의 데이터를 반감기 기준으로 가져오기
    diffs_selected = [abs(half_life - selected_half_life) for half_life in half_lives]
    sorted_selected_indices = np.argsort(diffs_selected)[:100]  # 차이가 가장 작은 100개의 인덱스
    sorted_selected_half_lives = sorted([half_lives[i] for i in sorted_selected_indices])  # 반감기 값을 오름차순 정렬
    
    fig, ax = plt.subplots(figsize=(15, 6))
    
    # 주변 100개의 데이터를 산포도로 표시
    ax.scatter(range(len(sorted_selected_half_lives)), sorted_selected_half_lives, color='blue', label='Half-life')
    
    # 선택된 동위원소 강조
    ax.scatter(selected_idx, selected_half_life, color='orange', label=f'Selected Isotope: {selected_isotope}')
    ax.set_xlabel(labels['isotope_index'])
    ax.set_ylabel(labels['half_life'])
    ax.set_title(labels['scatter_around_title'])  # 영어 고정 제목 사용
    ax.set_yscale('log')  # 로그 스케일 설정
    ax.legend()
    
    st.pyplot(fig)

# 결과 표시 (영어로 고정)
st.write(f"Selected Isotope: **{selected_isotope}**")
st.write(f"**Half-life of selected isotope: {selected_half_life} years**")
