# Task: Explain

Use when user asks for detailed walkthrough of code, architecture, or completed
work. Unlike normal terse implementation summaries, optimize for teaching and
accurate mental model.

## Procedure

1. Re-read relevant code, tests, docs, decisions, and plan from disk. Do not explain
   from conversation memory.
2. Start with problem, users, constraints, and high-level solution.
3. Define project-specific terms and assumptions before using them heavily.
4. Walk components in execution or interaction order, not alphabetical file order.
5. Explain why important choices exist, including rejected alternatives or
   constraints captured in decision records.
6. Trace one realistic example end-to-end from input through observable output.
7. Connect tests to behaviors they prove and identify what remains unverified.
8. Distinguish working behavior from scaffolding, planned work, and unsupported
   cases. Use plan status and code evidence, not optimism.
9. Close with practical usage, extension points, limitations, and next steps.

## Output

Patient, structured walkthrough in chat unless user requests written artifact.
Quote only code needed to anchor explanation; prefer file and symbol references for
rest.
