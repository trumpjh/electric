#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zipfile
from xml.etree import ElementTree as ET
import re

# DOCX 파일 읽기
docx_path = '전기기능사 시험문제(2025-2023).docx'

with zipfile.ZipFile(docx_path, 'r') as zip_ref:
    xml_content = zip_ref.read('word/document.xml')

# XML 파싱
root = ET.fromstring(xml_content)
namespaces = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
}

# 모든 텍스트 추출
text_elements = root.findall('.//w:t', namespaces)
full_text = ''.join([elem.text for elem in text_elements if elem.text])

# 전체 길이 확인
print(f"전체 텍스트 길이: {len(full_text)} 글자\n")

# 파일에 저장 (분석용)
with open('full_text.txt', 'w', encoding='utf-8') as f:
    f.write(full_text)
    
print("파일이 'full_text.txt'로 저장되었습니다")
print("\n첫 3000자:")
print(full_text[:3000])
