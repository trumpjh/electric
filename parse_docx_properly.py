from docx import Document
import re
import json

# DOCX 파일 열기
doc = Document('전기기능사 시험문제(2025-2023).docx')

# 모든 단락 추출
paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]

# 문제 파싱
problems = []
problem_num = 1
i = 0

while i < len(paragraphs):
    para = paragraphs[i]
    
    # "문제"를 포함하고 "?"를 포함한 단락 찾기
    if '문제' in para or '?' in para:
        question = para
        # 정답 추출 (①②③④ 중 하나)
        answer_match = re.search(r'[①②③④]', question)
        if answer_match:
            answer_char = answer_match.group()
            answer_num = {'①': 1, '②': 2, '③': 3, '④': 4}[answer_char]
            # 정답 기호를 제거한 질문
            question = question[:answer_match.start()]
        else:
            answer_num = 1  # 기본값
        
        # 다음 단락이 선택지인지 확인
        if i + 1 < len(paragraphs):
            options_para = paragraphs[i + 1]
            # ①②③④로 시작하는지 확인
            if '①' in options_para and '②' in options_para:
                # 선택지 분리
                options = re.split(r'[①②③④]', options_para)
                options = [opt.strip() for opt in options if opt.strip()]
                
                # 설명 찾기
                explanation = ''
                if i + 2 < len(paragraphs) and '설명)' in paragraphs[i + 2]:
                    explanation = paragraphs[i + 2]
                
                # 카테고리 추출
                category = '전기이론'  # 기본값
                if '전기설비' in explanation:
                    category = '전기설비'
                elif '전기기기' in explanation:
                    category = '전기기기'
                elif '전기이론' in explanation:
                    category = '전기이론'
                
                problem = {
                    'number': problem_num,
                    'text': question.strip(),
                    'options': options[:4] if len(options) >= 4 else options,
                    'answer': answer_num,
                    'category': category,
                    'explanation': explanation
                }
                problems.append(problem)
                problem_num += 1
                i += 3
                continue
        
        i += 1
    else:
        i += 1

# JSON으로 저장
output = {
    'total': len(problems),
    'problems': problems
}

with open('parsed_problems_new.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"✓ 총 {len(problems)}개 문제 파싱됨\n")
for p in problems[:3]:
    print(f"문제 {p['number']}: {p['text'][:50]}...")
    print(f"  선택지: {p['options']}")
    print(f"  정답: {p['answer']}번")
    print(f"  단원: {p['category']}")
    print()

print(f"결과: 'parsed_problems_new.json' 저장됨")
