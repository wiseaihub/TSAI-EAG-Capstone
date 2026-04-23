import { test, expect } from "@playwright/test";

test.describe("login surface smoke", () => {
  test("unauthenticated visitor lands on the login panel", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("heading", { name: /wise clinical portal/i })).toBeVisible();
    await expect(page.getByLabel(/email/i)).toBeVisible();
    // Tab button + CTA both read "Sign in"; asserting count >= 1 is sufficient for smoke.
    const signIn = page.getByRole("button", { name: /^sign in$/i });
    await expect(signIn.first()).toBeVisible();
  });

  test("auth mode tabs switch between sign-in, register, and forgot-password", async ({ page }) => {
    await page.goto("/");

    // Click the mode tabs (first occurrence = tab row; CTA follows below).
    await page.getByRole("button", { name: /create patient account/i }).first().click();
    await expect(page.getByLabel(/confirm password/i)).toBeVisible();

    await page.getByRole("button", { name: /forgot password/i }).first().click();
    await expect(page.getByRole("button", { name: /send reset link/i })).toBeVisible();
    await expect(page.getByLabel(/^password$/i)).toHaveCount(0);

    await page.getByRole("button", { name: /^sign in$/i }).first().click();
    await expect(page.getByLabel(/^password$/i)).toBeVisible();
  });
});
