import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MentalHealthWorkflow } from "./mh-workflow";

function baseState(overrides = {}) {
  return {
    loading: false,
    result: null,
    error: "",
    hint: "",
    ...overrides,
  };
}

describe("MentalHealthWorkflow", () => {
  it("submits validated payload and timeout to onAnalyze", async () => {
    const user = userEvent.setup();
    const onAnalyze = vi.fn();

    render(
      <MentalHealthWorkflow
        mode="doctor"
        pollTimeoutSeconds={900}
        state={baseState()}
        onAnalyze={onAnalyze}
      />
    );

    await user.type(screen.getByLabelText(/optional note/i), "Patient reports poor sleep");
    await user.click(screen.getByRole("button", { name: /run mental health screening/i }));

    expect(onAnalyze).toHaveBeenCalledTimes(1);
    expect(onAnalyze).toHaveBeenCalledWith({
      payload: {
        include_s18: true,
        fast: true,
        suicidal_ideation: false,
        self_harm_intent: false,
        concern_text: "Patient reports poor sleep",
        phq9_total: 12,
        gad7_total: 8,
      },
      timeoutMs: 1200000,
    });
  });

  it("shows validation error and blocks submit callback on invalid PHQ-9 total", async () => {
    const user = userEvent.setup();
    const onAnalyze = vi.fn();

    render(
      <MentalHealthWorkflow
        mode="doctor"
        pollTimeoutSeconds={900}
        state={baseState()}
        onAnalyze={onAnalyze}
      />
    );

    await user.clear(screen.getByLabelText(/phq-9 total/i));
    await user.type(screen.getByLabelText(/phq-9 total/i), "40");
    await user.click(screen.getByRole("button", { name: /run mental health screening/i }));

    expect(screen.getByText(/phq-9 total must be 0 to 27/i)).toBeInTheDocument();
    expect(onAnalyze).not.toHaveBeenCalled();
  });

  it("renders result cards and crisis section when screening result is present", () => {
    render(
      <MentalHealthWorkflow
        mode="doctor"
        pollTimeoutSeconds={900}
        state={baseState({
          result: {
            screening: {
              risk_level: "high",
              confidence: "0.89",
              display_labels: ["PHQ9 severe"],
              crisis_message: "Immediate in-person assessment advised",
            },
            wise: {
              risk_level: "moderate",
              confidence: "0.70",
              flags: ["sleep disturbance"],
            },
            recommendations: ["Escalate to emergency psychiatric care"],
          },
        })}
        onAnalyze={vi.fn()}
      />
    );

    expect(screen.getByText(/^local screening$/i)).toBeInTheDocument();
    expect(screen.getByText(/^s18 narrative screening$/i)).toBeInTheDocument();
    expect(screen.getAllByText(/immediate in-person assessment advised/i).length).toBeGreaterThan(0);
    expect(screen.getAllByText(/escalate to emergency psychiatric care/i).length).toBeGreaterThan(0);
  });
});
