#!/bin/bash
set -e

# DB 연결 정보 (env 파일에서 불러옴)
HOST=${DB_HOST:-db}
PORT=${DB_PORT:-5432}
USER=${POSTGRES_USER:-myuser}
DB=${POSTGRES_DB:-mydb}

echo "⏳ Waiting for Postgres at $HOST:$PORT..."

# DB가 준비될 때까지 대기
until pg_isready -h $HOST -p $PORT -U $USER > /dev/null 2>&1; do
  echo "  ...still waiting"
  sleep 2
done

echo "✅ Postgres is ready!"

# seed.py 실행 (실패해도 FastAPI는 실행되도록 || true 사용 가능)
echo "🚀 Running seed.py..."
python scripts/seed.py || echo "⚠️ seed.py 실행 실패 (무시하고 계속 진행)"

# FastAPI 실행
echo "🚀 Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
