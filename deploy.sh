#!/bin/bash

echo "🚀 Steam Analytics Dashboard 배포 스크립트"
echo "=========================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git이 설치되어 있지 않습니다. 먼저 Git을 설치해주세요."
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "📁 Git 저장소 초기화 중..."
    git init
    git add .
    git commit -m "Initial commit"
fi

echo "📋 배포 옵션을 선택하세요:"
echo "1. Streamlit Cloud (추천 - 무료)"
echo "2. Heroku"
echo "3. Docker"
echo "4. 로컬 테스트"

read -p "선택 (1-4): " choice

case $choice in
    1)
        echo "🌐 Streamlit Cloud 배포 준비 중..."
        echo "1. GitHub에 코드를 푸시하세요:"
        echo "   git remote add origin <your-github-repo-url>"
        echo "   git push -u origin main"
        echo ""
        echo "2. https://share.streamlit.io 에서 배포하세요"
        echo "3. GitHub 계정으로 로그인"
        echo "4. 저장소 선택 후 배포"
        ;;
    2)
        echo "☁️ Heroku 배포 준비 중..."
        if ! command -v heroku &> /dev/null; then
            echo "❌ Heroku CLI가 설치되어 있지 않습니다."
            echo "https://devcenter.heroku.com/articles/heroku-cli 에서 설치하세요."
            exit 1
        fi
        
        echo "Heroku 앱 생성 중..."
        heroku create steam-analytics-$(date +%s)
        echo "배포 중..."
        git push heroku main
        echo "✅ 배포 완료! 앱 URL: $(heroku info -s | grep web_url | cut -d= -f2)"
        ;;
    3)
        echo "🐳 Docker 배포 준비 중..."
        if ! command -v docker &> /dev/null; then
            echo "❌ Docker가 설치되어 있지 않습니다."
            echo "https://docs.docker.com/get-docker/ 에서 설치하세요."
            exit 1
        fi
        
        echo "Docker 이미지 빌드 중..."
        docker build -t steam-analytics .
        echo "Docker 컨테이너 실행 중..."
        docker run -d -p 8501:8501 --name steam-analytics-app steam-analytics
        echo "✅ 배포 완료! http://localhost:8501 에서 접속하세요."
        ;;
    4)
        echo "🧪 로컬 테스트 실행 중..."
        streamlit run steam_analytics/dashboard/streamlit_app.py
        ;;
    *)
        echo "❌ 잘못된 선택입니다."
        exit 1
        ;;
esac

echo ""
echo "🎉 배포가 완료되었습니다!" 