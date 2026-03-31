import { useMemo, useState } from "react";
import { BrainCircuit } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "../../components/ui/alert";
import { Button } from "../../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card";
import { Input } from "../../components/ui/input";
import { Label } from "../../components/ui/label";
import { Switch } from "../../components/ui/switch";
import { Textarea } from "../../components/ui/textarea";
import {
  CrisisAlert,
  FlagListCard,
  RecommendationsCard,
  RiskSummaryCard,
  TechnicalDetails,
} from "../shared/result-panels";

function helperTextByMode(mode) {
  if (mode === "doctor") {
    return "Clinical screening support for PHQ-9/GAD-7 with optional S18 narrative review.";
  }
  return "Guided emotional wellness screening with optional advanced narrative analysis.";
}

function buildMentalHealthPayload({
  includeS18,
  mhFast,
  suicidalIdeation,
  selfHarmIntent,
  concernText,
  usePhq9Items,
  phq9Items,
  phq9Total,
  gad7Total,
}) {
  const payload = {
    include_s18: includeS18,
    fast: mhFast,
    suicidal_ideation: suicidalIdeation,
    self_harm_intent: selfHarmIntent,
  };

  const trimmed = concernText.trim();
  if (trimmed) payload.concern_text = trimmed;

  if (usePhq9Items) {
    const items = phq9Items.map((x) => {
      const n = parseInt(String(x).trim(), 10);
      if (Number.isNaN(n) || n < 0 || n > 3) {
        throw new Error("Each PHQ-9 item score must be between 0 and 3.");
      }
      return n;
    });
    if (items.length !== 9) throw new Error("PHQ-9 requires exactly 9 item scores.");
    payload.phq9_items = items;
  } else {
    const phq = parseInt(phq9Total, 10);
    if (phq9Total !== "" && !Number.isNaN(phq)) {
      if (phq < 0 || phq > 27) throw new Error("PHQ-9 total must be 0 to 27.");
      payload.phq9_total = phq;
    }
  }

  const gad = parseInt(gad7Total, 10);
  if (gad7Total !== "" && !Number.isNaN(gad)) {
    if (gad < 0 || gad > 21) throw new Error("GAD-7 total must be 0 to 21.");
    payload.gad7_total = gad;
  }

  const hasPhq = usePhq9Items || (phq9Total !== "" && !Number.isNaN(parseInt(phq9Total, 10)));
  const hasGad = gad7Total !== "" && !Number.isNaN(parseInt(gad7Total, 10));
  if (!hasPhq && !hasGad) {
    throw new Error("Provide PHQ-9 (total or 9 items) and/or GAD-7 total.");
  }
  return payload;
}

export function MentalHealthWorkflow({ mode, pollTimeoutSeconds, state, onAnalyze }) {
  const [usePhq9Items, setUsePhq9Items] = useState(false);
  const [phq9Total, setPhq9Total] = useState("12");
  const [phq9Items, setPhq9Items] = useState(() => Array(9).fill("0"));
  const [gad7Total, setGad7Total] = useState("8");
  const [suicidalIdeation, setSuicidalIdeation] = useState(false);
  const [selfHarmIntent, setSelfHarmIntent] = useState(false);
  const [concernText, setConcernText] = useState("");
  const [includeS18, setIncludeS18] = useState(true);
  const [mhFast, setMhFast] = useState(true);
  const [formError, setFormError] = useState("");

  const timeoutHint = useMemo(() => {
    const backendWindowMs = Math.max(300000, pollTimeoutSeconds * 1000);
    if (!includeS18) return 120000;
    return Math.max(600000, backendWindowMs + 300000);
  }, [includeS18, pollTimeoutSeconds]);

  function onSubmit() {
    setFormError("");
    try {
      const payload = buildMentalHealthPayload({
        includeS18,
        mhFast,
        suicidalIdeation,
        selfHarmIntent,
        concernText,
        usePhq9Items,
        phq9Items,
        phq9Total,
        gad7Total,
      });
      onAnalyze({ payload, timeoutMs: timeoutHint });
    } catch (error) {
      setFormError(error?.message || String(error));
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-xl">
          <BrainCircuit className="h-5 w-5 text-violet-600" />
          Mental Health Workflow
        </CardTitle>
        <CardDescription className="max-w-2xl">{helperTextByMode(mode)}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-5">
        {formError ? (
          <Alert variant="warning">
            <AlertTitle>Input needs attention</AlertTitle>
            <AlertDescription>{formError}</AlertDescription>
          </Alert>
        ) : null}

        {state.error ? (
          <Alert variant="destructive">
            <AlertTitle>Mental health request failed</AlertTitle>
            <AlertDescription>
              {state.error}
              {state.hint ? <p className="mt-2 text-xs">{state.hint}</p> : null}
            </AlertDescription>
          </Alert>
        ) : null}

        <Alert variant="warning">
          <AlertTitle>Safety notice</AlertTitle>
          <AlertDescription>
            Screening output is supportive only and does not replace licensed clinical care.
          </AlertDescription>
        </Alert>

        <div className="grid gap-4 md:grid-cols-2">
          <div className="space-y-2 md:col-span-2">
            <div className="flex items-center gap-3 rounded-xl border bg-slate-50/80 p-4">
              <Switch checked={usePhq9Items} onCheckedChange={setUsePhq9Items} id="mh-phq-items" />
              <Label htmlFor="mh-phq-items">Use 9 PHQ-9 item scores (0-3 each) instead of total</Label>
            </div>
          </div>
          {usePhq9Items ? (
            <div className="grid gap-2 md:col-span-2 md:grid-cols-3">
              {phq9Items.map((value, index) => (
                <div className="space-y-1" key={`phq-item-${index}`}>
                  <Label htmlFor={`phq-item-${index}`}>PHQ-9 item {index + 1}</Label>
                  <Input
                    id={`phq-item-${index}`}
                    type="number"
                    min={0}
                    max={3}
                    value={value}
                    onChange={(e) => {
                      const next = [...phq9Items];
                      next[index] = e.target.value;
                      setPhq9Items(next);
                    }}
                  />
                </div>
              ))}
            </div>
          ) : (
            <div className="space-y-2">
              <Label htmlFor="mh-phq-total">PHQ-9 total (0-27)</Label>
              <Input
                id="mh-phq-total"
                type="number"
                min={0}
                max={27}
                value={phq9Total}
                onChange={(e) => setPhq9Total(e.target.value)}
              />
            </div>
          )}
          <div className="space-y-2">
            <Label htmlFor="mh-gad-total">GAD-7 total (0-21)</Label>
            <Input
              id="mh-gad-total"
              type="number"
              min={0}
              max={21}
              value={gad7Total}
              onChange={(e) => setGad7Total(e.target.value)}
            />
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          <div className="flex items-center gap-3 rounded-xl border bg-slate-50/80 p-4">
            <Switch checked={suicidalIdeation} onCheckedChange={setSuicidalIdeation} id="mh-suicidal" />
            <Label htmlFor="mh-suicidal">Suicidal ideation reported</Label>
          </div>
          <div className="flex items-center gap-3 rounded-xl border bg-slate-50/80 p-4">
            <Switch checked={selfHarmIntent} onCheckedChange={setSelfHarmIntent} id="mh-self-harm" />
            <Label htmlFor="mh-self-harm">Self-harm intent reported</Label>
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="mh-note">Optional note (context only)</Label>
          <Textarea
            id="mh-note"
            value={concernText}
            onChange={(e) => setConcernText(e.target.value)}
            placeholder="Enter optional context"
          />
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          <div className="flex items-center gap-3 rounded-xl border bg-slate-50/80 p-4">
            <Switch checked={includeS18} onCheckedChange={setIncludeS18} id="mh-include-s18" />
            <Label htmlFor="mh-include-s18">Include S18 narrative pass</Label>
          </div>
          <div className="flex items-center gap-3 rounded-xl border bg-slate-50/80 p-4">
            <Switch checked={mhFast} onCheckedChange={setMhFast} id="mh-fast" disabled={!includeS18} />
            <Label htmlFor="mh-fast">Use fast S18 mode</Label>
          </div>
        </div>

        <Button onClick={onSubmit} disabled={state.loading} className="w-full sm:w-auto">
          {state.loading ? "Running mental health screening..." : "Run mental health screening"}
        </Button>
        {state.loading ? (
          <p className="text-xs text-[var(--muted-foreground)]">
            {includeS18
              ? `S18-enabled run may take up to ${Math.ceil(timeoutHint / 60000)} minutes.`
              : "Local-only run should complete quickly."}
          </p>
        ) : null}

        {state.result ? (
          <div className="grid gap-4 lg:grid-cols-2">
            <RiskSummaryCard title="Local screening" summary={state.result.screening} />
            <RiskSummaryCard title="S18 narrative screening" summary={state.result.wise} />
            <FlagListCard title="Local screening labels" flags={state.result.screening?.display_labels} />
            <FlagListCard title="S18 flags" flags={state.result.wise?.flags} />
            <RecommendationsCard recommendations={state.result.recommendations} />
            <CrisisAlert screening={state.result.screening} />
            <TechnicalDetails data={state.result} />
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
}

