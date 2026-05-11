#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re

# 파싱된 문제 읽기
with open('parsed_problems.json', 'r', encoding='utf-8') as f:
    problems = json.load(f)

# 문제 텍스트 정리
for prob in problems:
    text = prob['text']
    
    # "2025년도 제1회 문제" 같은 접두사 제거
    text = re.sub(r'^.*?문제', '', text)
    
    # CHAPTER 이전의 불필요한 내용 제거 (설명 부분)
    if 'CHAPTER' in text:
        text = text[text.find('?'):]  # "?"부터 시작하도록
    
    # 문장 끝의 "?"만 남기기
    question_match = re.search(r'([^?]*\?)', text)
    if question_match:
        text = question_match.group(1)
    
    text = text.strip()
    
    # "진동이 심한" 같은 이중 단어 정리
    text = re.sub(r'(.)\1+', r'\1', text)
    
    prob['text'] = text

# 결과 확인
print("정리된 문제들:\n")
for prob in problems:
    print(f"문제 {prob['number']}: {prob['text']}")
    print(f"  카테고리: {prob['category']}")
    print(f"  정답: {prob['answer']}번")
    print()

# 수정된 JSON 저장
with open('parsed_problems_cleaned.json', 'w', encoding='utf-8') as f:
    json.dump(problems, f, ensure_ascii=False, indent=2)

print(f"정리된 문제가 'parsed_problems_cleaned.json'으로 저장되었습니다")
