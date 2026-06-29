import streamlit as st
import re
from graph.workflow import invoke_smart
 

st.set_page_config(
    page_title="Smart Trip Planner",
    page_icon="✈️",
    layout="wide"
)
 
st.title("✈️ Smart Trip Planning Assistant")


# def extract_fields_from_text(text, state):
#     text_lower = text.lower()
 
#     # Budget Extraction
#     budget_match = re.search(r'(\d{4,6})', text_lower)
#     if budget_match:
#         state["trip_budget"] = int(budget_match.group(1))
 
#     # Days Extraction
#     days_match = re.search(r'(\d+)[-\s]?day', text_lower)
#     if days_match:
#         state["trip_days"] = int(days_match.group(1))
 
#     # Place Extraction (basic demo)
#     places = ["mumbai", "goa", "delhi", "manali", "jaipur"]
#     for p in places:
#         if p in text_lower:
#             state["trip_place"] = p.capitalize()
 
#     # Month Extraction
#     months = [
#         "january","february","march","april","may","june",
#         "july","august","september","october","november","december"
#     ]
#     for m in months:
#         if m in text_lower:
#             state["trip_dates"] = m.capitalize()
 
#     return state

def extract_fields_from_text(text, state):
    text_lower = text.lower()

    # ✅ Budget Extraction (keep this - useful for quick detection)
    budget_match = re.search(r'(\d{4,6})', text_lower)
    if budget_match:
        state["trip_budget"] = int(budget_match.group(1))

    # ✅ Days Extraction (keep this)
    days_match = re.search(r'(\d+)[-\s]?day', text_lower)
    if days_match:
        state["trip_days"] = int(days_match.group(1))


    # ✅ Month Extraction (optional but safe)
    months = [
        "january","february","march","april","may","june",
        "july","august","september","october","november","december"
    ]
    for m in months:
        if m in text_lower:
            state["trip_dates"] = m.capitalize()

    return state
 

# Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
 
if "trip_state" not in st.session_state:
    st.session_state.trip_state = {}
 

# Sidebar
with st.sidebar:
    st.header("🔍 Agent Outputs")
 
    state = st.session_state.trip_state
 
    choice = st.selectbox(
        "Select agent output:",
        [
            "Weather & best time",
            "Destination",
            "Transport",
            "Budget",
            "Final Itinerary",
        ],
    )
 
    if choice == "Weather & best time":
        st.write(state.get("weather_info", "Not available"))
        st.markdown(f"**Best time:** {state.get('best_time', 'Not available')}")
 
    elif choice == "Destination":
        st.write(state.get("place_info", "Not available"))
 
    elif choice == "Transport":
        st.write(state.get("transport_info", "Not available"))
 
    elif choice == "Budget":
        st.write(state.get("budget_info", "Not available"))
 
    elif choice == "Final Itinerary":
        st.write(state.get("final_itinerary", "Not available"))
 
    # Replan Info
    replan_msg = state.get("_replan_message", "")
    if replan_msg:
        st.divider()
        st.subheader("♻️ Replan Info")
        st.info(replan_msg)
 
        changed = state.get("_changed_fields", [])
        if changed:
            st.markdown(f"**Changed:** `{'`, `'.join(changed)}`")
 
        ran = state.get("_replan_agents", [])
        all_agents = ["weather", "destination", "transport", "budget", "itinerary"]
        skipped = [a for a in all_agents if a not in ran]
 
        if ran:
            st.markdown(f"**Ran:** `{'`, `'.join(ran)}`")
        if skipped:
            st.markdown(f"**Skipped:** `{'`, `'.join(skipped)}`")
 

# Chat History Display
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
 
# --------------------------------------------------
# Chat Input
# --------------------------------------------------
user_input = st.chat_input("Describe your trip...")
 
if user_input:
 
    # Show user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })
 
    with st.chat_message("user"):
        st.markdown(user_input)
 
    with st.chat_message("assistant"):
        with st.spinner("Planning your trip..."):
 
            # FULL previous state
            prev_state = st.session_state.trip_state.copy()
 
            # Build current state
            current = prev_state.copy()
            current["user_input"] = user_input
 
            # CRITICAL FIX: Extract BEFORE replan
            current = extract_fields_from_text(user_input, current)
 
            current["chat_history"] = [
                m["content"]
                for m in st.session_state.chat_history
                if m["role"] == "user"
            ]
 
            current["trace"] = []
 
            # Smart execution
            result, replan_msg = invoke_smart(current, prev_state)
 
            # Save state
            st.session_state.trip_state = result
 
            
            # Response Handling
            if result.get("need_clarification"):
                response = (
                    "Please provide: "
                    + ", ".join(result.get("missing_fields", []))
                )
                st.warning(response)
 
            elif result.get("final_itinerary"):
 
                changed = result.get("_changed_fields", [])
                ran_agents = result.get("_replan_agents", [])
 
                if changed:
                    label_map = {
                        "trip_place": "destination",
                        "trip_dates": "travel dates",
                        "trip_days": "trip duration",
                        "trip_budget": "budget",
                        "trip_style": "trip style",
                    }
 
                    readable = [label_map.get(f, f) for f in changed]
 
                    response = (
                        f"♻️ Replanned → Updated: `{'`, `'.join(readable)}`\n\n"
                        f"Agents run: `{'`, `'.join(ran_agents)}`\n\n"
                        f"✅ Trip updated!"
                    )
                else:
                    response = "✅ Trip plan generated!"
 
                st.success(response)
 
            else:
                response = "⚠️ Not enough info to generate plan."
                st.warning(response)
 
    # Save assistant response
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response
    })
 

# Final Output
st.divider()
st.subheader("Final Trip Plan")
 
if st.session_state.trip_state.get("final_itinerary"):
    st.markdown(st.session_state.trip_state["final_itinerary"])
else:
    st.info("Your final trip itinerary will appear here.")
 