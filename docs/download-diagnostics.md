# Model download diagnostics · 2026-10-15

## Scope and provenance

Runtime loads bundled local assets; synchronization is a separate explicit command. The importer uses the upstream project's published Pages endpoint. SHA256 values are pinned in `scripts/fetch-models.py`, alongside the previously verified Git blob IDs. This preserves version identity rather than accepting whatever is currently published. Upstream license/provenance remains separate from the application license.

## Controlled observations

- System curl 8.7.1 uses SecureTransport / LibreSSL 3.3.6. Python urllib uses LibreSSL 2.8.3. There are no proxy environment keys in the diagnostic process.
- `urllib.request.getproxies()` discovers the macOS system HTTP/HTTPS proxy on loopback port 7897, without credentials. Clash read-only observation reports system proxy enabled, TUN disabled, rule mode. No configuration, mode, node, DNS or system proxy was changed.
- Original host/path: `curl -L --fail --max-time 30 https://raw.githubusercontent.com/JohanBellander/BodyExplorer/main/public/anatomy.glb -o /tmp/muscle-atlas-raw-diagnostic.glb`. It exits 28 after 30.006 seconds, HTTP 000, zero downloaded bytes. Historical exit 35/reset was not reproduced in this trial; the failure currently manifests as a timeout.
- urllib GET of the raw mapping and Pages mapping each returns HTTP 200 and 89,477 bytes.
- Same raw anatomy URL with curl's per-process explicit system proxy succeeds in two independent fresh downloads: HTTP 200, 25,133,568 bytes, 2.761 seconds and 1.079 seconds. Both match SHA256 `6e84529b60b64cc8f8d5cef665fda932e359e828b66d0c2dd44ec1bd9d0bd01f`.

The best-supported controllable cause is route selection: urllib honors macOS system proxy discovery while unconfigured curl does not use that route. This comparison isolates the route while keeping curl and the original URL constant. It does not identify the upstream network equipment responsible for the historical connection reset, nor establish that direct raw connectivity is repaired.

Reproduce explicit routing without changing global settings (use the locally discovered system proxy; do not paste proxy credentials):

```sh
curl --proxy http://127.0.0.1:7897 -L --fail --max-time 30 \
  https://raw.githubusercontent.com/JohanBellander/BodyExplorer/main/public/anatomy.glb \
  -o /tmp/muscle-atlas-proxy-check.glb
shasum -a 256 /tmp/muscle-atlas-proxy-check.glb
```

## Durable paths compared

1. Change global proxy environment or network configuration. Could make all CLI clients use the route, but affects other projects and bypass preferences; unnecessary scope and not selected.
2. Use an explicit proxy for each curl invocation. Repeatedly verified against the original raw URL, leaves system configuration untouched, but requires callers to maintain route selection. Useful documented diagnostic, not an implicit fallback.
3. Keep the project importer on urllib with platform proxy discovery, official upstream URL, pinned digest, and verified local cache. Selected: portable standard-library implementation, no credentials/config mutation, offline runtime, integrity independent of endpoint behavior. Pages use does not prove direct raw transport repaired.

## Importer contract

`python3 scripts/fetch-models.py --offline` validates both bundled SHA256 values and performs no requests. The default command also skips every valid cached asset. Invalid existing finals remain in place until a fully verified replacement is ready.

A download has at most three attempts, 30-second socket timeout, and bounded backoff. Logs expose asset, attempt, exception class, partial bytes and verified digest without dumping proxy or error secrets. Retries restore progress after interruption; they are not evidence of a network fix.

Partial files use `.part`. A Range response is appended only with status 206 and a parseable Content-Range beginning at the exact partial length and ending at the declared total. A server ignoring Range with 200 causes truncation/restart. Untrustworthy 206, 416, or digest mismatch discards only the temporary partial. Successful final SHA256 is mandatory before atomic replacement. Mapping's source-code mirror is also atomically replaced. Range alone does not prove version continuity; the final pinned SHA256 does.

## Verification and residual debt

Eight Python unit tests cover offline cache hit, trustworthy resume after an interrupted transfer, ignored Range, invalid Range, corrupt content preservation, bounded transport failure, and truncated payload. Real full downloads verify the importer separately from fixtures. Fresh Python process offline checks verify the bundled cache.

The project's asset import reliability can be verified independently of raw direct connectivity. The original unqualified curl path still fails and should remain explicitly deferred if the debt entry includes system-wide transport. Reopen if importing a pinned asset fails or a required CLI raw operation needs direct connectivity; next action is a separately authorized direct-route/network investigation. No accepted risk or global transport repair is claimed.
