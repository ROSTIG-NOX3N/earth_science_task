import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import json
from languages import get_labels  # languages.py에서 라벨 가져오기

# 방사성 동위원소 데이터 읽기 및 파싱
def parse_isotope_data(data):
    isotope_data = []
    if isinstance(data, list) and data[0] == "Dataset":
        for entry in data[1]:
            if entry[0] == "Association":
                isotope_name = None
                half_life = None
                for rule in entry[1:]:
                    if rule[0] == "Rule":
                        key = rule[1].strip("'")
                        value = rule[2].strip("'") if isinstance(rule[2], str) else rule[2]
                        if key == "Isotope":
                            isotope_name = value
                        elif key == "Half Life":
                            half_life = float(value)
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
    st.stop()

# 언어 선택 (한국어, 영어, 일본어 지원)
language = st.selectbox('언어를 선택해주세요 / Select language:', ['English', '한국어', '日本語'])
labels = get_labels(language)  # 선택된 언어에 맞는 라벨 가져오기

# 입력 연대 (1~9999 범위 강제)
input_age = st.number_input(labels['input_age'], min_value=1, max_value=9999, value=1, help="1에서 9999 사이의 연대를 입력해주세요.")

# 동위원소 이름과 넘버 분리
isotope_names = [item.split('-')[0] for item in [entry[0] for entry in isotope_data]]
isotope_numbers = [item.split('-')[1] for item in [entry[0] for entry in isotope_data]]

# 동위원소 이름 중복 제거
unique_isotope_names = list(set(isotope_names))

# 1. 첫 번째 선택 칸: 동위원소 이름 선택
selected_isotope_name = st.selectbox(labels['select_isotope_name'], unique_isotope_names)

# 2. 두 번째 선택 칸: 선택된 동위원소의 넘버 선택
filtered_isotope_numbers = [num for name, num in zip(isotope_names, isotope_numbers) if name == selected_isotope_name]
selected_isotope_number = st.selectbox(f'{selected_isotope_name} {labels["select_isotope_number"]}', filtered_isotope_numbers)

# 선택된 동위원소
selected_isotope = f'{selected_isotope_name}-{selected_isotope_number}'
selected_idx = [entry[0] for entry in isotope_data].index(selected_isotope)
selected_half_life = isotope_data[selected_idx][1]

# 입력된 연대와 반감기 차이를 계산하여 가장 가까운 동위원소 찾기
half_lives = [item[1] for item in isotope_data]
diffs = [abs(half_life - input_age) for half_life in half_lives]
nearest_idx = np.argmin(diffs)
nearest_isotope = isotope_data[nearest_idx][0]
nearest_half_life = isotope_data[nearest_idx][1]

# 1. 모든 동위원소 산포도 그리기 (점 크기 줄이기) - 그래프 내용은 영어로 유지
fig, ax = plt.subplots(figsize=(15, 6))
ax.scatter(range(len(half_lives)), half_lives, color='blue', label='Half-life', s=10)

# 입력된 연대에 가장 가까운 동위원소 강조 및 화살표 추가 (영어로 표시)
ax.annotate(f'Closest to input age ({input_age} years): {nearest_isotope}', xy=(nearest_idx, nearest_half_life),
            xytext=(nearest_idx, nearest_half_life * 1.5),
            arrowprops=dict(facecolor='green', shrink=0.05))

# 선택된 동위원소 강조 (영어로 표시)
ax.scatter(selected_idx, selected_half_life, color='orange', label=f'Selected Isotope: {selected_isotope}', s=50)
ax.axhline(y=input_age, color='gray', linestyle='--', label=f'Input Age: {input_age}')

# 라벨 및 제목 설정 (그래프 내부는 영어로 유지)
ax.set_xlabel('Isotope Index')
ax.set_ylabel('Half-life (years)')
ax.set_title('Scatter plot of Isotope Half-lives')
ax.set_yscale('log')
ax.legend()

# 그래프 출력
st.pyplot(fig)

# 동일한 이름의 동위원소만 산포도로 그리기 버튼
if st.button(labels['plot_same_name']):
    filtered_isotopes = [(name, number, half_life) for name, number, half_life in zip(isotope_names, isotope_numbers, half_lives) if name == selected_isotope_name]
    fig, ax = plt.subplots(figsize=(15, 6))
    for i, (name, number, half_life) in enumerate(filtered_isotopes):
        ax.scatter(i, half_life, color='blue', label=f'{name}-{number}' if i == 0 else "", s=50)
    ax.scatter(filtered_isotope_numbers.index(selected_isotope_number), selected_half_life, color='orange', label=f'Selected Isotope: {selected_isotope}', s=100)
    ax.set_xlabel('Isotope Index')
    ax.set_ylabel('Half-life (years)')
    ax.set_title(f'Scatter plot of all isotopes with the name {selected_isotope_name}')
    ax.set_yscale('log')
    ax.legend()
    st.pyplot(fig)

# 결과 표시 (UI는 언어에 따라 변경됨, 그래프 내부는 영어로 유지)
st.write(f"{labels['selected_isotope']} **{selected_isotope}**")
st.write(f"**{labels['selected_half_life']}: {selected_half_life} {labels['half_life_years']}**")
st.write(f"{labels['nearest_isotope']}: **{nearest_isotope}** ({nearest_half_life} {labels['half_life_years']})")
