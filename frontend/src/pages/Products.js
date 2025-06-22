import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function Products({ reportData }) {
  if (!reportData) return <div>Loading...</div>;

  return (
    <div className="page">
      <h1>Product Performance</h1>
      
      <div className="chart-section">
        <h2>Revenue by Product Category</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={reportData.product_data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="product_category" />
            <YAxis />
            <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
            <Bar dataKey="total_revenue" fill="#82ca9d" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-section">
        <h2>Units Sold by Category</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={reportData.product_data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="product_category" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="units_sold" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-section">
        <h2>Profit Margin by Category</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={reportData.product_data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="product_category" />
            <YAxis />
            <Tooltip formatter={(value) => `${(value * 100).toFixed(1)}%`} />
            <Bar dataKey="avg_margin" fill="#ffc658" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default Products;