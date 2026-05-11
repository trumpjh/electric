from docx import Document
import re
import json

# DOCX 파일 열기
doc = Document('전기기능사 시험문제(2025-2023).docx')

print("=" * 80)
print("2025년도 제1회 문제 파싱 (15개)")
print("=" * 80)

# 모든 단락을 인덱스와 함께 저장
all_paras = []
for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    has_image = any(run._element.xpath('.//pic:pic') for run in para.runs)
    all_paras.append({
        'index': i,
        'text': text,
        'has_image': has_image
    })

print(f"\n총 {len(all_paras)}개 단락 추출됨")

# 문제 찾기 (? 포함하고 ①②③④ 포함)
problem_indices = []
for i, para in enumerate(all_paras):
    if '?' in para['text'] and any(c in para['text'] for c in '①②③④'):
        problem_indices.append(i)
        
print(f"문제로 추정되는 단락: {len(problem_indices)}개")
print(f"인덱스: {problem_indices}\n")

# 각 문제마다 필요한 정보 추출
problems = []

for problem_idx in problem_indices:
    para = all_paras[problem_idx]
    question = para['text']
    has_image = para['has_image']
    
    # 정답 추출
    answer_match = re.search(r'[①②③④]', question)
    if answer_match:
        answer_char = answer_match.group()
        answer_num = {'①': 1, '②': 2, '③': 3, '④': 4}[answer_char]
        question = question[:answer_match.start()].strip()
    else:
        answer_num = 1
    
    # 선택지 찾기
    options = []
    options_idx = None
    
    # 문제 다음 단락들에서 선택지 찾기
    for j in range(problem_idx + 1, min(problem_idx + 10, len(all_paras))):
        p = all_paras[j]
        if not p['text']:  # 빈 줄 스킵
            continue
        if re.match(r'^[①②③④]', p['text']) or re.search(r'[①②③④]', p['text']):
            # 선택지로 추정
            options_text = p['text']
            options = re.split(r'[①②③④]', options_text)
            options = [opt.strip() for opt in options if opt.strip()]
            options_idx = j
            break
    
    # 단원과 설명 찾기
    category = '전기이론'  # 기본값
    explanation = ''
    
    if options_idx:
        for j in range(options_idx + 1, min(options_idx + 10, len(all_paras))):
            p = all_paras[j]
            if 'CHAPTER' in p['text']:
                if '전기설비' in p['text']:
                    category = '전기설비'
                elif '전기기기' in p['text']:
                    category = '전기기기'
                elif '전기이론' in p['text']:
                    category = '전기이론'
                
                # 다음 단락이 설명
                if j + 1 < len(all_paras):
                    explanation = all_paras[j + 1]['text']
                break
    
    # 선택지가 4개 이상이면 저장
    if len(options) >= 4:
        problem = {
            'number': len(problems) + 1,
            'text': question,
            'options': options[:4],
            'answer': answer_num,
            'category': category,
            'explanation': explanation,
            'has_image': has_image
        }
        problems.append(problem)
        
        image_mark = " 🖼️" if has_image else ""
        print(f"✓ 문제 {problem['number']}: {question[:50]}...{image_mark}")
        print(f"  선택지: {len(problem['options'])}개, 정답: {answer_num}번, {category}")

print(f"\n" + "=" * 80)
print(f"✓ 총 {len(problems)}개 문제 파싱 완료")

# JSON으로 저장
output = {
    'total': len(problems),
    'year': 2025,
    'round': 1,
    'title': '2025년도 제1회',
    'problems': problems
}

with open('docx_2025_1_complete.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"✓ 결과: 'docx_2025_1_complete.json' 저장됨")
