from langgraph.graph import StateGraph, END
 
from graph.state import TripState
from graph.replan import agents_to_run, detect_changed_fields, describe_replan
 
from agents.planner import planner_agent
from agents.weather_agent import weather_agent
from agents.destination_agent import destination_agent
from agents.transport_agent import transport_agent
from agents.budget_agent import budget_agent
from agents.itinerary_agent import itinerary_agent
 
 
AGENT_FN = {
    "weather": weather_agent,
    "destination": destination_agent,
    "transport": transport_agent,
    "budget": budget_agent,
    "itinerary": itinerary_agent,
}
 
 
# Route after planner
def route_after_planner(state: dict) -> str:
    return "ask_user" if state.get("need_clarification") else "proceed"
 
 
# Build dynamic graph
def build_graph(agents: list = None):
    if agents is None:
        agents = list(AGENT_FN.keys())
 
    graph = StateGraph(TripState)
 
    graph.add_node("planner", planner_agent)
 
    for name in agents:
        graph.add_node(name, AGENT_FN[name])
 
    graph.set_entry_point("planner")
 
    if agents:
        graph.add_conditional_edges(
            "planner",
            route_after_planner,
            {
                "ask_user": END,
                "proceed": agents[0],
            },
        )
 
        for i in range(len(agents) - 1):
            graph.add_edge(agents[i], agents[i + 1])
 
        graph.add_edge(agents[-1], END)
    else:
        graph.add_conditional_edges(
            "planner",
            route_after_planner,
            {
                "ask_user": END,
                "proceed": END,
            },
        )
 
    return graph.compile()
 
def invoke_smart(current_state: dict, prev_state: dict):

    # ✅ Step 1: Run planner FIRST to extract everything using LLM
    planner_output = planner_agent(current_state.copy())

    # ✅ Step 2: Check if first run
    is_first_run = not bool(prev_state)

    # ✅ Step 3: Detect changes AFTER planner extraction
    if is_first_run:
        changed = set()
    else:
        changed = detect_changed_fields(prev_state, planner_output)

    # ✅ Step 4: Decide agents
    agents = agents_to_run(changed, is_first_run)

    # ✅ Step 5: Replan message
    replan_msg = describe_replan(changed, agents)

    print(f"\n[Replan] {replan_msg}")
    print(f"[Replan] Agents running: {agents}\n")

    # ✅ Step 6: Merge previous + updated planner state
    merged_state = {**prev_state, **planner_output}

    # ✅ Step 7: Build graph
    graph = build_graph(agents)

    # ✅ Step 8: Run graph
    result = graph.invoke(merged_state)

    # ✅ Step 9: Preserve old outputs for skipped agents
    for agent in AGENT_FN.keys():
        if agent not in agents:
            if agent in prev_state:
                result[agent] = prev_state[agent]

    # ✅ Step 10: Save replanning metadata
    result["_replan_agents"] = agents
    result["_replan_message"] = replan_msg
    result["_changed_fields"] = list(changed)

    return result, replan_msg


# def invoke_smart(current_state: dict, prev_state: dict):
    
#     is_first_run = not bool(prev_state)
 
#     if is_first_run:
#         changed = set()
#     else:
#         changed = detect_changed_fields(prev_state, current_state)
 
#     agents = agents_to_run(changed, is_first_run)
#     replan_msg = describe_replan(changed, agents)
 
#     print(f"\n[Replan] {replan_msg}")
#     print(f"[Replan] Agents running: {agents}\n")
 
    
#     merged_state = {**prev_state, **current_state}
 
#     graph = build_graph(agents)
#     result = graph.invoke(merged_state)
 
  
#     for agent in AGENT_FN.keys():
#         if agent not in agents:
#             if agent in prev_state:
#                 result[agent] = prev_state[agent]
 

#     result["_replan_agents"] = agents
#     result["_replan_message"] = replan_msg
#     result["_changed_fields"] = list(changed)
 
#     return result, replan_msg
 
 

if __name__ == "__main__":
    try:
        build_graph().get_graph().draw_mermaid_png(
            output_file_path="graph_diagram.png"
        )
        print("Graph saved as graph_diagram.png")
    except Exception as e:
        print(" Could not render diagram:", e)
 
 