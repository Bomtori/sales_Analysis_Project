import pandas as pd
from sqlalchemy import create_engine, text
import os

DB_URL = os.getenv("DB_URL", "postgresql+psycopg2://myuser:mypass@db:5432/mydb")
engine = create_engine(DB_URL)

details_path = "/app/data/Details.xlsx"
sales_path = "/app/data/Sales.xlsx"

load_order = [
    "locations",
    "promotions",
    "channels",
    "dates",
    "classifications",
    "product_classes",
    "products",
    "customers"
]

def table_exists(table_name: str) -> bool:
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT to_regclass(:tname)"), {"tname": f"public.{table_name}"}
        ).scalar()
        return result is not None

for sheet in load_order:
    if not table_exists(sheet):
        raise RuntimeError(f"❌ 테이블 {sheet} 가 DB에 없음. init.sql 먼저 실행 필요!")

    df = pd.read_excel(details_path, sheet_name=sheet)
    df = df.where(pd.notnull(df), None)

    if sheet == "dates":
        # date_id는 SERIAL → 제거
        if "date_id" in df.columns:
            df = df.drop(columns=["date_id"])
        # Excel에서 yyyymmdd 형식이라면 변환
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

    if sheet == "customers":
        # 컬럼 보정: gender/birth_date 없으면 디폴트 채우기
        if "gender" not in df.columns:
            df["gender"] = "U"
        if "birth_date" not in df.columns:
            df["birth_date"] = pd.to_datetime("2000-01-01")

    df.to_sql(sheet, engine, if_exists="append", index=False, method="multi")
    print(f"✅ {sheet} 테이블 적재 완료")

# Sales
if not table_exists("sales"):
    raise RuntimeError("❌ 테이블 sales 가 DB에 없음. init.sql 먼저 실행 필요!")

sales_df = pd.read_excel(sales_path, sheet_name="sales")
sales_df = sales_df.where(pd.notnull(sales_df), None)

if "date_id" in sales_df.columns:
    sales_df["date_id"] = pd.to_datetime(sales_df["date_id"], format="%Y%m%d", errors="coerce")

sales_df.to_sql("sales", engine, if_exists="append", index=False, method="multi")
print("✅ sales 테이블 적재 완료")