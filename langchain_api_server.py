from flask import Flask, jsonify
from flask_cors import CORS
from langchain_redshift_agent import LangChainRedshiftAgent

app = Flask(__name__)
CORS(app)

@app.route('/api/report', methods=['GET'])
def get_financial_report():
    try:
        from langchain_redshift_agent import query_redshift_data
        import json
        
        # Get actual data from the database/mock
        revenue_data = json.loads(query_redshift_data('monthly_revenue'))
        expense_data = json.loads(query_redshift_data('expense_breakdown'))
        customer_data = json.loads(query_redshift_data('customer_metrics'))
        
        # Add product data (mock for now)
        product_data = [
            {'product_category': 'Electronics', 'units_sold': 15000, 'total_revenue': 3200000, 'avg_margin': 0.35},
            {'product_category': 'Clothing', 'units_sold': 25000, 'total_revenue': 1800000, 'avg_margin': 0.55},
            {'product_category': 'Home & Garden', 'units_sold': 8000, 'total_revenue': 1200000, 'avg_margin': 0.42}
        ]
        
        # Format comprehensive report with actual data
        report = {
            'revenue_data': revenue_data,
            'expense_data': expense_data,
            'customer_data': customer_data,
            'product_data': product_data,
            'summary': {
                'total_revenue': sum(item['revenue'] for item in revenue_data),
                'total_expenses': sum(item['total_expense'] for item in expense_data),
                'new_customers': sum(item['new_customers'] for item in customer_data),
                'avg_ltv': sum(item['avg_ltv'] for item in customer_data) / len(customer_data) if customer_data else 0
            },
            'timestamp': 'LangChainAnalyst',
            'status': 'success'
        }
        
        return jsonify(report)
    except Exception as e:
        print(f"Error generating report: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)