import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random

load_dotenv()

class RedshiftTableSetup:
    def __init__(self):
        self.redshift_config = {
            'host': os.getenv('REDSHIFT_HOST'),
            'port': os.getenv('REDSHIFT_PORT', '5439'),
            'database': os.getenv('REDSHIFT_DB', 'dev'),
            'user': os.getenv('REDSHIFT_USER'),
            'password': os.getenv('REDSHIFT_PASSWORD')
        }
    
    def connect(self):
        """Connect to Redshift"""
        try:
            conn = psycopg2.connect(**self.redshift_config, connect_timeout=30)
            return conn
        except Exception as e:
            print(f"Connection failed: {e}")
            return None
    
    def create_tables(self):
        """Create all required tables"""
        conn = self.connect()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        # Drop existing tables
        drop_queries = [
            "DROP TABLE IF EXISTS sales_transactions CASCADE;",
            "DROP TABLE IF EXISTS expenses CASCADE;",
            "DROP TABLE IF EXISTS customers CASCADE;",
            "DROP TABLE IF EXISTS product_sales CASCADE;"
        ]
        
        # Create tables
        create_queries = [
            """
            CREATE TABLE sales_transactions (
                transaction_id VARCHAR(50) PRIMARY KEY,
                transaction_date DATE NOT NULL,
                region VARCHAR(50) NOT NULL,
                amount DECIMAL(12,2) NOT NULL,
                customer_id VARCHAR(50),
                product_id VARCHAR(50)
            );
            """,
            
            """
            CREATE TABLE expenses (
                expense_id VARCHAR(50) PRIMARY KEY,
                expense_date DATE NOT NULL,
                category VARCHAR(50) NOT NULL,
                amount DECIMAL(12,2) NOT NULL,
                description VARCHAR(200)
            );
            """,
            
            """
            CREATE TABLE customers (
                customer_id VARCHAR(50) PRIMARY KEY,
                first_purchase_date DATE NOT NULL,
                lifetime_value DECIMAL(12,2) NOT NULL,
                region VARCHAR(50)
            );
            """,
            
            """
            CREATE TABLE product_sales (
                sale_id VARCHAR(50) PRIMARY KEY,
                sale_date DATE NOT NULL,
                product_category VARCHAR(50) NOT NULL,
                quantity_sold INTEGER NOT NULL,
                revenue DECIMAL(12,2) NOT NULL,
                profit_margin DECIMAL(5,4) NOT NULL
            );
            """
        ]
        
        try:
            # Drop existing tables
            for query in drop_queries:
                cursor.execute(query)
                print(f"✅ Executed: {query.split()[2]}")
            
            # Create new tables
            for query in create_queries:
                cursor.execute(query)
                table_name = query.split()[2]
                print(f"✅ Created table: {table_name}")
            
            conn.commit()
            print("🎉 All tables created successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    
    def populate_mock_data(self):
        """Populate tables with mock data"""
        conn = self.connect()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        try:
            # Generate sales transactions
            print("📊 Generating sales transactions...")
            regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America']
            
            sales_data = []
            for i in range(1000):
                date = datetime.now() - timedelta(days=random.randint(1, 365))
                region = random.choice(regions)
                amount = round(random.uniform(100, 50000), 2)
                sales_data.append((f'TXN_{i:04d}', date.date(), region, amount, f'CUST_{i%200:04d}', f'PROD_{i%50:03d}'))
            
            cursor.executemany(
                "INSERT INTO sales_transactions VALUES (%s, %s, %s, %s, %s, %s)",
                sales_data
            )
            print(f"✅ Inserted {len(sales_data)} sales transactions")
            
            # Generate expenses
            print("💰 Generating expenses...")
            categories = ['Operations', 'Marketing', 'R&D', 'HR', 'IT', 'Legal']
            
            expense_data = []
            for i in range(500):
                date = datetime.now() - timedelta(days=random.randint(1, 365))
                category = random.choice(categories)
                amount = round(random.uniform(1000, 100000), 2)
                expense_data.append((f'EXP_{i:04d}', date.date(), category, amount, f'{category} expense {i}'))
            
            cursor.executemany(
                "INSERT INTO expenses VALUES (%s, %s, %s, %s, %s)",
                expense_data
            )
            print(f"✅ Inserted {len(expense_data)} expenses")
            
            # Generate customers
            print("👥 Generating customers...")
            customer_data = []
            for i in range(200):
                first_purchase = datetime.now() - timedelta(days=random.randint(30, 730))
                ltv = round(random.uniform(500, 10000), 2)
                region = random.choice(regions)
                customer_data.append((f'CUST_{i:04d}', first_purchase.date(), ltv, region))
            
            cursor.executemany(
                "INSERT INTO customers VALUES (%s, %s, %s, %s)",
                customer_data
            )
            print(f"✅ Inserted {len(customer_data)} customers")
            
            # Generate product sales
            print("🛍️ Generating product sales...")
            categories = ['Electronics', 'Clothing', 'Home & Garden', 'Books', 'Sports', 'Beauty']
            
            product_data = []
            for i in range(800):
                date = datetime.now() - timedelta(days=random.randint(1, 90))
                category = random.choice(categories)
                quantity = random.randint(1, 100)
                revenue = round(random.uniform(50, 5000), 2)
                margin = round(random.uniform(0.1, 0.7), 4)
                product_data.append((f'SALE_{i:04d}', date.date(), category, quantity, revenue, margin))
            
            cursor.executemany(
                "INSERT INTO product_sales VALUES (%s, %s, %s, %s, %s, %s)",
                product_data
            )
            print(f"✅ Inserted {len(product_data)} product sales")
            
            conn.commit()
            print("🎉 All mock data inserted successfully!")
            
            # Show table counts
            tables = ['sales_transactions', 'expenses', 'customers', 'product_sales']
            print("\n📈 Table Summary:")
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  {table}: {count:,} records")
            
            return True
            
        except Exception as e:
            print(f"❌ Error populating data: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
    
    def setup_complete_database(self):
        """Complete database setup"""
        print("🚀 Starting Redshift Database Setup")
        print("=" * 50)
        
        if self.create_tables():
            if self.populate_mock_data():
                print("\n✅ Database setup completed successfully!")
                print("Your RedshiftFinancialAgent is now ready to use!")
                return True
        
        print("\n❌ Database setup failed!")
        return False

if __name__ == "__main__":
    setup = RedshiftTableSetup()
    setup.setup_complete_database()