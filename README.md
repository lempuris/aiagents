# Financial AI Agent Dashboard

A React-based dashboard for displaying AI-powered financial insights from Redshift data.

## Features

- **Interactive Dashboard** with revenue, expense, customer, and product analytics
- **AI-Generated Insights** powered by OpenAI GPT-4
- **Real-time Data** from Amazon Redshift (with mock data fallback)
- **Responsive Charts** using Recharts library
- **Multi-page Navigation** for detailed analysis

## Setup

### 1. Environment Configuration

Copy the example environment file and add your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:
- `OPENAI_API_KEY`: Your OpenAI API key
- `REDSHIFT_HOST`: Your Redshift cluster endpoint
- `REDSHIFT_DATABASE`: Database name
- `REDSHIFT_USER`: Database username  
- `REDSHIFT_PASSWORD`: Database password

### 2. Backend Setup

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Start the Flask API server:
```bash
python api_server.py
```

### 3. Frontend Setup

Install and start the React application:
```bash
cd frontend
npm install
npm start
```

## Usage

1. Start the Flask API server (port 5000)
2. Start the React frontend (port 3000)
3. Navigate through different pages:
   - Dashboard: Overview metrics
   - Revenue: Revenue analysis with regional breakdown
   - Expenses: Expense tracking by category
   - Customers: Customer acquisition and LTV metrics
   - Products: Product performance analysis
   - AI Insights: AI-generated financial analysis

## Security

- All sensitive credentials are stored in `.env` (not tracked by Git)
- Use `.env.example` as a template for required environment variables
- Never commit actual API keys or database credentials

## Architecture

- **Backend**: Flask API serving financial data from Redshift
- **Frontend**: React SPA with routing and chart visualization
- **AI**: OpenAI GPT-4 for generating financial insights
- **Database**: Amazon Redshift for data storage