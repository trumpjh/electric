from docx import Document
import re
import json

# DOCX 파일 열기
doc = Document('전기기능사 시험문제(2025-2023).docx')

# 모든 문단 추출
print("DOCX 파일 단락 분석:")
print("=" * 80)

paragraphs = []
for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    if text:
        print(f"[단락 {i}] {text[:100]}...")
        paragraphs.append(text)

print("\n" + "=" * 80)
print(f"총 {len(paragraphs)}개 단락 추출됨\n")

# 단락을 텍스트 파일로 저장
with open('paragraphs.txt', 'w', encoding='utf-8') as f:
    for i, para in enumerate(paragraphs):
        f.write(f"[단락 {i}]\n{para}\n\n")

print("'paragraphs.txt'에 저장되었습니다")
