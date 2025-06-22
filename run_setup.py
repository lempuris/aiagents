#!/usr/bin/env python3
"""
Quick setup script for Redshift Financial Agent
Run this after fixing your network connectivity issues
"""

from setup_redshift_tables import RedshiftTableSetup
from redshift_financial_agent import RedshiftFinancialAgent

def main():
    print("🚀 Redshift Financial Agent Setup")
    print("=" * 40)
    
    # Step 1: Setup database
    print("\n1️⃣ Setting up database tables...")
    setup = RedshiftTableSetup()
    
    if setup.setup_complete_database():
        print("\n2️⃣ Testing the financial agent...")
        
        # Step 2: Test the agent
        agent = RedshiftFinancialAgent()
        
        # Quick test query
        print("\n🧪 Running test query...")
        revenue_data = agent.execute_query('monthly_revenue')
        
        if revenue_data:
            print(f"✅ Agent working! Retrieved {len(revenue_data)} revenue records")
            
            # Run a quick report
            print("\n3️⃣ Generating sample report...")
            agent.create_comprehensive_report()
        else:
            print("❌ Agent test failed")
    else:
        print("\n❌ Database setup failed. Please check your connection settings.")
        print("\nTroubleshooting steps:")
        print("1. Verify your .env file has correct Redshift credentials")
        print("2. Check security groups allow port 5439 from your IP")
        print("3. Ensure Redshift cluster is publicly accessible")

if __name__ == "__main__":
    main()