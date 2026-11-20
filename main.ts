// news-image-20261120-cand-c: copies the pre-built entry.png to the output dir.
// The image itself was composed programmatically (PIL) from the verified
// 40-story list for Friday 20 November 2026; this script only copies it.
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const EXPECTED_SHA256 =
  "740439425442a7351223315fa5eee8d817d6eda7ce94754b847af06f44bacc4b";

const here = fileURLToPath(new URL(".", import.meta.url));
const sourcePath = join(here, "entry.png");
let bytes: Buffer;
try {
  bytes = readFileSync(sourcePath);
} catch {
  throw new Error(`cannot read entry.png at ${sourcePath}: file missing or unreadable`);
}
if (bytes.length === 0) {
  throw new Error(`entry.png is empty (0 bytes) at ${sourcePath}`);
}
if (bytes.length > 1048576) {
  throw new Error(
    `entry.png too large: ${bytes.length} bytes exceeds 1 MiB limit (1048576 bytes)`,
  );
}

const digest = createHash("sha256").update(bytes).digest("hex");
if (digest !== EXPECTED_SHA256) {
  throw new Error(
    `entry.png sha256 mismatch: got ${digest}, expected ${EXPECTED_SHA256}`,
  );
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "entry.png"), bytes);
console.log(`entry.png sha256 ${digest}`);
