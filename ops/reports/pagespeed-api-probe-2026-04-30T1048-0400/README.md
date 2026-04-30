# PageSpeed API Unblock Probe

- Generated: 2026-04-30 10:48 EDT
- Google Cloud project: `dlm-pagespeed-20260430`
- API enabled: `pagespeedonline.googleapis.com`
- API key storage: `~/.config/dresslikemommy/pagespeed.env`
- Key restriction: PageSpeed Insights API only

The probe ran the first canonical target (`https://www.dresslikemommy.com/`) for both mobile and desktop through the official PageSpeed Insights API.

Artifacts:

- `psi-api-summary.csv`
- `manifest.json`
- `raw/`

Result:

- Planned requests: `2`
- Completed requests: `2`
- Successful PSI API responses: `2`
- Blocked by quota/auth: `false`

Full canonical run command:

```sh
python3 ops/scripts/run_pagespeed_api_batch.py
```

The runner defaults to:

- targets: `ops/reports/pagespeed-baseline-2026-04-30T093756-0400/psi-targets-canonical-default.csv`
- strategies: `mobile desktop`
- categories: `performance accessibility best-practices seo`
- local env file: `~/.config/dresslikemommy/pagespeed.env`
- output directory: timestamped under `ops/reports/pagespeed-api-*`

The run is resumable. Re-running the same command with the same output directory skips existing raw JSON unless `--force` is passed.
