# Starter `single-webapp` golden subject

This directory is the fixed, zero-dependency subject used by the Starter S1
golden-path acceptance. The application exposes:

- `GET /health` for owned-PID readiness;
- `GET /` for the real Chromium exercise;
- `GET /data.json?run=...` for one same-origin business fact read from
  `app/fact.json`.

The sample itself does not contain a VeriTrail Plan or local machine path. The S1
acceptance copies it into two clean subject roots and uses one sealed Profile and Plan.
The only content difference is the `status` value in `app/fact.json`: the PASS copy
returns `ready`, while the FAIL copy returns `blocked`. This is an independent
acceptance pair, not an M6 causal comparison. The preregistered expectation never
changes, so failure remains a business-fact mismatch rather than environment sabotage
or a post-observation change to the judging standard.
