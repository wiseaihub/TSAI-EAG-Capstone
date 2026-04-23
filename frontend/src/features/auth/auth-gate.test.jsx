import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { AccountHeader, LoginPanel, PasswordRecoveryPanel } from "./auth-gate";

function renderLoginPanel(overrides = {}) {
  const props = {
    email: "",
    password: "",
    confirmPassword: "",
    authError: "",
    infoMessage: "",
    onEmailChange: vi.fn(),
    onPasswordChange: vi.fn(),
    onConfirmPasswordChange: vi.fn(),
    onLogin: vi.fn(),
    onSignUp: vi.fn(),
    onForgotPassword: vi.fn(),
    onClearMessages: vi.fn(),
    ...overrides,
  };
  render(<LoginPanel {...props} />);
  return props;
}

// The LoginPanel has a mode-switcher with tab buttons ("Sign in", "Create patient account",
// "Forgot password") AND a submit CTA with the same accessible name. Disambiguate by
// picking the last match ordered in DOM — the CTA always renders after the tab row.
function lastButton(nameMatcher) {
  const matches = screen.getAllByRole("button", { name: nameMatcher });
  return matches[matches.length - 1];
}

describe("LoginPanel", () => {
  it("renders the sign-in tab by default with email + password fields", () => {
    renderLoginPanel();
    expect(screen.getByRole("heading", { name: /wise clinical portal/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^password$/i)).toBeInTheDocument();
    expect(screen.getAllByRole("button", { name: /^sign in$/i }).length).toBeGreaterThanOrEqual(1);
  });

  it("fires onLogin when the sign-in CTA is clicked", async () => {
    const user = userEvent.setup();
    const props = renderLoginPanel({ email: "doc@wise.test", password: "secret" });
    await user.click(lastButton(/^sign in$/i));
    expect(props.onLogin).toHaveBeenCalledTimes(1);
  });

  it("switches to register mode and shows confirm-password + clears messages", async () => {
    const user = userEvent.setup();
    const props = renderLoginPanel();
    await user.click(lastButton(/create patient account/i));
    expect(props.onClearMessages).toHaveBeenCalled();
    expect(screen.getByLabelText(/confirm password/i)).toBeInTheDocument();
  });

  it("switches to forgot-password mode and hides the password field", async () => {
    const user = userEvent.setup();
    renderLoginPanel();
    await user.click(lastButton(/forgot password/i));
    expect(screen.queryByLabelText(/^password$/i)).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: /send reset link/i })).toBeInTheDocument();
  });

  it("renders authError as a destructive alert", () => {
    renderLoginPanel({ authError: "Invalid login credentials" });
    expect(screen.getByText(/invalid login credentials/i)).toBeInTheDocument();
  });
});

describe("AccountHeader", () => {
  it("shows the signed-in email and fires onLogout", async () => {
    const user = userEvent.setup();
    const onLogout = vi.fn();
    render(<AccountHeader session={{ user: { email: "doc@wise.test" } }} onLogout={onLogout} />);
    expect(screen.getByText("doc@wise.test")).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: /log out/i }));
    expect(onLogout).toHaveBeenCalledTimes(1);
  });
});

describe("PasswordRecoveryPanel", () => {
  it("fires onSubmit when update button clicked", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();
    render(
      <PasswordRecoveryPanel
        newPassword="new-pass"
        confirmPassword="new-pass"
        authError=""
        onNewPasswordChange={vi.fn()}
        onConfirmPasswordChange={vi.fn()}
        onSubmit={onSubmit}
      />
    );
    await user.click(screen.getByRole("button", { name: /update password/i }));
    expect(onSubmit).toHaveBeenCalledTimes(1);
  });
});
