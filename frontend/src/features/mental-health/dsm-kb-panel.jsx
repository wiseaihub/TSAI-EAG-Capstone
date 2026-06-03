import { BookOpen, Library } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "../../components/ui/alert";
import { Badge } from "../../components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card";

/** Explains how DSM-5–style reference material is used when S18 is enabled. */
export function DsmKbWorkflowHint({ includeS18 }) {
  return (
    <Alert className="border-indigo-200 bg-indigo-50/60">
      <Library className="h-4 w-4 text-indigo-700" />
      <AlertTitle className="text-indigo-950">DSM‑5 reference knowledge base</AlertTitle>
      <AlertDescription className="space-y-2 text-sm leading-relaxed text-indigo-950/90">
        <p>
          When <strong>Include S18 narrative pass</strong> is on, WISE sends a <code className="rounded bg-white/80 px-1">[Task: mental_health]</code>{" "}
          query to your integrated S18 runtime. If that stack has the mental‑health RAG folder indexed (for example{" "}
          <code className="rounded bg-white/80 px-1">wise/mental_health/DSM‑5_reference.pdf</code>), retrieval can ground the narrative in
          DSM‑5–aligned reference text.
        </p>
        <p className="text-xs text-indigo-950/80">
          This is adjunct reference material for clinicians, not automated diagnosis. Institutional licensing and privacy rules for the manual
          still apply.
        </p>
        {!includeS18 ? (
          <p className="text-xs font-medium text-amber-900">
            S18 is currently off — only local PHQ‑9/GAD‑7 scoring runs; no remote DSM‑5 RAG pass.
          </p>
        ) : (
          <div className="flex flex-wrap gap-2 pt-1">
            <Badge variant="outline" className="border-indigo-300 bg-white/90 text-indigo-900">
              S18 + mental_health task
            </Badge>
            <Badge variant="outline" className="border-indigo-300 bg-white/90 text-indigo-900">
              Optional RAG grounding
            </Badge>
          </div>
        )}
      </AlertDescription>
    </Alert>
  );
}

function normalizeLines(value) {
  if (!value) return [];
  if (Array.isArray(value)) return value.map((x) => String(x || "").trim()).filter(Boolean);
  const s = String(value).trim();
  return s ? [s] : [];
}

/** After a run: show narrative and KB-style snippets returned from S18 (when the adapter extracts them). */
export function DsmKbWiseGrounding({ wise }) {
  if (!wise || typeof wise !== "object") return null;

  const snippets = normalizeLines(wise.kb_snippets);
  const narrative = typeof wise.wise_narrative === "string" ? wise.wise_narrative.trim() : "";

  if (!narrative && snippets.length === 0) return null;

  return (
    <Card className="border-indigo-200/90 bg-white">
      <CardHeader className="pb-2">
        <CardTitle className="flex items-center gap-2 text-base">
          <BookOpen className="h-4 w-4 text-indigo-700" />
          DSM‑5 KB grounding (S18)
        </CardTitle>
        <CardDescription>
          Excerpts and narrative fields extracted from the S18 run when the planner exposes retrievals or long‑form output.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {narrative ? (
          <div className="space-y-2">
            <p className="text-xs font-semibold uppercase tracking-wide text-[var(--muted-foreground)]">
              Narrative synthesis
            </p>
            <div className="max-h-72 overflow-y-auto rounded-lg border bg-slate-50/90 p-3 text-sm leading-relaxed whitespace-pre-wrap">
              {narrative}
            </div>
          </div>
        ) : null}

        {snippets.length > 0 ? (
          <div className="space-y-2">
            <p className="text-xs font-semibold uppercase tracking-wide text-[var(--muted-foreground)]">
              Retrieved reference snippets
            </p>
            <ul className="space-y-2 text-sm leading-relaxed">
              {snippets.map((line, idx) => (
                <li key={`snippet-${idx}-${line.slice(0, 40)}`} className="rounded-lg border border-indigo-100 bg-indigo-50/40 p-3">
                  {line}
                </li>
              ))}
            </ul>
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
}
