#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json

with open('full_text.txt', 'r', encoding='utf-8') as f:
    full_text = f.read()

# "설명)"으로 분할
blocks = full_text.split('설명)')

problems = []
problem_number = 1

# 각 블록 처리
for i in range(0, len(blocks) - 1, 2):
    problem_block = blocks[i].strip()
    explanation_block = blocks[i + 1].strip() if i + 1 < len(blocks) else ""
    
    if not problem_block or len(problem_block) < 10:
        continue
    
    # 문제 블록에서 마지막 "?"와 정답 기호 찾기
    last_question = problem_block.rfind('?')
    if last_question == -1:
        continue
    
    # "?"  뒤의 부분에서 정답 기호 찾기
    after_question = problem_block[last_question + 1:]
    answer_match = re.search(r'[①②③④]', after_question)
    
    if not answer_match:
        continue
    
    correct_answer_char = answer_match.group()
    answer_pos = last_question + 1 + answer_match.start()
    
    # 문제 텍스트: 처음부터 "?"까지
    question_text = problem_block[:last_question + 1].strip()
    
    # 선택지: 정답 기호 뒤의 모든 텍스트
    options_text = problem_block[answer_pos + 1:].strip()
    
    # ①②③④로 구분된 선택지 추출
    option_parts = re.split(r'[①②③④]', options_text)
    options = [opt.strip() for opt in option_parts[1:] if opt.strip()]
    
    if len(options) < 4:
        continue
    
    options = options[:4]
    
    # 카테고리 추출
    category_match = re.search(r'(전기설비|전기기기|전기이론|전기안전)', explanation_block)
    category = category_match.group(1) if category_match else "전기설비"
    
    # 설명 추출 (CHAPTER 이전까지)
    chapter_pos = explanation_block.find('CHAPTER')
    if chapter_pos != -1:
        explanation = explanation_block[:chapter_pos].strip()
    else:
        # CHAPTER가 없으면 첫 200자까지
        explanation = explanation_block[:200].strip()
    
    # 정답 숫자로 변환
    answer_map = {'①': 1, '②': 2, '③': 3, '④': 4}
    correct_answer = answer_map.get(correct_answer_char, 1)
    
    problem = {
        'id': f'2025-1-{problem_number}',
        'number': problem_number,
        'text': question_text,
        'options': options,
        'answer': correct_answer,
        'category': category,
        'explanation': explanation
    }
    
    problems.append(problem)
    problem_number += 1

# 결과 출력
print(f"총 {len(problems)}개 문제 파싱됨\n")
for prob in problems:
    print(f"문제 {prob['number']}: {prob['text']}")
    print(f"  카테고리: {prob['category']}, 정답: {prob['answer']}번")
    print(f"  선택지: {', '.join(prob['options'][:2])}...")
    print()

# JSON 저장
with open('parsed_problems.json', 'w', encoding='utf-8') as f:
    json.dump(problems, f, ensure_ascii=False, indent=2)

print(f"\n파싱 완료: {len(problems)}개 문제")
print("파일: parsed_problems.json")
