import { Card, CardContent, CardHeader, CardTitle } from "../../components/ui/card";

const DIAGNOSIS_KEYS = ["diagnosis", "Diagnosis", "primary_diagnosis", "assessment", "summary"];
const RED_FLAG_KEYS = [
  "critical_red_flags",
  "criticalRedFlags",
  "Critical Red Flags",
  "red_flags",
  "redFlags",
  "flags",
];
const ACTION_KEYS = [
  "recommended_action",
  "recommendedAction",
  "Recommended Action",
  "recommendation",
  "next_step",
  "next_steps",
  "recommendations",
];

const CRITICAL_FLAG_PATTERN =
  /(critical|crisis|urgent|severe|suicid|self[_\s-]?harm|hemorrhage|sepsis|anemia|thrombocytopenia|leukocytosis)/i;

function toText(value) {
  if (value == null) return "";
  if (Array.isArray(value)) {
    return value
      .map((item) => String(item || "").trim())
      .filter(Boolean)
      .join(" | ");
  }
  if (typeof value === "object") return "";
  return String(value).trim();
}

function asList(value) {
  if (Array.isArray(value)) return value.map((v) => String(v || "").trim()).filter(Boolean);
  if (typeof value === "string" && value.trim()) return [value.trim()];
  return [];
}

function pickFirstText(candidates, keys) {
  for (const source of candidates) {
    if (!source || typeof source !== "object") continue;
    for (const key of keys) {
      const text = toText(source[key]);
      if (text) return text;
    }
  }
  return "";
}

function extractSummaryFromResult(result, kindLabel) {
  if (!result || typeof result !== "object") return null;

  const candidates = [result];
  if (result.cbc) candidates.push(result.cbc);
  if (result.screening) candidates.push(result.screening);
  if (result.wise) candidates.push(result.wise);

  let diagnosis = pickFirstText(candidates, DIAGNOSIS_KEYS);
  if (!diagnosis) {
    const displayLabels = asList(result.cbc?.display_labels ?? result.screening?.display_labels ?? result.display_labels);
    if (displayLabels.length) diagnosis = displayLabels[0];
  }
  if (!diagnosis) {
    const risk = toText(result.wise?.risk_level || result.cbc?.risk_level || result.screening?.risk_level || result.risk_level);
    if (risk) diagnosis = `${risk} risk profile`;
  }

  let redFlags = [];
  for (const source of candidates) {
    if (!source || typeof source !== "object") continue;
    for (const key of RED_FLAG_KEYS) {
      redFlags = redFlags.concat(asList(source[key]));
    }
  }
  redFlags = Array.from(new Set(redFlags));
  const criticalFlags = redFlags.filter((flag) => CRITICAL_FLAG_PATTERN.test(flag));
  const redFlagText = (criticalFlags.length ? criticalFlags : redFlags).slice(0, 3).join(" | ");

  let action = pickFirstText(candidates, ACTION_KEYS);
  if (!action) {
    action = toText(result.screening?.crisis_message);
  }

  if (!diagnosis && !redFlagText && !action) return null;
  return {
    source: kindLabel,
    diagnosis: diagnosis || "No diagnosis field returned.",
    redFlags: redFlagText || "No critical red flags returned.",
    action: action || "No recommended action returned.",
  };
}

export function QuickSummaryCard({ cbcResult, mhResult }) {
  const cbcSummary = extractSummaryFromResult(cbcResult, "CBC");
  const mhSummary = extractSummaryFromResult(mhResult, "Mental Health");
  const summaries = [mhSummary, cbcSummary].filter(Boolean);
  if (summaries.length === 0) return null;

  return (
    <Card className="border-slate-900 bg-slate-950 text-slate-50 shadow-[0_18px_42px_rgba(2,6,23,0.48)]">
      <CardHeader className="pb-3">
        <CardTitle className="text-base uppercase tracking-[0.08em] text-slate-100">Quick Summary</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {summaries.map((summary) => (
          <div key={summary.source} className="rounded-xl border border-slate-700 bg-slate-900/60 p-4">
            <p className="mb-3 text-xs font-semibold uppercase tracking-[0.1em] text-emerald-300">{summary.source}</p>
            <div className="grid gap-3 md:grid-cols-3">
              <div>
                <p className="text-[11px] font-semibold uppercase tracking-[0.08em] text-slate-300">Diagnosis</p>
                <p className="mt-1 text-sm leading-relaxed text-white">{summary.diagnosis}</p>
              </div>
              <div>
                <p className="text-[11px] font-semibold uppercase tracking-[0.08em] text-slate-300">Critical Red Flags</p>
                <p className="mt-1 text-sm leading-relaxed text-rose-200">{summary.redFlags}</p>
              </div>
              <div>
                <p className="text-[11px] font-semibold uppercase tracking-[0.08em] text-slate-300">Recommended Action</p>
                <p className="mt-1 text-sm leading-relaxed text-emerald-100">{summary.action}</p>
              </div>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
