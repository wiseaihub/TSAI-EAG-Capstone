import { cva } from "class-variance-authority";
import { cn } from "../../lib/utils";

const badgeVariants = cva(
  "inline-flex items-center rounded-full px-2.5 py-1 text-[11px] font-semibold tracking-wide uppercase transition-colors",
  {
    variants: {
      variant: {
        default: "bg-[var(--primary)] text-[var(--primary-foreground)]",
        secondary: "bg-[var(--secondary)] text-[var(--secondary-foreground)]",
        outline: "border border-[var(--border)] text-[var(--foreground)]",
        risk_high: "risk-high",
        risk_moderate: "risk-moderate",
        risk_low: "risk-low",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

function Badge({ className, variant, ...props }) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />;
}

export { Badge };
