import { useMemo, useState } from "react";
import { BrainCircuit } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "../../components/ui/alert";
import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card";
import { Input } from "../../components/ui/input";
import { Label } from "../../components/ui/label";
import { Switch } from "../../components/ui/switch";
import { Textarea } from "../../components/ui/textarea";
import { cn } from "../../lib/utils";
import {
  CrisisAlert,
  FlagListCard,
  HighRiskEscalationNotice,
  RecommendationsCard,
  RiskSummaryCard,
  TechnicalDetails,
} from "../shared/result-panels";
import { ClinicalPilotBanner } from "../shared/clinical-pilot-banner";
import {
  FREQUENCY_OPTIONS,
  GAD7_ITEMS,
  PHQ9_ITEMS,
  gad7SeverityLabel,
  phq9SeverityLabel,
  sumAnswers,
} from "./questionnaires";

function helperTextByMode(mode) {
  if (mode === "doctor") {
    return "Psychologist-focused guided intake for PHQ-9/GAD-7 with optional S18 narrative review.";
  }
  return "Guided emotional wellness screening with optional advanced narrative analysis.";
}

const WORKFLOW_STEPS = [
  {
    id: "intake",
    title: "Intake context",
    description: "Capture presenting details and workflow options before scoring.",
  },
  {
    id: "phq9",
    title: "PHQ-9 depression screener",
    description: "Answer all nine PHQ-9 questions for the last two weeks.",
  },
  {
    id: "gad7",
    title: "GAD-7 anxiety screener",
    description: "Answer all seven GAD-7 questions for the last two weeks.",
  },
  {
    id: "safety",
    title: "Safety and escalation check",
    description: "Review self-harm indicators and document immediate safety signals.",
  },
  {
    id: "review",
    title: "Clinical review and submit",
    description: "Validate totals and run the screening engine.",
  },
];

const FUNCTIONAL_IMPACT_OPTIONS = [
  "Not difficult at all",
  "Somewhat difficult",
  "Very difficult",
  "Extremely difficult",
];

function emptyAnswers(count) {
  return Array.from({ length: count }, () => null);
}

function isComplete(answerList) {
  return answerList.every((value) => typeof value === "number");
}

function buildConcernText({ patientLabel, presentingConcern, concernText, functionalImpact, safetyPlanNote }) {
  const sections = [];
  if (patientLabel.trim()) sections.push(`Patient label: ${patientLabel.trim()}`);
  if (presentingConcern.trim()) sections.push(`Presenting concern: ${presentingConcern.trim()}`);
  if (functionalImpact.trim()) sections.push(`Functional impact: ${functionalImpact.trim()}`);
  if (concernText.trim()) sections.push(`Clinical notes: ${concernText.trim()}`);
  if (safetyPlanNote.trim()) sections.push(`Safety notes: ${safetyPlanNote.trim()}`);
  return sections.join("\n");
}

function buildMentalHealthPayload({
  includeS18,
  mhFast,
  phqAnswers,
  gadAnswers,
  suicidalIdeation,
  selfHarmIntent,
  concernText,
}) {
  if (!isComplete(phqAnswers)) {
    throw new Error("Complete all PHQ-9 questions before submitting.");
  }
  if (!isComplete(gadAnswers)) {
    throw new Error("Complete all GAD-7 questions before submitting.");
  }
  const derivedFromPhqItem9 = Number(phqAnswers[8]) > 0;
  const payload = {
    include_s18: includeS18,
    fast: mhFast,
    phq9_items: phqAnswers.map(Number),
    gad7_total: sumAnswers(gadAnswers.map(Number)),
    suicidal_ideation: Boolean(suicidalIdeation || derivedFromPhqItem9),
    self_harm_intent: Boolean(selfHarmIntent),
  };
  const trimmed = concernText.trim();
  if (trimmed) {
    if (trimmed.length > 4000) {
      throw new Error("Clinical notes are too long. Keep combined context under 4000 characters.");
    }
    payload.concern_text = trimmed;
  }
  return payload;
}

function QuestionnaireStep({ title, items, answers, onSelect }) {
  return (
    <section className="space-y-4">
      <h3 className="text-sm font-semibold uppercase tracking-wide text-[var(--muted-foreground)]">{title}</h3>
      {items.map((item, index) => (
        <div key={item.id} className="rounded-xl border p-4">
          <p className="text-sm font-medium leading-relaxed">
            {index + 1}. {item.prompt}
          </p>
          <div className="mt-3 grid gap-2 sm:grid-cols-2 xl:grid-cols-4">
            {FREQUENCY_OPTIONS.map((option) => {
              const selected = answers[index] === option.value;
              return (
                <button
                  key={`${item.id}-${option.value}`}
                  type="button"
                  onClick={() => onSelect(index, option.value)}
                  className={cn(
                    "rounded-lg border px-3 py-2 text-left text-sm transition-colors",
                    selected
                      ? "border-indigo-500 bg-indigo-50 text-indigo-950"
                      : "border-[var(--border)] bg-white hover:bg-[var(--accent)]"
                  )}
                >
                  <span className="block text-xs font-semibold uppercase tracking-wide text-[var(--muted-foreground)]">
                    {option.value}
                  </span>
                  <span>{option.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      ))}
    </section>
  );
}

export function MentalHealthWorkflow({ mode, pollTimeoutSeconds, state, onAnalyze }) {
  const [activeStep, setActiveStep] = useState(0);
  const [patientLabel, setPatientLabel] = useState("");
  const [presentingConcern, setPresentingConcern] = useState("");
  const [functionalImpact, setFunctionalImpact] = useState("");
  const [phqAnswers, setPhqAnswers] = useState(() => emptyAnswers(PHQ9_ITEMS.length));
  const [gadAnswers, setGadAnswers] = useState(() => emptyAnswers(GAD7_ITEMS.length));
  const [suicidalIdeation, setSuicidalIdeation] = useState(false);
  const [selfHarmIntent, setSelfHarmIntent] = useState(false);
  const [concernText, setConcernText] = useState("");
  const [safetyPlanNote, setSafetyPlanNote] = useState("");
  const [includeS18, setIncludeS18] = useState(true);
  const [mhFast, setMhFast] = useState(true);
  const [formError, setFormError] = useState("");

  const phqReady = isComplete(phqAnswers);
  const gadReady = isComplete(gadAnswers);
  const phqTotal = phqReady ? sumAnswers(phqAnswers.map(Number)) : null;
  const gadTotal = gadReady ? sumAnswers(gadAnswers.map(Number)) : null;
  const item9Score = typeof phqAnswers[8] === "number" ? phqAnswers[8] : null;
  const suicidalFromPhqItem9 = Number(item9Score || 0) > 0;
  const crisisLikely = Boolean(suicidalIdeation || suicidalFromPhqItem9 || selfHarmIntent);

  const timeoutHint = useMemo(() => {
    const backendWindowMs = Math.max(300000, pollTimeoutSeconds * 1000);
    if (!includeS18) return 120000;
    return Math.max(600000, backendWindowMs + 300000);
  }, [includeS18, pollTimeoutSeconds]);

  function validateStep(stepIndex) {
    if (stepIndex === 1 && !phqReady) {
      return "Answer every PHQ-9 item before moving forward.";
    }
    if (stepIndex === 2 && !gadReady) {
      return "Answer every GAD-7 item before moving forward.";
    }
    return "";
  }

  function goToNextStep() {
    const problem = validateStep(activeStep);
    if (problem) {
      setFormError(problem);
      return;
    }
    setFormError("");
    setActiveStep((prev) => Math.min(prev + 1, WORKFLOW_STEPS.length - 1));
  }

  function onSubmit() {
    setFormError("");
    try {
      const combinedConcernText = buildConcernText({
        patientLabel,
        presentingConcern,
        concernText,
        functionalImpact,
        safetyPlanNote,
      });
      const payload = buildMentalHealthPayload({
        includeS18,
        mhFast,
        phqAnswers,
        gadAnswers,
        suicidalIdeation,
        selfHarmIntent,
        concernText: combinedConcernText,
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
        <ClinicalPilotBanner pillar="mental-health" />

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

        <div className="space-y-4">
          <div className="flex flex-wrap gap-2">
            {WORKFLOW_STEPS.map((step, index) => {
              const isActive = index === activeStep;
              const isLocked = index > activeStep + 1;
              const isCompleteStep =
                (step.id === "phq9" && phqReady) ||
                (step.id === "gad7" && gadReady) ||
                (step.id === "review" && phqReady && gadReady);
              return (
                <button
                  key={step.id}
                  type="button"
                  disabled={isLocked}
                  onClick={() => {
                    if (index > activeStep) {
                      const problem = validateStep(activeStep);
                      if (problem) {
                        setFormError(problem);
                        return;
                      }
                    }
                    setFormError("");
                    setActiveStep(index);
                  }}
                  className={cn(
                    "rounded-full border px-3 py-1.5 text-xs font-semibold transition-colors",
                    isActive
                      ? "border-indigo-600 bg-indigo-600 text-white"
                      : "border-[var(--border)] bg-white text-[var(--foreground)] hover:bg-[var(--accent)]",
                    isLocked ? "cursor-not-allowed opacity-60 hover:bg-white" : null
                  )}
                >
                  {step.title}
                  {isCompleteStep ? <span className="ml-1">- done</span> : null}
                </button>
              );
            })}
          </div>
          <div className="rounded-xl border bg-slate-50/80 p-4">
            <p className="text-xs font-semibold uppercase tracking-[0.12em] text-[var(--muted-foreground)]">
              Step {activeStep + 1} of {WORKFLOW_STEPS.length}
            </p>
            <p className="mt-1 text-sm font-semibold">{WORKFLOW_STEPS[activeStep].title}</p>
            <p className="text-sm text-[var(--muted-foreground)]">{WORKFLOW_STEPS[activeStep].description}</p>
          </div>
        </div>

        {activeStep === 0 ? (
          <section className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="mh-patient-label">Patient label (optional)</Label>
              <Input
                id="mh-patient-label"
                value={patientLabel}
                onChange={(event) => setPatientLabel(event.target.value)}
                placeholder="Example: OPD-MH-042"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="mh-functional-impact">Functional impact</Label>
              <select
                id="mh-functional-impact"
                value={functionalImpact}
                onChange={(event) => setFunctionalImpact(event.target.value)}
                className="h-10 w-full rounded-lg border border-[var(--border)] bg-[var(--input)] px-3 text-sm"
              >
                <option value="">Select impact level</option>
                {FUNCTIONAL_IMPACT_OPTIONS.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </div>
            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="mh-presenting-concern">Presenting concern</Label>
              <Textarea
                id="mh-presenting-concern"
                value={presentingConcern}
                onChange={(event) => setPresentingConcern(event.target.value)}
                placeholder="Chief complaint, duration, and observed symptoms"
              />
            </div>
            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="mh-note">Clinical notes (optional)</Label>
              <Textarea
                id="mh-note"
                value={concernText}
                onChange={(event) => setConcernText(event.target.value)}
                placeholder="Context, psychosocial factors, and therapy notes"
              />
            </div>
            <div className="flex items-center gap-3 rounded-xl border bg-slate-50/80 p-4">
              <Switch checked={includeS18} onCheckedChange={setIncludeS18} id="mh-include-s18" />
              <div className="space-y-1">
                <Label htmlFor="mh-include-s18">Include S18 narrative pass</Label>
                <p className="text-xs text-[var(--muted-foreground)]">Enable additional context-sensitive analysis.</p>
              </div>
            </div>
            <div className="flex items-center gap-3 rounded-xl border bg-slate-50/80 p-4">
              <Switch checked={mhFast} onCheckedChange={setMhFast} id="mh-fast" disabled={!includeS18} />
              <div className="space-y-1">
                <Label htmlFor="mh-fast">Use fast S18 mode</Label>
                <p className="text-xs text-[var(--muted-foreground)]">
                  Fast mode returns earlier when narrative depth can be lighter.
                </p>
              </div>
            </div>
          </section>
        ) : null}

        {activeStep === 1 ? (
          <QuestionnaireStep
            title="PHQ-9 (past 2 weeks)"
            items={PHQ9_ITEMS}
            answers={phqAnswers}
            onSelect={(index, value) =>
              setPhqAnswers((prev) => {
                const next = [...prev];
                next[index] = value;
                return next;
              })
            }
          />
        ) : null}

        {activeStep === 2 ? (
          <QuestionnaireStep
            title="GAD-7 (past 2 weeks)"
            items={GAD7_ITEMS}
            answers={gadAnswers}
            onSelect={(index, value) =>
              setGadAnswers((prev) => {
                const next = [...prev];
                next[index] = value;
                return next;
              })
            }
          />
        ) : null}

        {activeStep === 3 ? (
          <section className="space-y-4">
            {suicidalFromPhqItem9 ? (
              <Alert variant="warning">
                <AlertTitle>PHQ-9 item 9 indicates elevated concern</AlertTitle>
                <AlertDescription>
                  Item 9 score is {item9Score}. Suicidal ideation will be flagged automatically for risk triage.
                </AlertDescription>
              </Alert>
            ) : null}
            <div className="grid gap-4 md:grid-cols-2">
              <div className="flex items-center gap-3 rounded-xl border bg-slate-50/80 p-4">
                <Switch checked={suicidalIdeation} onCheckedChange={setSuicidalIdeation} id="mh-suicidal" />
                <div className="space-y-1">
                  <Label htmlFor="mh-suicidal">Suicidal ideation reported clinically</Label>
                  <p className="text-xs text-[var(--muted-foreground)]">
                    Use this when ideation is disclosed beyond PHQ-9 responses.
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3 rounded-xl border bg-slate-50/80 p-4">
                <Switch checked={selfHarmIntent} onCheckedChange={setSelfHarmIntent} id="mh-self-harm" />
                <div className="space-y-1">
                  <Label htmlFor="mh-self-harm">Self-harm intent reported</Label>
                  <p className="text-xs text-[var(--muted-foreground)]">
                    Triggers immediate crisis pathway recommendations.
                  </p>
                </div>
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="mh-safety-notes">Safety plan and escalation notes (optional)</Label>
              <Textarea
                id="mh-safety-notes"
                value={safetyPlanNote}
                onChange={(event) => setSafetyPlanNote(event.target.value)}
                placeholder="Document immediate supports, contacts, and referral pathway."
              />
            </div>
          </section>
        ) : null}

        {activeStep === 4 ? (
          <section className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              <Card className="border-slate-200/90">
                <CardHeader className="pb-2">
                  <CardTitle className="text-base">PHQ-9 summary</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2 text-sm">
                  <p>Total score: {phqTotal ?? "Incomplete"}</p>
                  <p>Severity: {phqTotal === null ? "Incomplete" : phq9SeverityLabel(phqTotal)}</p>
                  <p>Item 9 score: {item9Score ?? "Incomplete"}</p>
                </CardContent>
              </Card>
              <Card className="border-slate-200/90">
                <CardHeader className="pb-2">
                  <CardTitle className="text-base">GAD-7 summary</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2 text-sm">
                  <p>Total score: {gadTotal ?? "Incomplete"}</p>
                  <p>Severity: {gadTotal === null ? "Incomplete" : gad7SeverityLabel(gadTotal)}</p>
                  <p>Functional impact: {functionalImpact || "Not documented"}</p>
                </CardContent>
              </Card>
            </div>

            <div className="rounded-xl border bg-slate-50/80 p-4">
              <p className="text-sm font-semibold">Safety triage snapshot</p>
              <div className="mt-2 flex flex-wrap items-center gap-2">
                <Badge variant={crisisLikely ? "risk_high" : "risk_low"}>
                  {crisisLikely ? "Escalate safety pathway" : "No acute safety trigger flagged"}
                </Badge>
                {suicidalFromPhqItem9 ? <Badge variant="risk_moderate">PHQ-9 item 9 positive</Badge> : null}
                {selfHarmIntent ? <Badge variant="risk_high">Self-harm intent reported</Badge> : null}
              </div>
            </div>
          </section>
        ) : null}

        <div className="flex flex-wrap gap-2">
          <Button variant="outline" onClick={() => setActiveStep((prev) => Math.max(prev - 1, 0))} disabled={activeStep === 0}>
            Previous
          </Button>
          {activeStep < WORKFLOW_STEPS.length - 1 ? (
            <Button onClick={goToNextStep}>Continue</Button>
          ) : (
            <Button onClick={onSubmit} disabled={state.loading || mode !== "doctor"}>
              {state.loading ? "Running mental health screening..." : "Run mental health screening"}
            </Button>
          )}
        </div>
        {mode !== "doctor" ? (
          <p className="text-xs text-[var(--muted-foreground)]">
            Psychologist/doctor role is required to run screening. You can still review the questionnaire flow.
          </p>
        ) : null}
        {state.loading ? (
          <p className="text-xs text-[var(--muted-foreground)]">
            {includeS18
              ? `S18-enabled run may take up to ${Math.ceil(timeoutHint / 60000)} minutes.`
              : "Local-only run should complete quickly."}
          </p>
        ) : null}

        {state.result ? (
          <div className="grid gap-4 lg:grid-cols-2">
            <div className="lg:col-span-2 space-y-3">
              <HighRiskEscalationNotice summary={state.result.screening} />
              <CrisisAlert screening={state.result.screening} />
            </div>
            <RiskSummaryCard title="Screening Summary (Local)" summary={state.result.screening} />
            <RiskSummaryCard title="Narrative Summary (S18)" summary={state.result.wise} />
            <FlagListCard title="Risk Flags (Local)" flags={state.result.screening?.display_labels} />
            <FlagListCard title="Risk Flags (S18)" flags={state.result.wise?.flags} />
            <RecommendationsCard recommendations={state.result.recommendations} label="Recommended clinical next steps" />
            <TechnicalDetails data={state.result} />
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
}

