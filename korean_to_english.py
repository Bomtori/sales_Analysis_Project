import pandas as pd
import os

# 한글 → 영어 매핑
SALES_COLUMNS = {
    "날짜": "date",
    "제품코드": "product_id",
    "고객코드": "customer_id",
    "프로모션코드": "promotion_id",
    "채널코드": "channel_id",
    "지역": "region",
    "quantity": "quantity",
    "unitprice": "unitprice"
}

DETAILS_COLUMNS = {
    "제품코드": "product_id",
    "제품명": "product_name",
    "카테고리": "category",
    "가격": "price"
}

# 경로 설정 (상황에 맞게 조정)
DATA_DIR = "./data"       # 프로젝트 폴더 안의 data 디렉토리
OUTPUT_DIR = "./data/converted"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_sales():
    df = pd.read_excel(f"{DATA_DIR}/Sales.xlsx")
    df = df.rename(columns=SALES_COLUMNS)
    output_path = f"{OUTPUT_DIR}/Sales_converted.xlsx"
    df.to_excel(output_path, index=False)
    print(f"✅ Sales 변환 완료 → {output_path}")

def convert_details():
    df = pd.read_excel(f"{DATA_DIR}/Details.xlsx")
    df = df.rename(columns=DETAILS_COLUMNS)
    output_path = f"{OUTPUT_DIR}/Details_converted.xlsx"
    df.to_excel(output_path, index=False)
    print(f"✅ Details 변환 완료 → {output_path}")

if __name__ == "__main__":
    convert_sales()
    convert_details()
