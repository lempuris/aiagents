import React from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

function Revenue({ reportData }) {
  if (!reportData) return <div>Loading...</div>;

  const revenueByRegion = reportData.revenue_data.reduce((acc, item) => {
    const existing = acc.find(x => x.region === item.region);
    if (existing) {
      existing.revenue += item.revenue;
    } else {
      acc.push({ region: item.region, revenue: item.revenue });
    }
    return acc;
  }, []);

  const colors = ['#8884d8', '#82ca9d', '#ffc658'];

  return (
    <div className="page">
      <h1>Revenue Analysis</h1>
      
      <div className="chart-section">
        <h2>Revenue by Month & Region</h2>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={reportData.revenue_data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
            <Bar dataKey="revenue" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-section">
        <h2>Revenue by Region</h2>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={revenueByRegion}
              dataKey="revenue"
              nameKey="region"
              cx="50%"
              cy="50%"
              outerRadius={100}
              label={({region, value}) => `${region}: $${value.toLocaleString()}`}
            >
              {revenueByRegion.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
              ))}
            </Pie>
            <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default Revenue;