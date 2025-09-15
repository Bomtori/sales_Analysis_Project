# 📊 Sales Analysis Project

## 📌 프로젝트 개요
이 프로젝트는 **판매 데이터(Sales, Details)** 를 PostgreSQL DB에 적재하고,  
이를 **FastAPI 기반 백엔드**에서 API 형태로 제공하며,  
**React + Recharts 프론트엔드**에서 시각화하는 **풀스택 분석 애플리케이션**입니다.  

Docker + docker-compose 로 통합 구성되어,  
개발 환경에 상관없이 `docker-compose up` 한 번으로 실행 가능합니다.  

---

## 👥 팀원 역할

| 이름     | 담당 역할 |
|----------|-----------------------------------|
| **박범철** | 서버 구성, Docker 설정, PostgreSQL 구성 |
| **김현재** | FastAPI 백엔드 API 통신 설계 및 구현 |
| **박지예** | React 프론트엔드 개발 및 시각화 구현 |

---

## 📂 프로젝트 구조

```plaintext
.
├─ backend/                 # FastAPI 백엔드
│  ├─ app/
│  │   ├─ main.py           # FastAPI 진입점 (라우터 포함)
│  │   ├─ api/              # REST API 라우트
│  │   │   └─ analytics.py  # 판매 분석 API (연도별, 지역별 등)
│  │   ├─ db/
│  │   │   └─ session.py    # SQLAlchemy 세션 관리
│  │   └─ models/
│  │       └─ models.py     # DB 모델 정의 (Sales, Locations 등)
│  ├─ scripts/
│  │   ├─ seed.py           # Excel 데이터를 DB에 적재
│  │   └─ test_connection.py# DB 연결 테스트
│  ├─ requirements.txt      # Python 의존성
│  └─ Dockerfile            # Backend Docker 설정
│
├─ frontend/                # React 프론트엔드
│  ├─ src/
│  │   ├─ components/       # 차트 컴포넌트 (Recharts 기반)
│  │   │   ├─ CategoryYearChart.jsx
│  │   │   ├─ ChannelSalesChart.jsx
│  │   │   ├─ RegionSalesChart.jsx
│  │   │   ├─ PromotionSalesChart.jsx
│  │   │   └─ SummaryCard.jsx
│  │   ├─ pages/
│  │   │   └─ Dashboard.jsx # 대시보드 페이지
│  │   └─ utils/
│  │       └─ api.js        # 백엔드 API 호출 유틸
│  ├─ Dockerfile            # Frontend Docker 설정
│  ├─ nginx.conf            # Nginx 설정 (정적 파일 서빙)
│  └─ vite.config.js        # Vite 설정
│
├─ db/
│  └─ init.sql              # PostgreSQL 초기 스키마 생성
│
├─ data/
│  ├─ Sales.xlsx            # 판매 데이터
│  └─ Details.xlsx          # 세부 데이터
│
├─ docker-compose.yml       # 전체 서비스 오케스트레이션
├─ .env                     # 환경 변수 (DB, 포트 등)
└─ korean_to_english.py     # 데이터 전처리 스크립트
```

---

## ⚙️ 기술 스택

- **Backend**: FastAPI, SQLAlchemy, psycopg2  
- **Frontend**: React, Vite, Recharts  
- **Database**: PostgreSQL  
- **Infra**: Docker, docker-compose, Nginx  

---

## 🔄 동작 흐름

1. **데이터 적재**  
   - `data/Sales.xlsx`, `data/Details.xlsx` → `backend/scripts/seed.py` 실행 → PostgreSQL 테이블에 저장  
   - 스키마 정의: `db/init.sql`  

2. **백엔드 API (FastAPI)**  
   - `/api/analytics/` 엔드포인트 제공  
   - 예시:  
     - `GET /api/analytics/yearly` → 연도별 판매량  
     - `GET /api/analytics/region` → 지역별 판매량  
     - `GET /api/analytics/channel` → 판매 채널별 매출  
   - DB 세션 관리 (`app/db/session.py`) → SQLAlchemy ORM 활용  

3. **프론트엔드 (React + Recharts)**  
   - `src/utils/api.js` 에서 Axios 호출로 API 데이터 가져옴  
   - `Dashboard.jsx` 에서 차트 컴포넌트로 데이터 전달  
   - `Recharts` 라이브러리로 시각화 (막대 차트, 파이 차트 등)  

4. **서버 배포**  
   - `frontend/Dockerfile` → React 빌드 후 Nginx에서 정적 파일 서빙  
   - `backend/Dockerfile` → Uvicorn + FastAPI 실행  
   - `docker-compose.yml` → DB, Backend, Frontend 컨테이너를 묶어 실행  

---

## 🐳 Docker Compose 구성

```yaml
version: "3.9"
services:
  db:
    image: postgres:15
    container_name: postgres_db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: 1111
      POSTGRES_DB: sales_db
    volumes:
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    container_name: fastapi_backend
    depends_on:
      - db
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    container_name: react_frontend
    depends_on:
      - backend
    ports:
      - "80:80"

volumes:
  postgres_data:
```

---

## 🚀 실행 방법

```bash
# 1. 저장소 클론
git clone <repo_url>
cd sales_analysis_project

# 2. 환경 변수 설정 (.env)
cp .env.example .env

# 3. Docker Compose 실행
docker-compose up -d --build

# 4. 접속
# 프론트엔드 대시보드
http://localhost

# 백엔드 Swagger Docs
http://localhost:8000/docs
```

---

## 📈 주요 기능
- Excel 데이터를 PostgreSQL DB에 적재  
- REST API 제공 (연도/지역/채널별 매출 분석)  
- React 기반 판매 대시보드 시각화  
- Docker 기반 서버 자동화 실행  

---
