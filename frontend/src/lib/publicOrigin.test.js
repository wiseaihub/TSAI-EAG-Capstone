import { describe, it, expect, afterEach, vi } from "vitest";
import { getPublicAppOrigin } from "./publicOrigin";

describe("getPublicAppOrigin", () => {
  afterEach(() => {
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
  });

  it("prefers VITE_PUBLIC_APP_URL and strips trailing slashes", () => {
    vi.stubEnv("VITE_PUBLIC_APP_URL", "https://app.example.com///");
    vi.stubGlobal("window", { location: { origin: "http://localhost:3000" } });
    expect(getPublicAppOrigin()).toBe("https://app.example.com");
  });

  it("falls back to window.location.origin when env is unset", () => {
    vi.stubEnv("VITE_PUBLIC_APP_URL", "");
    vi.stubGlobal("window", { location: { origin: "http://localhost:5173" } });
    expect(getPublicAppOrigin()).toBe("http://localhost:5173");
  });

  it("returns empty string when env unset and origin is unavailable", () => {
    vi.stubEnv("VITE_PUBLIC_APP_URL", "");
    vi.stubGlobal("window", {});
    expect(getPublicAppOrigin()).toBe("");
  });
});
