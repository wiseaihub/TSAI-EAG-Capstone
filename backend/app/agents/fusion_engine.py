def fuse_results(results: dict):
    total_confidence = sum(r["confidence"] for r in results.values())
    avg_confidence = round(total_confidence / len(results), 2)

    high_risk = any(r["risk_level"] == "High" for r in results.values())

    return {
        "overall_risk": "High" if high_risk else "Moderate",
        "overall_confidence": avg_confidence,
        "agents": results
    }
