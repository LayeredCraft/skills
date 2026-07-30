# Testing

Discover repository test framework, directory layout, naming, fixture strategy,
coverage expectations, and CI commands before adding tests. Match established
patterns unless change explicitly improves them.

## Coverage strategy

- Test behavior and contracts, not private implementation details.
- Add regression test that fails before bug fix and passes after it.
- Cover happy path, important boundaries, failure paths, and security-relevant
  negative cases proportional to risk.
- Keep tests deterministic: control time, randomness, concurrency, locale,
  filesystem, and network where they affect outcomes.
- Prefer smallest test level proving behavior, then add integration or end-to-end
  coverage for wiring and boundary risks unit tests cannot catch.
- Test new public entry points in isolation so existing paths cannot accidentally
  initialize state or mask missing wiring.
- For generators, compilers, serializers, migrations, plugins, or packaging,
  verify realistic consumer output in addition to unit tests.
- Avoid mocks where real lightweight collaborators reveal more behavior. Mock
  external boundaries or expensive/non-deterministic dependencies deliberately.
- Keep fixtures readable and focused. Use builders/factories only when they reduce
  repeated noise without hiding relevant setup.
- Assert meaningful outcomes and diagnostics; avoid snapshots so broad that
  reviewers cannot distinguish intentional changes from churn.

## Verification

Inspect unfamiliar scripts before running them. Ask before commands that install
software, use network or credentials, mutate external systems, or may be
destructive. Run safe narrow tests during development, then repository-required
validation: formatting/linting, build/type-check, unit tests, integration tests,
and packaging or consumer checks as applicable.

Report exact commands and results. If environment prevents a check, state what was
not run and why. Never infer success from compilation alone.
