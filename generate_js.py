#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

# 파싱된 문제 읽기
with open('parsed_problems.json', 'r', encoding='utf-8') as f:
    problems = json.load(f)

# data.js에 추가할 JavaScript 코드 생성
js_code = "// 추가된 문제들\n"
js_code += "problemsData['2025-2'] = {\n"
js_code += "    year: 2025,\n"
js_code += "    round: 2,\n"
js_code += "    title: '2025년도 제2회',\n"
js_code += "    subject: '전기기능사',\n"
js_code += "    problems: [\n"

# 각 문제를 JavaScript 객체로 변환
for prob in problems:
    js_code += "        {\n"
    js_code += f"            id: '2025-2-{prob['number']}',\n"
    js_code += f"            number: {prob['number']},\n"
    
    # 텍스트 정리
    text = prob['text'].replace("'", "\\'")
    if len(text) > 100:
        text = text[:100] + "..."
    js_code += f"            text: '{text}',\n"
    
    js_code += f"            options: [\n"
    
    for i, opt in enumerate(prob['options']):
        opt_text = str(opt).replace("'", "\\'")
        js_code += f"                '{opt_text}',\n"
    
    js_code += f"            ],\n"
    js_code += f"            answer: {prob['answer']},\n"
    js_code += f"            category: '{prob['category']}',\n"
    js_code += f"            explanation: '설명 추가 필요'\n"
    js_code += "        },\n"

js_code += "    ]\n"
js_code += "};\n"

# 파일에 저장
with open('data_js_addition.txt', 'w', encoding='utf-8') as f:
    f.write(js_code)

print("생성된 JavaScript 코드 (data_js_addition.txt):")
print(js_code)
