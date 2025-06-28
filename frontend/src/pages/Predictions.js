import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area, BarChart, Bar } from 'recharts';
import axios from 'axios';
import '../predictions.css';

const Predictions = () => {
  const [predictions, setPredictions] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('revenue');
  const [insightsTab, setInsightsTab] = useState('trends');

  useEffect(() => {
    fetchPredictions();
  }, []);

  const fetchPredictions = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/predictions');
      setPredictions(response.data);
    } catch (error) {
      console.error('Error fetching predictions:', error);
      setPredictions(getMockPredictions());
    } finally {
      setLoading(false);
    }
  };

  const getMockPredictions = () => ({
    revenue_forecast: {
      predictions: [
        { month: '2024-04-01', linear_forecast: 2950000, polynomial_forecast: 3100000, confidence_lower: 2700000, confidence_upper: 3200000, growth_rate: 5.4 },
        { month: '2024-05-01', linear_forecast: 3100000, polynomial_forecast: 3300000, confidence_lower: 2850000, confidence_upper: 3350000, growth_rate: 10.7 },
        { month: '2024-06-01', linear_forecast: 3250000, polynomial_forecast: 3520000, confidence_lower: 3000000, confidence_upper: 3500000, growth_rate: 16.1 }
      ],
      model_accuracy: { r2_score: 0.85, mae: 150000 },
      historical_data: [
        { month: '2024-01-01', actual_revenue: 4300000 },
        { month: '2024-02-01', actual_revenue: 4200000 },
        { month: '2024-03-01', actual_revenue: 4900000 }
      ]
    },
    expense_forecast: {
      predictions: [
        { month: '2024-04-01', predicted_expense: 1280000, trend: 'increasing' },
        { month: '2024-05-01', predicted_expense: 1320000, trend: 'increasing' },
        { month: '2024-06-01', predicted_expense: 1360000, trend: 'increasing' }
      ],
      trend_analysis: { monthly_growth_rate: 3.2, total_predicted_6m: 7800000 }
    },
    customer_forecast: {
      predictions: [
        { month: '2024-04-01', predicted_new_customers: 1480, predicted_avg_ltv: 2580, predicted_revenue_impact: 3818400 },
        { month: '2024-05-01', predicted_new_customers: 1520, predicted_avg_ltv: 2620, predicted_revenue_impact: 3982400 },
        { month: '2024-06-01', predicted_new_customers: 1560, predicted_avg_ltv: 2660, predicted_revenue_impact: 4149600 }
      ],
      insights: { customer_growth_trend: 'positive', ltv_trend: 'increasing' }
    },
    ai_insights: 'Based on predictive analysis, revenue is expected to grow 5-16% over the next 6 months, driven by strong customer acquisition trends and increasing LTV. Expenses will grow moderately at 3.2% monthly rate.'
  });

  const formatCurrency = (value) => `$${(value / 1000000).toFixed(1)}M`;
  const formatNumber = (value) => value.toLocaleString();

  if (loading) return <div className="loading">Loading predictions...</div>;

  const renderRevenueForecast = () => {
    const combinedData = [
      ...predictions.revenue_forecast.historical_data.map(item => ({
        month: item.month.substring(0, 7),
        actual: item.actual_revenue,
        type: 'historical'
      })),
      ...predictions.revenue_forecast.predictions.map(item => ({
        month: item.month.substring(0, 7),
        linear: item.linear_forecast,
        polynomial: item.polynomial_forecast,
        lower: item.confidence_lower,
        upper: item.confidence_upper,
        type: 'forecast'
      }))
    ];

    return (
      <div className="prediction-section">
        <div className="section-header">
          <h3>📈 Revenue Forecast</h3>
          <div className="accuracy-badge">
            Model Accuracy: {(predictions.revenue_forecast.model_accuracy.r2_score * 100).toFixed(1)}%
          </div>
        </div>
        
        <div className="chart-container">
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={combinedData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis tickFormatter={formatCurrency} />
              <Tooltip formatter={(value) => formatCurrency(value)} />
              <Legend />
              <Line type="monotone" dataKey="actual" stroke="#8884d8" strokeWidth={3} name="Historical Revenue" />
              <Line type="monotone" dataKey="linear" stroke="#82ca9d" strokeWidth={2} strokeDasharray="5 5" name="Linear Forecast" />
              <Line type="monotone" dataKey="polynomial" stroke="#ffc658" strokeWidth={2} strokeDasharray="10 5" name="Polynomial Forecast" />
              <Area dataKey="upper" fill="#82ca9d" fillOpacity={0.1} />
              <Area dataKey="lower" fill="#82ca9d" fillOpacity={0.1} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="forecast-cards">
          {predictions.revenue_forecast.predictions.slice(0, 3).map((pred, index) => (
            <div key={index} className="forecast-card">
              <div className="forecast-month">{pred.month.substring(0, 7)}</div>
              <div className="forecast-value">{formatCurrency(pred.linear_forecast)}</div>
              <div className={`growth-rate ${pred.growth_rate > 0 ? 'positive' : 'negative'}`}>
                {pred.growth_rate > 0 ? '↗' : '↘'} {Math.abs(pred.growth_rate).toFixed(1)}%
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderExpenseForecast = () => (
    <div className="prediction-section">
      <div className="section-header">
        <h3>💰 Expense Forecast</h3>
        <div className="trend-badge">
          Monthly Growth: {predictions.expense_forecast.trend_analysis.monthly_growth_rate.toFixed(1)}%
        </div>
      </div>
      
      <div className="chart-container">
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={predictions.expense_forecast.predictions}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" tickFormatter={(value) => value.substring(0, 7)} />
            <YAxis tickFormatter={formatCurrency} />
            <Tooltip formatter={(value) => formatCurrency(value)} />
            <Bar dataKey="predicted_expense" fill="#ff7c7c" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="expense-summary">
        <div className="summary-card">
          <h4>6-Month Projection</h4>
          <div className="big-number">{formatCurrency(predictions.expense_forecast.trend_analysis.total_predicted_6m)}</div>
        </div>
      </div>
    </div>
  );

  const renderCustomerForecast = () => (
    <div className="prediction-section">
      <div className="section-header">
        <h3>👥 Customer Growth Forecast</h3>
        <div className="trend-badges">
          <span className={`trend-badge ${predictions.customer_forecast.insights.customer_growth_trend}`}>
            Customer Growth: {predictions.customer_forecast.insights.customer_growth_trend}
          </span>
          <span className={`trend-badge ${predictions.customer_forecast.insights.ltv_trend}`}>
            LTV Trend: {predictions.customer_forecast.insights.ltv_trend}
          </span>
        </div>
      </div>
      
      <div className="chart-container">
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={predictions.customer_forecast.predictions}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" tickFormatter={(value) => value.substring(0, 7)} />
            <YAxis />
            <Tooltip />
            <Area type="monotone" dataKey="predicted_new_customers" stackId="1" stroke="#8884d8" fill="#8884d8" />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="customer-metrics">
        {predictions.customer_forecast.predictions.slice(0, 3).map((pred, index) => (
          <div key={index} className="metric-card">
            <div className="metric-month">{pred.month.substring(0, 7)}</div>
            <div className="metric-row">
              <span>New Customers:</span>
              <span className="metric-value">{formatNumber(pred.predicted_new_customers)}</span>
            </div>
            <div className="metric-row">
              <span>Avg LTV:</span>
              <span className="metric-value">${formatNumber(pred.predicted_avg_ltv)}</span>
            </div>
            <div className="metric-row revenue-impact">
              <span>Revenue Impact:</span>
              <span className="metric-value">{formatCurrency(pred.predicted_revenue_impact)}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="predictions-page">
      <div className="page-header">
        <h2>🔮 Predictive Financial Analysis</h2>
        <button onClick={fetchPredictions} className="refresh-btn">Refresh Predictions</button>
      </div>

      <div className="prediction-tabs">
        <button 
          className={`tab ${activeTab === 'revenue' ? 'active' : ''}`}
          onClick={() => setActiveTab('revenue')}
        >
          Revenue Forecast
        </button>
        <button 
          className={`tab ${activeTab === 'expenses' ? 'active' : ''}`}
          onClick={() => setActiveTab('expenses')}
        >
          Expense Forecast
        </button>
        <button 
          className={`tab ${activeTab === 'customers' ? 'active' : ''}`}
          onClick={() => setActiveTab('customers')}
        >
          Customer Growth
        </button>
      </div>

      <div className="prediction-content">
        {activeTab === 'revenue' && renderRevenueForecast()}
        {activeTab === 'expenses' && renderExpenseForecast()}
        {activeTab === 'customers' && renderCustomerForecast()}
      </div>

      <div className="ai-insights-section">
        <div className="insights-header">
          <div className="insights-icon">🤖</div>
          <div>
            <h3>AI Predictive Insights</h3>
            <p className="insights-subtitle">Advanced analysis powered by machine learning</p>
          </div>
        </div>
        
        <div className="insights-tabs">
          <button 
            className={`insights-tab ${insightsTab === 'trends' ? 'active' : ''}`}
            onClick={() => setInsightsTab('trends')}
          >
            📊 Trends
          </button>
          <button 
            className={`insights-tab ${insightsTab === 'risks' ? 'active' : ''}`}
            onClick={() => setInsightsTab('risks')}
          >
            ⚠️ Risks
          </button>
          <button 
            className={`insights-tab ${insightsTab === 'recommendations' ? 'active' : ''}`}
            onClick={() => setInsightsTab('recommendations')}
          >
            💡 Actions
          </button>
        </div>
        
        <div className="ai-insights-content">
          {(() => {
            const sections = predictions.ai_insights.split(/\d+\./)
              .filter(section => section.trim())
              .map((section, index) => ({
                title: ['Key Trends & Insights', 'Performance Drivers', 'Risk Factors', 'Strategic Recommendations', 'Forecast Implications'][index] || 'Analysis',
                content: section.trim(),
                icon: ['📊', '🚀', '⚠️', '💡', '🔮'][index] || '📈',
                category: ['trends', 'trends', 'risks', 'recommendations', 'recommendations'][index] || 'trends'
              }));
            
            const filteredSections = sections.filter(section => section.category === insightsTab);
            
            return filteredSections.map((section, index) => (
              <div key={index} className="insight-section">
                <div className="section-title">
                  <span className="section-icon">{section.icon}</span>
                  {section.title}
                </div>
                <div className="insight-card">
                  <div className="insight-text">{section.content}</div>
                </div>
              </div>
            ));
          })()}
        </div>
      </div>
    </div>
  );
};

export default Predictions;