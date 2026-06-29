# ✈️ Smart Trip Planning Assistant

A multi-agent trip planner built with **LangGraph**, **Gemini**, and **Serper (Google Search)**, with a **Streamlit** chat UI.

The system uses a **dynamic multi-agent workflow with smart replanning**. Instead of running all agents every time, it detects user changes and selectively executes only the affected agents.

---

## Workflow

```mermaid
flowchart TD

    U([User Input])

    U --> PL[Planner Agent
    <br/>Extracts all fields using LLM
    <br/>Updates state]

    PL --> RC[Replan Controller
    <br/>Detects changed fields
    <br/>Selects required agents]

    RC -->|Missing info| ASK([Ask User]) --> U

    RC -->|First run or Changes| W[Weather Agent
    <br/>OpenWeather + Serper]

    W --> D[Destination Agent
    <br/>Serper + Gemini]

    D --> T[Transport Agent
    <br/>Serper]

    T --> B[Budget Agent
    <br/>Serper + Gemini]

    B --> I[Itinerary Agent
    <br/>Gemini]

    I --> OUT([Final Day-wise Plan])

    OUT --> FU{User follow-up?}

    FU -->|Yes| U
    FU -->|No| END([End])
``