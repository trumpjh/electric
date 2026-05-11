from docx import Document
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import re
import json
import os

# 출력 디렉토리 생성
os.makedirs('problem_images', exist_ok=True)

# DOCX 파일 열기
doc = Document('전기기능사 시험문제(2025-2023).docx')

print("=" * 80)
print("DOCX 파일 그림 및 문제 추출")
print("=" * 80)

# 모든 단락 추출
paragraphs = []
for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    has_image = any(run._element.xpath('.//pic:pic') for run in para.runs)
    
    if text or has_image:
        paragraphs.append({
            'index': i,
            'text': text,
            'has_image': has_image
        })

# 그림 추출
def extract_images_from_docx():
    """DOCX에서 이미지 추출"""
    image_count = 0
    from zipfile import ZipFile
    
    with ZipFile('전기기능사 시험문제(2025-2023).docx') as zip_ref:
        # media 폴더의 이미지 파일 추출
        for file_info in zip_ref.filelist:
            if file_info.filename.startswith('word/media/'):
                image_data = zip_ref.read(file_info.filename)
                # 파일명 추출
                filename = os.path.basename(file_info.filename)
                output_path = f'problem_images/{filename}'
                
                with open(output_path, 'wb') as f:
                    f.write(image_data)
                
                print(f"✓ 그림 추출: {output_path} ({len(image_data)} bytes)")
                image_count += 1
    
    return image_count

image_count = extract_images_from_docx()
print(f"\n총 {image_count}개 그림 추출됨\n")

# 문제 파싱 로직
print("=" * 80)
print("문제 파싱 시작")
print("=" * 80)

problems = []
i = 0
problem_num = 1

while i < len(paragraphs):
    para = paragraphs[i]
    
    # 문제 찾기 (? 포함하고 정답 기호 포함)
    if '?' in para['text']:
        question = para['text']
        
        # 정답 추출 (①②③④)
        answer_match = re.search(r'[①②③④]', question)
        if answer_match:
            answer_char = answer_match.group()
            answer_num = {'①': 1, '②': 2, '③': 3, '④': 4}[answer_char]
            question = question[:answer_match.start()].strip()
        else:
            answer_num = 1
        
        # 그림 확인
        image_filename = None
        if para['has_image']:
            print(f"🖼️ 문제 {problem_num}: 그림 포함")
            # 다음 단락이 선택지일 가능성이 높음
        
        # 선택지 찾기 (다음 단락)
        options = []
        options_idx = i + 1
        
        # 그림이 있으면 그 다음 단락이 선택지
        if para['has_image'] and options_idx < len(paragraphs):
            options_idx = i + 1
        
        if options_idx < len(paragraphs):
            options_para = paragraphs[options_idx]
            if '①' in options_para['text']:
                # 선택지 분리
                options_text = options_para['text']
                options = re.split(r'[①②③④]', options_text)
                options = [opt.strip() for opt in options if opt.strip()]
                options = options[:4]
        
        # 단원 찾기
        category = '전기이론'
        explanation = ''
        
        # 선택지 이후로 몇 칸 찾기
        search_idx = options_idx + 1
        while search_idx < len(paragraphs) and search_idx < options_idx + 10:
            p = paragraphs[search_idx]
            if 'CHAPTER' in p['text']:
                if '전기설비' in p['text']:
                    category = '전기설비'
                elif '전기기기' in p['text']:
                    category = '전기기기'
                elif '전기이론' in p['text']:
                    category = '전기이론'
                break
            search_idx += 1
        
        # 설명 찾기
        if search_idx < len(paragraphs):
            explanation = paragraphs[search_idx]['text']
        
        # 문제 객체 생성
        if len(options) >= 4:
            problem = {
                'number': problem_num,
                'text': question,
                'options': options,
                'answer': answer_num,
                'category': category,
                'explanation': explanation,
                'image': image_filename
            }
            problems.append(problem)
            problem_num += 1
            print(f"✓ 문제 {len(problems)}: {question[:40]}... (정답: {answer_num}번, {category})")
        
        i = search_idx + 2
    else:
        i += 1

# JSON으로 저장
output = {
    'total': len(problems),
    'year': 2025,
    'round': 1,
    'problems': problems
}

with open('parsed_problems_complete.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n✓ 총 {len(problems)}개 문제 파싱 완료")
print(f"✓ 결과: 'parsed_problems_complete.json' 저장됨")
