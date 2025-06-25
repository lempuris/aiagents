import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class LLMAgent:
    def __init__(self, name, system_prompt):
        self.name = name
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.system_prompt = system_prompt
        self.conversation_history = []
    
    def think(self, user_input):
        # Auto-reset if memory gets too large
        if len(self.conversation_history) > 10:
            print("Memory limit reached. Clearing conversation history.")
            self.reset_memory()
            
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.conversation_history)
        print(f"user input: {user_input}")
        print(f"messages: {messages}")
        messages.append({"role": "user", "content": user_input})
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150
        )
        
        ai_response = response.choices[0].message.content
        
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        self.conversation_history.append({"role": "assistant", "content": ai_response})
        
        return ai_response
    
    def reset_memory(self):
        self.conversation_history = []

# Usage example
if __name__ == "__main__":
    assistant = LLMAgent(
        "Assistant", 
        "You are a helpful AI assistant that provides concise, practical advice."
    )
    
    queries = [
        "How do I improve my Python skills?",
        "What's the best way to debug code?",
        "Can you suggest a project for beginners?",
        "What are Python decorators?",
        "How do I handle exceptions?",
        "What's the difference between lists and tuples?",
        "How do I work with APIs in Python?",
        "What are lambda functions?",
        "How do I use virtual environments?",
        "What's object-oriented programming?"
    ]
    
    for query in queries:
        response = assistant.think(query)
        print(f"User: {query}")
        print(f"Agent: {response}\n")