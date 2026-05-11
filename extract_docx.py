#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zipfile
from xml.etree import ElementTree as ET

# DOCX 파일 읽기 (DOCX는 ZIP 형식)
docx_path = '전기기능사 시험문제(2025-2023).docx'

try:
    with zipfile.ZipFile(docx_path, 'r') as zip_ref:
        # document.xml 읽기
        xml_content = zip_ref.read('word/document.xml')
        
    # XML 파싱
    root = ET.fromstring(xml_content)
    
    # 네임스페이스 정의
    namespaces = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    }
    
    # 모든 텍스트 추출
    text_elements = root.findall('.//w:t', namespaces)
    full_text = ''.join([elem.text for elem in text_elements if elem.text])
    
    # 문서 출력
    print(full_text[:3000])
    print("\n\n=== 총 길이 ===")
    print(f"전체 텍스트 길이: {len(full_text)} 글자")
    
except Exception as e:
    print(f"오류: {e}")
    import traceback
    traceback.print_exc()
