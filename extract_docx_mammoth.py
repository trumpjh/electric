#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mammoth를 사용한 정밀한 DOCX 분석
- 수학/공학 기호 보존
- 서식 정보 추출
- 복잡한 레이아웃 처리
"""

import mammoth
import re
from pathlib import Path

docx_path = "전기기능사 시험문제(2025-2023).docx"

print("=" * 60)
print("📖 Mammoth를 사용한 고정밀 DOCX 분석")
print("=" * 60)

try:
    # Mammoth로 변환
    with open(docx_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html_output = result.value
        messages = result.messages
    
    print(f"\n✅ DOCX 읽기 성공: {docx_path}")
    
    # 변환 경고/에러 출력
    if messages:
        print(f"\n⚠️ 변환 메시지 ({len(messages)}개):")
        for i, msg in enumerate(messages[:10], 1):
            print(f"  {i}. {msg}")
    
    # HTML 저장 (검토용)
    html_path = "docx_output_mammoth.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_output)
    print(f"\n💾 HTML 저장: {html_path}")
    
    # 텍스트 추출 (기호 보존)
    # HTML 태그 제거하되 기호는 보존
    text = html_output
    
    # 기본 HTML 태그 제거
    text = re.sub(r'<[^>]+>', '', text)
    # HTML 엔티티 디코딩
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&amp;', '&')
    text = text.replace('&quot;', '"')
    text = text.replace('&apos;', "'")
    
    # 문제 구분
    problems = []
    current_problem = ""
    
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 수학 기호/특수문자 표시
        special_chars = []
        for char in line:
            if ord(char) > 127 and char not in '가나다라마바사아자차카타파하':
                special_chars.append(char)
        
        current_problem += line + "\n"
        
        # 선택지 판별 (①②③④ 또는 ①~④)
        if any(c in line for c in ['①', '②', '③', '④']):
            if current_problem.count('\n') > 3:  # 문제+보기 충분하면
                problems.append(current_problem.strip())
                current_problem = ""
    
    if current_problem.strip():
        problems.append(current_problem.strip())
    
    print(f"\n📊 문제 감지: {len(problems)}개")
    
    # 첫 5개 문제 상세 출력
    print("\n" + "=" * 60)
    print("📝 추출된 문제 샘플 (처음 5개)")
    print("=" * 60)
    
    for i, problem in enumerate(problems[:5], 1):
        print(f"\n【문제 {i}】")
        print("-" * 40)
        
        # 특수문자 분석
        special_chars = set()
        for char in problem:
            if ord(char) > 127:
                special_chars.add(char)
        
        if special_chars and '가나다라마바사아자차카타파하' not in ''.join(special_chars):
            print(f"🔤 특수 기호: {', '.join(sorted(special_chars))}")
        
        # 내용
        lines = problem.split('\n')
        for j, line in enumerate(lines[:8]):  # 처음 8줄만
            if line:
                print(f"  {line}")
        
        if len(lines) > 8:
            print(f"  ... ({len(lines)-8}줄 더)")
    
    # 통계
    print("\n" + "=" * 60)
    print("📈 텍스트 통계")
    print("=" * 60)
    print(f"전체 텍스트 길이: {len(text):,} 자")
    print(f"감지된 문제 수: {len(problems)}")
    
    # 특수 기호 모음
    all_special = set()
    for problem in problems:
        for char in problem:
            if ord(char) > 127 and '가나다라마바사아자차카타파하' not in char:
                all_special.add(char)
    
    if all_special:
        print(f"\n🔤 전체 특수 기호 목록 ({len(all_special)}개):")
        for char in sorted(all_special):
            print(f"  '{char}' (U+{ord(char):04X})", end="  ")
        print()
    
    print("\n✅ Mammoth 분석 완료!")
    print(f"💡 HTML 파일({html_path})을 브라우저로 열어 정확한 서식 확인 가능")

except FileNotFoundError:
    print(f"❌ 파일을 찾을 수 없음: {docx_path}")
except Exception as e:
    print(f"❌ 오류: {e}")
    import traceback
    traceback.print_exc()
