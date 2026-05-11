// 전역 상태 관리
let appState = {
    testDate: '',
    studentName: '',
    selectedProblems: [],
    currentQuestionIndex: 0,
    userAnswers: {},
    allProblems: [],
    shuffledOptions: {},
    answered: {}
};

// 초기화
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    setDefaultDate();
});

// 기본 날짜 설정 (오늘)
function setDefaultDate() {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    document.getElementById('testDate').value = `${year}-${month}-${day}`;
}

// 배열 섞기 함수 (Fisher-Yates 알고리즘)
function shuffleArray(array) {
    const arr = [...array];
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
}

// 이벤트 리스너 설정
function setupEventListeners() {
    // 초기 정보 입력 화면
    document.getElementById('startBtn').addEventListener('click', startQuiz);
    
    // 탭 선택
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', switchTab);
    });
    
    // 문제 선택 화면
    document.getElementById('startQuizBtn').addEventListener('click', startQuizSession);
    document.getElementById('backToInfoBtn').addEventListener('click', backToInfo);
    
    // 문제 풀기 화면
    document.getElementById('prevBtn').addEventListener('click', previousQuestion);
    document.getElementById('nextBtn').addEventListener('click', nextQuestion);
    document.getElementById('submitBtn').addEventListener('click', submitQuiz);
    
    // 결과 화면
    document.getElementById('retryBtn').addEventListener('click', retryQuiz);
    document.getElementById('newTestBtn').addEventListener('click', startNew);
}

// 화면 전환 함수
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');
}

// ===== 초기 정보 입력 화면 =====
function startQuiz() {
    const testDate = document.getElementById('testDate').value;
    const studentName = document.getElementById('studentName').value;
    
    if (!testDate || !studentName.trim()) {
        alert('날짜와 성명을 모두 입력해주세요!');
        return;
    }
    
    appState.testDate = testDate;
    appState.studentName = studentName;
    appState.userAnswers = {};
    appState.shuffledOptions = {};
    appState.answered = {};
    
    // 문제 선택 화면으로 이동
    displayYearSelection();
    displaySubjectSelection();
    showScreen('selectScreen');
}

// ===== 문제 선택 화면 =====
function displayYearSelection() {
    const container = document.getElementById('yearSubjectContainer');
    container.innerHTML = '';
    
    // 년도별/회차별로 버튼 생성
    const years = [2025, 2024, 2023];
    const rounds = [1, 2, 3, 4];
    
    years.forEach(year => {
        rounds.forEach(round => {
            const key = `${year}-${round}`;
            if (problemsData[key]) {
                const data = problemsData[key];
                const problemCount = data.problems ? data.problems.length : 0;
                
                const item = document.createElement('div');
                item.className = 'selection-item';
                item.innerHTML = `
                    <label>
                        <input type="checkbox" value="${key}">
                        <strong>${year}년도<br>제${round}회</strong>
                        <small>(${problemCount}문제)</small>
                    </label>
                `;
                
                item.querySelector('input').addEventListener('change', function() {
                    if (this.checked) {
                        item.classList.add('selected');
                    } else {
                        item.classList.remove('selected');
                    }
                });
                
                container.appendChild(item);
            }
        });
    });
}

function displaySubjectSelection() {
    const container = document.getElementById('subjectContainer');
    container.innerHTML = '';
    
    // 단원별 선택 옵션 생성
    subjectCategories.forEach(subject => {
        const item = document.createElement('div');
        item.className = 'selection-item';
        item.innerHTML = `
            <label>
                <input type="checkbox" value="${subject}">
                <strong>${subject}</strong>
            </label>
        `;
        
        item.querySelector('input').addEventListener('change', function() {
            if (this.checked) {
                item.classList.add('selected');
            } else {
                item.classList.remove('selected');
            }
        });
        
        container.appendChild(item);
    });
}

function switchTab(e) {
    const tabName = e.target.dataset.tab;
    
    // 탭 버튼 활성화
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    e.target.classList.add('active');
    
    // 탭 콘텐츠 표시
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(tabName).classList.add('active');
}

function startQuizSession() {
    // 선택된 문제들 수집
    const selectedCheckboxes = document.querySelectorAll('.selection-item input[type="checkbox"]:checked');
    
    if (selectedCheckboxes.length === 0) {
        alert('최소 하나 이상의 문제를 선택해주세요!');
        return;
    }
    
    appState.allProblems = [];
    appState.selectedProblems = [];  // 선택 경로별 정보 저장
    
    // 현재 활성 탭 확인
    const activeTab = document.querySelector('.tab-content.active').id;
    
    if (activeTab === 'byYear') {
        // 년도별 선택
        selectedCheckboxes.forEach(checkbox => {
            const key = checkbox.value;
            if (problemsData[key] && problemsData[key].problems) {
                const problems = problemsData[key].problems;
                problems.forEach(problem => {
                    problem.selectionMethod = 'byYear';
                    problem.selectionValue = key;
                });
                appState.allProblems.push(...problems);
                appState.selectedProblems.push({
                    method: 'byYear',
                    value: key,
                    label: `${key.split('-')[0]}년도 제${key.split('-')[1]}회`
                });
            }
        });
    } else {
        // 단원별 선택 (category 기반)
        selectedCheckboxes.forEach(checkbox => {
            const selectedCategory = checkbox.value;
            let categoryProblems = [];
            for (const key in problemsData) {
                if (problemsData[key].problems) {
                    problemsData[key].problems.forEach(problem => {
                        if (problem.category === selectedCategory) {
                            problem.selectionMethod = 'bySubject';
                            problem.selectionValue = selectedCategory;
                            categoryProblems.push(problem);
                            appState.allProblems.push(problem);
                        }
                    });
                }
            }
            if (categoryProblems.length > 0) {
                appState.selectedProblems.push({
                    method: 'bySubject',
                    value: selectedCategory,
                    label: selectedCategory
                });
            }
        });
    }
    
    // 중복 제거
    const uniqueIds = new Set();
    appState.allProblems = appState.allProblems.filter(problem => {
        if (uniqueIds.has(problem.id)) {
            return false;
        }
        uniqueIds.add(problem.id);
        return true;
    });
    
    // 문제 순서 섞기
    appState.allProblems = shuffleArray(appState.allProblems);
    
    if (appState.allProblems.length === 0) {
        alert('선택된 카테고리에 문제가 없습니다. 먼저 문제를 추가해주세요!');
        return;
    }
    
    // 사용자 답변 초기화
    appState.userAnswers = {};
    appState.shuffledOptions = {};
    appState.answered = {};
    appState.allProblems.forEach(problem => {
        appState.userAnswers[problem.id] = null;
        appState.answered[problem.id] = false;
        // 선택지 섞기 저장 (문제마다 고정)
        const originalIndices = [0, 1, 2, 3];
        const shuffledIndices = shuffleArray(originalIndices);
        appState.shuffledOptions[problem.id] = {
            shuffled: shuffledIndices,
            mapping: {}
        };
        shuffledIndices.forEach((originalIdx, shuffledIdx) => {
            if (originalIdx + 1 === problem.answer) {
                appState.shuffledOptions[problem.id].mapping[shuffledIdx] = shuffledIdx + 1;
            }
        });
    });
    
    appState.currentQuestionIndex = 0;
    displayQuestion();
    showScreen('quizScreen');
}

function backToInfo() {
    showScreen('infoScreen');
}

// ===== 문제 풀기 화면 =====
function displayQuestion() {
    const problem = appState.allProblems[appState.currentQuestionIndex];
    
    if (!problem) return;
    
    // 헤더 업데이트
    const total = appState.allProblems.length;
    const current = appState.currentQuestionIndex + 1;
    document.getElementById('quizTitle').textContent = `문제 풀기`;
    document.getElementById('progressText').textContent = `${current} / ${total}`;
    document.getElementById('progressFill').style.width = `${(current / total) * 100}%`;
    
    // 문제 표시
    document.getElementById('questionNumber').textContent = `${problem.number}번 (${problem.category})`;
    document.getElementById('questionText').textContent = problem.text;
    
    // 설명 섹션 초기화
    const explanationSection = document.getElementById('explanationSection');
    explanationSection.style.display = 'none';
    
    // 선택지 표시 (섞인 순서로)
    const optionsContainer = document.getElementById('optionsContainer');
    optionsContainer.innerHTML = '';
    
    const shuffleData = appState.shuffledOptions[problem.id];
    const shuffledIndices = shuffleData.shuffled;
    
    shuffledIndices.forEach((originalIdx, shuffledIdx) => {
        const optionNum = shuffledIdx + 1;
        const originalAnswer = originalIdx + 1;  // 원본 인덱스 기반 정답
        const originalOption = problem.options[originalIdx];
        const optionDiv = document.createElement('div');
        optionDiv.className = 'option';
        optionDiv.id = `option-${problem.id}-${shuffledIdx}`;
        
        const isSelected = appState.userAnswers[problem.id] === originalAnswer;
        const isAnswered = appState.answered[problem.id];
        
        if (isSelected) {
            optionDiv.classList.add('selected');
        }
        
        // 이미 답변한 경우 정/오답 표시
        if (isAnswered) {
            const correctAnswer = problem.answer;
            const isCorrect = originalAnswer === correctAnswer;
            if (isSelected && isCorrect) {
                optionDiv.classList.add('correct');
            } else if (isSelected && !isCorrect) {
                optionDiv.classList.add('incorrect');
            } else if (!isSelected && originalAnswer === correctAnswer) {
                optionDiv.classList.add('correct');
            }
        }
        
        optionDiv.innerHTML = `
            <input type="radio" name="answer" value="${optionNum}" 
                   id="option${optionNum}" ${isSelected ? 'checked' : ''} 
                   ${isAnswered ? 'disabled' : ''}>
            <label for="option${optionNum}" class="option-label">${originalOption}</label>
        `;
        
        if (!isAnswered) {
            optionDiv.querySelector('input').addEventListener('change', function() {
                selectAnswer(problem, originalAnswer);  // 원본 인덱스 기반 정답 저장
            });
        }
        
        optionsContainer.appendChild(optionDiv);
    });
    
    // 이미 답변한 경우 설명 표시
    if (appState.answered[problem.id]) {
        showExplanation(problem);
    }
    
    // 버튼 상태 업데이트
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');
    
    prevBtn.disabled = appState.currentQuestionIndex === 0;
    nextBtn.disabled = appState.currentQuestionIndex >= total - 1;
    
    if (appState.currentQuestionIndex === total - 1) {
        nextBtn.style.display = 'none';
        submitBtn.style.display = appState.answered[problem.id] ? 'block' : 'none';
    } else {
        nextBtn.style.display = 'block';
        submitBtn.style.display = 'none';
    }
}

function selectAnswer(problem, answerNum) {
    appState.userAnswers[problem.id] = answerNum;
    appState.answered[problem.id] = true;
    
    // 화면 업데이트 (정/오답 표시 및 설명)
    displayQuestion();
}

function showExplanation(problem) {
    const explanationSection = document.getElementById('explanationSection');
    const explanationText = document.getElementById('explanationText');
    
    const userAnswer = appState.userAnswers[problem.id];
    const isCorrect = userAnswer === problem.answer;
    
    // 섞인 선택지에서 정답의 실제 위치 구하기
    const shuffledIndices = appState.shuffledOptions[problem.id].shuffled;
    const correctOriginalIndex = problem.answer - 1;
    const correctShuffledPosition = shuffledIndices.indexOf(correctOriginalIndex) + 1;
    
    let explanation = '';
    if (isCorrect) {
        explanation = `<strong style="color: #48bb78;">✓ 정답입니다!</strong><br>`;
    } else {
        explanation = `<strong style="color: #f56565;">✗ 오답입니다. 정답은 ${correctShuffledPosition}번입니다.</strong><br>`;
    }
    explanation += problem.explanation;
    
    explanationText.innerHTML = explanation;
    explanationSection.style.display = 'block';
}

function previousQuestion() {
    if (appState.currentQuestionIndex > 0) {
        appState.currentQuestionIndex--;
        displayQuestion();
    }
}

function nextQuestion() {
    const problem = appState.allProblems[appState.currentQuestionIndex];
    
    // 답변하지 않았으면 경고
    if (!appState.answered[problem.id]) {
        alert('현재 문제에 답변해주세요!');
        return;
    }
    
    if (appState.currentQuestionIndex < appState.allProblems.length - 1) {
        appState.currentQuestionIndex++;
        displayQuestion();
    }
}

function submitQuiz() {
    // 마지막 문제 답변 확인
    const lastProblem = appState.allProblems[appState.allProblems.length - 1];
    if (!appState.answered[lastProblem.id]) {
        alert('마지막 문제에 답변해주세요!');
        return;
    }
    
    // 정답 개수 계산
    let correctCount = 0;
    appState.allProblems.forEach(problem => {
        if (appState.userAnswers[problem.id] === problem.answer) {
            correctCount++;
        }
    });
    
    const totalCount = appState.allProblems.length;
    const correctRate = Math.round((correctCount / totalCount) * 100);
    
    // 결과 화면에 데이터 표시
    document.getElementById('resultName').textContent = appState.studentName;
    document.getElementById('resultDate').textContent = formatDate(appState.testDate);
    document.getElementById('correctCount').textContent = correctCount;
    document.getElementById('totalCount').textContent = totalCount;
    document.getElementById('correctRate').textContent = `${correctRate}%`;
    
    // 선택한 문제 목록 표시
    displaySelectedProblems();
    
    showScreen('resultScreen');
}

function displaySelectedProblems() {
    const container = document.getElementById('selectedProblemsTable');
    
    // 1. 선택 경로별 점수 (사용자가 선택한 경로)
    const selectionStats = {};
    appState.selectedProblems.forEach(selection => {
        const key = `${selection.method}|${selection.value}`;
        selectionStats[key] = {
            label: selection.label,
            method: selection.method,
            total: 0,
            correct: 0
        };
    });
    
    appState.allProblems.forEach(problem => {
        const key = `${problem.selectionMethod}|${problem.selectionValue}`;
        if (selectionStats[key]) {
            selectionStats[key].total++;
            if (appState.userAnswers[problem.id] === problem.answer) {
                selectionStats[key].correct++;
            }
        }
    });
    
    // 2. 연도/회차별로 자동 분류 (문제 ID 파싱)
    const yearRoundStats = {};
    appState.allProblems.forEach(problem => {
        const parts = problem.id.split('-');
        if (parts.length >= 2) {
            const year = parts[0];
            const round = parts[1];
            const key = `${year}-${round}`;
            if (!yearRoundStats[key]) {
                yearRoundStats[key] = {
                    label: `${year}년도 제${round}회`,
                    total: 0,
                    correct: 0
                };
            }
            yearRoundStats[key].total++;
            if (appState.userAnswers[problem.id] === problem.answer) {
                yearRoundStats[key].correct++;
            }
        }
    });
    
    // 3. 단원별로 자동 분류
    const categoryStats = {};
    appState.allProblems.forEach(problem => {
        const category = problem.category;
        if (!categoryStats[category]) {
            categoryStats[category] = {
                label: category,
                total: 0,
                correct: 0
            };
        }
        categoryStats[category].total++;
        if (appState.userAnswers[problem.id] === problem.answer) {
            categoryStats[category].correct++;
        }
    });
    
    // HTML 생성
    let html = '<div class="selection-summary">';
    
    // 선택 경로별 요약 (사용자가 선택한 경로)
    const byYearStats = Object.values(selectionStats).filter(s => s.method === 'byYear');
    const bySubjectStats = Object.values(selectionStats).filter(s => s.method === 'bySubject');
    
    if (byYearStats.length > 0) {
        html += '<h3>선택: 년도별 / 회차별</h3><div class="summary-items">';
        byYearStats.forEach(stat => {
            html += `<div class="summary-item">
                <span class="summary-label">${stat.label}</span>
                <span class="summary-score">${stat.correct}/${stat.total}점</span>
            </div>`;
        });
        html += '</div>';
    }
    
    if (bySubjectStats.length > 0) {
        html += '<h3>선택: 단원별</h3><div class="summary-items">';
        bySubjectStats.forEach(stat => {
            html += `<div class="summary-item">
                <span class="summary-label">${stat.label}</span>
                <span class="summary-score">${stat.correct}/${stat.total}점</span>
            </div>`;
        });
        html += '</div>';
    }
    
    // 자동 분류: 연도/회차별 (만약 여러 회차가 포함되어 있다면)
    const yearRoundArray = Object.values(yearRoundStats);
    if (yearRoundArray.length > 1) {
        html += '<h3>분류: 년도별 / 회차별</h3><div class="summary-items">';
        yearRoundArray.forEach(stat => {
            html += `<div class="summary-item">
                <span class="summary-label">${stat.label}</span>
                <span class="summary-score">${stat.correct}/${stat.total}점</span>
            </div>`;
        });
        html += '</div>';
    }
    
    // 자동 분류: 단원별 (만약 여러 단원이 포함되어 있다면)
    const categoryArray = Object.values(categoryStats);
    if (categoryArray.length > 1) {
        html += '<h3>분류: 단원별</h3><div class="summary-items">';
        categoryArray.forEach(stat => {
            html += `<div class="summary-item">
                <span class="summary-label">${stat.label}</span>
                <span class="summary-score">${stat.correct}/${stat.total}점</span>
            </div>`;
        });
        html += '</div>';
    }
    
    html += '</div>';
    
    // 상세 문제 목록
    html += '<h3 style="margin-top: 30px;">상세 문제 목록</h3>';
    html += '<table class="problems-table"><thead><tr><th>문제</th><th>정답</th><th>선택</th><th>결과</th></tr></thead><tbody>';
    
    appState.allProblems.forEach(problem => {
        const userAnswer = appState.userAnswers[problem.id];
        const isCorrect = userAnswer === problem.answer;
        const resultClass = isCorrect ? 'correct-answer' : 'wrong-answer';
        const resultText = isCorrect ? '✓ 정답' : '✗ 오답';
        
        const userAnswerText = userAnswer ? `${userAnswer}번` : '미응답';
        
        html += `
            <tr>
                <td>${problem.number}번</td>
                <td>${problem.answer}번</td>
                <td>${userAnswerText}</td>
                <td class="${resultClass}">${resultText}</td>
            </tr>
        `;
    });
    
    html += '</tbody></table>';
    container.innerHTML = html;
}

function formatDate(dateString) {
    const date = new Date(dateString + 'T00:00:00');
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}년 ${month}월 ${day}일`;
}

// ===== 결과 화면 =====
function retryQuiz() {
    appState.currentQuestionIndex = 0;
    appState.userAnswers = {};
    appState.answered = {};
    appState.allProblems.forEach(problem => {
        appState.userAnswers[problem.id] = null;
        appState.answered[problem.id] = false;
    });
    displayQuestion();
    showScreen('quizScreen');
}

function startNew() {
    appState = {
        testDate: '',
        studentName: '',
        selectedProblems: [],
        currentQuestionIndex: 0,
        userAnswers: {},
        allProblems: [],
        shuffledOptions: {},
        answered: {}
    };
    setDefaultDate();
    showScreen('infoScreen');
}
