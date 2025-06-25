import json
import os
from datetime import datetime, timedelta

class QuotaManager:
    def __init__(self, quota_file="quota_usage.json"):
        self.quota_file = quota_file
        self.daily_limit = 1000  # tokens
        self.load_usage()
    
    def load_usage(self):
        """Load usage data from file"""
        if os.path.exists(self.quota_file):
            with open(self.quota_file, 'r') as f:
                self.usage_data = json.load(f)
        else:
            self.usage_data = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'tokens_used': 0,
                'requests_made': 0
            }
    
    def save_usage(self):
        """Save usage data to file"""
        with open(self.quota_file, 'w') as f:
            json.dump(self.usage_data, f)
    
    def can_make_request(self, estimated_tokens=100):
        """Check if request can be made within quota"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Reset if new day
        if self.usage_data['date'] != today:
            self.usage_data = {
                'date': today,
                'tokens_used': 0,
                'requests_made': 0
            }
        
        return (self.usage_data['tokens_used'] + estimated_tokens) <= self.daily_limit
    
    def record_usage(self, tokens_used):
        """Record token usage"""
        self.usage_data['tokens_used'] += tokens_used
        self.usage_data['requests_made'] += 1
        self.save_usage()
    
    def get_remaining_quota(self):
        """Get remaining quota for today"""
        return max(0, self.daily_limit - self.usage_data['tokens_used'])