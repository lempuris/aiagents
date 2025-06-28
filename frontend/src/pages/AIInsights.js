import React, { useState } from 'react';
import '../ai-insights.css';

function AIInsights({ reportData }) {
  const [activeInsightTab, setActiveInsightTab] = useState('revenue');
  
  if (!reportData || !reportData.ai_insights) return <div>Loading AI insights...</div>;

  const { ai_insights } = reportData;

  const insights = {
    revenue: { title: 'Revenue Analysis', content: ai_insights.revenue, icon: '📊' },
    expenses: { title: 'Expense Analysis', content: ai_insights.expenses, icon: '💰' },
    summary: { title: 'Executive Summary', content: ai_insights.executive_summary, icon: '🎯' }
  };

  const formatInsightContent = (content) => {
    // Split by numbered sections (1., 2., etc.)
    const sections = content.split(/\d+\./)
      .filter(section => section.trim())
      .map((section, index) => ({
        title: ['Key Trends & Insights', 'Performance Drivers', 'Risk Factors', 'Strategic Recommendations', 'Forecast Implications'][index] || 'Analysis',
        content: section.trim(),
        icon: ['📊', '🚀', '⚠️', '💡', '🔮'][index] || '💡'
      }));
    
    // If no numbered sections found, treat as single content
    if (sections.length <= 1) {
      return content.split('.').filter(sentence => sentence.trim()).map((sentence, index) => (
        <div key={index} className="insight-point">
          <div className="insight-bullet">💡</div>
          <div className="insight-sentence">{sentence.trim()}.</div>
        </div>
      ));
    }
    
    return sections.map((section, index) => (
      <div key={index} className="insight-section">
        <div className="section-title">
          <span className="section-icon">{section.icon}</span>
          {section.title}
        </div>
        <div className="insight-point">
          <div className="insight-sentence">{section.content}</div>
        </div>
      </div>
    ));
  };

  return (
    <div className="ai-insights-page">
      <div className="page-header">
        <h2>🤖 AI-Generated Insights</h2>
        <p className="header-subtitle">Powered by advanced financial analysis</p>
      </div>
      
      <div className="insights-tabs">
        <button 
          className={`insights-tab ${activeInsightTab === 'revenue' ? 'active' : ''}`}
          onClick={() => setActiveInsightTab('revenue')}
        >
          📊 Revenue
        </button>
        <button 
          className={`insights-tab ${activeInsightTab === 'expenses' ? 'active' : ''}`}
          onClick={() => setActiveInsightTab('expenses')}
        >
          💰 Expenses
        </button>
        <button 
          className={`insights-tab ${activeInsightTab === 'summary' ? 'active' : ''}`}
          onClick={() => setActiveInsightTab('summary')}
        >
          🎯 Summary
        </button>
      </div>
      
      <div className="insight-content-section">
        <div className="insight-header">
          <div className="insight-icon-large">{insights[activeInsightTab].icon}</div>
          <div>
            <h3>{insights[activeInsightTab].title}</h3>
            <p className="insight-subtitle">AI-powered analysis and recommendations</p>
          </div>
        </div>
        
        <div className="insight-content">
          {insights[activeInsightTab].content ? 
            formatInsightContent(insights[activeInsightTab].content) :
            <div className="no-content">Analysis not available</div>
          }
        </div>
      </div>
    </div>
  );
}

export default AIInsights;