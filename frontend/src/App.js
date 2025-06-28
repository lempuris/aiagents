import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import Navigation from './components/Navigation';
import Dashboard from './pages/Dashboard';
import Revenue from './pages/Revenue';
import Expenses from './pages/Expenses';
import Customers from './pages/Customers';
import Products from './pages/Products';
import AIInsights from './pages/AIInsights';
import Predictions from './pages/Predictions';
import './App.css';

function App() {
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReport();
  }, []);

  const fetchReport = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/report');
      setReportData(response.data);
    } catch (error) {
      console.error('Error fetching report:', error);
      setReportData(getMockData());
    } finally {
      setLoading(false);
    }
  };

  const getMockData = () => ({
    revenue_data: [
      { month: '2024-01', region: 'North America', revenue: 2500000 },
      { month: '2024-02', region: 'North America', revenue: 2300000 },
      { month: '2024-03', region: 'North America', revenue: 2800000 },
      { month: '2024-01', region: 'Europe', revenue: 1800000 },
      { month: '2024-02', region: 'Europe', revenue: 1900000 },
      { month: '2024-03', region: 'Europe', revenue: 2100000 }
    ],
    expense_data: [
      { month: '2024-01', category: 'Operations', total_expense: 800000 },
      { month: '2024-02', category: 'Operations', total_expense: 750000 },
      { month: '2024-03', category: 'Operations', total_expense: 900000 },
      { month: '2024-01', category: 'Marketing', total_expense: 400000 },
      { month: '2024-02', category: 'Marketing', total_expense: 450000 },
      { month: '2024-03', category: 'Marketing', total_expense: 500000 }
    ],
    customer_data: [
      { month: '2024-01', new_customers: 1250, avg_ltv: 2400 },
      { month: '2024-02', new_customers: 1180, avg_ltv: 2350 },
      { month: '2024-03', new_customers: 1420, avg_ltv: 2500 }
    ],
    product_data: [
      { product_category: 'Electronics', units_sold: 15000, total_revenue: 3200000, avg_margin: 0.35 },
      { product_category: 'Clothing', units_sold: 25000, total_revenue: 1800000, avg_margin: 0.55 },
      { product_category: 'Home & Garden', units_sold: 8000, total_revenue: 1200000, avg_margin: 0.42 }
    ],
    ai_insights: {
      revenue: 'Revenue shows strong growth in Q1 2024, with North America leading at $7.6M total. March performance (+21% vs Feb) indicates positive momentum.',
      expenses: 'Operating expenses trending upward but controlled at $2.45M total. Marketing spend increased 25% in Q1, showing investment in growth.',
      executive_summary: 'Strong financial performance with $13.4M revenue vs $3.8M expenses, yielding 71.6% profit margin. Electronics leading product performance.'
    }
  });

  if (loading) return <div className="loading">Loading financial report...</div>;

  return (
    <Router>
      <div className="App">
        <header className="header">
          <h1>Financial Reports Dashboard</h1>
          <button onClick={fetchReport} className="refresh-btn">Refresh Report</button>
        </header>
        
        <Navigation />
        
        <Routes>
          <Route path="/" element={<Dashboard reportData={reportData} />} />
          <Route path="/revenue" element={<Revenue reportData={reportData} />} />
          <Route path="/expenses" element={<Expenses reportData={reportData} />} />
          <Route path="/customers" element={<Customers reportData={reportData} />} />
          <Route path="/products" element={<Products reportData={reportData} />} />
          <Route path="/ai-insights" element={<AIInsights reportData={reportData} />} />
          <Route path="/predictions" element={<Predictions />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;