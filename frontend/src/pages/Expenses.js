import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

function Expenses({ reportData }) {
  if (!reportData) return <div>Loading...</div>;

  const expensesByCategory = reportData.expense_data.reduce((acc, item) => {
    const existing = acc.find(x => x.category === item.category);
    if (existing) {
      existing.total_expense += item.total_expense;
    } else {
      acc.push({ category: item.category, total_expense: item.total_expense });
    }
    return acc;
  }, []);

  const colors = ['#ff7300', '#00ff00'];

  return (
    <div className="page">
      <h1>Expense Analysis</h1>
      
      <div className="chart-section">
        <h2>Monthly Expenses by Category</h2>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={reportData.expense_data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
            <Bar dataKey="total_expense" fill="#ff7300" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-section">
        <h2>Total Expenses by Category</h2>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={expensesByCategory}
              dataKey="total_expense"
              nameKey="category"
              cx="50%"
              cy="50%"
              outerRadius={100}
              label={({category, value}) => `${category}: $${value.toLocaleString()}`}
            >
              {expensesByCategory.map((entry, index) => (
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

export default Expenses;