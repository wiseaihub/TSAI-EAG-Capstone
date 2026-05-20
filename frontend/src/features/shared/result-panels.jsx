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

function normalizeLines(value) {
  if (!value) return [];
  if (Array.isArray(value)) return value.map((x) => String(x || "").trim()).filter(Boolean);
  const s = String(value).trim();
  return s ? [s] : [];
}

export function RiskSummaryCard({ title, summary }) {
  if (!summary) return null;
  const rationaleLines = normalizeLines(summary.rationale_lines);
  const citations = normalizeLines(summary.evidence_citations);
  const disclaimer = summary.disclaimer ? String(summary.disclaimer).trim() : "";

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
        {disclaimer ? (
          <p className="rounded-lg bg-amber-50/90 p-2.5 text-xs leading-relaxed text-amber-950">{disclaimer}</p>
        ) : null}
        {rationaleLines.length > 0 ? (
          <div className="space-y-1">
            <p className="text-xs font-semibold uppercase tracking-wide text-[var(--muted-foreground)]">
              Transparent rationale
            </p>
            <ul className="list-disc space-y-1 pl-5 text-sm leading-relaxed">
              {rationaleLines.map((line, idx) => (
                <li key={`${idx}-${line.slice(0, 24)}`}>{line}</li>
              ))}
            </ul>
          </div>
        ) : null}
        {citations.length > 0 ? (
          <div className="space-y-1">
            <p className="text-xs font-semibold uppercase tracking-wide text-[var(--muted-foreground)]">
              Evidence / methods notes
            </p>
            <ul className="list-disc space-y-1 pl-5 text-xs leading-relaxed text-[var(--muted-foreground)]">
              {citations.map((c, idx) => (
                <li key={`${idx}-${c.slice(0, 24)}`}>{c}</li>
              ))}
            </ul>
          </div>
        ) : null}
        {Array.isArray(summary.flags) && summary.flags.length > 0 ? (
          <div className="space-y-1">
            <p className="text-xs font-semibold uppercase tracking-wide text-[var(--muted-foreground)]">
              Diagnostic flags
            </p>
            <ul className="list-disc space-y-1 pl-5 text-xs leading-relaxed text-rose-900">
              {summary.flags.map((flag, idx) => (
                <li key={`${idx}-${String(flag).slice(0, 24)}`}>{String(flag)}</li>
              ))}
            </ul>
          </div>
        ) : null}
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

/** When local deterministic tier is High and no MH crisis banner already covers escalation. */
export function HighRiskEscalationNotice({ summary }) {
  if (!summary) return null;
  if (summary.crisis_message) return null;
  const rl = String(summary.risk_level || "").toLowerCase();
  if (!rl.includes("high")) return null;
  return (
    <Alert variant="destructive">
      <AlertTitle>High risk tier — prioritize clinical correlation</AlertTitle>
      <AlertDescription className="text-sm leading-relaxed">
        Local screening engines flagged a high-concern band. Correlate with history, examination, and institutional
        pathways before disposition. This CDSS does not replace clinician judgement or emergency protocols.
      </AlertDescription>
    </Alert>
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

