def get_labels(language):
    # 모든 그래프 내부 라벨은 영어로만 고정
    return {
        'input_age': 'Enter a comparison age:' if language == 'English' else '지질의 연대를 입력해주세요:',
        'select_isotope': 'Select an isotope:' if language == 'English' else '동위원소를 선택해주세요:',
        'scatter_plot_title': 'Scatter plot of Isotope Half-lives',  # 영어 고정
        'histogram_title': 'Histogram of 100 Closest Isotope Half-lives to Input Age',  # 영어 고정
        'scatter_around_title': 'Scatter plot of 100 Closest Isotopes to Selected Isotope',  # 영어 고정
        'half_life': 'Half-life (years)',  # 영어 고정
        'isotope_index': 'Isotope Index',  # 영어 고정
        'closest': 'Closest to',
        'selected': 'Selected Isotope:',
        'input_age_label': 'Input Age:',
        'annotate_closest': 'Closest to',
        'annotate_selected': 'Selected Isotope:',
        'half_life_of_selected_isotope': 'Half-life of selected isotope'
    }
