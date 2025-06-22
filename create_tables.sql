-- Drop existing tables if they exist
DROP TABLE IF EXISTS sales_transactions CASCADE;
DROP TABLE IF EXISTS expenses CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS product_sales CASCADE;

-- Create sales_transactions table
CREATE TABLE sales_transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    transaction_date DATE NOT NULL,
    region VARCHAR(50) NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    customer_id VARCHAR(50),
    product_id VARCHAR(50)
);

-- Create expenses table
CREATE TABLE expenses (
    expense_id VARCHAR(50) PRIMARY KEY,
    expense_date DATE NOT NULL,
    category VARCHAR(50) NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    description VARCHAR(200)
);

-- Create customers table
CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    first_purchase_date DATE NOT NULL,
    lifetime_value DECIMAL(12,2) NOT NULL,
    region VARCHAR(50)
);

-- Create product_sales table
CREATE TABLE product_sales (
    sale_id VARCHAR(50) PRIMARY KEY,
    sale_date DATE NOT NULL,
    product_category VARCHAR(50) NOT NULL,
    quantity_sold INTEGER NOT NULL,
    revenue DECIMAL(12,2) NOT NULL,
    profit_margin DECIMAL(5,4) NOT NULL
);

-- Verify tables were created
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('sales_transactions', 'expenses', 'customers', 'product_sales');