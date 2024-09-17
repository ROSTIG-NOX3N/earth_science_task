# --- 모원소-자원소 그래프 그리기 ---
if selected_tab == 'Mother-Daughter Isotope':  # 새로운 탭 추가

    st.header('모원소와 자원소의 변화 그래프')

    # 선택된 동위원소의 반감기를 사용
    selected_half_life = isotope_data[selected_idx][2]  # 선택된 동위원소의 반감기

    # 붕괴 상수 계산 (λ = ln(2) / 반감기)
    decay_constant = np.log(2) / selected_half_life

    # 시간 범위 설정 (입력된 연대를 기준으로 0에서 입력된 연대까지)
    time = np.linspace(0, input_age_seconds, 500)

    # 모원소의 양 계산
    mother_isotope = initial_mother_isotope * np.exp(-decay_constant * time)

    # 자원소의 양 계산 (자원소는 모원소의 감소량만큼 증가)
    daughter_isotope = initial_mother_isotope - mother_isotope

    # --- 그래프 그리기 ---
    fig, ax = plt.subplots(figsize=(10, 6))

    # 모원소의 양 그래프
    ax.plot(time, mother_isotope, label='Mother Isotope', color='blue')

    # 자원소의 양 그래프
    ax.plot(time, daughter_isotope, label='Daughter Isotope', color='red')

    # 그래프 설정
    ax.set_title(f'Amount of Mother and Daughter Isotopes over Time for {selected_isotope}')
    ax.set_xlabel('Time (seconds)' if time_unit == 'seconds' else 'Time (years)')
    ax.set_ylabel('Isotope Amount')
    ax.grid(True)
    ax.legend()

    # 그래프 출력
    st.pyplot(fig)
