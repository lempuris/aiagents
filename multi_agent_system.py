# Import necessary modules
from dataclasses import dataclass  # Helps create simple classes for data storage
from typing import List, Dict       # Type hints for better code documentation
import random                      # For generating random choices

# @dataclass automatically creates __init__, __repr__, and other methods
@dataclass
class Message:
    """A simple data class to represent messages between agents"""
    sender: str        # Who sent the message
    receiver: str      # Who should receive the message
    content: str       # The actual message content
    message_type: str  # Type of message (e.g., "info", "request", "response")

class Agent:
    """Base class for all agents in the system"""
    
    def __init__(self, name, role):
        """Initialize an agent with a name and role"""
        self.name = name          # Agent's unique identifier
        self.role = role          # Agent's job/responsibility
        self.inbox = []           # List to store incoming messages
        self.knowledge = {}       # Dictionary to store agent's knowledge
    
    def send_message(self, receiver, content, message_type="info"):
        """Create and return a new message to send to another agent"""
        return Message(self.name, receiver, content, message_type)
    
    def receive_message(self, message):
        """Add a received message to the agent's inbox"""
        self.inbox.append(message)
    
    def process_messages(self):
        """Process all messages in inbox and return any responses"""
        responses = []  # List to collect response messages
        
        # Loop through each message in the inbox
        for message in self.inbox:
            response = self.handle_message(message)  # Process the message
            if response:  # If there's a response, add it to the list
                responses.append(response)
        
        self.inbox.clear()  # Clear inbox after processing
        return responses
    
    def handle_message(self, message):
        """Handle a specific message - to be overridden by subclasses"""
        # This is a "base" method that child classes will replace
        return None

class DataAnalyst(Agent):
    """Specialized agent that performs data analysis"""
    
    def __init__(self, name):
        # Call the parent class constructor with role "analyst"
        super().__init__(name, "analyst")
        self.data_insights = []  # List to store analysis results
    
    def handle_message(self, message):
        """Override parent method to handle data analysis requests"""
        # Check if this is a data analysis request
        if message.message_type == "data_request":
            # Simulate data analysis by randomly choosing a trend
            trend = random.choice(['increasing', 'decreasing', 'stable'])
            insight = f"Analysis shows trend: {trend}"
            
            # Store the insight for future reference
            self.data_insights.append(insight)
            
            # Send the analysis result back to whoever requested it
            return self.send_message(message.sender, insight, "analysis_result")
        
        # Return None if we can't handle this message type
        return None

class DecisionMaker(Agent):
    """Specialized agent that makes business decisions based on analysis"""
    
    def __init__(self, name):
        # Call parent constructor with role "decision_maker"
        super().__init__(name, "decision_maker")
        self.decisions = []  # List to store all decisions made
    
    def handle_message(self, message):
        """Override parent method to handle analysis results and make decisions"""
        # Check if this is an analysis result from the DataAnalyst
        if message.message_type == "analysis_result":
            # Make decision based on the analysis content
            if "increasing" in message.content:
                decision = "Expand operations"
            elif "decreasing" in message.content:
                decision = "Reduce costs"
            else:  # "stable" trend
                decision = "Maintain current strategy"
            
            # Store the decision for future reference
            self.decisions.append(decision)
            
            # Send the decision to the coordinator
            return self.send_message("coordinator", f"Decision: {decision}", "decision")
        
        # Return None if we can't handle this message type
        return None

class Coordinator(Agent):
    """Special agent that manages and coordinates other agents"""
    
    def __init__(self, name):
        # Call parent constructor with role "coordinator"
        super().__init__(name, "coordinator")
        self.agents = {}        # Dictionary to store all managed agents
        self.message_queue = [] # Queue for managing message flow
    
    def add_agent(self, agent):
        """Add a new agent to the system"""
        # Store agent using its name as the key
        self.agents[agent.name] = agent
    
    def route_message(self, message):
        """Send a message to the correct recipient"""
        # Check if the receiver is one of our managed agents
        if message.receiver in self.agents:
            self.agents[message.receiver].receive_message(message)
        # Check if the message is for the coordinator itself
        elif message.receiver == "coordinator":
            self.receive_message(message)
    
    def orchestrate(self, task):
        """Main method that coordinates the entire multi-agent workflow"""
        print(f"Coordinating task: {task}")
        
        # Step 1: Start the workflow by requesting data analysis
        data_request = Message("coordinator", "analyst", "Need market analysis", "data_request")
        self.route_message(data_request)
        
        # Step 2: Process messages in multiple rounds to allow agents to communicate
        for round_num in range(3):  # Run for 3 rounds
            print(f"\n--- Round {round_num + 1} ---")
            
            # Let each agent process their messages
            for agent in self.agents.values():
                responses = agent.process_messages()  # Get agent's responses
                
                # Route each response to its intended recipient
                for response in responses:
                    print(f"{response.sender} -> {response.receiver}: {response.content}")
                    self.route_message(response)
            
            # Process any messages sent to the coordinator
            self.process_messages()

# This block only runs when the script is executed directly (not imported)
if __name__ == "__main__":
    # Step 1: Create instances of each type of agent
    coordinator = Coordinator("coordinator")        # The main orchestrator
    analyst = DataAnalyst("analyst")                # Handles data analysis
    decision_maker = DecisionMaker("decision_maker") # Makes business decisions
    
    # Step 2: Register the agents with the coordinator
    coordinator.add_agent(analyst)      # Add analyst to the system
    coordinator.add_agent(decision_maker) # Add decision maker to the system
    
    # Step 3: Start the collaborative workflow
    coordinator.orchestrate("Market Strategy Planning")