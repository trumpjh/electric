import json

# 파싱된 문제 읽기
with open('parsed_problems_new.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# JavaScript 코드 생성
js_code = "problemsData['2025-2'] = {\n"
js_code += "    year: 2025,\n"
js_code += "    round: 2,\n"
js_code += "    title: '2025년도 제2회',\n"
js_code += "    subject: '전기기능사',\n"
js_code += "    problems: [\n"

for prob in data['problems']:
    js_code += "        {\n"
    js_code += f"            id: '2025-2-{prob['number']}',\n"
    js_code += f"            number: {prob['number']},\n"
    
    # 텍스트 정리
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
    explanation = prob.get('explanation', '').replace("'", "\\'")
    js_code += f"            explanation: '{explanation}'\n"
    js_code += "        },\n"

js_code += "    ]\n"
js_code += "};\n"

# 파일로 저장
with open('js_code_to_add.txt', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("✓ JavaScript 코드 생성 완료")
print(f"✓ 파일: js_code_to_add.txt")
print(f"\n생성된 코드 미리보기:\n")
print(js_code[:500] + "...\n")
