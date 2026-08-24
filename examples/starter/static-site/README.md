# Starter `static-site` golden subject

This subject is deliberately build-free and loopback-only. The Starter 0.2
`static-site` preset generates a DRAFT that configures Core to serve
`site/index.html` through an owned CPython `http.server`; authoring itself does
not execute repository scripts, start the server, or infer a build.

The page exposes two explicit browser facts:

- `main` is visible;
- `[data-testid='static-status']` contains `static evidence ready`.

The example has no remote assets, secret, package manager, framework runtime,
container, or external service.
