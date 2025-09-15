from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Numeric, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


# 📌 Location Table
class Location(Base):
    __tablename__ = "locations"

    location_id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=False)
    district = Column(String, nullable=False)
    region = Column(String, nullable=False)

    customers = relationship("Customer", back_populates="location")


# 📌 Promotion Table
class Promotion(Base):
    __tablename__ = "promotions"

    promotion_id = Column(Integer, primary_key=True, autoincrement=True)
    promotion_name = Column(String, nullable=False)
    discount_rate = Column(Float)

    sales = relationship("Sale", back_populates="promotion")


# 📌 Channel Table
class Channel(Base):
    __tablename__ = "channels"

    channel_id = Column(Integer, primary_key=True, autoincrement=True)
    channel_name = Column(String, nullable=False)

    sales = relationship("Sale", back_populates="channel")


# 📌 Date Dimension Table
class DateDim(Base):
    __tablename__ = "dates"

    date_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    month_no = Column(Integer, nullable=False)
    month_name = Column(String, nullable=False)

# 📌 Customer Table
class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    location_id = Column(Integer, ForeignKey("locations.location_id"), nullable=False)
    customer_name = Column(String, nullable=False)
    gender = Column(String(1), nullable=False)
    birth_date = Column(Date, nullable=False)

    location = relationship("Location", back_populates="customers")
    sales = relationship("Sale", back_populates="customer")


# 📌 Classification Table
class Classification(Base):
    __tablename__ = "classifications"

    classification_id = Column(Integer, primary_key=True, autoincrement=True)
    classification_name = Column(String, nullable=False)

    product_classes = relationship("ProductClassification", back_populates="classification")


# 📌 Product Classification Table
class ProductClassification(Base):
    __tablename__ = "product_classes"

    product_class_id = Column(String, primary_key=True)
    product_class_name = Column(String, nullable=False)
    classification_id = Column(Integer, ForeignKey("classifications.classification_id"), nullable=False)

    classification = relationship("Classification", back_populates="product_classes")
    products = relationship("Product", back_populates="product_classification")


# 📌 Product Table
class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    cost = Column(Numeric(10, 2), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    product_class_id = Column(String, ForeignKey("product_classes.product_class_id"), nullable=False)

    product_classification = relationship("ProductClassification", back_populates="products")
    sales = relationship("Sale", back_populates="product")


# 📌 Sales Fact Table
class Sale(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True, index=True)
    date_id = Column(DateTime, nullable=False)   # ✅ 그냥 DateTime
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    promotion_id = Column(Integer, ForeignKey("promotions.promotion_id"))
    channel_id = Column(Integer, ForeignKey("channels.channel_id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    city = Column(String, nullable=False)        # ✅ 그냥 String

    # ✅ FK 있는 것만 relationship 유지
    promotion = relationship("Promotion", back_populates="sales")
    channel = relationship("Channel", back_populates="sales")
    customer = relationship("Customer", back_populates="sales")
    product = relationship("Product", back_populates="sales")

class RegionSales(Base):
    __tablename__ = "region_sales"
    __table_args__ = {"extend_existing": True}

    region = Column(String, primary_key=True)
    total_sales = Column(Numeric(10,2))
