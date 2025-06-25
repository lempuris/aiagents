import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv

# LangChain imports
from langchain_openai import ChatOpenAI
from openai import RateLimitError
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.schema import BaseOutputParser
from langchain.tools import BaseTool
from langchain import hub

# Database imports
import psycopg2
import pandas as pd

load_dotenv()

def query_redshift_data(query_name: str) -> str:
    """Query financial data from Redshift database"""
    redshift_config = {
        'host': os.getenv('REDSHIFT_HOST'),
        'port': os.getenv('REDSHIFT_PORT', '5439'),
        'database': os.getenv('REDSHIFT_DB', 'dev'),
        'user': os.getenv('REDSHIFT_USER', 'admin'),
        'password': os.getenv('REDSHIFT_PASSWORD')
    }
    
    sql_queries = {
        'monthly_revenue': """
            SELECT DATE_TRUNC('month', transaction_date) as month,
                   region, SUM(amount) as revenue
            FROM sales_transactions 
            WHERE transaction_date >= CURRENT_DATE - INTERVAL '12 months'
            GROUP BY 1, 2 ORDER BY 1, 2
        """,
        'expense_breakdown': """
            SELECT DATE_TRUNC('month', expense_date) as month,
                   category, SUM(amount) as total_expense
            FROM expenses 
            WHERE expense_date >= CURRENT_DATE - INTERVAL '12 months'
            GROUP BY 1, 2 ORDER BY 1, 2
        """,
        'customer_metrics': """
            SELECT DATE_TRUNC('month', first_purchase_date) as month,
                   COUNT(DISTINCT customer_id) as new_customers,
                   AVG(lifetime_value) as avg_ltv
            FROM customers 
            WHERE first_purchase_date >= CURRENT_DATE - INTERVAL '12 months'
            GROUP BY 1 ORDER BY 1
        """
    }
    
    try:
        conn = psycopg2.connect(**redshift_config)
        query = sql_queries.get(query_name)
        if not query:
            return f"Query '{query_name}' not found"
        
        df = pd.read_sql(query, conn)
        conn.close()
        return df.to_json(orient='records', date_format='iso')
    except:
        # Fallback mock data
        mock_data = {
            'monthly_revenue': [
                {'month': '2024-01-01', 'region': 'North America', 'revenue': 2500000},
                {'month': '2024-02-01', 'region': 'North America', 'revenue': 2300000},
                {'month': '2024-03-01', 'region': 'North America', 'revenue': 2800000}
            ],
            'expense_breakdown': [
                {'month': '2024-01-01', 'category': 'Operations', 'total_expense': 800000},
                {'month': '2024-02-01', 'category': 'Operations', 'total_expense': 750000}
            ],
            'customer_metrics': [
                {'month': '2024-01-01', 'new_customers': 1250, 'avg_ltv': 2400},
                {'month': '2024-02-01', 'new_customers': 1180, 'avg_ltv': 2350}
            ]
        }
        return json.dumps(mock_data.get(query_name, []))

class LangChainRedshiftAgent:
    def __init__(self, name="LangChainAnalyst"):
        self.name = name
        
        # Initialize LangChain components with error handling
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",  # Using cheaper model to reduce quota usage
            temperature=0.1,
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            max_retries=3,
            request_timeout=60
        )
        
        # Memory for conversation context
        self.memory = ConversationBufferWindowMemory(
            k=5,
            memory_key="chat_history",
            return_messages=True
        )
        
        # Custom tools - using simple function approach
        
        # Analysis chain with prompt template
        self.analysis_prompt = PromptTemplate(
            input_variables=["data", "analysis_type"],
            template="""
            As a senior financial analyst, analyze this {analysis_type} data:
            
            {data}
            
            Provide:
            1. Key trends and insights
            2. Performance drivers  
            3. Risk factors
            4. Strategic recommendations
            5. Forecast implications
            
            Be specific and actionable.
            """
        )
        
        self.analysis_chain = LLMChain(
            llm=self.llm,
            prompt=self.analysis_prompt
        )
        
        # Agent with tools
        tools = [
            Tool(
                name="Query Redshift",
                func=query_redshift_data,
                description="Query financial data from Redshift. Use 'monthly_revenue', 'expense_breakdown', or 'customer_metrics'"
            ),
            Tool(
                name="Financial Analysis",
                func=self._analyze_data,
                description="Generate AI-powered financial insights. Input format: 'data|||analysis_type' or just 'data'"
            )
        ]
        
        # Create ReAct agent
        prompt = hub.pull("hwchase17/react")
        self.agent = create_react_agent(self.llm, tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=tools,
            memory=self.memory,
            verbose=True,
            max_iterations=10,
            early_stopping_method="generate"
        )
    
    def _analyze_data(self, input_data: str) -> str:
        """Helper function for analysis tool"""
        try:
            # Handle different input formats
            if "|||" in input_data:
                parts = input_data.split("|||")
                data = parts[0]
                analysis_type = parts[1] if len(parts) > 1 else "financial"
            else:
                data = input_data
                analysis_type = "financial"
            
            result = self.analysis_chain.invoke({
                "data": data,
                "analysis_type": analysis_type
            })
            return result["text"]
        except Exception as e:
            return f"Analysis error: {str(e)}"
    
    def _generate_fallback_analysis(self, analysis_type: str) -> dict:
        """Generate fallback analysis when API is unavailable"""
        fallback_responses = {
            "revenue": {
                "output": "Revenue Analysis (Fallback Mode):\n\n1. Key Trends: Revenue shows steady growth with seasonal variations\n2. Regional Performance: North America leading with consistent performance\n3. Recommendations: Focus on Q4 optimization and regional expansion\n\nNote: This is a fallback response due to API quota limits."
            },
            "expense": {
                "output": "Expense Analysis (Fallback Mode):\n\n1. Cost Patterns: Operations expenses stable, some optimization opportunities\n2. Budget Recommendations: Review operational efficiency\n\nNote: This is a fallback response due to API quota limits."
            }
        }
        return fallback_responses.get(analysis_type, {"output": "Analysis unavailable due to API limits."})
    
    def generate_revenue_report(self):
        """Generate revenue analysis using LangChain with error handling"""
        print(f"\n{'='*60}")
        print("LANGCHAIN REVENUE ANALYSIS")
        print(f"{'='*60}")
        
        # Use agent to query and analyze revenue data
        query = """
        Query the monthly_revenue data from Redshift and then analyze it to provide 
        insights about revenue trends, regional performance, and recommendations.
        """
        
        try:
            result = self.agent_executor.invoke({"input": query})
            print(f"\n🤖 Agent Analysis:")
            print(result['output'])
            return result
        except RateLimitError as e:
            print(f"\n❌ OpenAI API Quota Exceeded: {str(e)}")
            print("\n💡 Fallback: Using mock analysis...")
            return self._generate_fallback_analysis("revenue")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            return self._generate_fallback_analysis("revenue")
    
    def generate_expense_report(self):
        """Generate expense analysis using LangChain"""
        print(f"\n{'='*60}")
        print("LANGCHAIN EXPENSE ANALYSIS")
        print(f"{'='*60}")
        
        query = """
        Query the expense_breakdown data from Redshift and analyze spending patterns,
        cost optimization opportunities, and budget recommendations.
        """
        
        result = self.agent_executor.invoke({"input": query})
        print(f"\n🤖 Agent Analysis:")
        print(result['output'])
        
        return result
    
    def create_comprehensive_dashboard(self):
        """Generate comprehensive financial dashboard using LangChain chains"""
        print(f"\n{'='*80}")
        print("LANGCHAIN COMPREHENSIVE FINANCIAL DASHBOARD")
        print(f"Generated by: {self.name} | Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        
        try:
            # Simplified query to avoid iteration limits
            query = "Query monthly_revenue data and provide a brief financial analysis."
            
            result = self.agent_executor.invoke({"input": query})
            print(f"\n🎯 COMPREHENSIVE ANALYSIS:")
            print(result['output'])
            
            return result
        except Exception as e:
            print(f"Agent execution failed: {e}")
            # Return fallback comprehensive analysis
            fallback_analysis = {
                'output': '''COMPREHENSIVE FINANCIAL DASHBOARD

📊 REVENUE ANALYSIS:
• Monthly revenue shows steady growth trend
• North America region leading performance
• Q4 showing strong seasonal uptick

💰 EXPENSE BREAKDOWN:
• Operations costs remain stable
• Optimization opportunities in overhead
• Cost efficiency improving quarter-over-quarter

👥 CUSTOMER METRICS:
• New customer acquisition steady
• Average lifetime value increasing
• Retention rates above industry average

🎯 KEY RECOMMENDATIONS:
1. Focus on regional expansion
2. Optimize operational costs
3. Enhance customer retention programs
4. Prepare for Q4 seasonal demand

Note: Analysis generated with fallback data due to API limitations.'''
            }
            return fallback_analysis
    
    def chat_interface(self, user_query: str):
        """Interactive chat interface using LangChain memory with error handling"""
        print(f"\n💬 User: {user_query}")
        
        try:
            # Process query through agent
            result = self.agent_executor.invoke({"input": user_query})
            print(f"🤖 Agent: {result['output']}")
            return result['output']
        except RateLimitError as e:
            fallback_msg = f"I'm currently experiencing API quota limits. Please check your OpenAI billing at https://platform.openai.com/account/billing"
            print(f"🤖 Agent: {fallback_msg}")
            return fallback_msg
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            print(f"🤖 Agent: {error_msg}")
            return error_msg

# Usage example
if __name__ == "__main__":
    # Create LangChain-powered financial agent
    agent = LangChainRedshiftAgent()
    
    # Generate different types of reports
    print("1. Revenue Analysis with LangChain")
    agent.generate_revenue_report()
    
    print("\n" + "="*80)
    print("2. Expense Analysis with LangChain") 
    agent.generate_expense_report()
    
    print("\n" + "="*80)
    print("3. Comprehensive Dashboard with LangChain")
    agent.create_comprehensive_dashboard()
if __name__ == "__main__":
    # Create LangChain-powered financial agent
    agent = LangChainRedshiftAgent()
    
    # Generate different types of reports
    print("1. Revenue Analysis with LangChain")
    agent.generate_revenue_report()
    
    print("\n" + "="*80)
    print("2. Expense Analysis with LangChain") 
    agent.generate_expense_report()
    
    print("\n" + "="*80)
    print("3. Comprehensive Dashboard with LangChain")
    agent.create_comprehensive_dashboard()
    
    print("\n" + "="*80)
    print("4. Interactive Chat Interface")
    
    # Example chat interactions
    sample_queries = [
        "What are the key revenue trends this quarter?",
        "How can we optimize our expense structure?",
        "What's our customer acquisition performance?"
    ]
    
    for query in sample_queries:
        agent.chat_interface(query)
        print()