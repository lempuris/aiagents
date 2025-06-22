import socket
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def test_network_connectivity():
    """Test basic network connectivity to Redshift"""
    host = os.getenv('REDSHIFT_HOST', 'default-workgroup.176835474511.us-east-2.redshift-serverless.amazonaws.com')
    port = int(os.getenv('REDSHIFT_PORT', '5439'))
    
    print(f"Testing connection to {host}:{port}")
    
    try:
        # Test socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print("✅ Network connectivity: SUCCESS")
            return True
        else:
            print("❌ Network connectivity: FAILED")
            print("   - Check security groups allow port 5439")
            print("   - Verify VPC/subnet configuration")
            print("   - Ensure Redshift is publicly accessible")
            return False
            
    except Exception as e:
        print(f"❌ Network test failed: {e}")
        return False

def test_redshift_auth():
    """Test Redshift authentication"""
    if not test_network_connectivity():
        return False
        
    config = {
        'host': os.getenv('REDSHIFT_HOST'),
        'port': os.getenv('REDSHIFT_PORT', '5439'),
        'database': os.getenv('REDSHIFT_DB', 'dev'),
        'user': os.getenv('REDSHIFT_USER'),
        'password': os.getenv('REDSHIFT_PASSWORD')
    }
    
    try:
        conn = psycopg2.connect(**config, connect_timeout=30)
        print("✅ Redshift authentication: SUCCESS")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Redshift Connection Diagnostics")
    print("=" * 40)
    test_redshift_auth()