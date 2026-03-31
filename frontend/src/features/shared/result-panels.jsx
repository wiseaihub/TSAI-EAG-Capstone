import { Alert, AlertDescription, AlertTitle } from "../../components/ui/alert";
import { Badge } from "../../components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card";

function badgeVariantForRisk(risk) {
  const normalized = String(risk || "").toLowerCase();
  if (normalized.includes("high")) return "risk_high";
  if (normalized.includes("moderate")) return "risk_moderate";
  if (normalized.includes("low")) return "risk_low";
  return "outline";
}

export function RiskSummaryCard({ title, summary }) {
  if (!summary) return null;
  return (
    <Card className="border-slate-200/90">
      <CardHeader className="pb-3">
        <CardTitle className="text-base">{title}</CardTitle>
        <CardDescription>Primary risk indicators from the latest run.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="flex items-center gap-3">
          <span className="text-sm text-[var(--muted-foreground)]">Risk Level</span>
          <Badge variant={badgeVariantForRisk(summary.risk_level)}>
            {String(summary.risk_level || "Unknown")}
          </Badge>
        </div>
        <p className="text-sm">
          <span className="text-[var(--muted-foreground)]">Confidence:</span>{" "}
          <span className="font-medium">{String(summary.confidence ?? "n/a")}</span>
        </p>
        {summary.session_id && (
          <p className="text-xs text-[var(--muted-foreground)]">
            Session ID: {summary.session_id}
          </p>
        )}
      </CardContent>
    </Card>
  );
}

export function FlagListCard({ title, flags, emptyLabel = "No flags returned." }) {
  const normalizedFlags = Array.isArray(flags) ? flags : [];
  return (
    <Card className="border-slate-200/90">
      <CardHeader className="pb-3">
        <CardTitle className="text-base">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        {normalizedFlags.length === 0 ? (
          <p className="text-sm text-[var(--muted-foreground)]">{emptyLabel}</p>
        ) : (
          <ul className="space-y-2 text-sm leading-relaxed">
            {normalizedFlags.map((flag, idx) => (
              <li key={`${flag}-${idx}`} className="rounded-lg bg-slate-50 p-2.5">
                {String(flag)}
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}

export function RecommendationsCard({ recommendations, label }) {
  if (!Array.isArray(recommendations) || recommendations.length === 0) return null;
  return (
    <Card className="border-emerald-200 bg-emerald-50/50">
      <CardHeader className="pb-3">
        <CardTitle className="text-base">{label || "Recommended next steps"}</CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="space-y-2 text-sm leading-relaxed">
          {recommendations.map((item, idx) => (
            <li key={`${item}-${idx}`}>{String(item)}</li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}

export function CrisisAlert({ screening }) {
  if (!screening) return null;
  if (!screening.crisis_message && !screening.disclaimer) return null;
  return (
    <Alert variant={screening.crisis_message ? "destructive" : "warning"}>
      <AlertTitle>
        {screening.crisis_message ? "Immediate escalation guidance" : "Clinical safety notice"}
      </AlertTitle>
      <AlertDescription>
        <div className="space-y-2">
          {screening.disclaimer ? <p>{screening.disclaimer}</p> : null}
          {screening.crisis_message ? <p className="font-semibold">{screening.crisis_message}</p> : null}
        </div>
      </AlertDescription>
    </Alert>
  );
}

export function TechnicalDetails({ data }) {
  if (!data) return null;
  return (
    <details className="rounded-xl border bg-slate-50/80 p-3 text-xs">
      <summary className="cursor-pointer font-medium text-slate-700">Technical details (raw JSON)</summary>
      <pre className="mt-3 overflow-x-auto whitespace-pre-wrap text-slate-700">
        {JSON.stringify(data, null, 2)}
      </pre>
    </details>
  );
}

