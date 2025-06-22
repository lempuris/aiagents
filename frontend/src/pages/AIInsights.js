import React from 'react';

function AIInsights({ reportData }) {
  if (!reportData || !reportData.ai_insights) return <div>Loading AI insights...</div>;

  const { ai_insights } = reportData;

  const insights = [
    { title: 'Revenue Analysis', content: ai_insights.revenue, icon: '📊', color: '#4CAF50' },
    { title: 'Expense Analysis', content: ai_insights.expenses, icon: '💰', color: '#FF9800' },
    { title: 'Executive Summary', content: ai_insights.executive_summary, icon: '🎯', color: '#2196F3' }
  ];

  return (
    <div className="page">
      <div className="ai-header">
        <h1>🤖 AI-Generated Insights</h1>
        <p>Powered by advanced financial analysis</p>
      </div>
      
      <div className="insights-grid">
        {insights.map((insight, index) => (
          <div key={index} className="insight-card" style={{ borderLeft: `4px solid ${insight.color}` }}>
            <div className="insight-header">
              <span className="insight-icon">{insight.icon}</span>
              <h2>{insight.title}</h2>
            </div>
            <div className="insight-text">
              {insight.content || `${insight.title} not available`}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default AIInsights;