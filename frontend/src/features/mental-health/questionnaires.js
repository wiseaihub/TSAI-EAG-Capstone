export const FREQUENCY_OPTIONS = [
  { value: 0, label: "Not at all" },
  { value: 1, label: "Several days" },
  { value: 2, label: "More than half the days" },
  { value: 3, label: "Nearly every day" },
];

export const PHQ9_ITEMS = [
  { id: "phq1", prompt: "Little interest or pleasure in doing things" },
  { id: "phq2", prompt: "Feeling down, depressed, or hopeless" },
  { id: "phq3", prompt: "Trouble falling or staying asleep, or sleeping too much" },
  { id: "phq4", prompt: "Feeling tired or having little energy" },
  { id: "phq5", prompt: "Poor appetite or overeating" },
  {
    id: "phq6",
    prompt: "Feeling bad about yourself, or that you are a failure, or have let yourself or your family down",
  },
  {
    id: "phq7",
    prompt: "Trouble concentrating on things, such as reading the newspaper or watching television",
  },
  {
    id: "phq8",
    prompt: "Moving or speaking so slowly that other people could have noticed, or being so fidgety or restless that you have been moving around a lot more than usual",
  },
  { id: "phq9", prompt: "Thoughts that you would be better off dead, or of hurting yourself in some way" },
];

export const GAD7_ITEMS = [
  { id: "gad1", prompt: "Feeling nervous, anxious, or on edge" },
  { id: "gad2", prompt: "Not being able to stop or control worrying" },
  { id: "gad3", prompt: "Worrying too much about different things" },
  { id: "gad4", prompt: "Trouble relaxing" },
  { id: "gad5", prompt: "Being so restless that it is hard to sit still" },
  { id: "gad6", prompt: "Becoming easily annoyed or irritable" },
  { id: "gad7", prompt: "Feeling afraid as if something awful might happen" },
];

export function sumAnswers(answers) {
  return answers.reduce((total, value) => total + value, 0);
}

export function phq9SeverityLabel(total) {
  if (total < 5) return "Minimal";
  if (total < 10) return "Mild";
  if (total < 15) return "Moderate";
  if (total < 20) return "Moderately severe";
  return "Severe";
}

export function gad7SeverityLabel(total) {
  if (total < 5) return "Minimal";
  if (total < 10) return "Mild";
  if (total < 15) return "Moderate";
  return "Severe";
}
