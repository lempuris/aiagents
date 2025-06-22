import requests
import json
from datetime import datetime

class ToolAgent:
    def __init__(self, name):
        self.name = name
        self.tools = {
            'get_weather': self.get_weather,
            'calculate': self.calculate,
            'get_time': self.get_time
        }
    
    def get_weather(self, city):
        # Mock weather API call
        weather_data = {
            'London': {'temp': 15, 'condition': 'Cloudy'},
            'New York': {'temp': 22, 'condition': 'Sunny'},
            'Tokyo': {'temp': 18, 'condition': 'Rainy'}
        }
        return weather_data.get(city, {'temp': 20, 'condition': 'Unknown'})
    
    def calculate(self, expression):
        try:
            # Safe evaluation for basic math
            allowed_chars = set('0123456789+-*/.() ')
            if all(c in allowed_chars for c in expression):
                return eval(expression)
            return "Invalid expression"
        except:
            return "Calculation error"
    
    def get_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def use_tool(self, tool_name, *args):
        if tool_name in self.tools:
            return self.tools[tool_name](*args)
        return f"Tool '{tool_name}' not available"
    
    def process_request(self, request):
        # Simple request parsing
        if 'weather' in request.lower():
            city = 'London'  # Default city
            for word in request.split():
                if word.capitalize() in ['London', 'Tokyo', 'New York']:
                    city = word.capitalize()
            return self.use_tool('get_weather', city)
        
        elif 'calculate' in request.lower() or any(op in request for op in ['+', '-', '*', '/']):
            # Extract mathematical expression
            import re
            expr = re.search(r'[\d+\-*/\.\s()]+', request)
            if expr:
                return self.use_tool('calculate', expr.group().strip())
        
        elif 'time' in request.lower():
            return self.use_tool('get_time')
        
        return "I don't understand that request"

# Usage example
if __name__ == "__main__":
    agent = ToolAgent("UtilityAgent")
    
    requests = [
        "What's the weather in London?",
        "Calculate 15 + 27 * 2",
        "What time is it?",
        "Weather in Tokyo please"
    ]
    
    for req in requests:
        result = agent.process_request(req)
        print(f"Request: {req}")
        print(f"Response: {result}\n")