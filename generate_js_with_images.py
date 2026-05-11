import json

# 파싱된 문제 읽기
with open('docx_2025_1_complete.json', 'r', encoding='utf-8') as f:
    parsed_data = json.load(f)

# 이미지 매핑 (문제 번호별)
image_mapping = {
    2: 'problem_images/image2.png'  # 문제 2에 그림 있음
}

# JavaScript 코드 생성
js_code = "problemsData['2025-1'] = {\n"
js_code += "    year: 2025,\n"
js_code += "    round: 1,\n"
js_code += "    title: '2025년도 제1회',\n"
js_code += "    subject: '전기기능사',\n"
js_code += "    problems: [\n"

for prob in parsed_data['problems']:
    js_code += "        {\n"
    js_code += f"            id: '2025-1-{prob['number']}',\n"
    js_code += f"            number: {prob['number']},\n"
    
    # 텍스트
    text = prob['text'].replace("'", "\\'")
    js_code += f"            text: '{text}',\n"
    
    # 선택지
    js_code += "            options: [\n"
    for opt in prob['options']:
        opt_text = str(opt).replace("'", "\\'")
        js_code += f"                '{opt_text}',\n"
    js_code += "            ],\n"
    
    # 정답
    js_code += f"            answer: {prob['answer']},\n"
    
    # 단원
    js_code += f"            category: '{prob['category']}',\n"
    
    # 설명
    explanation = prob['explanation'].replace("'", "\\'")
    js_code += f"            explanation: '{explanation}',\n"
    
    # 그림
    if prob['number'] in image_mapping:
        image_path = image_mapping[prob['number']]
        js_code += f"            image: '{image_path}'\n"
    else:
        js_code += f"            image: null\n"
    
    js_code += "        },\n"

js_code += "    ]\n"
js_code += "};\n"

# 파일로 저장
with open('data_js_2025_1_updated.txt', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("✓ JavaScript 코드 생성 완료")
print(f"✓ 파일: data_js_2025_1_updated.txt")
print(f"✓ 포함된 문제: {len(parsed_data['problems'])}개")
print(f"✓ 그림 포함 문제: {sum(1 for p in parsed_data['problems'] if p['number'] in image_mapping)}개")
