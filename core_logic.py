import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END

# 1. Define the State
# This holds the context / memory throughout the execution of the agent.
class AgentState(TypedDict):
    destination: str
    nationality: str
    dates: str
    purpose: str
    # The output we want to generate
    visa_checklist: str
    messages: Annotated[list, operator.add]

# 2. Define the Nodes (The functions that do the work)

def analyze_requirements(state: AgentState):
    """
    Node to analyze the travel requirements. 
    In a real app, you would call an LLM (e.g., GPT-4) here passing the state variables.
    """
    print(f"--- Analyzing requirements for {state['nationality']} traveling to {state['destination']} ---")
    
    # Mock LLM generation or Tool call
    # messages list can be used to track the chain of thought or conversation history
    return {"messages": ["Analysis complete: Visa is required."]}

def generate_checklist(state: AgentState):
    """
    Node to generate the actual checklist based on analysis.
    Again, an LLM would format this beautifully based on specific rules.
    """
    print("--- Generating Visa Checklist ---")
    
    # Mock LLM formatted output
    checklist = f"""
### Visa Checklist
**Destination:** {state['destination']}
**Nationality:** {state['nationality']}
**Dates:** {state['dates']}
**Purpose:** {state['purpose']}

* **Visa Type:** Tourist e-Visa
* **Passport:** Must be valid for at least 6 months from arrival
* **Forms:** Online application form
* **Currency:** Proof of sufficient funds (e.g., recent bank statements)
* **Insurance:** Travel insurance with medical coverage recommended
* **Processing Time:** Approximately 5-7 business days
    """
    
    # Update the state with the final checklist
    return {"visa_checklist": checklist, "messages": ["Checklist generated."]}

# 3. Build the Graph

# Initialize the graph with our state schema
workflow = StateGraph(AgentState)

# Add our nodes to the graph
workflow.add_node("analyzer", analyze_requirements)
workflow.add_node("checklist_generator", generate_checklist)

# Add edges to define the flow (Simple Sequence in this case)
workflow.add_edge(START, "analyzer")
workflow.add_edge("analyzer", "checklist_generator")
workflow.add_edge("checklist_generator", END)

# Compile the graph into an executable LangGraph application
app = workflow.compile()

# 4. Example Usage
if __name__ == "__main__":
    # The initial input provided by the Business User
    user_input = {
        "destination": "Japan",
        "nationality": "American",
        "dates": "Dec 1st - Dec 15th, 2024",
        "purpose": "Tourism and sightseeing"
    }
    
    print("Starting Agent execution...\n")
    # Invoke the compiled graph with the initial state
    final_state = app.invoke(user_input)
    
    print("\n--- FINAL OUTPUT ---")
    print(final_state.get("visa_checklist"))
