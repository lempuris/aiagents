import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function Customers({ reportData }) {
  if (!reportData || !reportData.customer_data) return <div>Loading...</div>;

  return (
    <div className="page">
      <h1>Customer Metrics</h1>
      
      <div className="metrics-grid">
        <div className="metric-card">
          <h3>Total New Customers</h3>
          <p className="metric-value">
            {reportData.customer_data.reduce((sum, item) => sum + item.new_customers, 0).toLocaleString()}
          </p>
        </div>
        <div className="metric-card">
          <h3>Average LTV</h3>
          <p className="metric-value">
            ${Math.round(reportData.customer_data.reduce((sum, item) => sum + item.avg_ltv, 0) / reportData.customer_data.length).toLocaleString()}
          </p>
        </div>
      </div>

      <div className="chart-section">
        <h2>New Customers by Month</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={reportData.customer_data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="new_customers" stroke="#82ca9d" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-section">
        <h2>Average Customer Lifetime Value</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={reportData.customer_data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
            <Line type="monotone" dataKey="avg_ltv" stroke="#8884d8" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default Customers;