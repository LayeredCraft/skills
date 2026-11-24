# Configuration and options

**Summary.** Keep startup focused on explicit wiring. Group growing registrations by owner. Bind related settings to typed options and validate required values at startup.

## Contents

- [Keep startup focused on composition](#keep-startup-focused-on-composition)
- [Small app registration](#small-app-registration)
- [Registration by project](#registration-by-project)
- [Set and bind configuration](#set-and-bind-configuration)
- [Choose the options lifetime](#choose-the-options-lifetime)
- [Verify trimming and Native AOT](#verify-trimming-and-native-aot)

## Keep startup focused on composition

Use `Program.cs` to show what the host adds. Keep a small registration list inline. As it grows, put setup in the project or business area that owns the services and call named methods explicitly from `Program.cs`. Extract a group when its name makes the startup flow easier to read. Keep options and their validation with the concern that owns them.

Register application handlers and infrastructure services explicitly. Avoid assembly scanning for project-owned registrations. Each named method should make it easy to find the service, implementation, and lifetime. A project with no services to register, such as a pure Domain project, can stay independent of DI.

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
