# Configuration and options

**Summary.** Keep the host choice, registrations, and run sequence visible in `Program.cs`. Group registration details by owner. Bind related settings to typed options and validate required values at startup.

## Contents

- [Keep startup focused on composition](#keep-startup-focused-on-composition)
- [Show custom startup and shutdown](#show-custom-startup-and-shutdown)
- [Small app registration](#small-app-registration)
- [Registration by project](#registration-by-project)
- [Set and bind configuration](#set-and-bind-configuration)
- [Choose the options lifetime](#choose-the-options-lifetime)
- [Verify trimming and Native AOT](#verify-trimming-and-native-aot)

## Keep startup focused on composition

Use `Program.cs` as the composition root. Show which host runs, what it registers, what must succeed before it starts, and what happens when it stops. Keep builder creation, order-sensitive configuration, registration calls, `Build()`, and the run sequence visible. For a web host, also show the middleware order and top-level endpoint group mappings. Judge the file by how easily readers can follow those decisions. Line count is secondary.

Keep a small registration list inline. Group related registrations in named `Add` methods near the feature or adapter that owns them. Keep details such as HTTP client settings, options validation, and worker lifetimes inside those methods. Pick names that tell the reader what each call adds. Register app-owned services explicitly so readers can see which implementations and lifetimes the app uses without tracing assembly scanning or automatic discovery. A project with no services to register, such as a pure Domain project, can stay independent of DI.

## Show custom startup and shutdown

Use the framework's run call for a standard lifecycle. When the app has custom startup or shutdown policy, keep the major steps and the decisions that control them in `Program.cs`. Show what prevents startup, what must finish before shutdown completes, and which outcomes determine the exit code. Call named methods for the work at each step. Use explicit awaits when one step must finish before the next begins. Use LINQ or functional helpers where they make transformations or decisions easier to read. If a builder or run wrapper hides the process order, move that sequence into `Program.cs`.

GAFS Notification is an example of a custom lifecycle. Its steps run in this order.

1. Load `.env`, create the Generic Host builder, and apply secret-file overrides.
2. Call the named registration methods and build the host.
3. Check Mullvad and validate rules before starting workers.
4. Start workers and send the startup alert.
5. Wait for shutdown, drain the workers, and send the shutdown alert when appropriate.
6. Return the exit code.

Keep VPN response parsing, alert throttling, and queue draining with their existing owners. When moving lifecycle calls, preserve the behavior on failed preflight, fatal errors, and graceful shutdown, including which alerts run and which exit code is returned.

## Small app registration

A handful of registrations can stay in `Program.cs`. Keep the endpoint mapping with the operation.

```csharp
builder.Services.AddDbContext<ShippingDbContext>(
    options => options.UseSqlServer(connectionString));
builder.Services.AddScoped<GetShipment.Handler>();

var app = builder.Build();
GetShipment.Map(app);
app.Run();
```

## Registration by project

When Application and Infrastructure are separate, Application registers its handlers and Infrastructure registers its providers and adapters. The host supplies deployment settings and calls both methods. A large project can group registrations by business area. Name methods for what they add, such as `AddShippingInfrastructure` or `AddApiAuthentication`.

```csharp
// Program.cs
var connectionString = builder.Configuration.GetConnectionString("Shipping")
    ?? throw new InvalidOperationException("The Shipping connection string is required.");

builder.Services.AddShippingApplication();
builder.Services.AddShippingInfrastructure(connectionString);

var app = builder.Build();
app.MapShippingEndpoints();
app.Run();
```

```csharp
// Application/Shipping/ShippingRegistration.cs
public static class ShippingApplicationRegistration
{
    public static IServiceCollection AddShippingApplication(this IServiceCollection services)
    {
        services.AddScoped<CancelShipment>();
        return services;
    }
}
```

```csharp
// Infrastructure/Shipping/ShippingRegistration.cs
public static class ShippingInfrastructureRegistration
{
    public static IServiceCollection AddShippingInfrastructure(
        this IServiceCollection services, string connectionString)
    {
        services.AddDbContext<ShippingDbContext>(
            options => options.UseSqlServer(connectionString));
        services.AddScoped<IShippingDbContext>(
            sp => sp.GetRequiredService<ShippingDbContext>());

        return services;
    }
}
```

The interface and concrete type resolve to the same scoped context. The API owns route mapping:

```csharp
// Api/Shipping/ShippingEndpoints.cs
public static class ShippingEndpoints
{
    public static void MapShippingEndpoints(this IEndpointRouteBuilder endpoints)
    {
        CancelShipmentEndpoint.Map(endpoints);
    }
}
```

Configure any needed authentication and authorization policies in the host. [Minimal API registration](../delivery/api-feature-slices.md#register-and-evolve-the-operation).

## Set and bind configuration

- Put static, non-secret defaults in `appsettings.json`. Put deployed values that vary by environment in deployment configuration. Use a secret store for secrets and the local runner's facilities for local settings.
- Bind related settings to a typed options class. Use a direct read for a genuinely standalone value in composition when a type adds no clarity. Keep settings out of business models and EF entities.
- Give a required section a clear name. Bind public writable properties in a class the options system can construct. Use a mutable collection for binding and expose a read-only view where that helps callers.
- Use validation at startup for values the app needs to run. Data annotations need a registered validator. For relationships between settings, use a predicate or a named validator when the logic warrants one.

```csharp
public sealed class PaymentOptions
{
    public const string SectionName = "Payments";

    [Required, Url]
    public string BaseUrl { get; set; } = "";

    [Range(1, 300)]
    public int TimeoutSeconds { get; set; } = 30;
}

[OptionsValidator]
public partial class ValidatePaymentOptions : IValidateOptions<PaymentOptions>
{
}
```

```csharp
builder.Services.AddSingleton<IValidateOptions<PaymentOptions>, ValidatePaymentOptions>();
builder.Services
    .AddOptions<PaymentOptions>()
    .BindConfiguration(PaymentOptions.SectionName)
    .ValidateOnStart();
```

Use `Payments__BaseUrl` for the environment-variable form of `Payments:BaseUrl`. For named framework options such as an authentication scheme, configure the named instance through the options builder and inject the settings it needs.

## Choose the options lifetime

| Need                                       | Inject                |
| ------------------------------------------ | --------------------- |
| Settings remain fixed for the app lifetime | `IOptions<T>`         |
| A consistent snapshot per request or scope | `IOptionsSnapshot<T>` |
| A singleton needs to read updated values   | `IOptionsMonitor<T>`  |

Read `IOptionsMonitor<T>.CurrentValue` at the point of use when reload matters. Reload depends on the configuration provider.

## Verify trimming and Native AOT

For trimming or Native AOT, use supported configuration binder generation and the generated options validator. Check the build for trimming warnings before replacing typed binding with manual reads. Native AOT publishing enables configuration binding generation by default. For other builds, set `EnableConfigurationBindingGenerator` when needed. [Options pattern](https://learn.microsoft.com/en-us/dotnet/core/extensions/options), [Configuration binding source generator](https://learn.microsoft.com/en-us/dotnet/core/extensions/configuration-generator).
