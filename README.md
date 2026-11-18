# 11주차 Python pytest 실습

## 1. 프로젝트 소개
성적 CSV 파일을 읽어 학생의 이름과 점수를 추출하는 파이썬 프로그램입니다.

## 2. 주요 기능
- CSV 파일 읽기
- 이름과 점수 구분
- 점수 유효성 검사
- 잘못된 데이터 건너뛰기
- 유효한 데이터와 건너뛴 데이터 반환

## 3. 실행 환경
- Python 3.12
- pytest
- pytest-cov

## 4. 실행 방법
다음 명령어로 테스트를 실행할 수 있습니다.

```bash
python -m pytest -v
```

커버리지를 확인하려면 다음 명령어를 실행합니다.

```bash
python -m pytest --cov=load_scores --cov-report=term-missing
```

## 5. 테스트 결과
- 직접 작성한 테스트: 8개 통과
- AI A 테스트: 13개 통과
- AI B 테스트: 12개 통과
- 전체 테스트: 33개 통과
- 커버리지: 80%

## 6. 사용 도구
- Visual Studio Code
- Python
- pytest
- ChatGPT
- GitHub
