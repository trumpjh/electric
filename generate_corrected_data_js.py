#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate corrected data.js with:
1. Fixed problem texts (remove ? ①②③④)
2. Fixed options for problems 6, 14
3. Improved explanations
4. Image mappings for problems 5, 14
"""

import re
import json

# Manual data corrections based on user feedback
CORRECTED_DATA = {
    "2025-1": {
        "year": 2025,
        "round": 1,
        "title": "2025년도 제1회",
        "subject": "전기기능사",
        "problems": [
            {
                "id": "2025-1-1",
                "number": 1,
                "text": "진동이 심한 전기 기계기구의 단자에 전선을 접속할 때 사용되는것은?",
                "options": ["커플링", "압착단자", "링슬리브", "스프링와셔"],
                "answer": 4,
                "category": "전기설비",
                "explanation": "진동이 있는 단자에 전선을 접속할 때 스프링 와셔 또는 이중너트를 사용하여 접속한다.",
                "image": None
            },
            {
                "id": "2025-1-2",
                "number": 2,
                "text": "다음 EQ 심벌은 무엇을 나타내는가?",
                "options": ["지진감지기", "소형 변압기", "누전경보기", "전류제한기"],
                "answer": 1,
                "category": "전기설비",
                "explanation": "EQ는 지진 감지기로 지진을 가리키는 영어 단어(Earthquake)에서 글자를 따와서 심벌로 사용한다.",
                "image": "problem_images/image1.png"
            },
            {
                "id": "2025-1-3",
                "number": 3,
                "text": "다음 보기 중 접지시스템의 종류가 아닌 것은?",
                "options": ["단독접지", "공통접지", "통합접지", "보호접지"],
                "answer": 4,
                "category": "전기설비",
                "explanation": "접지시스템의 시설 종류에는 단독 접지, 공통 접지, 통합 접지가 있다.",
                "image": None
            },
            {
                "id": "2025-1-4",
                "number": 4,
                "text": "전기기기의 철심 재료로 규소강판을 많이 사용하는 이유로 가장 적당한 것은?",
                "options": ["와류손을줄이기 위해", "맴돌이 전류를 없애기 위해", "히스테리시스손을줄이기 위해", "구리손을줄이기 위해"],
                "answer": 3,
                "category": "전기기기",
                "explanation": "철심은 전기기기에서 자기회로를 만드는 부분으로 회전에 따른 자속 방향이 수시로 변화하여 와류손이나 히스테리시스손으로 인한 철손이 발생한다. 와류손은 얇은 철심을 여러 겹 겹친 성층 철심을 사용하여, 히스테리시스손은 규소 강판 철심을 사용하여 각각 줄일 수 있다.",
                "image": None
            },
            {
                "id": "2025-1-5",
                "number": 5,
                "text": "다음 회로의전기저항값은?",
                "options": ["6.4", "7.4", "10.4", "12.4"],
                "answer": 2,
                "category": "전기이론",
                "explanation": "회로에서 R1(8Ω)과 R2(8Ω)가 병렬 연결되고, 이것이 R3(3Ω)과 직렬 연결되어 있으므로: R병렬 = (8×8)/(8+8) = 4Ω, R전체 = 4 + 3.4 = 7.4Ω",
                "image": "problem_images/image2.png"
            },
            {
                "id": "2025-1-6",
                "number": 6,
                "text": "2전력계법에 의해 3상 전력을 측정하여 전력계가 P1, P2를 나타냈다면 무효전력의 식은?",
                "options": ["√3(P1 - P2)", "(P1 - P2)", "√3P1P2", "(P1 + P2)"],
                "answer": 1,
                "category": "전기이론",
                "explanation": "2전력계법으로 3상 전력을 측정할 때 유효전력 P = P1 + P2, 무효전력 Q = √3(P1 - P2)이다.",
                "image": None
            },
            {
                "id": "2025-1-7",
                "number": 7,
                "text": "1차 전압 6,300[V], 2차 전압 210[V]. 주파수 60[Hz]의 변압기가 있다. 이 변압기의 권수비는?",
                "options": ["30", "40", "50", "60"],
                "answer": 1,
                "category": "전기기기",
                "explanation": "권수비 = 1차 전압 / 2차 전압 = 6300 / 210 = 30",
                "image": None
            },
            {
                "id": "2025-1-8",
                "number": 8,
                "text": "다음 중 전위의 단위가 아닌 것은?",
                "options": ["[V/m]", "[V]", "[N·m/c]", "[J/C]"],
                "answer": 1,
                "category": "전기이론",
                "explanation": "전위의 단위는 [V]를 사용한다. [V/m]은 전계의 단위이고, 전기가 한 일 W = VQ (단, Q: 전하량)이다.",
                "image": None
            },
            {
                "id": "2025-1-9",
                "number": 9,
                "text": "4극 고정자, 홈 수 36의 3상 유도 전동기의 홈 간격은 전기 각의 몇 도인가?",
                "options": ["5°", "10°", "15°", "20°"],
                "answer": 4,
                "category": "전기기기",
                "explanation": "4극(P=2)의 3상 유도 전동기에서 홈 수 n=36이면, 홈 간격의 전기각 = (180° × 홈 수) / (극수 × 3) = (180 × 36) / (4 × 3) = 540/3 = 20°",
                "image": None
            },
            {
                "id": "2025-1-10",
                "number": 10,
                "text": "주파수 60[Hz]의 회로에 접속되어 슬립 3%, 회전수 1,164[rpm]으로 회전하고 있는 유도 전동기의 극수는?",
                "options": ["4", "6", "8", "10"],
                "answer": 2,
                "category": "전기기기",
                "explanation": "슬립 s = 0.03 = (Ns - N) / Ns에서, Ns(동기속도) = 120f/P = 120×60/P rpm, N = 1164 rpm이므로 0.03 = (120×60/P - 1164) / (120×60/P) 를 풀면 P=6(극수)이다.",
                "image": None
            },
            {
                "id": "2025-1-11",
                "number": 11,
                "text": "전선 접속 시 사용도는 슬리브(Sleeve)의 종류가 아닌 것은?",
                "options": ["E형", "S형", "D형", "P형"],
                "answer": 3,
                "category": "전기설비",
                "explanation": "전선 접속 시 사용되는 슬리브(Sleeve)의 종류에는 C형, E형, P형, S형 등이 있다.",
                "image": None
            },
            {
                "id": "2025-1-12",
                "number": 12,
                "text": "3상 유도 전동기의 원선도를 그리는 데 필요하지 않은 것은?",
                "options": ["저항 측정", "무부하 시험", "구속 시험", "슬립 측정"],
                "answer": 4,
                "category": "전기기기",
                "explanation": "원선도 작성에 필요한 시험으로는 저항 측정 시험, 무부하 시험, 구속 시험 등이 있다.",
                "image": None
            },
            {
                "id": "2025-1-13",
                "number": 13,
                "text": "22.9[kV-Y] 가공전선의 굵기는 단면적이 몇 mm²이상이어야 하는가?(단, 동선의 경우이다.)",
                "options": ["22", "32", "40", "50"],
                "answer": 1,
                "category": "전기설비",
                "explanation": "특고압 가공전선의 굵기는 구리(동)선의 경우 단면적이 22mm² 이상이어야 한다.",
                "image": None
            },
            {
                "id": "2025-1-14",
                "number": 14,
                "text": "금속몰드의 지지점 간의 거리는 몇 [m] 이하로 하는 것이 가장바람직한가?",
                "options": ["1", "1.5", "2", "3"],
                "answer": 2,
                "category": "전기설비",
                "explanation": "금속몰드공사에서 금속 도체의 지지점 간의 거리는 안전상 1.5[m] 이하가 되도록 규정되어 있다. 이는 처짐을 방지하고 기계적 강도를 보장하기 위함이며, 절연 물질을 적절히 지지하여 내구성을 유지한다.",
                "image": "problem_images/image3.png"
            },
            {
                "id": "2025-1-15",
                "number": 15,
                "text": "영구 자석 또는 전자석 끝부분에 설치한 자성 재료편으로서, 전기자에 대응하여 계자 자속을 공극에 적당히 분포시키는 역할을 하는 것은 무엇인가?",
                "options": ["자극편", "정류자", "공극", "브러시"],
                "answer": 1,
                "category": "전기기기",
                "explanation": "자극편: 영구 자석 또는 전자석으로 구성되어 주 자속을 만들고 분포 시키는 부분으로 계자라고도 한다.",
                "image": None
            }
        ]
    },
    "2025-2": {
        "year": 2025,
        "round": 2,
        "title": "2025년도 제2회",
        "subject": "전기기능사",
        "problems": []
    },
    "2025-3": {
        "year": 2025,
        "round": 3,
        "title": "2025년도 제3회",
        "subject": "전기설비",
        "problems": []
    },
    "2025-4": {
        "year": 2025,
        "round": 4,
        "title": "2025년도 제4회",
        "subject": "전기설비",
        "problems": []
    },
    "2024-1": {
        "year": 2024,
        "round": 1,
        "title": "2024년도 제1회",
        "subject": "전기설비",
        "problems": []
    },
    "2024-2": {
        "year": 2024,
        "round": 2,
        "title": "2024년도 제2회",
        "subject": "전기설비",
        "problems": []
    },
    "2024-3": {
        "year": 2024,
        "round": 3,
        "title": "2024년도 제3회",
        "subject": "전기설비",
        "problems": []
    },
    "2024-4": {
        "year": 2024,
        "round": 4,
        "title": "2024년도 제4회",
        "subject": "전기설비",
        "problems": []
    },
    "2023-1": {
        "year": 2023,
        "round": 1,
        "title": "2023년도 제1회",
        "subject": "전기설비",
        "problems": []
    },
    "2023-2": {
        "year": 2023,
        "round": 2,
        "title": "2023년도 제2회",
        "subject": "전기설비",
        "problems": []
    },
    "2023-3": {
        "year": 2023,
        "round": 3,
        "title": "2023년도 제3회",
        "subject": "전기설비",
        "problems": []
    },
    "2023-4": {
        "year": 2023,
        "round": 4,
        "title": "2023년도 제4회",
        "subject": "전기설비",
        "problems": []
    }
}

# Generate JavaScript output
js_output = "// 문제 데이터\n"
js_output += "const problemsData = " + json.dumps(CORRECTED_DATA, ensure_ascii=False, indent=4) + ";"

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(js_output)

print("✓ data.js updated successfully")
print(f"✓ 2025-1: {len(CORRECTED_DATA['2025-1']['problems'])} problems")
