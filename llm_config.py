import os
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama

def get_llm_config(use_local=False):
    """Get LLM configuration based on preference"""
    
    if use_local:
        # Use local Ollama model (free)
        return Ollama(
            model="llama2",  # or "mistral", "codellama"
            temperature=0.1
        )
    else:
        # Use OpenAI with error handling
        return ChatOpenAI(
            model="gpt-3.5-turbo",  # Cheaper than gpt-4
            temperature=0.1,
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            max_retries=3,
            request_timeout=60
        )

# Environment variables for quota management
OPENAI_QUOTA_CHECK = {
    'daily_limit': 1000,  # Set your daily token limit
    'current_usage': 0,   # Track usage
    'reset_time': None    # Track reset time
}