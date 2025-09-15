from sqlalchemy import func, extract
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models import models   # models/models.py
from app.models.models import RegionSales
from app.db import session      # db/session.py

router = APIRouter(prefix="/analytics", tags=["Analytics"])


# 1. 총 매출액 (Total Sales)
@router.get("/total_sales")
def total_sales(db: Session = Depends(session.get_db)):
    print("Hello")
    total = db.query(func.sum(models.Sale.quantity * models.Sale.unit_price)).scalar()
    return {"total_sales": float(total or 0)}


# 2. 총 매출 이익 (Total Profit)
@router.get("/total_profit")
def total_profit(db: Session = Depends(session.get_db)):
    total = (
        db.query(func.sum((models.Sale.unit_price - models.Product.cost) * models.Sale.quantity))
        .join(models.Product, models.Sale.product_id == models.Product.product_id)
        .scalar()
    )
    return {"total_profit": float(total or 0)}


# 3. 거래 건수 (Transaction Count)
@router.get("/transactions")
def transaction_count(db: Session = Depends(session.get_db)):
    count = db.query(func.count(models.Sale.sale_id)).scalar()
    return {"transactions": count}


# 4. 고객 수 (Unique Customers)
@router.get("/customers")
def customer_count(db: Session = Depends(session.get_db)):
    count = db.query(func.count(func.distinct(models.Sale.customer_id))).scalar()
    return {"customers": count}

# 5. 권역별 매출
@router.get("/sales_by_region")
def sales_by_region(db: Session = Depends(session.get_db)):
    rows = db.query(RegionSales).all()
    return [{"region": r.region, "sales": float(r.total_sales)} for r in rows]

# 6. 연도별 매출 (Sales by Year)
@router.get("/sales_by_year")
def sales_by_year(db: Session = Depends(session.get_db)):
    rows = (
        db.query(
            extract("year", models.Sale.date_id).label("year"),
            func.sum(models.Sale.quantity * models.Sale.unit_price).label("total_sales")
        )
        .group_by("year")
        .order_by("year")
        .all()
    )
    return [{"year": r[0], "sales": float(r[1])} for r in rows]


# 7. 채널별 매출 (Sales by Channel)
@router.get("/sales_by_channel")
def sales_by_channel(db: Session = Depends(session.get_db)):
    rows = (
        db.query(models.Channel.channel_name, func.sum(models.Sale.quantity * models.Sale.unit_price))
        .join(models.Channel, models.Sale.channel_id == models.Channel.channel_id)
        .group_by(models.Channel.channel_name)
        .all()
    )
    return [{"channel": r[0], "sales": float(r[1])} for r in rows]


# 8. 프로모션별 매출 (Sales by Promotion)
@router.get("/sales_by_promotion")
def sales_by_promotion(db: Session = Depends(session.get_db)):
    rows = (
        db.query(models.Promotion.promotion_name, func.sum(models.Sale.quantity * models.Sale.unit_price))
        .join(models.Promotion, models.Sale.promotion_id == models.Promotion.promotion_id)
        .group_by(models.Promotion.promotion_name)
        .all()
    )
    return [{"promotion": r[0], "sales": float(r[1])} for r in rows]


# 9. 연도별 분류 매출 (Sales by Year and Classification)
@router.get("/sales_by_year_and_classification")
def sales_by_year_and_classification(db: Session = Depends(session.get_db)):
    rows = (
        db.query(
            extract("year", models.Sale.date_id).label("year"),
            models.Classification.classification_name,
            func.sum(models.Sale.quantity * models.Sale.unit_price)
        )
        .join(models.Product, models.Sale.product_id == models.Product.product_id)
        .join(models.ProductClassification, models.Product.product_class_id == models.ProductClassification.product_class_id)
        .join(models.Classification, models.ProductClassification.classification_id == models.Classification.classification_id)
        .group_by("year", models.Classification.classification_name)
        .order_by("year", models.Classification.classification_name)
        .all()
    )
    return [{"year": int(r[0]), "classification": r[1], "sales": float(r[2])} for r in rows]


# 10. 연도별 이익률 (Profit Margin %)
@router.get("/profit_margin_by_year")
def profit_margin_by_year(db: Session = Depends(session.get_db)):
    rows = (
        db.query(
            extract("year", models.Sale.date_id).label("year"),
            func.sum(models.Sale.quantity * models.Sale.unit_price).label("total_sales"),
            func.sum((models.Sale.unit_price - models.Product.cost) * models.Sale.quantity).label("total_profit")
        )
        .join(models.Product, models.Sale.product_id == models.Product.product_id)
        .group_by("year")
        .order_by("year")
        .all()
    )

    results = []
    for year, total_sales, total_profit in rows:
        margin = (total_profit / total_sales * 100) if total_sales and total_sales > 0 else 0
        results.append({
            "year": int(year),
            "profit_margin_percent": round(margin, 2)
        })

    return results
