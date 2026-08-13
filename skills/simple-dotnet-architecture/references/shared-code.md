# Shared Code and Capabilities

Group code by ownership and purpose, not by technical type. Do not create global `Services`, `Models`, `Helpers`, or `Common` folders as default destinations.

## Decide whether to extract a service

Keep logic in the handler when it is short and specific to one operation. Extract a concrete service when a cohesive capability, business policy, or integration is reused by multiple operations. A service does real work; it is not a forwarding layer between a handler and `DbContext`.

```text
Handler          -> coordinates one operation
Service          -> reusable capability or policy
Typed client     -> external system boundary
DbContext        -> EF Core persistence and unit of work
```

Do not create `ProductService` merely to contain `Get`, `Create`, `Update`, and `Delete` methods that repeat normal EF Core access. Register services as concrete types by default; use an interface only for an interchangeable provider, a genuine module boundary, or runtime implementation selection.

## Place code with its owner

Use these locations in a new application; preserve a coherent existing convention instead.

```text
Features/
  Products/
    GetProduct.cs
    CreateProduct.cs
    ProductSummary.cs           # intentionally shared by product handlers
    ProductAvailability.cs      # capability used only by product operations
    ProductsModule.cs
  Orders/
    PlaceOrder.cs

Capabilities/
  Pricing/
    PricingService.cs           # capability used by Products and Orders
  Payments/
    PaymentClient.cs            # typed boundary to an external provider

SharedKernel/
  Money.cs                      # stable domain concept, not a convenience DTO
  Currency.cs
```

- Keep operation-only helpers and models in the operation file or directory.
- Keep feature-owned services and models in that feature folder.
- Give a cross-feature capability its own named folder, such as `Capabilities/Pricing`; do not hide it in a generic shared folder.
- Keep a typed external client with its integration/provider, not with the caller that first used it.
- Create `SharedKernel` only for small, stable concepts with a shared meaning. Do not put convenience DTOs there.

The folder names are defaults, not a required project layout. The important rule is that a file's location reveals its owner and intended consumers.

## Keep models at the narrowest scope

```text
Endpoint Request/Response       -> nested in the endpoint
One handler's projection        -> nested Handler.Result, only if meaningful
Several handlers in one feature -> named model in that feature
Message contract                -> owned/versioned at the messaging boundary
Stable domain value object      -> SharedKernel, only when truly shared
```

Do not share an endpoint contract with a handler, another endpoint, or a message consumer just because the fields match. Do not share an EF entity as a DTO. Duplicate a small contract until sharing reflects an intentional, stable concept.

## Examples

`PricingService` is a cross-feature capability because both product previews and order placement use the same pricing policy:

```csharp
public sealed class PricingService
{
    public PriceQuote Quote(Product product, int quantity, CustomerTier tier) =>
        new(product.Id, product.Price * quantity, product.Currency);
}

public sealed record PriceQuote(Guid ProductId, decimal Total, string Currency);
```

`ProductAvailability` stays in `Features/Products` when only product operations need it:

```csharp
public sealed class ProductAvailability(AppDbContext db)
{
    public Task<bool> IsAvailableAsync(Guid productId, CancellationToken ct) =>
        db.Products.AnyAsync(x => x.Id == productId && x.IsActive, ct);
}
```

`PaymentClient` is a provider boundary, so an interface may be useful if multiple providers must be selected or a provider-specific implementation must be isolated:

```csharp
public interface IPaymentProvider
{
    Task<PaymentResult> ChargeAsync(ChargeRequest request, CancellationToken ct);
}

public sealed class StripePaymentClient(HttpClient http) : IPaymentProvider
{
    public Task<PaymentResult> ChargeAsync(ChargeRequest request, CancellationToken ct) =>
        throw new NotImplementedException();
}
```

Test a service's business behavior directly. Test typed clients at the HTTP boundary. Do not introduce interfaces only to mock feature-local services or handlers.
