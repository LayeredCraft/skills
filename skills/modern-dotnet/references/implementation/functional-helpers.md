# Functional helpers

**Summary.** Use distinct success and failure cases in a generic Result. Reuse small helpers when they make a sequence of operations easier to read.

## Contents

- [Define distinct result cases](#define-distinct-result-cases)
- [Implement the helpers](#implement-the-helpers)
- [Compose a pricing operation](#compose-a-pricing-operation)
- [Model ordinary absence](#model-ordinary-absence)

## Define distinct result cases

Use the application's existing Result when it has one. If several operations need a shared Result, give it a named home near its callers, such as `Application/Outcomes/Result.cs`. Keep the case types in the same file while they are easy to scan. For a named operation with distinct expected states, use an [operation-specific union](expected-outcomes.md#choose-the-outcome-shape).

```csharp
public readonly record struct Success<T>(T Value);
public readonly record struct Failure<TError>(TError Error);
public union Result<T, TError>(Success<T>, Failure<TError>);
```

`new Success<string>("SH-42")` and `new Failure<string>("Provider rejected the quote")` convert unambiguously to `Result<string, string>`. Both carry strings, but the wrappers give the cases distinct meanings and types.

## Implement the helpers

`Map` changes the successful value. `Bind` calls another operation that can return a failure. `Tap` observes a successful value and passes the original result through. Each skips its callback when the result is a failure. Keep commits and required effects explicit in the handler.

```csharp
public static class ResultExtensions
{
    public static Result<TNext, TError> Map<T, TNext, TError>(
        this Result<T, TError> result, Func<T, TNext> map) => result switch
    {
        Success<T> success => new Success<TNext>(map(success.Value)),
        Failure<TError> failure => failure
    };

    public static Result<TNext, TError> Bind<T, TNext, TError>(
        this Result<T, TError> result, Func<T, Result<TNext, TError>> bind) => result switch
    {
        Success<T> success => bind(success.Value),
        Failure<TError> failure => failure
    };

    public static Result<T, TError> Tap<T, TError>(
        this Result<T, TError> result, Action<T> observe)
    {
        if (result is Success<T> success)
            observe(success.Value);

        return result;
    }
}
```

These helpers expect an initialized union. Account for `null` at a boundary where a nullable or default-initialized value can reach the match. [C# union exhaustiveness](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/union#union-exhaustiveness).

These helpers are synchronous. Match a successful result and explicitly await required asynchronous work, or use the application's existing async helpers. An async lambda passed to `Tap` becomes `async void`, and an async lambda passed to `Map` produces a successful value containing a task.

## Compose a pricing operation

Use a short chain when the order is obvious. Here both `LoadQuote` and `ApplyDiscount` return `Result<Quote, PricingError>`. A failure skips the rest of the chain.

```csharp
return LoadQuote(orderId)
    .Bind(ApplyDiscount)
    .Tap(quote => logger.LogDebug("Priced order {OrderId}", orderId))
    .Map(quote => new QuoteDto(quote.Total));
```

Match the final result inline at the entry point. Use a local variable or a normal branch when that makes the next action clearer.

## Model ordinary absence

Use an explicit option when absence is the entire alternative. Use an operation-specific name such as `ShipmentNotFound` when it tells the caller what is missing.

```csharp
public readonly record struct Some<T>(T Value);
public readonly record struct None;
public union Option<T>(Some<T>, None);
```
