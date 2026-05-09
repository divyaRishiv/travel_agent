import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END

# 1. State Definition
class AgentState(TypedDict):
    destination: str
    nationality: str
    dates: str
    purpose: str
    visa_checklist: str
    
    # New fields to support guardrails
    is_valid_input: bool
    is_valid_output: bool
    error_message: str
    
    messages: Annotated[list, operator.add]

# 2. Guardrails (Validation Nodes)

def input_guardrail(state: AgentState):
    """
    GUARDRAIL 1: Validates the initial input before doing expensive work.
    Ensures destination and nationality are provided and are logical strings.
    """
    print("--- [Guardrail] Validating Input ---")
    dest = state.get("destination", "")
    nat = state.get("nationality", "")
    
    if not dest or not nat:
        return {"is_valid_input": False, "error_message": "Destination and Nationality are required."}
    
    if dest.isnumeric() or nat.isnumeric():
        return {"is_valid_input": False, "error_message": "Invalid country names provided (cannot be numbers)."}
        
    return {"is_valid_input": True, "error_message": "", "messages": ["Input passed guardrail."]}

def analyze_requirements(state: AgentState):
    print(f"--- Analyzing requirements for {state['nationality']} to {state['destination']} ---")
    return {"messages": ["Analysis complete: Visa is required."]}

def generate_checklist(state: AgentState):
    print("--- Generating Visa Checklist ---")
    # Mock LLM formatted output
    checklist = f"""
### Visa Checklist
**Destination:** {state['destination']}
**Nationality:** {state['nationality']}
* **Visa Type:** Tourist e-Visa
* **Passport:** Valid for 6 months
    """
    return {"visa_checklist": checklist, "messages": ["Checklist generated."]}

def output_guardrail(state: AgentState):
    """
    GUARDRAIL 2: Validates the LLM's output before returning it to the user.
    Checks if critical keywords/sections are actually present in the checklist.
    """
    print("--- [Guardrail] Validating Output ---")
    checklist = state.get("visa_checklist", "")
    
    # Check for hallucinated or missing crucial info
    required_keywords = ["Visa Type", "Passport"]
    
    for kw in required_keywords:
        if kw not in checklist:
            return {
                "is_valid_output": False, 
                "error_message": f"Output missing required section: {kw}",
                "visa_checklist": "Error: Checklist generation failed security validation."
            }
            
    return {"is_valid_output": True, "messages": ["Output passed guardrail."]}

# 3. Conditional Routing Logic (Deciding what to do based on Guardrails)

def route_after_input(state: AgentState):
    """If input is bad, skip the rest of the graph and go to END."""
    if state.get("is_valid_input"):
        return "analyze"
    return "end"

def route_after_output(state: AgentState):
    """
    If output is bad, go to END. 
    (In an advanced agent, you might route back to 'generate_checklist' here to self-correct!)
    """
    return "end"

# 4. Build the Graph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("input_validator", input_guardrail)
workflow.add_node("analyzer", analyze_requirements)
workflow.add_node("checklist_generator", generate_checklist)
workflow.add_node("output_validator", output_guardrail)

# Add Edges with Conditional Logic
workflow.add_edge(START, "input_validator")

# Use conditional edges to route based on guardrail checks
workflow.add_conditional_edges("input_validator", route_after_input, {"analyze": "analyzer", "end": END})

workflow.add_edge("analyzer", "checklist_generator")
workflow.add_edge("checklist_generator", "output_validator")

# Route based on output validation
workflow.add_conditional_edges("output_validator", route_after_output, {"end": END})

app = workflow.compile()

# =====================================================================
# 5. EVALUATIONS (Evals) Framework
# =====================================================================

def run_evals():
    """
    EVALS: A testing framework run independently of the main app.
    It feeds diverse scenarios into the agent and asserts the outcomes are correct.
    This ensures future changes to prompts/logic don't break the agent.
    """
    print("\n================ RUNNING EVALS ================\n")
    
    # Define our evaluation dataset
    test_cases = [
        {
            "name": "Positive Case: Valid Input should produce a checklist",
            "input": {"destination": "Japan", "nationality": "American", "dates": "Dec 1st", "purpose": "Tourism"},
            "expect_error": False,
            "required_in_output": "Visa Type"
        },
        {
            "name": "Negative Case: Numbers instead of countries should trigger input guardrail",
            "input": {"destination": "123", "nationality": "456", "dates": "Dec 1st", "purpose": "Tourism"},
            "expect_error": True,
            "required_in_output": None
        },
        {
            "name": "Negative Case: Missing nationality should trigger input guardrail",
            "input": {"destination": "Japan", "nationality": "", "dates": "Dec 1st", "purpose": "Tourism"},
            "expect_error": True,
            "required_in_output": None
        }
    ]
    
    passed_tests = 0
    for i, test in enumerate(test_cases):
        print(f"Test {i+1}: {test['name']}")
        
        # Invoke the agent
        result = app.invoke(test["input"])
        
        # Evaluate 1: Did it error as expected?
        has_error = bool(result.get("error_message"))
        error_pass = (has_error == test["expect_error"])
        
        # Evaluate 2: If no error expected, does output contain required text?
        output_pass = True
        if not test["expect_error"] and test["required_in_output"]:
            output_pass = test["required_in_output"] in result.get("visa_checklist", "")
            
        if error_pass and output_pass:
            print("  ✅ PASS\n")
            passed_tests += 1
        else:
            print("  ❌ FAIL")
            print(f"     Expected Error: {test['expect_error']}, Got Error: {has_error}\n")
            
    print(f"Evals Score: {passed_tests}/{len(test_cases)} Passed")
    print("===============================================\n")


if __name__ == "__main__":
    # 1. Run the test suite (Evals)
    run_evals()
    
    # 2. Run a normal invocation to see the flow
    print("--- Normal Execution Example ---")
    user_input = {"destination": "France", "nationality": "Indian", "dates": "Jan 2025", "purpose": "Business"}
    final_state = app.invoke(user_input)
    
    print("\nFinal Graph Result:")
    if final_state.get("error_message"):
        print(f"BLOCKED BY GUARDRAIL: {final_state['error_message']}")
    else:
        print(final_state.get("visa_checklist"))
