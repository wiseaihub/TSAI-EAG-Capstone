import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { CbcWorkflow } from "./cbc-workflow";

function baseState(overrides = {}) {
  return {
    loading: false,
    result: null,
    error: "",
    hint: "",
    ...overrides,
  };
}

describe("CbcWorkflow", () => {
  it("submits normalized payload and timeout to onAnalyze", async () => {
    const user = userEvent.setup();
    const onAnalyze = vi.fn();

    render(
      <CbcWorkflow
        mode="doctor"
        pollTimeoutSeconds={900}
        state={baseState()}
        onAnalyze={onAnalyze}
      />
    );

    await user.clear(screen.getByLabelText(/hemoglobin/i));
    await user.type(screen.getByLabelText(/hemoglobin/i), "11.2");
    await user.selectOptions(screen.getByLabelText(/sex for interpretation/i), "female");
    await user.click(screen.getByRole("button", { name: /run cbc analysis/i }));

    expect(onAnalyze).toHaveBeenCalledTimes(1);
    expect(onAnalyze).toHaveBeenCalledWith({
      payload: {
        sex: "female",
        hemoglobin: 11.2,
        wbc: 7000,
        rbc: 4.5,
        platelets: 250000,
      },
      fastMode: true,
      timeoutMs: 960000,
    });
  });

  it("shows loading state with disabled submit", () => {
    render(
      <CbcWorkflow
        mode="doctor"
        pollTimeoutSeconds={900}
        state={baseState({ loading: true })}
        onAnalyze={vi.fn()}
      />
    );

    expect(screen.getByRole("button", { name: /running cbc analysis/i })).toBeDisabled();
    expect(screen.getByText(/current wait window/i)).toBeInTheDocument();
  });

  it("renders result cards when state.result exists", () => {
    render(
      <CbcWorkflow
        mode="doctor"
        pollTimeoutSeconds={900}
        state={baseState({
          result: {
            cbc: {
              risk_level: "low",
              confidence: "0.82",
              display_labels: ["HGB"],
              flags: ["mild anemia"],
            },
            wise: {
              risk_level: "moderate",
              confidence: "0.71",
              flags: ["follow up in 2 weeks"],
            },
            recommendations: ["repeat CBC in 2 weeks"],
          },
        })}
        onAnalyze={vi.fn()}
      />
    );

    expect(screen.getByText(/cbc local engine/i)).toBeInTheDocument();
    expect(screen.getByText(/wise narrative engine/i)).toBeInTheDocument();
    expect(screen.getAllByText(/repeat cbc in 2 weeks/i).length).toBeGreaterThan(0);
  });
});
