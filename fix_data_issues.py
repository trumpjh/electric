#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix data.js issues:
1. Remove "? ①②③④" from problem text
2. Fix option parsing for problems 6, 14
3. Improve explanations
4. Add/fix image mappings
"""

import json
import re
from pathlib import Path

# Read original parsed data
with open('docx_precise_parsed.json', 'r', encoding='utf-8') as f:
    problems_raw = json.load(f)

# Manual fixes for known issues
FIXES = {
    # Problem 2: Image symbol issue - first element is image
    1: {
        'text': 'EQ 심벌는 무엇의 심벌인가?',
    },
    # Problem 5: Add complete explanation
    4: {
        'explanation': '저항값이 R1과 R2가 병렬 연결되고, 이것이 R3과 직렬 연결되어 있으므로: R_total = (R1×R2)/(R1+R2) + R3',
        'has_image': True,
        'image_path': 'problem_images/image2.png'
    },
    # Problem 6: Fix formula parsing issue
    5: {
        'options_raw': '√3(P1 - P2) | (P1 - P2) | √3P1P2 | (P1 + P2)',
        'explanation': '2전력계법으로 3상 전력을 측정할 때 유효전력 P = P1 + P2, 무효전력 Q = √3(P1 - P2)이다.'
    },
    # Problem 9: Improve explanation
    8: {
        'explanation': '4극(P=2)의 3상 유도 전동기에서 홈 수 n=36이면, 홈 간격의 전기각 = (180° × 홈 수) / (극수 × 3) = (180 × 36) / (4 × 3) = 540/3 = 20°'
    },
    # Problem 10: Fix explanation
    9: {
        'explanation': '슬립 s = 0.03 = (Ns - N) / Ns에서, Ns(동기속도) = 120f/P = 120×60/P rpm, N = 1164 rpm이므로: 0.03 = (120×60/P - 1164) / (120×60/P) 를 풀면 P=6(극수)'
    },
    # Problem 13: Fix formula in text  
    12: {
        'text': '22.9[kV-Y] 가공전선의 굵기는 단면적이 몇 mm²이상이어야 하는가?(단, 동선의 경우이다.)'
    },
    # Problem 14: Fix option parsing and add explanation + image
    13: {
        'options_raw': '1 | 1.5 | 2 | 3',
        'explanation': '금속몰드공사에서 금속 도체의 지지점 간의 거리는 안전상 1.5[m] 이하가 되도록 규정되어 있다. 이는 처짐을 방지하고 기계적 강도를 보장하기 위함이다.',
        'has_image': True,
        'image_path': 'problem_images/image3.png'
    }
}

def parse_options_from_raw(raw_str):
    """Parse option string into list of 4 options"""
    if ' | ' in raw_str:
        return raw_str.split(' | ')
    
    # Original parsing logic
    options = []
    pattern = r'[①②③④]\s*([^①②③④]+?)(?=[①②③④]|$)'
    matches = re.findall(pattern, raw_str)
    if len(matches) >= 4:
        return [m.strip() for m in matches[:4]]
    
    return ['', '', '', '']

def clean_problem_text(text):
    """Remove '? ①②③④' from problem text"""
    # Remove answer indicator
    text = re.sub(r'\?\s*[①②③④]\s*\[?수식\]?', '?', text)
    text = re.sub(r'\?\s*\[?수식\]?\s*$', '?', text)
    return text.strip()

def extract_answer(text, options_str):
    """Extract answer number from text"""
    match = re.search(r'\?\s*([①②③④])', text)
    if match:
        char_map = {'①': 1, '②': 2, '③': 3, '④': 4}
        return char_map.get(match.group(1), 1)
    return 1

# Process problems
corrected_problems = []
for i, prob in enumerate(problems_raw):
    corrected = {}
    
    # Apply fixes if available
    if i in FIXES:
        fix = FIXES[i]
        corrected.update(fix)
    
    # Copy original fields
    corrected.setdefault('text', clean_problem_text(prob['text']))
    
    # Parse options
    if 'options_raw' in corrected:
        options_list = parse_options_from_raw(corrected['options_raw'])
    else:
        options_list = []
        for opt_str in prob['options']:
            pattern = r'[①②③④]\s*([^①②③④]+?)(?=[①②③④]|$)'
            matches = re.findall(pattern, opt_str)
            if matches:
                options_list.extend([m.strip() for m in matches])
        options_list = options_list[:4]
    
    corrected.setdefault('options', options_list)
    corrected.setdefault('answer', extract_answer(prob['text'], ' '.join(prob['options'])))
    corrected.setdefault('explanation', prob.get('explanation', ''))
    corrected.setdefault('has_image', prob.get('has_image', False))
    corrected.setdefault('has_math', prob.get('has_math', False))
    corrected.setdefault('image_path', prob.get('image_path', None))
    
    corrected_problems.append(corrected)

# Print corrections
print("=" * 60)
print("CORRECTED PROBLEMS")
print("=" * 60)

for i, prob in enumerate(corrected_problems, 1):
    print(f"\n【{i}】 {prob.get('text', '')[:60]}")
    print(f"  Options: {prob.get('options', [])}")
    print(f"  Answer: {prob.get('answer')}")
    print(f"  Image: {prob.get('image_path')}")
    print(f"  Explanation: {prob.get('explanation', '')[:80]}...")

# Save to file for review
with open('corrected_problems.json', 'w', encoding='utf-8') as f:
    json.dump(corrected_problems, f, ensure_ascii=False, indent=2)

print("\n✓ Corrected problems saved to corrected_problems.json")
