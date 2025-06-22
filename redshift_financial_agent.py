import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Uncomment these for actual Redshift connection
import psycopg2
import pandas as pd

load_dotenv()

class RedshiftFinancialAgent:
    def __init__(self, name="RedshiftAnalyst"):
        self.name = name
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Redshift connection parameters
        self.redshift_config = {
            'host': os.getenv('REDSHIFT_HOST'),
            'port': os.getenv('REDSHIFT_PORT', '5439'),
            'database': os.getenv('REDSHIFT_DB', 'dev'),
            'user': os.getenv('REDSHIFT_USER', 'admin'),
            'password': os.getenv('REDSHIFT_PASSWORD')
        }
        
        # SQL query templates
        self.sql_queries = {
            'monthly_revenue': """
                SELECT 
                    DATE_TRUNC('month', transaction_date) as month,
                    region,
                    SUM(amount) as revenue
                FROM sales_transactions 
                WHERE transaction_date >= CURRENT_DATE - INTERVAL '12 months'
                GROUP BY 1, 2
                ORDER BY 1, 2
            """,
            
            'expense_breakdown': """
                SELECT 
                    DATE_TRUNC('month', expense_date) as month,
                    category,
                    SUM(amount) as total_expense
                FROM expenses 
                WHERE expense_date >= CURRENT_DATE - INTERVAL '12 months'
                GROUP BY 1, 2
                ORDER BY 1, 2
            """,
            
            'customer_metrics': """
                SELECT 
                    DATE_TRUNC('month', first_purchase_date) as month,
                    COUNT(DISTINCT customer_id) as new_customers,
                    AVG(lifetime_value) as avg_ltv
                FROM customers 
                WHERE first_purchase_date >= CURRENT_DATE - INTERVAL '12 months'
                GROUP BY 1
                ORDER BY 1
            """,
            
            'product_performance': """
                SELECT 
                    product_category,
                    SUM(quantity_sold) as units_sold,
                    SUM(revenue) as total_revenue,
                    AVG(profit_margin) as avg_margin
                FROM product_sales 
                WHERE sale_date >= CURRENT_DATE - INTERVAL '3 months'
                GROUP BY 1
                ORDER BY total_revenue DESC
            """
        }
    
    def connect_to_redshift(self):
        """Establish connection to Redshift with timeout and retry"""
        import time
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                conn = psycopg2.connect(
                    host=self.redshift_config['host'],
                    port=self.redshift_config['port'],
                    database=self.redshift_config['database'],
                    user=self.redshift_config['user'],
                    password=self.redshift_config['password'],
                    connect_timeout=30  # 30 second timeout
                )
                print(f"✅ Connected to Redshift successfully")
                return conn
            except psycopg2.OperationalError as e:
                if "timeout" in str(e).lower():
                    print(f"⚠️ Connection timeout (attempt {attempt + 1}/{max_retries})")
                    if attempt < max_retries - 1:
                        time.sleep(5)  # Wait 5 seconds before retry
                        continue
                print(f"❌ Network error: Check security groups and VPC settings")
                print(f"Error details: {e}")
                return None
            except Exception as e:
                print(f"❌ Connection error: {e}")
                return None
        
        print(f"❌ Failed to connect after {max_retries} attempts")
        return None
        
        # # Mock connection for demo
        # print("🔗 Connected to Redshift (Mock)")
        # return "mock_connection"
    
    def execute_query(self, query_name, custom_query=None):
        """Execute SQL query against Redshift"""
        conn = self.connect_to_redshift()
        if not conn:
            print(f"⚠️ Using mock data for {query_name}")
            return self.get_mock_data(query_name)
        
        query = custom_query or self.sql_queries.get(query_name)
        if not query:
            print(f"❌ No query found for: {query_name}")
            return []
        
        try:
            print(f"🔍 Executing query: {query_name}")
            df = pd.read_sql(query, conn)
            print(f"✅ Retrieved {len(df)} records from Redshift")
            return df.to_dict('records')
        except Exception as e:
            print(f"❌ Query execution error: {e}")
            print(f"⚠️ Falling back to mock data for {query_name}")
            return self.get_mock_data(query_name)
        finally:
            if conn:
                conn.close()
    
    def get_mock_data(self, query_name):
        """Mock data for demonstration"""
        mock_datasets = {
            'monthly_revenue': [
                {'month': '2024-01-01', 'region': 'North America', 'revenue': 2500000},
                {'month': '2024-02-01', 'region': 'North America', 'revenue': 2300000},
                {'month': '2024-03-01', 'region': 'North America', 'revenue': 2800000},
                {'month': '2024-01-01', 'region': 'Europe', 'revenue': 1800000},
                {'month': '2024-02-01', 'region': 'Europe', 'revenue': 1900000},
                {'month': '2024-03-01', 'region': 'Europe', 'revenue': 2100000},
            ],
            'expense_breakdown': [
                {'month': '2024-01-01', 'category': 'Operations', 'total_expense': 800000},
                {'month': '2024-02-01', 'category': 'Operations', 'total_expense': 750000},
                {'month': '2024-03-01', 'category': 'Operations', 'total_expense': 900000},
                {'month': '2024-01-01', 'category': 'Marketing', 'total_expense': 400000},
                {'month': '2024-02-01', 'category': 'Marketing', 'total_expense': 450000},
                {'month': '2024-03-01', 'category': 'Marketing', 'total_expense': 500000},
            ],
            'customer_metrics': [
                {'month': '2024-01-01', 'new_customers': 1250, 'avg_ltv': 2400},
                {'month': '2024-02-01', 'new_customers': 1180, 'avg_ltv': 2350},
                {'month': '2024-03-01', 'new_customers': 1420, 'avg_ltv': 2500},
            ],
            'product_performance': [
                {'product_category': 'Electronics', 'units_sold': 15000, 'total_revenue': 3200000, 'avg_margin': 0.35},
                {'product_category': 'Clothing', 'units_sold': 25000, 'total_revenue': 1800000, 'avg_margin': 0.55},
                {'product_category': 'Home & Garden', 'units_sold': 8000, 'total_revenue': 1200000, 'avg_margin': 0.42},
            ]
        }
        return mock_datasets.get(query_name, [])
    
    def generate_ai_analysis(self, data, analysis_type):
        """Generate AI-powered financial analysis"""
        # Convert Timestamp objects to strings for JSON serialization
        def json_serializer(obj):
            if hasattr(obj, 'isoformat'):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
        prompt = f"""
        As a senior financial analyst, analyze this {analysis_type} data:
        
        {json.dumps(data, indent=2, default=json_serializer)}
        
        Provide:
        1. Key trends and insights
        2. Performance drivers
        3. Risk factors
        4. Strategic recommendations
        5. Forecast implications
        
        Be specific and actionable.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a CFO-level financial analyst with expertise in data-driven insights."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    def create_comprehensive_report(self):
        """Generate comprehensive financial report from Redshift data"""
        print(f"\n{'='*80}")
        print("COMPREHENSIVE FINANCIAL ANALYSIS REPORT")
        print(f"Generated by: {self.name} | Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        
        # 1. Revenue Analysis
        print(f"\n📊 REVENUE ANALYSIS")
        print("-" * 50)
        revenue_data = self.execute_query('monthly_revenue')
        
        total_revenue = sum(r['revenue'] for r in revenue_data)
        print(f"Total Revenue (Last 3 months): ${total_revenue:,}")
        
        for item in revenue_data:
            print(f"{str(item['month'])[:7]}: ${item['revenue']:,} ({item['region']})")
        
        revenue_insights = self.generate_ai_analysis(revenue_data, "revenue")
        print(f"\n🤖 AI Insights - Revenue:")
        print(revenue_insights)
        
        # 2. Expense Analysis
        print(f"\n💰 EXPENSE ANALYSIS")
        print("-" * 50)
        expense_data = self.execute_query('expense_breakdown')
        
        total_expenses = sum(e['total_expense'] for e in expense_data)
        print(f"Total Expenses (Last 3 months): ${total_expenses:,}")
        
        for item in expense_data:
            print(f"{str(item['month'])[:7]}: ${item['total_expense']:,} ({item['category']})")
        
        expense_insights = self.generate_ai_analysis(expense_data, "expenses")
        print(f"\n🤖 AI Insights - Expenses:")
        print(expense_insights)
        
        # 3. Customer Metrics
        print(f"\n👥 CUSTOMER METRICS")
        print("-" * 50)
        customer_data = self.execute_query('customer_metrics')
        
        for item in customer_data:
            print(f"{str(item['month'])[:7]}: {item['new_customers']} new customers | Avg LTV: ${item['avg_ltv']:,}")
        
        # 4. Product Performance
        print(f"\n🛍️ PRODUCT PERFORMANCE")
        print("-" * 50)
        product_data = self.execute_query('product_performance')
        
        for item in product_data:
            print(f"{item['product_category']}: {item['units_sold']:,} units | "
                  f"${item['total_revenue']:,} revenue | {item['avg_margin']:.1%} margin")
        
        # 5. Executive Summary
        print(f"\n🎯 EXECUTIVE SUMMARY")
        print("-" * 50)
        
        summary_data = {
            'total_revenue': total_revenue,
            'total_expenses': total_expenses,
            'net_profit': total_revenue - total_expenses,
            'profit_margin': ((total_revenue - total_expenses) / total_revenue) * 100,
            'customer_growth': customer_data,
            'top_products': product_data[:2]
        }
        
        executive_summary = self.generate_ai_analysis(summary_data, "executive summary")
        print(executive_summary)
        
        return {
            'revenue_data': revenue_data,
            'expense_data': expense_data,
            'customer_data': customer_data,
            'product_data': product_data,
            'summary': summary_data,
            'ai_insights': {
                'revenue': revenue_insights,
                'expenses': expense_insights,
                'executive_summary': executive_summary
            },
            'generated_at': datetime.now().isoformat()
        }

# Usage example
if __name__ == "__main__":
    # Create and run the financial reporting agent
    agent = RedshiftFinancialAgent()
    
    # Generate comprehensive report
    report = agent.create_comprehensive_report()
    
    print(f"\n{'='*80}")
    print("Report generation completed successfully!")
    print(f"{'='*80}")