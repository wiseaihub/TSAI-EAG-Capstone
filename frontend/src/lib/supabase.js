import { createClient } from "@supabase/supabase-js";

const supabaseUrl = "https://lfjihuzcshjpggtdrtne.supabase.co";
const supabaseAnonKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxmamlodXpjc2hqcGdndGRydG5lIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzMDQ2MDIsImV4cCI6MjA4Njg4MDYwMn0.G4mvQKWMRwdRlYUmFmJiWKgj5cUeXm-WVF-SSk6hPBc";

export const supabase = createClient(
  supabaseUrl,
  supabaseAnonKey
);
