import { Stethoscope, UserRound } from "lucide-react";
import { Tabs, TabsList, TabsTrigger } from "../../components/ui/tabs";

export function ModeSwitcher({ mode, onModeChange }) {
  return (
    <Tabs value={mode} onValueChange={onModeChange}>
      <TabsList>
        <TabsTrigger value="doctor" className="gap-2">
          <Stethoscope className="h-4 w-4" />
          Doctor View
        </TabsTrigger>
        <TabsTrigger value="patient" className="gap-2">
          <UserRound className="h-4 w-4" />
          Patient View
        </TabsTrigger>
      </TabsList>
    </Tabs>
  );
}
