from flask import Flask, jsonify
from flask_cors import CORS
from redshift_financial_agent import RedshiftFinancialAgent
import threading
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Global cache and agent instance
cache = {'report': None, 'predictions': None, 'timestamp': None}
cache_lock = threading.Lock()
agent_instance = None

def get_agent():
    global agent_instance
    if agent_instance is None:
        agent_instance = RedshiftFinancialAgent()
    return agent_instance

def is_cache_valid():
    if cache['timestamp'] is None:
        return False
    return datetime.now() - cache['timestamp'] < timedelta(minutes=5)

@app.route('/api/report', methods=['GET'])
def get_financial_report():
    try:
        with cache_lock:
            if cache['report'] is None or not is_cache_valid():
                agent = get_agent()
                cache['report'] = agent.create_comprehensive_report()
                cache['timestamp'] = datetime.now()
        return jsonify(cache['report'])
    except Exception as e:
        print(f"Error generating report: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/predictions', methods=['GET'])
def get_predictions():
    try:
        with cache_lock:
            if cache['predictions'] is None or not is_cache_valid():
                agent = get_agent()
                cache['predictions'] = agent.generate_comprehensive_predictions()
                cache['timestamp'] = datetime.now()
        return jsonify(cache['predictions'])
    except Exception as e:
        print(f"Error generating predictions: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)