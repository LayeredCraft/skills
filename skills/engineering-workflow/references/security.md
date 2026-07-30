# Security standards

Apply threat model appropriate to repository: service, library, CLI, build tool,
mobile app, infrastructure, firmware, or other system. Do not assume missing
network endpoint means no security boundary.

## Baseline

- Identify trust boundaries, attacker-controlled inputs, privileges, sensitive
  data, and externally observable outputs.
- Validate untrusted input at boundary; fail safely with actionable diagnostics.
- Use platform security primitives rather than custom cryptography or auth.
- Keep secrets out of source, fixtures, logs, generated artifacts, and examples.
- Use least privilege for credentials, filesystem, network, process execution,
  cloud roles, and CI permissions.
- Avoid dynamic execution, unsafe deserialization, command construction, and path
  traversal from untrusted data.
- Prevent sensitive data leakage through logs, errors, telemetry, caches, and test
  snapshots.
- Review dependency provenance, maintenance, licenses, advisories, transitive
  impact, and lockfile changes before adoption.
- Keep build scripts, plugins, analyzers, generators, and CI actions in threat
  model: they execute with developer or pipeline privileges.
- Consider abuse limits, race conditions, replay, rollback, and denial of service
  where relevant.

## Security-sensitive changes

For authentication, authorization, cryptography, secret handling, sandboxing,
parsing hostile input, package publishing, or privileged operations:

1. Document assets, actors, boundaries, and failure modes.
2. Prefer established design and current official guidance.
3. Add negative and boundary tests, not only happy-path tests.
4. Seek independent security review when impact warrants it.
5. Record residual risk and rollout/rollback plan.

Never weaken security controls merely to make tests or local development easier.
Use explicit development-only mechanisms with safe defaults instead.
