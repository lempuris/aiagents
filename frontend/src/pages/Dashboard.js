import React from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function Dashboard({ reportData }) {
  if (!reportData || !reportData.revenue_data || !reportData.expense_data || !reportData.product_data) {
    return <div>Loading...</div>;
  }

  const revenueByMonth = reportData.revenue_data.reduce((acc, item) => {
    const existing = acc.find(x => x.month === item.month);
    if (existing) {
      existing.revenue += item.revenue;
    } else {
      acc.push({ month: item.month, revenue: item.revenue });
    }
    return acc;
  }, []);

  return (
    <div className="page">
      <h1>Financial Dashboard</h1>
      
      <div className="metrics-grid">
        <div className="metric-card">
          <h3>Total Revenue</h3>
          <p className="metric-value">
            ${reportData.revenue_data.reduce((sum, item) => sum + item.revenue, 0).toLocaleString()}
          </p>
        </div>
        <div className="metric-card">
          <h3>Total Expenses</h3>
          <p className="metric-value">
            ${reportData.expense_data.reduce((sum, item) => sum + item.total_expense, 0).toLocaleString()}
          </p>
        </div>
        <div className="metric-card">
          <h3>Top Product</h3>
          <p className="metric-value">
            {reportData.product_data.sort((a, b) => b.total_revenue - a.total_revenue)[0]?.product_category}
          </p>
        </div>
      </div>

      <div className="chart-section">
        <h2>Revenue Trend</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={revenueByMonth}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
            <Line type="monotone" dataKey="revenue" stroke="#8884d8" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default Dashboard;