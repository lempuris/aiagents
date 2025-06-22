class SimpleAgent:
    def __init__(self, name):
        self.name = name
        self.memory = []
    
    def perceive(self, environment):
        return environment.get('temperature', 20)
    
    def decide(self, perception):
        if perception > 25:
            return "turn_on_ac"
        elif perception < 18:
            return "turn_on_heater"
        return "do_nothing"
    
    def act(self, action):
        self.memory.append(action)
        print(f"{self.name}: Memory updated with action '{action}'")
        print(f"{self.name}: Current memory: {self.memory}")
        print(f"{self.name}: Executing {action}")
        return action

# Usage example
if __name__ == "__main__":
    agent = SimpleAgent("ThermoAgent")
    
    environments = [
        {'temperature': 30},
        {'temperature': 15},
        {'temperature': 22}
    ]
    
    for env in environments:
        perception = agent.perceive(env)
        action = agent.decide(perception)
        agent.act(action)
        print(f"Temperature: {perception}°C, Action: {action}\n")