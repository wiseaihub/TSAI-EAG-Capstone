import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";

import { ClinicalPilotBanner } from "./clinical-pilot-banner";

describe("ClinicalPilotBanner", () => {
  it("renders CBC pillar copy", () => {
    render(<ClinicalPilotBanner pillar="cbc" />);
    expect(screen.getByText(/CBC — clinical decision support/i)).toBeInTheDocument();
    expect(screen.getByText(/licensed clinician/i)).toBeInTheDocument();
  });

  it("renders mental health pillar copy", () => {
    render(<ClinicalPilotBanner pillar="mental-health" />);
    expect(screen.getByText(/Mental health — clinical decision support/i)).toBeInTheDocument();
    expect(screen.getByText(/not for emergencies/i)).toBeInTheDocument();
  });
});
