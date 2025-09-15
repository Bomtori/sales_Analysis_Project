import pandas as pd
from sqlalchemy import create_engine

# DB 연결 URL
DB_URL = "postgresql+psycopg2://myuser:mypass@127.0.0.1:5433/mydb"


# 엔진 생성
engine = create_engine(DB_URL)

# 1. Sales.xlsx → sales 테이블
def load_sales():
    df = pd.read_excel("C:/Users/tj/Desktop/0915_project/data/Sales.xlsx")  # 위치 맞게 수정
    df.columns = [c.lower() for c in df.columns]  # 컬럼명 소문자 변환
    df.to_sql("sales", engine, if_exists="append", index=False)
    print("✅ Sales 데이터 적재 완료")

# 2. Details.xlsx → details 테이블
def load_details():
    df = pd.read_excel("C:/Users/tj/Desktop/0915_project/data/Details.xlsx")
    df.columns = [c.lower() for c in df.columns]
    df.to_sql("details", engine, if_exists="append", index=False)
    print("✅ Details 데이터 적재 완료")

# (선택) customers 테이블 생성
def load_customers():
    df = pd.read_excel("../Details.xlsx")  # 고객 정보가 Details에 포함된 경우
    if "customer_id" in df.columns and "customer_name" in df.columns:
        customers = df[["customer_id", "customer_name"]].drop_duplicates()
        customers.to_sql("customers", engine, if_exists="append", index=False)
        print("✅ Customers 데이터 적재 완료")

if __name__ == "__main__":
    load_sales()
    load_details()
    load_customers()
