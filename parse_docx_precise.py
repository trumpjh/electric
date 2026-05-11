#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
고정밀 DOCX 파싱 (수학 공식 포함)
- oMath 요소 추출
- 모든 문제 정확히 분리
- 보기와 설명 정확히 매칭
"""

import zipfile
import xml.etree.ElementTree as ET
import json
import re
from collections import defaultdict

docx_path = "전기기능사 시험문제(2025-2023).docx"

print("=" * 70)
print("🔬 고정밀 DOCX 파싱 (수학 공식 + 이미지 포함)")
print("=" * 70)

try:
    with zipfile.ZipFile(docx_path, 'r') as docx_zip:
        doc_xml = docx_zip.read('word/document.xml').decode('utf-8')
    
    # XML 파싱
    root = ET.fromstring(doc_xml)
    
    # 네임스페이스
    ns = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
        'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
    }
    
    # 모든 paragraph 추출
    paragraphs = root.findall('.//w:p', ns)
    
    def extract_para_content(para):
        """paragraph에서 텍스트, 수학공식, 그림 추출"""
        content = {
            'text': '',
            'has_math': False,
            'has_image': False,
            'math_count': 0,
            'image_count': 0
        }
        
        # 텍스트 추출
        for text_elem in para.findall('.//w:t', ns):
            if text_elem.text:
                content['text'] += text_elem.text
        
        # 수학 공식 확인
        math_elements = para.findall('.//m:oMath', ns)
        if math_elements:
            content['has_math'] = True
            content['math_count'] = len(math_elements)
            # 수학 공식을 [수식] 로 표시
            for _ in math_elements:
                content['text'] += ' [수식] '
        
        # 그림 확인
        pic_elements = para.findall('.//pic:pic', ns)
        if pic_elements:
            content['has_image'] = True
            content['image_count'] = len(pic_elements)
        
        return content
    
    # 모든 문제 추출
    print(f"\n📝 총 {len(paragraphs)}개 paragraph 분석 중...")
    
    problems = []
    current_problem = None
    
    for i, para in enumerate(paragraphs):
        content = extract_para_content(para)
        text = content['text'].strip()
        
        if not text:
            continue
        
        # 새 문제 시작 패턴: "문제내용? ④" 같은 형태
        if '?' in text and any(c in text for c in '①②③④'):
            if current_problem:
                problems.append(current_problem)
            current_problem = {
                'text': text,
                'options': [],
                'answer_indicator': re.search(r'[①②③④]', text),
                'has_image': content['has_image'],
                'has_math': content['has_math'],
                'math_count': content['math_count'],
                'image_count': content['image_count'],
                'para_index': i
            }
        
        # 보기 추출: "①...②...③...④..."
        elif current_problem and any(c in text for c in '①②③④'):
            # 선택지로 보기
            if len(text) < 200:  # 너무 길면 설명일 가능성
                current_problem['options'].append(text)
        
        # 설명 추출
        elif current_problem and not text.startswith('전기'):
            # 아직 설명이 없으면 추가
            if 'explanation' not in current_problem:
                current_problem['explanation'] = text
    
    if current_problem:
        problems.append(current_problem)
    
    print(f"✅ {len(problems)}개 문제 추출 완료!")
    
    # 결과 출력
    print("\n" + "=" * 70)
    print("🎯 추출된 문제 분석 (상세)")
    print("=" * 70)
    
    problem_with_math = 0
    problem_with_image = 0
    total_math = 0
    total_images = 0
    
    for i, prob in enumerate(problems, 1):
        print(f"\n【문제 {i}】")
        print(f"  📄 본문: {prob['text'][:60]}{'...' if len(prob['text']) > 60 else ''}")
        
        if prob['has_math']:
            print(f"  🔢 수학공식: {prob['math_count']}개")
            problem_with_math += 1
            total_math += prob['math_count']
        
        if prob['has_image']:
            print(f"  🖼️  그림: {prob['image_count']}개")
            problem_with_image += 1
            total_images += prob['image_count']
        
        if prob['options']:
            print(f"  📋 보기: {len(prob['options'])}개")
            for opt in prob['options'][:2]:
                print(f"     - {opt[:50]}...")
        
        if 'explanation' in prob:
            exp = prob['explanation']
            print(f"  💡 설명: {exp[:60]}{'...' if len(exp) > 60 else ''}")
    
    # 통계
    print("\n" + "=" * 70)
    print("📊 DOCX 데이터 통계")
    print("=" * 70)
    print(f"총 문제: {len(problems)}개")
    print(f"수학공식 포함: {problem_with_math}개 (총 {total_math}개 수식)")
    print(f"그림 포함: {problem_with_image}개 (총 {total_images}개)")
    print(f"설명 포함: {sum(1 for p in problems if 'explanation' in p)}개")
    
    # JSON 저장
    output_json = "docx_precise_parsed.json"
    # JSON 직렬화를 위해 불필요한 필드 제거
    for prob in problems:
        prob.pop('answer_indicator', None)
        prob.pop('para_index', None)
    
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(problems, f, ensure_ascii=False, indent=2)
    print(f"\n💾 JSON 저장: {output_json}")
    
    # 수학공식 함수 형태 분석
    print("\n" + "=" * 70)
    print("🔢 수학 공식 상세 분석")
    print("=" * 70)
    
    # 문제별 상세 정보
    for i, prob in enumerate(problems[:10], 1):  # 처음 10개만
        if prob['has_math']:
            print(f"\n문제 {i}: {prob['math_count']}개 수식")
            print(f"  {prob['text'][:70]}...")

except Exception as e:
    print(f"❌ 오류: {e}")
    import traceback
    traceback.print_exc()
