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

# 방사성 동위원소 데이터 불러오기
isotope_data = load_isotope_data('radio_data.txt')

# 입력 연대 (1에 가까운 값과 비교할 연대)
input_age = st.number_input('Enter a comparison age:', min_value=1, value=1)

# 반감기 값을 추출
half_lives = [item[1] for item in isotope_data]
isotope_names = [item[0] for item in isotope_data]

# 가장 1에 가까운 반감기 및 가장 큰 반감기 찾기
diffs = [abs(half_life - input_age) for half_life in half_lives]
nearest_idx = np.argmin(diffs)
farthest_idx = np.argmax(half_lives)

nearest_isotope = isotope_names[nearest_idx]
farthest_isotope = isotope_names[farthest_idx]

# 산포도 그리기
fig, ax = plt.subplots(figsize=(15, 6))
ax.scatter(range(len(half_lives)), half_lives, color='blue', label='Half-life')

# 1에 가장 가까운 동위원소에 화살표 추가
ax.annotate(f'Closest to {input_age}: {nearest_isotope}', xy=(nearest_idx, half_lives[nearest_idx]),
            xytext=(nearest_idx, half_lives[nearest_idx] * 1.5),
            arrowprops=dict(facecolor='green', shrink=0.05))

# 가장 먼 동위원소에 화살표 추가
ax.annotate(f'Farthest from {input_age}: {farthest_isotope}', xy=(farthest_idx, half_lives[farthest_idx]),
            xytext=(farthest_idx, half_lives[farthest_idx] / 1.5),
            arrowprops=dict(facecolor='red', shrink=0.05))

# 반감기 값은 로그 스케일로 표시 (큰 값들을 더 명확히 시각화하기 위해)
ax.set_yscale('log')

# 그래프 라벨 추가
ax.set_xlabel('Isotope Index')
ax.set_ylabel('Half-life (years)')
ax.set_title('Scatter plot of Isotope Half-lives with Annotations')

# 범례 추가
ax.legend()

# 그래프 출력
st.pyplot(fig)

# 결과 표시
st.write(f"Isotope closest to {input_age}: **{nearest_isotope}**")
st.write(f"Isotope farthest from {input_age}: **{farthest_isotope}**")
