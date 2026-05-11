#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
docx_precise_parsed.json을 data.js 형식으로 변환
- 정답 추출
- 보기 정제
- 카테고리 할당
"""

import json
import re

# JSON 읽기
with open('docx_precise_parsed.json', 'r', encoding='utf-8') as f:
    problems_data = json.load(f)

print("=" * 70)
print("🔄 JSON → JavaScript 형식 변환")
print("=" * 70)

# 카테고리 매핑 (각 문제별)
categories = [
    '전기설비',    # 1. 진동이 심한
    '전기설비',    # 2. 심벌
    '전기설비',    # 3. 접지시스템
    '전기기기',    # 4. 철심
    '전기이론',    # 5. 회로저항
    '전기이론',    # 6. 2전력계법
    '전기기기',    # 7. 변압기
    '전기이론',    # 8. 전위
    '전기기기',    # 9. 유도기
    '전기기기',    # 10. 유도기
    '전기설비',    # 11. 슬리브
    '전기기기',    # 12. 원선도
    '전기설비',    # 13. 가공전선
    '전기설비',    # 14. 금속몰드
    '전기기기',    # 15. 영구자석
]

# 이미지 매핑
image_mapping = {
    2: 'problem_images/image1.png'  # 문제 2: EQ 기호
}

def extract_answer(text):
    """텍스트에서 정답 추출 (? 뒤의 ①②③④)"""
    match = re.search(r'\?\s*([①②③④])', text)
    if match:
        answer_char = match.group(1)
        answer_map = {'①': 1, '②': 2, '③': 3, '④': 4}
        return answer_map.get(answer_char, 1)
    return 1

def parse_options(options_str):
    """보기 문자열을 분리하여 리스트로 변환"""
    result = []
    
    # 이미 4개 이상이 리스트로 분리된 경우
    if isinstance(options_str, list) and len(options_str) > 0:
        # 첫 번째 항목만 사용 (혼합된 경우)
        options_str = options_str[0] if len(options_str) == 1 else ' '.join(options_str)
    
    # 패턴 1: "①... ②... ③... ④..." (번호 포함)
    pattern1 = r'[①②③④]\s*([^①②③④]+?)(?=[①②③④]|$)'
    matches1 = re.findall(pattern1, options_str)
    
    if len(matches1) >= 4:
        result = [m.strip() for m in matches1[:4]]
    else:
        # 패턴 2: 첫 번째만 번호 없음 "... ②... ③... ④..."
        # "단독접지 ②공통접지 ③통합접지 ④보호접지" 같은 경우
        if '①' not in options_str:
            # 첫 항목을 찾기: 첫 ②까지
            first_idx = options_str.find('②')
            if first_idx > 0:
                first_item = options_str[:first_idx].strip()
                remaining = options_str[first_idx:]
                matches2 = re.findall(r'[②③④]\s*([^②③④]+?)(?=[②③④]|$)', remaining)
                result = [first_item] + [m.strip() for m in matches2[:3]]
        else:
            # 일반적인 경우
            matches2 = re.findall(r'[①②③④]\s*([^①②③④]+?)(?=[①②③④]|$)', options_str)
            result = [m.strip() for m in matches2[:4]]
    
    # 4개가 될 때까지 빈 항목 추가
    while len(result) < 4:
        result.append('')
    
    return result[:4]

# JavaScript 코드 생성
js_code = "const problemsData = {\n"
js_code += "    '2025-1': {\n"
js_code += "        year: 2025,\n"
js_code += "        round: 1,\n"
js_code += "        title: '2025년도 제1회',\n"
js_code += "        subject: '전기기능사',\n"
js_code += "        problems: [\n"

for i, prob in enumerate(problems_data, 1):
    # 정답 추출
    answer = extract_answer(prob['text'])
    
    # 보기 파싱
    options_text = prob['options'][0] if prob['options'] else ""
    options = parse_options(options_text)
    
    # 카테고리
    category = categories[i-1] if i <= len(categories) else '전기이론'
    
    # 이미지
    image = f"'problem_images/image1.png'" if i == 2 else "null"
    
    # 설명 정리 (너무 길면 자르기)
    explanation = prob['explanation'].replace("'", "\\'").replace("\n", " ")
    
    # JavaScript 객체 생성
    js_code += f"            {{\n"
    js_code += f"                id: '2025-1-{i}',\n"
    js_code += f"                number: {i},\n"
    
    # 텍스트 정리
    text_clean = prob['text'].replace("'", "\\'").replace("[", "(").replace("]", ")")
    js_code += f"                text: '{text_clean}',\n"
    js_code += f"                options: [\n"
    
    for opt in options:
        opt_clean = opt.replace("'", "\\'").strip()
        js_code += f"                    '{opt_clean}',\n"
    
    js_code += f"                ],\n"
    js_code += f"                answer: {answer},\n"
    js_code += f"                category: '{category}',\n"
    js_code += f"                explanation: '{explanation}',\n"
    js_code += f"                image: {image}\n"
    js_code += f"            }},\n"

js_code += "        ]\n"
js_code += "    },\n"
js_code += "    '2025-2': {\n"
js_code += "        year: 2025,\n"
js_code += "        round: 2,\n"
js_code += "        title: '2025년도 제2회',\n"
js_code += "        subject: '전기기능사',\n"
js_code += "        problems: []\n"
js_code += "    },\n"
js_code += "    // 다른 연도/회차는 계속...\n"
js_code += "};\n"

# 파일 저장
output_file = "data_js_15problems.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(js_code)

print(f"\n✅ JavaScript 코드 생성 완료!")
print(f"💾 파일: {output_file}")
print(f"\n📊 생성 통계:")
print(f"  - 총 문제: {len(problems_data)}개")
print(f"  - 정답 분포: ", end="")

answer_count = {}
for i, prob in enumerate(problems_data, 1):
    answer = extract_answer(prob['text'])
    answer_count[answer] = answer_count.get(answer, 0) + 1

for ans in [1, 2, 3, 4]:
    print(f"{ans}번: {answer_count.get(ans, 0)}개", end="  ")
print()

# 샘플 출력
print("\n" + "=" * 70)
print("📝 생성된 문제 샘플 (문제 1, 2)")
print("=" * 70)
print(js_code[:1500])
print("\n... (계속)")

