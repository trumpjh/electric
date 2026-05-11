import json

# 파싱된 문제 읽기
with open('docx_2025_1_complete.json', 'r', encoding='utf-8') as f:
    parsed_data = json.load(f)

# 이미지 매핑 (문제 ID 기반)
image_mapping = {
    '2025-1-2': 'problem_images/image2.png'
}

# JavaScript 객체 내용만 생성 (2025-1 problems 배열)
problems_js = "problems: [\n"

for prob in parsed_data['problems']:
    problems_js += "            {\n"
    problems_js += f"                id: '2025-1-{prob['number']}',\n"
    problems_js += f"                number: {prob['number']},\n"
    
    # 텍스트
    text = prob['text'].replace("'", "\\'")
    problems_js += f"                text: '{text}',\n"
    
    # 선택지
    problems_js += "                options: [\n"
    for opt in prob['options']:
        opt_text = str(opt).replace("'", "\\'")
        problems_js += f"                    '{opt_text}',\n"
    problems_js += "                ],\n"
    
    # 정답
    problems_js += f"                answer: {prob['answer']},\n"
    
    # 단원
    problems_js += f"                category: '{prob['category']}',\n"
    
    # 설명
    explanation = prob['explanation'].replace("'", "\\'")
    problems_js += f"                explanation: '{explanation}',\n"
    
    # 그림 (ID 기반)
    prob_id = f"2025-1-{prob['number']}"
    if prob_id in image_mapping:
        problems_js += f"                image: '{image_mapping[prob_id]}'\n"
    else:
        problems_js += f"                image: null\n"
    
    problems_js += "            },\n"

problems_js += "        ]\n"

# 파일로 저장
with open('2025_1_problems_only.txt', 'w', encoding='utf-8') as f:
    f.write(problems_js)

print("✓ 2025-1 problems 배열만 생성 완료")
print(f"✓ 파일: 2025_1_problems_only.txt")
print(f"✓ 포함된 문제: {len(parsed_data['problems'])}개")
