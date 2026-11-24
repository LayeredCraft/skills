# Integration and component tests

**Summary.** Favor component and integration tests. Share real database and broker fixtures where practical, and isolate each test's data.

## Contents

- [Choose what to exercise](#choose-what-to-exercise)
- [Share fixtures and isolate data](#share-fixtures-and-isolate-data)
- [Test a write race](#test-a-write-race)

## Choose what to exercise

Favor tests that exercise the operation through real dependencies. Use focused unit tests for domain rules that benefit from covering several cases quickly.

| What the test needs to prove                                                    | Where to test                               |
| ------------------------------------------------------------------------------- | ------------------------------------------- |
| A rule or state transition                                                      | Domain type                                 |
| Query translation, unique constraints, atomic writes, or optimistic concurrency | Handler with the production database engine |
| Binding, authorization, inline outcome mapping, or response shape               | HTTP component or integration test          |
| Delivery settlement, duplicate handling, ordering, or retry behavior            | Listener and broker integration             |
| Event source mapping, runtime permissions, or deployed trigger behavior         | Deployed integration test                   |

## Share fixtures and isolate data

Use Testcontainers with the production database engine where possible. Share containers, databases, and tables across tests to minimize startup. Apply migrations once per shared fixture. Isolate test data with unique keys, explicit cleanup, or controlled resets. Coordinate any full-table reset with tests using those tables. Use separate contexts per parallel operation. Exercise distinct providers only when they represent supported deployments.

Use real-provider tests for database behavior. An EF in-memory collection or mock cannot establish SQL translation, constraints, or transaction semantics. Test a worker with a controllable trigger or clock. Use a shared broker fixture when tests can isolate queues or consumer groups. [EF Core testing strategy](https://learn.microsoft.com/en-us/ef/core/testing/choosing-a-testing-strategy), [Testcontainers shared fixtures](https://dotnet.testcontainers.org/test_frameworks/xunit_net/).

## Test a write race

Use a distinct test row in the shared database. Open two scopes with separate contexts and load the row in both before either saves. Apply the competing domain transitions, save the winner, and assert that the stale write is rejected. Use a fresh context to verify the persisted state. For [dispatch and cancellation](../delivery/api-feature-slices.md#example-of-a-write-endpoint), exercise both winner orders and retry a duplicate cancellation to verify the listener's final disposition.
