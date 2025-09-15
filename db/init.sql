-- 1. locations
CREATE TABLE locations (
                           location_id INT PRIMARY KEY,
                           city VARCHAR(100) NOT NULL,
                           district VARCHAR(100) NOT NULL,
                           region VARCHAR(100) NOT NULL
);

-- 2. promotions
CREATE TABLE promotions (
                            promotion_id SERIAL PRIMARY KEY,
                            promotion_name VARCHAR(100) NOT NULL,
                            discount_rate FLOAT
);

-- 3. channels
CREATE TABLE channels (
                          channel_id SERIAL PRIMARY KEY,
                          channel_name VARCHAR(100) NOT NULL
);

-- 4. dates
CREATE TABLE dates (
                       date_id SERIAL PRIMARY KEY,
                       date DATE NOT NULL,
                       year INT NOT NULL,
                       quarter INT NOT NULL,
                       month_no INT NOT NULL,
                       month_name VARCHAR(50) NOT NULL
);

-- 5. classifications
CREATE TABLE classifications (
                                 classification_id SERIAL PRIMARY KEY,
                                 classification_name VARCHAR(100) NOT NULL
);

-- 6. customers
CREATE TABLE customers (
                           customer_id SERIAL PRIMARY KEY,
                           location_id INT REFERENCES locations(location_id) NOT NULL,
                           customer_name VARCHAR(100) NOT NULL,
                           gender CHAR(1) NOT NULL,
                           birth_date DATE NOT NULL
);

-- 7. product_classes
CREATE TABLE product_classes (
                                 product_class_id VARCHAR PRIMARY KEY,
                                 product_class_name VARCHAR(100) NOT NULL,
                                 classification_id INT REFERENCES classifications(classification_id) NOT NULL
);

-- 8. products
CREATE TABLE products (
                          product_id SERIAL PRIMARY KEY,
                          product_name VARCHAR(100) NOT NULL,
                          color VARCHAR(50) NOT NULL,
                          cost NUMERIC(10,2) NOT NULL,
                          price NUMERIC(10,2) NOT NULL,
                          product_class_id VARCHAR REFERENCES product_classes(product_class_id) NOT NULL
);

-- 9. sales
CREATE TABLE sales (
                       sale_id SERIAL PRIMARY KEY,
                       date_id TIMESTAMP NOT NULL,
                       product_id INT REFERENCES products(product_id) NOT NULL,
                       customer_id INT REFERENCES customers(customer_id) NOT NULL,
                       promotion_id INT REFERENCES promotions(promotion_id),
                       channel_id INT REFERENCES channels(channel_id),
                       quantity INT NOT NULL,
                       unit_price NUMERIC(10,2) NOT NULL,
                       city VARCHAR(100) NOT NULL
);

-- 10. RegionSales (권역 집계 뷰)
CREATE OR REPLACE VIEW region_sales AS
SELECT
    CASE
        -- 수도권
        WHEN city IN ('서울', '인천', '수원', '성남', '고양', '부천', '안양', '안산', '의정부',
                      '남양주', '안성', '과천', '용인', '동두천', '광명', '김포', '구리', '이천',
                      '평택', '의왕', '파주', '군포', '하남', '양주', '양평', '연천', '가평', '오산')
            THEN '수도권'

        -- 충청권
        WHEN city IN ('대전', '세종', '청주', '천안', '공주', '제천')
            THEN '충청권'

        -- 영남권
        WHEN city IN ('부산', '대구', '울산', '창원', '김해', '포항', '진주', '밀양', '안동', '양산', '통영')
            THEN '영남권'

        -- 강원권
        WHEN city IN ('춘천', '원주', '강릉', '속초', '동해', '태백')
            THEN '강원권'

        -- 호남권
        WHEN city IN ('광주', '전주', '군산', '익산', '목포', '여수', '나주', '담양')
            THEN '호남권'

        -- 제주권
        WHEN city IN ('제주')
            THEN '제주권'

        ELSE '기타'
        END AS region,
    SUM(quantity * unit_price) AS total_sales
FROM sales
GROUP BY region;
