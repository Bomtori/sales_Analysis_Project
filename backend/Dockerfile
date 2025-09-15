FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 🔑 Postgres client 설치 (pg_isready 포함)
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# ⚠️ .dockerignore 설정이 없으면 .venv까지 전부 복사됨 → 빌드 무거워짐
# 👉 루트에 .dockerignore 파일 만들고 불필요한 것 제외:
# .git
# .venv
# __pycache__
# *.pyc
# *.pyo

COPY . .

RUN chmod +x start.sh

# CMD는 기본 프로세스만 실행
CMD ["./start.sh"]
