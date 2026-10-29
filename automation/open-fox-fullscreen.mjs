/**
 * Open FOX Weather YouTube live and send fullscreen.
 * DRY_RUN=1 prints the URL and exits without launching Chrome.
 */
const VIDEO_ID = "wt6SIE7BXS8";
const URL = `https://www.youtube.com/watch?v=${VIDEO_ID}`;

export function foxUrl() {
  return URL;
}

if (process.env.DRY_RUN === "1") {
  console.log(URL);
  process.exit(0);
}

const { chromium } = await import("playwright");
const browser = await chromium.launch({
  channel: "chrome",
  headless: false,
});
const page = await browser.newPage();
await page.goto(URL, { waitUntil: "domcontentloaded" });
await page.keyboard.press("f");
if (process.env.KEEP_OPEN === "1") {
  await new Promise(() => {});
}
await browser.close();
