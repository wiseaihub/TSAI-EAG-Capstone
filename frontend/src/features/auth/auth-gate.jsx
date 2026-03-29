import { LogIn, LogOut } from "lucide-react";
import { Alert, AlertDescription } from "../../components/ui/alert";
import { Button } from "../../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card";
import { Input } from "../../components/ui/input";
import { Label } from "../../components/ui/label";

export function LoginPanel({
  email,
  password,
  authError,
  onEmailChange,
  onPasswordChange,
  onLogin,
}) {
  return (
    <Card className="mx-auto mt-12 w-full max-w-md">
      <CardHeader>
        <CardTitle className="text-2xl tracking-tight">WISE Clinical Portal</CardTitle>
        <CardDescription className="leading-relaxed">
          Secure sign-in for CBC and Mental Health workflows.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-5">
        {authError ? (
          <Alert variant="destructive">
            <AlertDescription>{authError}</AlertDescription>
          </Alert>
        ) : null}
        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <Input id="email" type="email" value={email} onChange={(e) => onEmailChange(e.target.value)} />
        </div>
        <div className="space-y-2">
          <Label htmlFor="password">Password</Label>
          <Input
            id="password"
            type="password"
            value={password}
            onChange={(e) => onPasswordChange(e.target.value)}
          />
        </div>
        <Button onClick={onLogin} className="w-full gap-2">
          <LogIn className="h-4 w-4" />
          Sign in
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
