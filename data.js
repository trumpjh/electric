// 문제 데이터
const problemsData = {
    '2025-1': {
        year: 2025,
        round: 1,
        title: '2025년도 제1회',
        subject: '전기설비',
        problems: [
            {
                id: '2025-1-1',
                number: 1,
                text: '다음 중 전기안전관리법에 대한 설명으로 가장 옳은 것은?',
                options: [
                    '① 전기사업자는 전기를 공급받는 자이다',
                    '② 전력계통은 발전소, 변전소, 배전선로로 구성된다',
                    '③ 전기설비는 전압과 무관하게 모두 신고 대상이다',
                    '④ 임시용 전기설비는 전기안전관리법의 적용을 받지 않는다'
                ],
                answer: 2
            },
            {
                id: '2025-1-2',
                number: 2,
                text: '전력계통의 주파수가 60Hz일 때, 기본파의 파장은 약 몇 m인가? (음속 340m/s)',
                options: [
                    '① 약 5.67m',
                    '② 약 56.7m',
                    '③ 약 567m',
                    '④ 약 5670m'
                ],
                answer: 1
            },
            {
                id: '2025-1-3',
                number: 3,
                text: '다음 중 교류 전압의 크기를 나타내는 방법으로 가장 많이 사용되는 것은?',
                options: [
                    '① 최댓값(Peak Value)',
                    '② 평균값(Average Value)',
                    '③ 실효값(RMS Value)',
                    '④ 순시값(Instantaneous Value)'
                ],
                answer: 3
            },
            {
                id: '2025-1-4',
                number: 4,
                text: '다음 중 직렬 RL 회로의 임피던스 계산식으로 옳은 것은? (R: 저항, XL: 유도 리액턴스)',
                options: [
                    '① Z = R + XL',
                    '② Z = √(R² + XL²)',
                    '③ Z = R × XL',
                    '④ Z = R - XL'
                ],
                answer: 2
            },
            {
                id: '2025-1-5',
                number: 5,
                text: '콘덴서에 교류 전류가 흘렀을 때 콘덴서의 용량성 리액턴스는 주파수가 증가하면 어떻게 변하는가?',
                options: [
                    '① 증가한다',
                    '② 감소한다',
                    '③ 변하지 않는다',
                    '④ 주파수와 무관하다'
                ],
                answer: 2
            },
            {
                id: '2025-1-6',
                number: 6,
                text: '전력의 종류 중 실제로 회로에서 소비되는 전력은?',
                options: [
                    '① 무효전력',
                    '② 실전력(유효전력)',
                    '③ 피상전력',
                    '④ 순시전력'
                ],
                answer: 2
            },
            {
                id: '2025-1-7',
                number: 7,
                text: '삼상 교류 전원의 선간 전압이 220V일 때 상전압의 크기는 약 몇 V인가?',
                options: [
                    '① 110V',
                    '② 127V',
                    '③ 220V',
                    '④ 380V'
                ],
                answer: 2
            },
            {
                id: '2025-1-8',
                number: 8,
                text: '다음 중 변압기의 1차 코일과 2차 코일의 관계로 올바른 것은?',
                options: [
                    '① 1차 전압 × 1차 전류 = 2차 전압 × 2차 전류',
                    '② 1차 전압 > 2차 전압이면 승압변압기이다',
                    '③ 권수비와 전압비는 같다',
                    '④ 1차와 2차의 전력이 항상 같다'
                ],
                answer: 3
            },
            {
                id: '2025-1-9',
                number: 9,
                text: '전동기의 효율(η)을 나타내는 식으로 옳은 것은?',
                options: [
                    '① η = 출력 / 입력',
                    '② η = 입력 / 출력',
                    '③ η = 손실 / 입력',
                    '④ η = (입력 + 출력) / 2'
                ],
                answer: 1
            },
            {
                id: '2025-1-10',
                number: 10,
                text: '교류 발전기에서 권수와 교류 전압의 관계로 올바른 것은?',
                options: [
                    '① 권수가 증가하면 전압이 감소한다',
                    '② 권수가 증가하면 전압이 증가한다',
                    '③ 권수와 전압은 무관하다',
                    '④ 주파수에만 영향을 받는다'
                ],
                answer: 2
            },
            {
                id: '2025-1-11',
                number: 11,
                text: '다음 중 안전 저전압의 기준으로 가장 옳은 것은?',
                options: [
                    '① 직류 120V 이하',
                    '② 교류 50V 이하',
                    '③ 직류 50V 이하',
                    '④ 교류 220V 이하'
                ],
                answer: 2
            },
            {
                id: '2025-1-12',
                number: 12,
                text: '접지 저항의 값에 영향을 미치지 않는 요소는?',
                options: [
                    '① 접지 전극의 크기와 형태',
                    '② 흙의 종류와 습도',
                    '③ 접지 전극의 깊이',
                    '④ 전기 장비의 용량'
                ],
                answer: 4
            },
            {
                id: '2025-1-13',
                number: 13,
                text: '배전반의 주차단기는 어느 곳에 설치해야 하는가?',
                options: [
                    '① 배전반 내부의 중앙',
                    '② 배전반의 입구에 가장 가까운 위치',
                    '③ 배전반의 가장 아래쪽',
                    '④ 배전반의 뒷면'
                ],
                answer: 2
            },
            {
                id: '2025-1-14',
                number: 14,
                text: '저압 배선의 내열성이 가장 좋은 절연 종류는?',
                options: [
                    '① PVC(염화비닐)',
                    '② VV(비닐 절연)',
                    '③ CV(가교 폴리에틸렌)',
                    '④ 고무 절연'
                ],
                answer: 3
            },
            {
                id: '2025-1-15',
                number: 15,
                text: '전기 재해를 방지하기 위한 기본 안전장치로 가장 중요한 것은?',
                options: [
                    '① 퓨즈',
                    '② 차단기',
                    '③ 접지',
                    '④ 부하 스위치'
                ],
                answer: 3
            }
        ]
    },
    // 다른 년도/회차는 추후 추가
    '2025-2': {
        year: 2025,
        round: 2,
        title: '2025년도 제2회',
        subject: '전기설비',
        problems: []
    },
    '2025-3': {
        year: 2025,
        round: 3,
        title: '2025년도 제3회',
        subject: '전기설비',
        problems: []
    },
    '2025-4': {
        year: 2025,
        round: 4,
        title: '2025년도 제4회',
        subject: '전기설비',
        problems: []
    },
    '2024-1': {
        year: 2024,
        round: 1,
        title: '2024년도 제1회',
        subject: '전기설비',
        problems: []
    },
    '2024-2': {
        year: 2024,
        round: 2,
        title: '2024년도 제2회',
        subject: '전기설비',
        problems: []
    },
    '2024-3': {
        year: 2024,
        round: 3,
        title: '2024년도 제3회',
        subject: '전기설비',
        problems: []
    },
    '2024-4': {
        year: 2024,
        round: 4,
        title: '2024년도 제4회',
        subject: '전기설비',
        problems: []
    },
    '2023-1': {
        year: 2023,
        round: 1,
        title: '2023년도 제1회',
        subject: '전기설비',
        problems: []
    },
    '2023-2': {
        year: 2023,
        round: 2,
        title: '2023년도 제2회',
        subject: '전기설비',
        problems: []
    },
    '2023-3': {
        year: 2023,
        round: 3,
        title: '2023년도 제3회',
        subject: '전기설비',
        problems: []
    },
    '2023-4': {
        year: 2023,
        round: 4,
        title: '2023년도 제4회',
        subject: '전기설비',
        problems: []
    }
};

// 단원별 구조
const subjectCategories = [
    '전기설비',
    '전기기기',
    '전기회로',
    '전기안전',
    '전기공사'
];

// 문제를 단원별로 분류하는 함수
function getProblemasBySubject(subject) {
    const problems = [];
    for (const key in problemsData) {
        if (problemsData[key].subject === subject) {
            problems.push({
                ...problemsData[key],
                key: key
            });
        }
    }
    return problems;
}
