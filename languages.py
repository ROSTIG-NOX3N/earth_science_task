def get_labels(language):
    if language == '한국어':
        return {
            # 기존 라벨...
            'section1_header': '섹션 1: 동위원소 산포도',
            'section2_header': '섹션 2: 챗봇',
            'input_age': '지질의 연대를 입력해주세요 (초 단위):',
            'select_isotope_name': '동위원소 이름을 선택해주세요:',
            'select_isotope_number': '동위원소 번호를 선택해주세요:',
            'scatter_plot_title': '동위원소 반감기 산포도',  # 그래프 내부는 영어로 고정되므로 이 라벨은 인터페이스에만 사용됩니다.
            'half_life': '반감기 (초)',
            'isotope_index': '동위원소 인덱스',
            'closest_to_age': '입력된 연대와 가장 가까운 동위원소',
            'selected_isotope': '선택된 동위원소',
            'plot_same_name': '동일한 이름의 동위원소 산포도 보기',
            'input_age_label': '입력 연대',
            'selected_half_life': '선택된 동위원소의 반감기',
            'nearest_isotope': '입력된 연대와 가장 가까운 동위원소',
            'half_life_seconds': '초 (반감기)',
            'nearest_to_one': '반감기가 1초에 가장 가까운 동위원소',
            'input_age_help': '동위원소를 비교할 연대(초 단위)를 입력하세요.',
            'seconds': '초',
            'isotope_not_found': '선택한 동위원소를 찾을 수 없습니다.',
            # 챗봇 라벨
            'chatbot_header': '챗봇',
            'error_message': '죄송합니다, 답변을 생성하는 데 실패했습니다.',
            'user': '사용자',
            'assistant': '어시스턴트',
            'question1': '질문 1',
            'question2': '질문 2',
            'question3': '질문 3',
            'paraphrases': {
                'question1': [
                    '동위원소를 활용한 지질의 연대측정은 어떻게 이루어져?',
                    '동위원소를 사용하여 지질 연대를 어떻게 측정하나요?',
                    '방사성 동위원소는 지질 시대를 결정하는 데 어떻게 사용되나요?'
                ],
                'question2': [
                    '동위원소를 활용한 지질의 연대측정을 할 때 동위원소를 왜 고정시키지 않을까?',
                    '지질 연대 측정 시 왜 특정 동위원소만 사용하지 않나요?',
                    '지질학에서 동위원소 선택은 왜 고정되어 있지 않나요?'
                ],
                'question3': [
                    '만약 지질의 연대를 모른다면 어떤 과정을 통해서 동위원소를 선택하고 연대를 측정할까?',
                    '지질 연대를 모를 때 어떤 동위원소를 선택하여 연대를 측정하나요?',
                    '연대 미상의 지질에 대해 동위원소 선택과 연대 측정은 어떻게 이루어지나요?'
                ]
            }
        }
    elif language == 'English':
        return {
            # Existing labels...
            'section1_header': 'Section 1: Isotope Scatter Plot',
            'section2_header': 'Section 2: Chatbot',
            'input_age': 'Enter a comparison age (in seconds):',
            'select_isotope_name': 'Select Isotope Name:',
            'select_isotope_number': 'Select Isotope Number:',
            'scatter_plot_title': 'Scatter plot of Isotope Half-lives',
            'half_life': 'Half-life (seconds)',
            'isotope_index': 'Isotope Index',
            'closest_to_age': 'Closest to input age',
            'selected_isotope': 'Selected Isotope',
            'plot_same_name': 'Plot Isotopes with the same name',
            'input_age_label': 'Input Age',
            'selected_half_life': 'Half-life of selected isotope',
            'nearest_isotope': 'Closest Isotope to Input Age',
            'half_life_seconds': 'seconds (Half-life)',
            'nearest_to_one': 'Isotope with Half-life closest to 1 second',
            'input_age_help': 'Please enter an age to compare isotopes (in seconds).',
            'seconds': 'seconds',
            'isotope_not_found': 'Selected isotope not found.',
            # Chatbot labels
            'chatbot_header': 'Chatbot',
            'error_message': 'Sorry, failed to generate a response.',
            'user': 'User',
            'assistant': 'Assistant',
            'question1': 'Question 1',
            'question2': 'Question 2',
            'question3': 'Question 3',
            'paraphrases': {
                'question1': [
                    'How is geological age dating done using isotopes?',
                    'How do we measure geological age using isotopes?',
                    'How are radioactive isotopes used to determine geological periods?'
                ],
                'question2': [
                    'Why don\'t we fix isotopes when measuring geological age?',
                    'Why don\'t we use only specific isotopes for geological dating?',
                    'Why is the choice of isotopes not fixed in geological age measurement?'
                ],
                'question3': [
                    'If we don\'t know the geological age, how do we choose isotopes and measure the age?',
                    'How do we select isotopes and measure age when the geological age is unknown?',
                    'How do geologists choose isotopes and determine age from samples with unknown ages?'
                ]
            }
        }
    elif language == '日本語':
        return {
            # 既存のラベル...
            'section1_header': 'セクション 1: 同位体の散布図',
            'section2_header': 'セクション 2: チャットボット',
            'input_age': '比較する年代を入力してください（秒単位）:',
            'select_isotope_name': '同位体名を選択してください:',
            'select_isotope_number': '同位体番号を選択してください:',
            'scatter_plot_title': '同位体の半減期の散布図',
            'half_life': '半減期 (秒)',
            'isotope_index': '同位体インデックス',
            'closest_to_age': '入力された年代に最も近い同位体',
            'selected_isotope': '選択された同位体',
            'plot_same_name': '同じ名前の同位体をプロットする',
            'input_age_label': '入力された年代',
            'selected_half_life': '選択された同位体の半減期',
            'nearest_isotope': '入力された年代に最も近い同位体',
            'half_life_seconds': '秒 (半減期)',
            'nearest_to_one': '半減期が1秒に最も近い同位体',
            'input_age_help': '同位体を比較するための年代（秒単位）を入力してください。',
            'seconds': '秒',
            'isotope_not_found': '選択した同位体が見つかりません。',
            # チャットボットのラベル
            'chatbot_header': 'チャットボット',
            'error_message': '申し訳ありませんが、応答の生成に失敗しました。',
            'user': 'ユーザー',
            'assistant': 'アシスタント',
            'question1': '質問 1',
            'question2': '質問 2',
            'question3': '質問 3',
            'paraphrases': {
                'question1': [
                    '同位体を利用した地質年代測定はどのように行われますか？',
                    '同位体を使って地質年代をどのように測定しますか？',
                    '放射性同位体は地質時代の決定にどのように使用されますか？'
                ],
                'question2': [
                    '同位体を用いた地質年代測定の際、なぜ同位体を固定しないのですか？',
                    '地質年代測定で特定の同位体のみを使用しないのはなぜですか？',
                    '地質学で同位体の選択が固定されていないのはなぜですか？'
                ],
                'question3': [
                    '地質年代がわからない場合、どのように同位体を選択し年代を測定しますか？',
                    '地質年代が不明なとき、同位体の選択と年代測定はどう行われますか？',
                    '地質学者は年代不明のサンプルからどのように同位体を選び年代を決定しますか？'
                ]
            }
        }
