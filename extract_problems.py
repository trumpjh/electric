#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from docx import Document
import json
import re

# DOCX 파일 읽기
doc = Document('전기기능사 시험문제(2025-2023).docx')

# 전체 텍스트 추출
all_text = []
for para in doc.paragraphs:
    if para.text.strip():
        all_text.append(para.text.strip())

# 출력하여 구조 파악
for i, line in enumerate(all_text[:100]):  # 처음 100줄 출력
    print(f"{i}: {line}")

print("\n\n=== 총 줄 수 ===")
print(f"총 {len(all_text)}줄")
