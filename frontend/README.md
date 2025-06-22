# Financial Reports Frontend

React application to display financial agent reports.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

## Backend API

Start the Flask API server:
```bash
cd ..
python api_server.py
```

The frontend will fetch data from `http://localhost:5000/api/report`