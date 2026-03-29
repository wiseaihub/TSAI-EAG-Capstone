import * as TabsPrimitive from "@radix-ui/react-tabs";
import { cn } from "../../lib/utils";

function Tabs({ className, ...props }) {
  return <TabsPrimitive.Root className={cn("w-full", className)} {...props} />;
}

function TabsList({ className, ...props }) {
  return (
    <TabsPrimitive.List
      className={cn(
        "inline-flex h-11 items-center justify-center rounded-xl border border-[var(--border)] bg-[var(--secondary)] p-1 text-[var(--secondary-foreground)]",
        className
      )}
      {...props}
    />
  );
}

function TabsTrigger({ className, ...props }) {
  return (
    <TabsPrimitive.Trigger
      className={cn(
        "inline-flex items-center justify-center whitespace-nowrap rounded-lg px-3.5 py-1.5 text-sm font-semibold transition-all data-[state=active]:bg-white data-[state=active]:text-[var(--foreground)] data-[state=active]:shadow-sm",
        className
      )}
      {...props}
    />
  );
}

function TabsContent({ className, ...props }) {
  return <TabsPrimitive.Content className={cn("mt-4", className)} {...props} />;
}

export { Tabs, TabsList, TabsTrigger, TabsContent };
