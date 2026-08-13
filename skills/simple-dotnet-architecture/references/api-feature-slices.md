# API Feature Slices

Use this reference for ASP.NET Core Minimal APIs targeting .NET 8 or later. Read the application's target framework before using version-specific APIs; the `AddValidation` note below applies only to .NET 10+. Start with one operation per file:

```text
HTTP request -> Endpoint -> Handler -> DbContext / services / external clients
```

The endpoint owns route and method, binding, HTTP request/response contracts, authentication and coarse authorization, status codes, and mapping. The handler owns one use case; do not use `HttpContext`, `IResult`, `Results`, or endpoint contract types inside it.

## Keep contracts local

Nest `Request` and `Response` inside the endpoint class. They are HTTP contracts for that route, not application models. Keep them distinct even when another endpoint currently has matching fields, so contracts can change independently.

Let the handler return the simplest useful application value: a domain/entity model, scalar, enum, or an explicit outcome. Nest `Result` inside the handler only when a handler-specific projection or outcome makes the operation clearer. It is application data, not an HTTP response. Extract a named model into the feature folder only when multiple handlers intentionally share the same concept.

```text
One endpoint       -> Endpoint.Request / Endpoint.Response
One handler        -> Handler.Result, only when it adds meaning
Multiple handlers  -> named shared model in the feature folder
```

Do not expose an EF entity directly as the HTTP response or reuse a handler result as an endpoint response just because its fields match. The endpoint maps application data to the HTTP contract. Do not create `Handler.Result` solely to duplicate `Endpoint.Response`.

```csharp
public static class GetProduct
{
    public static class Endpoint
    {
        public sealed record Response(Guid Id, string Name, decimal Price);

        public static void Map(IEndpointRouteBuilder app) =>
            app.MapGet("/products/{id:guid}", async (
                Guid id, Handler handler, CancellationToken ct) =>
            {
                var product = await handler.HandleAsync(id, ct);
                return product is null
                    ? Results.NotFound()
                    : Results.Ok(new Response(product.Id, product.Name, product.Price));
            })
            .RequireAuthorization();
    }

    public sealed class Handler(AppDbContext db)
    {
        public Task<Product?> HandleAsync(Guid id, CancellationToken ct) =>
            db.Products.AsNoTracking()
                .SingleOrDefaultAsync(x => x.Id == id, ct);
    }
}
```

Use this direct return when the operation already works with a suitable domain/entity model and the endpoint maps it immediately. Use a handler-specific projection when the query should fetch only needed columns or when its output has meaning distinct from the HTTP response. For example, `SearchProducts.Handler.Result` may represent search data while `SearchProducts.Endpoint.Response` represents the public JSON contract.

For a write, keep the input contract at the endpoint and pass only the application inputs to the handler:

```csharp
public static class CreateProduct
{
    public static class Endpoint
    {
        public sealed record Request(string Name, decimal Price);
        public sealed record Response(Guid Id, string Name, decimal Price);

        public static void Map(IEndpointRouteBuilder app) =>
            app.MapPost("/products", async (
                Request request, Handler handler, CancellationToken ct) =>
            {
                var product = await handler.HandleAsync(request.Name, request.Price, ct);
                return Results.Created($"/products/{product.Id}",
                    new Response(product.Id, product.Name, product.Price));
            });
    }

    public sealed class Handler(AppDbContext db)
    {
        public async Task<Product> HandleAsync(string name, decimal price, CancellationToken ct)
        {
            var product = new Product { Id = Guid.NewGuid(), Name = name, Price = price };
            db.Products.Add(product);
            await db.SaveChangesAsync(ct);
            return product;
        }
    }
}
```

Use feature-oriented files and composition:

```text
Features/
  Products/
    GetProduct.cs
    CreateProduct.cs
    SearchProducts.cs
    ProductsModule.cs          # feature composition: DI registration + route mapping
    ProductSummary.cs          # only when handlers intentionally share it
  Orders/
    GetOrder.cs
    PlaceOrder.cs
    OrdersModule.cs
```

Use a single file by default. An operation file may contain the endpoint, endpoint contracts, handler, and handler result; the file represents the operation, not a single class. Keep `Program.cs` as composition only. Register handlers and map routes per feature.

Place `ProductsModule.cs` at the root of `Features/Products`, beside its operation files—not in a global mapping or startup folder. It owns only the feature's `AddProducts` dependency registrations and `MapProducts` endpoint mappings. Keep route implementation in each operation's `Endpoint.Map`; the module calls those methods. `Program.cs` calls the module methods and owns application-wide setup such as the `DbContext`, authentication, exception handling, and OpenAPI.

Split one operation into a directory when the operation needs several cohesive supporting types—for example, a large mapping, complex validation, a policy, a state-machine/domain type, or focused operation tests—and the single file is no longer easy to scan:

```text
Features/
  Products/
    GetProduct/
      Endpoint.cs
      Handler.cs
```

Keep `Endpoint.cs` and `Handler.cs` in the same operation directory, with only that operation's supporting files. Do not split merely because there are multiple classes, an endpoint has a request and response, or another operation in the feature is large. Do not separate all endpoints from all handlers into feature-wide folders; keep code for the same operation together.

```csharp
public static class ProductsModule
{
    public static IServiceCollection AddProducts(this IServiceCollection services)
    {
        services.AddScoped<GetProduct.Handler>();
        services.AddScoped<CreateProduct.Handler>();
        return services;
    }

    public static IEndpointRouteBuilder MapProducts(this IEndpointRouteBuilder app)
    {
        GetProduct.Endpoint.Map(app);
        CreateProduct.Endpoint.Map(app);
        return app;
    }
}

// Program.cs
builder.Services.AddProducts();
var app = builder.Build();
app.MapProducts();
```

Put coarse authorization on endpoints or route groups. Perform resource ownership and business eligibility in the handler or a policy service, passing needed actor data rather than `HttpContext`. Use centralized exception handling and Problem Details for unexpected failures; map expected operation outcomes to HTTP status codes at the endpoint.

Validate request shape at the HTTP edge. In .NET 10+, Minimal APIs can use built-in validation through `AddValidation`; keep business invariants out of HTTP-only validation.

Test handler decisions without HTTP where that produces a clear, fast test. Add an API integration test for route binding, authorization, validation, status codes, and response contract. Do not create a repository solely to replace an EF Core test with a mock.
