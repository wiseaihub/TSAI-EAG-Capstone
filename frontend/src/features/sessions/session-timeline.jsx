import { Clock3, RefreshCcw } from "lucide-react";
import { Alert, AlertDescription } from "../../components/ui/alert";
import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card";

function badgeVariantForRisk(riskLevel) {
  const normalized = String(riskLevel || "").toLowerCase();
  if (normalized.includes("high")) return "risk_high";
  if (normalized.includes("moderate")) return "risk_moderate";
  if (normalized.includes("low")) return "risk_low";
  return "outline";
}

export function SessionTimeline({ sessions, loading, error, onRefresh }) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-start justify-between gap-3">
        <div>
          <CardTitle className="flex items-center gap-2">
            <Clock3 className="h-5 w-5 text-slate-600" />
            Recent Agent Sessions
          </CardTitle>
          <CardDescription>Latest persisted runs for the signed-in user.</CardDescription>
        </div>
        <Button variant="outline" onClick={onRefresh} disabled={loading} className="gap-2">
          <RefreshCcw className="h-4 w-4" />
          Refresh
        </Button>
      </CardHeader>
      <CardContent className="space-y-4">
        {error ? (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        ) : null}
        {loading ? <p className="text-sm text-[var(--muted-foreground)]">Loading sessions...</p> : null}
        {!loading && Array.isArray(sessions) && sessions.length === 0 ? (
          <p className="text-sm text-[var(--muted-foreground)]">No sessions available yet.</p>
        ) : null}
        <div className="space-y-3">
          {Array.isArray(sessions) &&
            sessions.map((item) => (
              <div
                key={item.session_id}
                className="rounded-xl border bg-slate-50/80 p-3.5"
              >
                <div className="mb-2 flex flex-wrap items-center gap-2">
                  <span className="text-sm font-medium">{item.agent_name || "unknown_agent"}</span>
                  <Badge variant={badgeVariantForRisk(item.risk_level)}>{item.risk_level || "Unknown"}</Badge>
                </div>
                <p className="text-xs text-[var(--muted-foreground)]">Session: {item.session_id}</p>
                <p className="text-xs text-[var(--muted-foreground)]">Confidence: {String(item.confidence ?? "n/a")}</p>
                {Array.isArray(item.flags) && item.flags.length > 0 ? (
                  <ul className="mt-2 space-y-1 text-xs">
                    {item.flags.slice(0, 4).map((flag, index) => (
                      <li key={`${item.session_id}-${index}`}>{String(flag)}</li>
                    ))}
                  </ul>
                ) : null}
              </div>
            ))}
        </div>
      </CardContent>
    </Card>
  );
}
