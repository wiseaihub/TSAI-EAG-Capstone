import { useState } from "react";
import { KeyRound, LogIn, LogOut, Mail, UserPlus } from "lucide-react";
import { Alert, AlertDescription } from "../../components/ui/alert";
import { Button } from "../../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card";
import { Input } from "../../components/ui/input";
import { Label } from "../../components/ui/label";

const AUTH_MODES = ["signin", "register", "forgot"];

export function LoginPanel({
  email,
  password,
  confirmPassword,
  authError,
  infoMessage,
  onEmailChange,
  onPasswordChange,
  onConfirmPasswordChange,
  onLogin,
  onSignUp,
  onForgotPassword,
  onClearMessages,
}) {
  const [mode, setMode] = useState("signin");

  function switchMode(next) {
    onClearMessages?.();
    setMode(next);
  }

  return (
    <Card className="mx-auto mt-12 w-full max-w-md">
      <CardHeader>
        <CardTitle className="text-2xl tracking-tight">WISE Clinical Portal</CardTitle>
        <CardDescription className="leading-relaxed">
          Shared sign-in for patient and doctor accounts. Doctor access is provisioned separately.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-5">
        <div className="flex flex-wrap gap-2 border-b border-slate-200 pb-1">
          {AUTH_MODES.map((m) => {
            const labels = { signin: "Sign in", register: "Create patient account", forgot: "Forgot password" };
            const active = mode === m;
            return (
              <button
                key={m}
                type="button"
                onClick={() => switchMode(m)}
                className={`rounded-md px-3 py-1.5 text-sm font-medium transition-colors ${
                  active
                    ? "bg-slate-900 text-white"
                    : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                }`}
              >
                {labels[m]}
              </button>
            );
          })}
        </div>

        {authError ? (
          <Alert variant="destructive">
            <AlertDescription>{authError}</AlertDescription>
          </Alert>
        ) : null}
        {infoMessage ? (
          <Alert>
            <AlertDescription>{infoMessage}</AlertDescription>
          </Alert>
        ) : null}

        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <Input id="email" type="email" value={email} onChange={(e) => onEmailChange(e.target.value)} autoComplete="email" />
        </div>

        {mode !== "forgot" ? (
          <>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => onPasswordChange(e.target.value)}
                autoComplete={mode === "register" ? "new-password" : "current-password"}
              />
            </div>
            {mode === "register" ? (
              <div className="space-y-2">
                <Label htmlFor="confirm-password">Confirm password</Label>
                <Input
                  id="confirm-password"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => onConfirmPasswordChange(e.target.value)}
                  autoComplete="new-password"
                />
              </div>
            ) : null}
          </>
        ) : null}

        {mode === "signin" ? (
          <Button onClick={onLogin} className="w-full gap-2">
            <LogIn className="h-4 w-4" />
            Sign in
          </Button>
        ) : null}
        {mode === "register" ? (
          <Button onClick={onSignUp} className="w-full gap-2">
            <UserPlus className="h-4 w-4" />
            Create account
          </Button>
        ) : null}
        {mode === "forgot" ? (
          <Button onClick={onForgotPassword} className="w-full gap-2">
            <Mail className="h-4 w-4" />
            Send reset link
          </Button>
        ) : null}
      </CardContent>
    </Card>
  );
}

export function PasswordRecoveryPanel({
  newPassword,
  confirmPassword,
  authError,
  onNewPasswordChange,
  onConfirmPasswordChange,
  onSubmit,
}) {
  return (
    <Card className="mx-auto mt-12 w-full max-w-md">
      <CardHeader>
        <CardTitle className="text-2xl tracking-tight">Set a new password</CardTitle>
        <CardDescription className="leading-relaxed">
          Choose a strong password for your WISE Clinical Portal account.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-5">
        {authError ? (
          <Alert variant="destructive">
            <AlertDescription>{authError}</AlertDescription>
          </Alert>
        ) : null}
        <div className="space-y-2">
          <Label htmlFor="new-password">New password</Label>
          <Input
            id="new-password"
            type="password"
            value={newPassword}
            onChange={(e) => onNewPasswordChange(e.target.value)}
            autoComplete="new-password"
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="recovery-confirm">Confirm new password</Label>
          <Input
            id="recovery-confirm"
            type="password"
            value={confirmPassword}
            onChange={(e) => onConfirmPasswordChange(e.target.value)}
            autoComplete="new-password"
          />
        </div>
        <Button onClick={onSubmit} className="w-full gap-2">
          <KeyRound className="h-4 w-4" />
          Update password
        </Button>
      </CardContent>
    </Card>
  );
}

export function AccountHeader({ session, onLogout }) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border bg-white px-5 py-4 shadow-[0_8px_24px_rgba(15,23,42,0.05)]">
      <div>
        <p className="text-sm text-[var(--muted-foreground)]">Signed in as</p>
        <p className="mt-0.5 text-sm font-semibold tracking-tight text-slate-900">{session?.user?.email}</p>
      </div>
      <Button variant="outline" onClick={onLogout} className="gap-2">
        <LogOut className="h-4 w-4" />
        Log out
      </Button>
    </div>
  );
}
