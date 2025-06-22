from flask import Flask, jsonify
from flask_cors import CORS
from redshift_financial_agent import RedshiftFinancialAgent

app = Flask(__name__)
CORS(app)

@app.route('/api/report', methods=['GET'])
def get_financial_report():
    try:
        agent = RedshiftFinancialAgent()
        report = agent.create_comprehensive_report()
        return jsonify(report)
    except Exception as e:
        print(f"Error generating report: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)