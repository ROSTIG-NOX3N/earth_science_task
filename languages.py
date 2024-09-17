def get_labels(language):
    if language == '한국어':
        return {
            'section1_header': '산포도 그래프',
            'section2_header': '챗봇',
            'select_mode': '모드를 선택하세요:',
            'default_mode': '사용자 기본 설정',
            'light_mode': '라이트 모드',
            'start_chatbot': '챗봇 시작하기(답변이 안나와도 누르세요)',
            'dark_mode': '다크 모드',
            'input_age': '비교할 연대 입력:',
            'select_time_unit': '단위를 선택하세요:',
            'select_isotope_name': '동위원소 이름을 선택해주세요:',
            'select_isotope_number': '동위원소 번호를 선택해주세요:',
            'isotope_not_found': '선택한 동위원소를 찾을 수 없습니다.',
            'select_tab': '탭을 선택하세요:',
            'chatbot_header': '챗봇',
            'error_message': '죄송합니다, 답변을 생성하는 데 실패했습니다.',
            'user': '사용자',
            'assistant': '어시스턴트',
            'question1': '방사성 동위원소를 활용하여 연대측정을 하는 방법이 궁금해요',
            'question2': '방사성 동위원소를 활용하여 연대측정을 할 때 왜 동위원소를 고정해서 사용하지 않을까요',
            'question3': '특정 지질의 연대를 모를때는 어떻게 연대측정을 하는건가요',
            'error_load_data': '데이터를 불러오는 데 실패했습니다.',
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
            },
            'free_question_label': '자유 질문을 입력하세요:',
            'ask_button': '질문하기',
            'mother_ratio_1s': '모원소 비율 (1초)',
            'daughter_ratio_1s': '자원소 비율 (1초)',
            'mother_ratio': '모원소 비율 (%)',
            'daughter_ratio': '자원소 비율 (%)',
            'mother_ratio_1s_label': '모원소 비율 (1초)',
            'daughter_ratio_1s_label': '자원소 비율 (1초)',
            'mother_daughter_graph_title': '모자원소 그래프',
            'time_seconds': '시간 (초)',
            'isotope_ratio_percent': '동위원소 비율 (%)',
            'positive_age_warning': '양의 값을 입력해 주세요.'
        }
    elif language == 'English':
        return {
            'section1_header': 'Scatter Plot',
            'section2_header': 'Chatbot',
            'select_mode': 'Select mode:',
            'default_mode': 'Default mode',
            'light_mode': 'Light mode',
            'start_chatbot': 'Start Chatbot (Please press even if there is no answer)',
            'dark_mode': 'Dark mode',
            'input_age': 'Enter a comparison age:',
            'select_time_unit': 'Select time unit:',
            'select_isotope_name': 'Select Isotope Name:',
            'select_isotope_number': 'Select Isotope Number:',
            'isotope_not_found': 'Selected isotope not found.',
            'select_tab': 'Select tab:',
            'chatbot_header': 'Chatbot',
            'error_message': 'Sorry, failed to generate a response.',
            'user': 'User',
            'assistant': 'Assistant',
            'question1': 'I am curious about how we use radioactive isotopes to date geological samples.',
            'question2': 'Why don’t we fix isotopes when using them for dating purposes?',
            'question3': 'How do we date geological samples when we don’t know their specific age?',
            'error_load_data': 'Failed to load data.',
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
            },
            'free_question_label': 'Enter your question:',
            'ask_button': 'Ask',
            'mother_ratio_1s': 'Mother Isotope Ratio at 1 second',
            'daughter_ratio_1s': 'Daughter Isotope Ratio at 1 second',
            'mother_ratio': 'Mother Isotope Ratio (%)',
            'daughter_ratio': 'Daughter Isotope Ratio (%)',
            'mother_ratio_1s_label': 'Mother Isotope Ratio at 1 second',
            'daughter_ratio_1s_label': 'Daughter Isotope Ratio at 1 second',
            'mother_daughter_graph_title': 'Mother-Daughter Graph',
            'time_seconds': 'Time (seconds)',
            'isotope_ratio_percent': 'Isotope Ratio (%)',
            'positive_age_warning': 'Please enter a positive value.'
        }
    elif language == '日本語':
        return {
            'section1_header': '散布図',
            'section2_header': 'チャットボット',
            'select_mode': 'モードを選択してください:',
            'default_mode': 'デフォルトモード',
            'light_mode': 'ライトモード',
            'start_chatbot': 'チャットボットを開始します（回答が出なくても押してください）',
            'dark_mode': 'ダークモード',
            'input_age': '比較する年代を入力してください:',
            'select_time_unit': '単位を選択してください:',
            'select_isotope_name': '同位体名を選択してください:',
            'select_isotope_number': '同位体番号を選択してください:',
            'isotope_not_found': '選択した同位体が見つかりません。',
            'select_tab': 'タブを選択してください:',
            'chatbot_header': 'チャットボット',
            'error_message': '申し訳ありませんが、応答の生成に失敗しました。',
            'user': 'ユーザー',
            'assistant': 'アシスタント',
            'question1': '放射性同位体を使って年代測定をする方法について知りたいです',
            'question2': 'なぜ放射性同位体を使って年代測定する際に同位体を固定して使用しないのでしょうか？',
            'question3': '特定の地質の年代が不明な場合、どのようにして年代測定を行うのですか？',
            'error_load_data': 'データの読み込みに失敗しました。',
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
            },
            'free_question_label': '自由質問を入力してください:',
            'ask_button': '質問する',
            'mother_ratio_1s': 'モ原子比率 (1秒)',
            'daughter_ratio_1s': '子原子比率 (1秒)',
            'mother_ratio': 'モ原子比率 (%)',
            'daughter_ratio': '子原子比率 (%)',
            'mother_ratio_1s_label': 'モ原子比率 (1秒)',
            'daughter_ratio_1s_label': '子原子比率 (1秒)',
            'mother_daughter_graph_title': 'モ子原子グラフ',
            'time_seconds': '時間 (秒)',
            'isotope_ratio_percent': '同位体比率 (%)',
            'positive_age_warning': '正の値を入力してください。'
        }
    else:
        return {}
