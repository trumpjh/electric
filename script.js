// 전역 상태 관리
let appState = {
    testDate: '',
    studentName: '',
    selectedProblems: [],
    currentQuestionIndex: 0,
    userAnswers: {},
    allProblems: []
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
    
    // 현재 활성 탭 확인
    const activeTab = document.querySelector('.tab-content.active').id;
    
    if (activeTab === 'byYear') {
        // 년도별 선택
        selectedCheckboxes.forEach(checkbox => {
            const key = checkbox.value;
            if (problemsData[key] && problemsData[key].problems) {
                appState.allProblems.push(...problemsData[key].problems);
            }
        });
    } else {
        // 단원별 선택
        selectedCheckboxes.forEach(checkbox => {
            const subject = checkbox.value;
            for (const key in problemsData) {
                if (problemsData[key].subject === subject && problemsData[key].problems) {
                    appState.allProblems.push(...problemsData[key].problems);
                }
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
    
    if (appState.allProblems.length === 0) {
        alert('선택된 카테고리에 문제가 없습니다. 먼저 문제를 추가해주세요!');
        return;
    }
    
    // 사용자 답변 초기화
    appState.userAnswers = {};
    appState.allProblems.forEach(problem => {
        appState.userAnswers[problem.id] = null;
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
    document.getElementById('questionNumber').textContent = `${problem.number}번`;
    document.getElementById('questionText').textContent = problem.text;
    
    // 선택지 표시
    const optionsContainer = document.getElementById('optionsContainer');
    optionsContainer.innerHTML = '';
    
    problem.options.forEach((option, index) => {
        const optionNum = index + 1;
        const optionDiv = document.createElement('div');
        optionDiv.className = 'option';
        
        const isSelected = appState.userAnswers[problem.id] === optionNum;
        if (isSelected) {
            optionDiv.classList.add('selected');
        }
        
        optionDiv.innerHTML = `
            <input type="radio" name="answer" value="${optionNum}" 
                   id="option${optionNum}" ${isSelected ? 'checked' : ''}>
            <label for="option${optionNum}" class="option-label">${option}</label>
        `;
        
        optionDiv.querySelector('input').addEventListener('change', function() {
            appState.userAnswers[problem.id] = optionNum;
            document.querySelectorAll('.option').forEach(opt => {
                opt.classList.remove('selected');
            });
            optionDiv.classList.add('selected');
        });
        
        optionsContainer.appendChild(optionDiv);
    });
    
    // 버튼 상태 업데이트
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');
    
    prevBtn.disabled = appState.currentQuestionIndex === 0;
    nextBtn.style.display = appState.currentQuestionIndex < total - 1 ? 'block' : 'none';
    submitBtn.style.display = appState.currentQuestionIndex === total - 1 ? 'block' : 'none';
}

function previousQuestion() {
    if (appState.currentQuestionIndex > 0) {
        appState.currentQuestionIndex--;
        displayQuestion();
    }
}

function nextQuestion() {
    if (appState.currentQuestionIndex < appState.allProblems.length - 1) {
        appState.currentQuestionIndex++;
        displayQuestion();
    }
}

function submitQuiz() {
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
    
    let html = '<table class="problems-table"><thead><tr><th>문제</th><th>정답</th><th>선택</th><th>결과</th></tr></thead><tbody>';
    
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
    appState.allProblems.forEach(problem => {
        appState.userAnswers[problem.id] = null;
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
        allProblems: []
    };
    setDefaultDate();
    showScreen('infoScreen');
}
