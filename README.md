# Steam Analytics Dashboard

스팀 게임 분석 대시보드 - 실시간 게임 통계 및 인기 게임 분석

## 🚀 주요 기능

### 1. Top 10 동시접속자수
- 실시간 스팀 Top 100 게임 중 상위 10개 게임의 동시접속자수 분석
- 게임명, 현재 접속자수, 최고 접속자수, 장르, 출시일 정보 표시
- 인터랙티브 바 차트로 시각화

### 2. 인기 장르 분석
- 장르별 현재 접속자수 통계
- 장르별 게임 수 통계
- 장르별 평균 접속자수 분석
- 원형 차트와 상세 통계 테이블 제공
- 접속자수/게임수/평균 접속자수 기준 정렬 가능

### 3. 인기 카테고리 분석
- 카테고리별 현재 접속자수 통계
- 카테고리별 게임 수 통계
- 카테고리별 평균 접속자수 분석
- 상세 통계 테이블 제공

### 4. 게임 세부 검색
- 개별 게임의 상세 정보 검색
- 게임명, 장르, 카테고리, 출시일, 가격, 설명 정보
- 게임 헤더 이미지 표시

## 🛠️ 기술 스택

- **Frontend**: Streamlit (Python 웹 프레임워크)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Streamlit Charts
- **Data Collection**: Selenium, Requests, Steam API
- **Language**: Python 3.x

## 📦 설치 및 실행

### 로컬 실행

1. **저장소 클론**
```bash
git clone <repository-url>
cd project_1
```

2. **의존성 설치**
```bash
pip install -r requirements.txt
```

3. **앱 실행**
```bash
streamlit run steam_analytics/dashboard/streamlit_app.py
```

4. **브라우저에서 접속**
```
http://localhost:8501
```

## 🌐 배포 방법

### 1. Streamlit Cloud (추천 - 무료)

1. **GitHub에 코드 업로드**
   - 이 프로젝트를 GitHub 저장소에 푸시

2. **Streamlit Cloud에서 배포**
   - [share.streamlit.io](https://share.streamlit.io) 접속
   - GitHub 계정으로 로그인
   - 저장소 선택 및 배포

### 2. Heroku

1. **Procfile 생성**
```
web: streamlit run steam_analytics/dashboard/streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

2. **Heroku CLI로 배포**
```bash
heroku create your-app-name
git push heroku main
```

### 3. Docker

1. **Dockerfile 생성**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "steam_analytics/dashboard/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. **Docker 실행**
```bash
docker build -t steam-analytics .
docker run -p 8501:8501 steam-analytics
```

## 📊 데이터 업데이트

- 스크레이퍼를 수동으로 실행하여 최신 데이터 수집
- 캐시된 데이터는 1시간 동안 유지
- 실시간 데이터는 Steam Charts와 Steam API에서 직접 수집

## 📁 프로젝트 구조

```
steam_analytics/
│
├── scraper/               # 데이터 수집 모듈
│   ├── fetch_realtime_top100.py    # 실시간 Top 100 게임 데이터
│   ├── fetch_game_metadata.py      # 게임 메타데이터 수집
│   └── config.py                   # 설정 파일
│
├── dashboard/             # 대시보드
│   ├── streamlit_app.py            # 메인 Streamlit 앱 (4가지 기능)
│   └── static/
│       └── style.css               # CSS 스타일
│
└── data/                  # 데이터 저장소
    └── raw/               # 원본 데이터
        ├── top100_games_*.json     # Top 100 게임 데이터
        └── game_metadata_*.json    # 게임 메타데이터
```

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해 주세요.

## ⚡️ 로컬 실행 vs. 배포(Cloud) 실행 안내

- **로컬 실행**: 직접 스크레이퍼를 돌려 최신 데이터를 생성/분석할 수 있습니다. (스크레이퍼 실행 시 requirements.txt의 주석 처리된 패키지도 설치 필요)
- **배포(Cloud) 실행**: 샘플 데이터가 포함되어 있으므로 별도의 데이터 수집 없이 바로 대시보드가 동작합니다.
- **샘플 데이터 생성**: 필요시 `python create_sample_data.py`로 샘플 데이터를 생성할 수 있습니다.
- **데이터 파일 관리**: 로컬에서는 대용량 데이터가 쌓일 수 있으니, `.gitignore`에서 데이터 파일은 git에 포함되지 않도록 관리합니다. 