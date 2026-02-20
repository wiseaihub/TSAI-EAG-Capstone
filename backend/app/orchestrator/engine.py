from app.agents.cbc_agent import analyze_cbc

def run_agents(payload):
    results = {}

    results["cbc"] = analyze_cbc(payload)

    # later:
    # results["vitals"] = analyze_vitals(...)
    # results["risk_fusion"] = aggregate(results)

    return results
