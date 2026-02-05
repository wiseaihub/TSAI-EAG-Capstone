> ⚠ Deprecated – see WISE_AI_CDSS_Architecture.md

## Architecture Diagram (Rendered)
![WISE AI CDSS Architecture](wise_ai_cdss_architecture.svg)

```mermaid
graph TD
    %% Actors
    Patient[Patient User]
    Doctor[Doctor User]

    %% EHR
    EHR[EHR UI<br/>(WISE Doctor)]

    %% WISE AI Components
    Plugin[WISE AI Plugin<br/>(Consent-based Capture & Research)]
    CDSS[WISE AI CDSS Web App<br/>(Agentic Reasoning UI)]
    KB[Shared Knowledge Bank]

    %% Agents
    SymptomAgent[Symptom Agent]
    CBCAgent[CBC / Lab Agent]
    TrendAgent[Trend / History Agent]
    ResearchAgent[Research Agent]
    ActionAgent[Action / Recommendation Agent]

    %% User Interaction
    Patient -->|Uses EHR| EHR
    Doctor -->|Uses EHR| EHR

    %% Invocation
    EHR -->|Click "WISE AI"| Plugin

    %% Data Capture
    Plugin -->|Consent-based Extraction| KB
    Plugin -->|Triggers Analysis| CDSS

    %% Agentic Reasoning
    CDSS --> SymptomAgent
    CDSS --> CBCAgent
    CDSS --> TrendAgent
    CDSS --> ResearchAgent

    SymptomAgent --> ActionAgent
    CBCAgent --> ActionAgent
    TrendAgent --> ActionAgent
    ResearchAgent --> ActionAgent

    %% Outputs
    ActionAgent -->|Recommendations, Notes, Guidance| CDSS

    %% Feedback Loop
    CDSS -->|Confidence Score & Missing Signals| CDSS
    CDSS -->|Optional Feedback| KB
