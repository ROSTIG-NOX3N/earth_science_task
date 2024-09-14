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

# 동위원소 이름과 넘버 분리
isotope_names = [item.split('-')[0] for item in [entry[0] for entry in isotope_data]]
isotope_numbers = [item.split('-')[1] for item in [entry[0] for entry in isotope_data]]

# 동위원소 이름 중복 제거
unique_isotope_names = list(set(isotope_names))

# 1. 첫 번째 선택 칸: 동위원소 이름 선택
selected_isotope_name = st.selectbox('Select Isotope Name:', unique_isotope_names)

# 2. 두 번째 선택 칸: 선택된 동위원소의 넘버 선택
# 선택된 동위원소 이름에 해당하는 넘버 필터링
filtered_isotope_numbers = [num for name, num in zip(isotope_names, isotope_numbers) if name == selected_isotope_name]
selected_isotope_number = st.selectbox(f'Select {selected_isotope_name} Number:', filtered_isotope_numbers)

# 선택된 동위원소
selected_isotope = f'{selected_isotope_name}-{selected_isotope_number}'
selected_idx = [entry[0] for entry in isotope_data].index(selected_isotope)
selected_half_life = isotope_data[selected_idx][1]

# 입력된 연대와 반감기 차이를 계산하여 가장 가까운 동위원소 찾기
half_lives = [item[1] for item in isotope_data]
diffs = [abs(half_life - input_age) for half_life in half_lives]
nearest_idx = np.argmin(diffs)  # 입력된 연대에 가장 가까운 동위원소의 인덱스
nearest_isotope = isotope_data[nearest_idx][0]
nearest_half_life = isotope_data[nearest_idx][1]

# 1. 모든 동위원소 산포도 그리기 (점 크기 줄이기)
fig, ax = plt.subplots(figsize=(15, 6))
ax.scatter(range(len(half_lives)), half_lives, color='blue', label='Half-life', s=10)  # 점 크기 줄임 (s=10)

# 입력된 연대에 가장 가까운 동위원소 강조 및 화살표 추가
ax.annotate(f'Closest to input age ({input_age} years): {nearest_isotope}', xy=(nearest_idx, nearest_half_life),
            xytext=(nearest_idx, nearest_half_life * 1.5),
            arrowprops=dict(facecolor='green', shrink=0.05))

# 선택된 동위원소 강조
ax.scatter(selected_idx, selected_half_life, color='orange', label=f'Selected Isotope: {selected_isotope}', s=50)  # 선택된 동위원소는 큰 크기로 표시
ax.axhline(y=input_age, color='gray', linestyle='--', label=f'Input Age: {input_age}')

# 라벨 및 제목 설정
ax.set_xlabel(labels['isotope_index'])
ax.set_ylabel(labels['half_life'])
ax.set_title(labels['scatter_plot_title'])
ax.set_yscale('log')  # 로그 스케일 설정
ax.legend()

# 그래프 출력
st.pyplot(fig)

# 결과 표시 (영어로 고정)
st.write(f"Selected Isotope: **{selected_isotope}**")
st.write(f"**Half-life of selected isotope: {selected_half_life} years**")
st.write(f"Closest Isotope to Input Age: **{nearest_isotope}** with half-life of {nearest_half_life} years")
