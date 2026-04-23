import "@testing-library/jest-dom/vitest";
import { afterEach, vi } from "vitest";
import { cleanup } from "@testing-library/react";

// Stub Vite env vars that components expect at import time so module loads don't throw.
// Tests that need different values can override per-test via vi.stubEnv.
if (!import.meta.env.VITE_SUPABASE_URL) {
  vi.stubEnv("VITE_SUPABASE_URL", "https://test.supabase.co");
}
if (!import.meta.env.VITE_SUPABASE_ANON_KEY) {
  vi.stubEnv("VITE_SUPABASE_ANON_KEY", "test-anon-key");
}

afterEach(() => {
  cleanup();
});
