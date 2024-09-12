import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 파일에서 방사성 동위원소 데이터 읽기
def load_isotope_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            name, half_life = line.strip().split(',')
            data.append((name, float(half_life)))
    return data

# 언어에 따른 레이블
def get_labels(language):
    if language == 'English':
        return {
            'input_age': 'Enter a comparison age:',
            'select_isotope': 'Select an isotope:',
            'scatter_plot_title': 'Scatter plot of Isotope Half-lives with Annotations',
            'half_life': 'Half-life (years)',
            'isotope_index': 'Isotope Index',
            'closest': 'Closest to',
            'selected': 'Selected Isotope:',
            'input_age_label': 'Input Age:',
            'annotate_closest': 'Closest to',
            'annotate_selected': 'Selected Isotope:'
        }
    else:  # 한국어
        return {
            'input_age': '비교할 연대 입력:',
            'select_isotope': '동위원소 선택:',
            'scatter_plot_title': '동위원소 반감기의 산포도 및 주석',
            'half_life': '반감기 (년)',
            'isotope_index': '동위원소 인덱스',
            'closest': '입력된 연대에 가장 가까운 동위원소',
            'selected': '선택된 동위원소:',
            'input_age_label': '입력된 연대:',
            'annotate_closest': '입력된 연대에 가장 가까운 원',
            'annotate_selected': '선택된 동위원소:'
        }

# 방사성 동위원소 데이터 불러오기
isotope_data = load_isotope_data('radio_data.txt')

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

# 산포도 그리기
fig, ax = plt.subplots(figsize=(15, 6))
ax.scatter(range(len(half_lives)), half_lives, color='blue', label='Half-life')

# 1에 가장 가까운 동위원소에 화살표 추가
ax.annotate(f'{labels["annotate_closest"]} {input_age}: {nearest_isotope}', xy=(nearest_idx, half_lives[nearest_idx]),
            xytext=(nearest_idx, half_lives[nearest_idx] * 1.5),
            arrowprops=dict(facecolor='green', shrink=0.05))

# 선택된 동위원소의 반감기 강조
ax.scatter(selected_idx, selected_half_life, color='orange', label=f'{labels["annotate_selected"]} {selected_isotope}')
ax.axhline(y=input_age, color='gray', linestyle='--', label=f'{labels["input_age_label"]} {input_age}')

# 반감기 값은 로그 스케일로 표시 (큰 값들을 더 명확히 시각화하기 위해)
ax.set_yscale('log')

# 그래프 라벨 추가
ax.set_xlabel(labels['isotope_index'])
ax.set_ylabel(labels['half_life'])
ax.set_title(labels['scatter_plot_title'])

# 범례 추가
ax.legend()

# 그래프 출력
st.pyplot(fig)

# 결과 표시
st.write(f"{labels['closest']} : **{nearest_isotope}**")
st.write(f"{labels['selected']} **{selected_isotope}**")
st.write(f"선택된 동위원소의 반감기: **{selected_half_life}**")
