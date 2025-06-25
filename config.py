# API Configuration
API_CONFIGS = {
    'original': {
        'port': 5000,
        'server_file': 'api_server.py'
    },
    'langchain': {
        'port': 5001,
        'server_file': 'langchain_api_server.py'
    }
}

# Frontend can switch between APIs by changing the base URL
BASE_URLS = {
    'original': 'http://localhost:5000',
    'langchain': 'http://localhost:5001'
}