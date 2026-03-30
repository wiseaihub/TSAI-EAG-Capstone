import { useMemo, useState } from "react";
import { FlaskConical } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "../../components/ui/alert";
import { Button } from "../../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card";
import { Input } from "../../components/ui/input";
import { Label } from "../../components/ui/label";
import { Switch } from "../../components/ui/switch";
import { FlagListCard, RecommendationsCard, RiskSummaryCard, TechnicalDetails } from "../shared/result-panels";

function helperTextByMode(mode) {
  if (mode === "doctor") {
    return "Use this panel for CBC triage support. Values are advisory and not a diagnosis.";
  }
  return "Enter your latest CBC values to generate a structured summary. This is educational support only.";
}

export function CbcWorkflow({ mode, pollTimeoutSeconds, state, onAnalyze }) {
  const [sex, setSex] = useState("");
  const [hemoglobin, setHemoglobin] = useState("13.5");
  const [wbc, setWbc] = useState("7000");
  const [rbc, setRbc] = useState("4.5");
  const [platelets, setPlatelets] = useState("250000");
  const [fastMode, setFastMode] = useState(true);

  const timeoutHint = useMemo(() => {
    const backendWindowMs = Math.max(300000, pollTimeoutSeconds * 1000);
    if (fastMode) {
      return Math.max(240000, backendWindowMs + 60000);
    }
    return Math.max(900000, backendWindowMs + 300000);
  }, [fastMode, pollTimeoutSeconds]);

  function onSubmit() {
    const payload = {
      ...(sex ? { sex } : {}),
      hemoglobin: parseFloat(hemoglobin) || 0,
      wbc: parseFloat(wbc) || 0,
      rbc: parseFloat(rbc) || 0,
      platelets: parseFloat(platelets) || 0,
    };
    onAnalyze({ payload, fastMode, timeoutMs: timeoutHint });
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-xl">
          <FlaskConical className="h-5 w-5 text-indigo-600" />
          CBC Workflow
        </CardTitle>
        <CardDescription className="max-w-2xl">{helperTextByMode(mode)}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-5">
        {state.error ? (
          <Alert variant="destructive">
            <AlertTitle>CBC request failed</AlertTitle>
            <AlertDescription>
              {state.error}
              {state.hint ? <p className="mt-2 text-xs">{state.hint}</p> : null}
            </AlertDescription>
          </Alert>
        ) : null}

        <div className="grid gap-4 md:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="cbc-sex">Sex for interpretation</Label>
            <select
              id="cbc-sex"
              value={sex}
              onChange={(e) => setSex(e.target.value)}
              className="h-10 w-full rounded-lg border border-[var(--border)] bg-[var(--input)] px-3 text-sm shadow-[inset_0_1px_0_rgba(255,255,255,0.8)]"
            >
              <option value="">Unknown / not provided</option>
              <option value="female">Female</option>
              <option value="male">Male</option>
            </select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="cbc-hemoglobin">Hemoglobin (g/dL)</Label>
            <Input
              id="cbc-hemoglobin"
              type="number"
              step="0.1"
              value={hemoglobin}
              onChange={(e) => setHemoglobin(e.target.value)}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="cbc-wbc">WBC (per uL)</Label>
            <Input id="cbc-wbc" type="number" step="100" value={wbc} onChange={(e) => setWbc(e.target.value)} />
          </div>
          <div className="space-y-2">
            <Label htmlFor="cbc-rbc">RBC (million/uL)</Label>
            <Input id="cbc-rbc" type="number" step="0.1" value={rbc} onChange={(e) => setRbc(e.target.value)} />
          </div>
          <div className="space-y-2">
            <Label htmlFor="cbc-platelets">Platelets (per uL)</Label>
            <Input
              id="cbc-platelets"
              type="number"
              step="1000"
              value={platelets}
              onChange={(e) => setPlatelets(e.target.value)}
            />
          </div>
        </div>

        <div className="flex items-start gap-3 rounded-xl border bg-slate-50/80 p-4">
          <Switch id="cbc-fast-mode" checked={fastMode} onCheckedChange={setFastMode} />
          <div className="space-y-1">
            <Label htmlFor="cbc-fast-mode">Fast mode for WISE pass</Label>
            <p className="text-xs text-[var(--muted-foreground)]">
              Fast mode usually returns sooner. Full mode may run for several minutes.
            </p>
          </div>
        </div>

        <Button onClick={onSubmit} disabled={state.loading} className="w-full sm:w-auto">
          {state.loading ? "Running CBC analysis..." : "Run CBC analysis"}
        </Button>
        {state.loading ? (
          <p className="text-xs text-[var(--muted-foreground)]">
            Current wait window: up to {Math.ceil(timeoutHint / 60000)} minutes while backend polling completes.
          </p>
        ) : null}

        {state.result ? (
          <div className="grid gap-4 lg:grid-cols-2">
            <RiskSummaryCard title="CBC Local Engine" summary={state.result.cbc} />
            <RiskSummaryCard title="WISE Narrative Engine" summary={state.result.wise} />
            <FlagListCard title="CBC flags" flags={state.result.cbc?.flags} />
            <FlagListCard title="WISE flags" flags={state.result.wise?.flags} />
            <RecommendationsCard recommendations={state.result.recommendations} />
            <TechnicalDetails data={state.result} />
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
}
