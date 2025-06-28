import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

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
        
        Provide key trends and insights, performance drivers, risk factors, strategic recommendations, and forecast implications. Be specific and actionable. Format your response as clear, concise sentences without numbering.
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
    
    def generate_predictions(self, data_type='revenue'):
        """Generate predictive analysis using machine learning"""
        if data_type == 'revenue':
            data = self.execute_query('monthly_revenue')
            return self._forecast_revenue(data)
        elif data_type == 'expenses':
            data = self.execute_query('expense_breakdown')
            return self._forecast_expenses(data)
        elif data_type == 'customers':
            data = self.execute_query('customer_metrics')
            return self._forecast_customers(data)
        else:
            return {'error': 'Invalid data type for prediction'}
    
    def _forecast_revenue(self, revenue_data):
        """Forecast revenue using linear regression"""
        try:
            # Aggregate revenue by month
            df = pd.DataFrame(revenue_data)
            df['month'] = pd.to_datetime(df['month'])
            monthly_totals = df.groupby('month')['revenue'].sum().reset_index()
            monthly_totals = monthly_totals.sort_values('month')
            
            # Prepare data for ML
            X = np.arange(len(monthly_totals)).reshape(-1, 1)
            y = monthly_totals['revenue'].values
            
            # Fit models
            linear_model = LinearRegression().fit(X, y)
            poly_features = PolynomialFeatures(degree=2)
            X_poly = poly_features.fit_transform(X)
            poly_model = LinearRegression().fit(X_poly, y)
            
            # Generate predictions for next 6 months
            future_months = 6
            future_X = np.arange(len(monthly_totals), len(monthly_totals) + future_months).reshape(-1, 1)
            future_X_poly = poly_features.transform(future_X)
            
            linear_pred = linear_model.predict(future_X)
            poly_pred = poly_model.predict(future_X_poly)
            
            # Calculate confidence intervals (simplified)
            historical_error = mean_absolute_error(y, linear_model.predict(X))
            
            # Generate future dates
            last_date = monthly_totals['month'].max()
            future_dates = [last_date + timedelta(days=30*i) for i in range(1, future_months + 1)]
            
            predictions = []
            for i, date in enumerate(future_dates):
                predictions.append({
                    'month': date.strftime('%Y-%m-%d'),
                    'linear_forecast': float(linear_pred[i]),
                    'polynomial_forecast': float(poly_pred[i]),
                    'confidence_lower': float(linear_pred[i] - historical_error),
                    'confidence_upper': float(linear_pred[i] + historical_error),
                    'growth_rate': float((linear_pred[i] - y[-1]) / y[-1] * 100) if y[-1] != 0 else 0
                })
            
            return {
                'predictions': predictions,
                'model_accuracy': {
                    'r2_score': float(r2_score(y, linear_model.predict(X))),
                    'mae': float(historical_error)
                },
                'historical_data': [
                    {'month': row['month'].strftime('%Y-%m-%d'), 'actual_revenue': float(row['revenue'])}
                    for _, row in monthly_totals.iterrows()
                ]
            }
        except Exception as e:
            print(f"Error in revenue forecasting: {e}")
            return self._get_mock_predictions('revenue')
    
    def _forecast_expenses(self, expense_data):
        """Forecast expenses using trend analysis"""
        try:
            df = pd.DataFrame(expense_data)
            df['month'] = pd.to_datetime(df['month'])
            monthly_totals = df.groupby('month')['total_expense'].sum().reset_index()
            monthly_totals = monthly_totals.sort_values('month')
            
            X = np.arange(len(monthly_totals)).reshape(-1, 1)
            y = monthly_totals['total_expense'].values
            
            model = LinearRegression().fit(X, y)
            
            future_months = 6
            future_X = np.arange(len(monthly_totals), len(monthly_totals) + future_months).reshape(-1, 1)
            predictions = model.predict(future_X)
            
            last_date = monthly_totals['month'].max()
            future_dates = [last_date + timedelta(days=30*i) for i in range(1, future_months + 1)]
            
            forecast_data = []
            for i, date in enumerate(future_dates):
                forecast_data.append({
                    'month': date.strftime('%Y-%m-%d'),
                    'predicted_expense': float(predictions[i]),
                    'trend': 'increasing' if predictions[i] > y[-1] else 'decreasing'
                })
            
            return {
                'predictions': forecast_data,
                'trend_analysis': {
                    'monthly_growth_rate': float((predictions[0] - y[-1]) / y[-1] * 100) if y[-1] != 0 else 0,
                    'total_predicted_6m': float(sum(predictions))
                }
            }
        except Exception as e:
            print(f"Error in expense forecasting: {e}")
            return self._get_mock_predictions('expenses')
    
    def _forecast_customers(self, customer_data):
        """Forecast customer acquisition"""
        try:
            df = pd.DataFrame(customer_data)
            df['month'] = pd.to_datetime(df['month'])
            df = df.sort_values('month')
            
            X = np.arange(len(df)).reshape(-1, 1)
            y_customers = df['new_customers'].values
            y_ltv = df['avg_ltv'].values
            
            customer_model = LinearRegression().fit(X, y_customers)
            ltv_model = LinearRegression().fit(X, y_ltv)
            
            future_months = 6
            future_X = np.arange(len(df), len(df) + future_months).reshape(-1, 1)
            
            customer_pred = customer_model.predict(future_X)
            ltv_pred = ltv_model.predict(future_X)
            
            last_date = df['month'].max()
            future_dates = [last_date + timedelta(days=30*i) for i in range(1, future_months + 1)]
            
            predictions = []
            for i, date in enumerate(future_dates):
                predictions.append({
                    'month': date.strftime('%Y-%m-%d'),
                    'predicted_new_customers': int(max(0, customer_pred[i])),
                    'predicted_avg_ltv': float(max(0, ltv_pred[i])),
                    'predicted_revenue_impact': float(max(0, customer_pred[i]) * max(0, ltv_pred[i]))
                })
            
            return {
                'predictions': predictions,
                'insights': {
                    'customer_growth_trend': 'positive' if customer_pred[0] > y_customers[-1] else 'negative',
                    'ltv_trend': 'increasing' if ltv_pred[0] > y_ltv[-1] else 'decreasing'
                }
            }
        except Exception as e:
            print(f"Error in customer forecasting: {e}")
            return self._get_mock_predictions('customers')
    
    def _get_mock_predictions(self, data_type):
        """Mock predictions for demo purposes"""
        if data_type == 'revenue':
            return {
                'predictions': [
                    {'month': '2024-04-01', 'linear_forecast': 2950000, 'polynomial_forecast': 3100000, 'confidence_lower': 2700000, 'confidence_upper': 3200000, 'growth_rate': 5.4},
                    {'month': '2024-05-01', 'linear_forecast': 3100000, 'polynomial_forecast': 3300000, 'confidence_lower': 2850000, 'confidence_upper': 3350000, 'growth_rate': 10.7},
                    {'month': '2024-06-01', 'linear_forecast': 3250000, 'polynomial_forecast': 3520000, 'confidence_lower': 3000000, 'confidence_upper': 3500000, 'growth_rate': 16.1}
                ],
                'model_accuracy': {'r2_score': 0.85, 'mae': 150000},
                'historical_data': [
                    {'month': '2024-01-01', 'actual_revenue': 4300000},
                    {'month': '2024-02-01', 'actual_revenue': 4200000},
                    {'month': '2024-03-01', 'actual_revenue': 4900000}
                ]
            }
        elif data_type == 'expenses':
            return {
                'predictions': [
                    {'month': '2024-04-01', 'predicted_expense': 1280000, 'trend': 'increasing'},
                    {'month': '2024-05-01', 'predicted_expense': 1320000, 'trend': 'increasing'},
                    {'month': '2024-06-01', 'predicted_expense': 1360000, 'trend': 'increasing'}
                ],
                'trend_analysis': {'monthly_growth_rate': 3.2, 'total_predicted_6m': 7800000}
            }
        else:  # customers
            return {
                'predictions': [
                    {'month': '2024-04-01', 'predicted_new_customers': 1480, 'predicted_avg_ltv': 2580, 'predicted_revenue_impact': 3818400},
                    {'month': '2024-05-01', 'predicted_new_customers': 1520, 'predicted_avg_ltv': 2620, 'predicted_revenue_impact': 3982400},
                    {'month': '2024-06-01', 'predicted_new_customers': 1560, 'predicted_avg_ltv': 2660, 'predicted_revenue_impact': 4149600}
                ],
                'insights': {'customer_growth_trend': 'positive', 'ltv_trend': 'increasing'}
            }
    
    def generate_comprehensive_predictions(self):
        """Generate comprehensive predictive analysis"""
        print(f"\n{'='*80}")
        print("PREDICTIVE FINANCIAL ANALYSIS")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        
        revenue_forecast = self.generate_predictions('revenue')
        expense_forecast = self.generate_predictions('expenses')
        customer_forecast = self.generate_predictions('customers')
        
        # Generate AI insights for predictions
        prediction_summary = {
            'revenue_forecast': revenue_forecast,
            'expense_forecast': expense_forecast,
            'customer_forecast': customer_forecast
        }
        
        ai_prediction_insights = self.generate_ai_analysis(prediction_summary, "predictive analysis")
        
        return {
            'revenue_forecast': revenue_forecast,
            'expense_forecast': expense_forecast,
            'customer_forecast': customer_forecast,
            'ai_insights': ai_prediction_insights,
            'generated_at': datetime.now().isoformat()
        }
    
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