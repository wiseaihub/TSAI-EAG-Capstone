import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { QuickSummaryCard } from "./quick-summary-card";

describe("QuickSummaryCard", () => {
  it("renders nothing when both results are null", () => {
    const { container } = render(<QuickSummaryCard cbcResult={null} mhResult={null} />);
    expect(container).toBeEmptyDOMElement();
  });

  it("extracts diagnosis, critical red flags, and recommended action from a CBC result", () => {
    const cbcResult = {
      diagnosis: "Mild anemia",
      critical_red_flags: ["Low hemoglobin", "Normal platelets"],
      recommended_action: "Repeat CBC in 4 weeks",
    };
    render(<QuickSummaryCard cbcResult={cbcResult} mhResult={null} />);

    expect(screen.getByText("CBC")).toBeInTheDocument();
    expect(screen.getByText("Mild anemia")).toBeInTheDocument();
    expect(screen.getByText(/low hemoglobin/i)).toBeInTheDocument();
    expect(screen.getByText(/repeat cbc/i)).toBeInTheDocument();
  });

  it("filters red flags to critical ones when mixed with benign flags", () => {
    const cbcResult = {
      diagnosis: "Evaluation pending",
      red_flags: ["mild fatigue", "suicidal ideation noted", "elevated WBC suggests leukocytosis"],
      recommended_action: "Refer to hematology",
    };
    render(<QuickSummaryCard cbcResult={cbcResult} mhResult={null} />);

    const flags = screen.getByText(/suicidal ideation/i);
    expect(flags).toBeInTheDocument();
    expect(flags.textContent).not.toMatch(/mild fatigue/i);
  });

  it("renders mental-health summary above the CBC summary when both are present", () => {
    const cbcResult = { diagnosis: "CBC normal", recommended_action: "No follow-up" };
    const mhResult = { diagnosis: "Moderate depression", recommended_action: "Schedule therapy" };
    render(<QuickSummaryCard cbcResult={cbcResult} mhResult={mhResult} />);

    const sources = screen.getAllByText(/^(CBC|Mental Health)$/);
    expect(sources.map((n) => n.textContent)).toEqual(["Mental Health", "CBC"]);
  });

  it("falls back to a risk-level phrase when no diagnosis field is returned", () => {
    const cbcResult = {
      wise: { risk_level: "high" },
    };
    render(<QuickSummaryCard cbcResult={cbcResult} mhResult={null} />);
    expect(screen.getByText(/high risk profile/i)).toBeInTheDocument();
  });
});
