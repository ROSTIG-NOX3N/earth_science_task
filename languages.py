def get_labels(language):
    if language == 'English':
        return {
            'input_age': 'Enter a comparison age:',
            'select_isotope': 'Select an isotope:',
            'closest': 'Closest to',
            'selected': 'Selected Isotope:',
            'input_age_label': 'Input Age:',
            'annotate_closest': 'Closest to',
            'annotate_selected': 'Selected Isotope:',
            'half_life_of_selected_isotope': 'Half-life of selected isotope'
        }
    elif language == '한국어':
        return {
            'input_age': '지질의 연대를 입력해주세요:',
            'select_isotope': '동위원소를 선택해주세요:',
            'closest': '가장 가까운 동위원소',
            'selected': '선택된 동위원소:',
            'input_age_label': '입력된 연대:',
            'annotate_closest': '가장 가까운 동위원소',
            'annotate_selected': '선택된 동위원소',
            'half_life_of_selected_isotope': '선택된 동위원소의 반감기(년)'
        }
