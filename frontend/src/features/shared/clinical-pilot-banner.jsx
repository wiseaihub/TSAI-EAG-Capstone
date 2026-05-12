import { Alert, AlertDescription, AlertTitle } from "../../components/ui/alert";

const PILLAR_COPY = {
  cbc: {
    title: "CBC — clinical decision support",
    bullets: [
      "Interpretation here is advisory and uses illustrative thresholds for triage support only—not a laboratory diagnosis.",
      "Correlation with symptoms, examination, and standard lab QC remains with the licensed clinician.",
      "Marked anemia, cytosis, or platelet patterns warrant urgent in-person evaluation when clinically appropriate.",
    ],
  },
  "mental-health": {
    title: "Mental health — clinical decision support",
    bullets: [
      "Screening scores support clinician judgement only and do not replace a psychiatric assessment or safety evaluation.",
      "Activate emergency or crisis pathways whenever imminent risk is suspected—this portal is not for emergencies.",
      "Escalation, consent, and documentation follow your institution's psychology/psychiatry protocols.",
    ],
  },
};

/**
 * Shared pilot-grade framing so CBC and MH pillars expose identical transparency posture.
 */
export function ClinicalPilotBanner({ pillar }) {
  const block = PILLAR_COPY[pillar];
  if (!block) return null;
  return (
    <Alert variant="warning">
      <AlertTitle>{block.title}</AlertTitle>
      <AlertDescription>
        <ul className="mt-2 list-disc space-y-1 pl-5 text-sm leading-relaxed">
          {block.bullets.map((line) => (
            <li key={line}>{line}</li>
          ))}
        </ul>
      </AlertDescription>
    </Alert>
  );
}
