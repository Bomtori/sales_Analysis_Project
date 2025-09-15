-- Sales 테이블 (매출 요약)
CREATE TABLE IF NOT EXISTS sales (
                                     sale_id SERIAL PRIMARY KEY,
                                     sale_date DATE NOT NULL,
                                     region VARCHAR(100),
    product VARCHAR(100),
    total_quantity INT,
    total_amount NUMERIC(12,2),
    created_at TIMESTAMP DEFAULT NOW()
    );

-- Details 테이블 (거래 상세)
CREATE TABLE IF NOT EXISTS details (
                                       detail_id SERIAL PRIMARY KEY,
                                       sale_id INT REFERENCES sales(sale_id) ON DELETE CASCADE,
    customer_id VARCHAR(50),
    product VARCHAR(100),
    quantity INT,
    price NUMERIC(10,2),
    discount NUMERIC(5,2),
    amount NUMERIC(12,2),
    region VARCHAR(100),
    transaction_date DATE,
    created_at TIMESTAMP DEFAULT NOW()
    );

-- Customers 테이블 (선택)
CREATE TABLE IF NOT EXISTS customers (
                                         customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    city VARCHAR(100),
    join_date DATE
    );
