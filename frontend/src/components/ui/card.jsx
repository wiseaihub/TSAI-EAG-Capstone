import { cn } from "../../lib/utils";

function Card({ className, ...props }) {
  return (
    <div
      className={cn(
        "rounded-2xl border bg-[var(--card)] text-[var(--card-foreground)] shadow-[0_10px_28px_rgba(15,23,42,0.06)]",
        className
      )}
      {...props}
    />
  );
}

function CardHeader({ className, ...props }) {
  return <div className={cn("flex flex-col space-y-2 p-6 md:p-7", className)} {...props} />;
}

function CardTitle({ className, ...props }) {
  return (
    <h3
      className={cn("text-lg font-semibold leading-tight tracking-tight text-slate-900", className)}
      {...props}
    />
  );
}

function CardDescription({ className, ...props }) {
  return <p className={cn("text-sm leading-relaxed text-[var(--muted-foreground)]", className)} {...props} />;
}

function CardContent({ className, ...props }) {
  return <div className={cn("p-6 pt-0 md:px-7 md:pb-7", className)} {...props} />;
}

export { Card, CardHeader, CardTitle, CardDescription, CardContent };
