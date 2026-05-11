#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOCX를 ZIP으로 열어 원본 XML을 직접 파싱
- 모든 수학 공식 추출 가능
- 서식 정보 완전 보존
"""

import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

docx_path = "전기기능사 시험문제(2025-2023).docx"

print("=" * 60)
print("🔍 DOCX Raw XML 분석 (고정밀 파싱)")
print("=" * 60)

try:
    # DOCX를 ZIP으로 열기
    with zipfile.ZipFile(docx_path, 'r') as docx_zip:
        # 파일 목록 확인
        file_list = docx_zip.namelist()
        print(f"\n📦 DOCX 내부 파일 ({len(file_list)}개):")
        
        # 주요 파일 표시
        for fname in file_list:
            if fname.startswith('word/'):
                size = docx_zip.getinfo(fname).file_size
                print(f"  {fname} ({size:,} bytes)")
        
        # document.xml 읽기
        doc_xml = docx_zip.read('word/document.xml').decode('utf-8')
        
        print(f"\n📄 document.xml 크기: {len(doc_xml):,} bytes")
        
        # XML 파싱
        root = ET.fromstring(doc_xml)
        
        # 네임스페이스 정의
        namespaces = {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
            'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
            'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
            'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
        }
        
        # 모든 paragraph 찾기
        paragraphs = root.findall('.//w:p', namespaces)
        print(f"\n📝 Paragraph 수: {len(paragraphs)}")
        
        # 첫 20개 paragraph 분석
        print("\n" + "=" * 60)
        print("📋 첫 20개 Paragraph 내용")
        print("=" * 60)
        
        for i, para in enumerate(paragraphs[:20], 1):
            # 텍스트 추출
            texts = []
            
            # 일반 텍스트
            for text_elem in para.findall('.//w:t', namespaces):
                if text_elem.text:
                    texts.append(text_elem.text)
            
            # 수학 공식
            math_elements = para.findall('.//m:oMath', namespaces)
            if math_elements:
                texts.append(f"[수학공식 x{len(math_elements)}]")
            
            # 그림
            pic_elements = para.findall('.//pic:pic', namespaces)
            if pic_elements:
                texts.append(f"[그림 x{len(pic_elements)}]")
            
            if texts:
                content = "".join(texts)
                if len(content) > 100:
                    content = content[:100] + "..."
                print(f"【{i:2d}】 {content}")
        
        # 전체 statistics
        print("\n" + "=" * 60)
        print("📊 DOCX 구조 분석")
        print("=" * 60)
        
        all_texts = []
        math_count = 0
        image_count = 0
        table_count = 0
        
        for para in paragraphs:
            for text_elem in para.findall('.//w:t', namespaces):
                if text_elem.text:
                    all_texts.append(text_elem.text)
            
            math_count += len(para.findall('.//m:oMath', namespaces))
            image_count += len(para.findall('.//pic:pic', namespaces))
        
        tables = root.findall('.//w:tbl', namespaces)
        table_count = len(tables)
        
        full_text = "".join(all_texts)
        
        print(f"전체 텍스트 길이: {len(full_text):,} 자")
        print(f"수학 공식(oMath): {math_count}개")
        print(f"그림(Picture): {image_count}개")
        print(f"표(Table): {table_count}개")
        
        # 특수 요소 찾기
        print("\n" + "=" * 60)
        print("🔤 발견된 특수 요소")
        print("=" * 60)
        
        # drawing 요소 (그림 포함)
        drawings = root.findall('.//w:drawing', namespaces)
        print(f"Drawing 요소: {len(drawings)}개")
        
        # run 요소 (서식 정보)
        runs = root.findall('.//w:r', namespaces)
        print(f"Run 요소 (서식): {len(runs)}개")
        
        # 특수 문자 발견
        special_chars = set()
        for char in full_text:
            if ord(char) > 127:
                special_chars.add(char)
        
        print(f"\n특수 문자 종류: {len(special_chars)}개")
        if special_chars:
            print("샘플:", ", ".join(sorted(list(special_chars))[:20]))
        
        # 저장
        xml_backup = "docx_raw_document.xml"
        with open(xml_backup, "w", encoding="utf-8") as f:
            f.write(doc_xml[:5000] + "\n... (내용 잘림)")
        
        print(f"\n✅ Raw XML 분석 완료!")
        print(f"💡 전체 XML은 {docx_path}의 word/document.xml에 있습니다")

except FileNotFoundError:
    print(f"❌ 파일 없음: {docx_path}")
except Exception as e:
    print(f"❌ 오류: {e}")
    import traceback
    traceback.print_exc()
