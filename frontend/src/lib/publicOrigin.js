/**
 * Origin used in Supabase `redirectTo` / `emailRedirectTo` (password reset, signup confirmation).
 *
 * In production Docker/Railway builds, set `VITE_PUBLIC_APP_URL` to the public site URL (no path),
 * e.g. `https://wise-ai-frontend-production.up.railway.app`.
 * Add the same URL (with trailing `/` if needed) under Supabase → Authentication → URL Configuration
 * → Redirect URLs, or Supabase may fall back to the project Site URL (often localhost during setup).
 */
export function getPublicAppOrigin() {
  const fromEnv = import.meta.env.VITE_PUBLIC_APP_URL?.trim();
  if (fromEnv) {
    return fromEnv.replace(/\/+$/, "");
  }
  if (typeof window !== "undefined" && window.location?.origin) {
    return window.location.origin;
  }
  return "";
}
