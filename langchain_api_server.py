from flask import Flask, jsonify
from flask_cors import CORS
from langchain_redshift_agent import LangChainRedshiftAgent

app = Flask(__name__)
CORS(app)

@app.route('/api/report', methods=['GET'])
def get_financial_report():
    try:
        agent = LangChainRedshiftAgent()
        result = agent.create_comprehensive_dashboard()
        
        # Extract the output text and format it like the original API
        if isinstance(result, dict) and 'output' in result:
            report = {
                'analysis': result['output'],
                'timestamp': agent.name,
                'status': 'success'
            }
        else:
            report = {
                'analysis': str(result),
                'timestamp': agent.name,
                'status': 'success'
            }
        
        return jsonify(report)
    except Exception as e:
        print(f"Error generating report: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)