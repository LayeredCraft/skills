# Configuration and Options

Configuration is data, not code. Every value is read once into a typed options object that the
binder populates for you, and consumed from there.

Do not pull values out of configuration by hand. `Configuration["Payment:ApiKey"]`, an injected
`IConfiguration`, and a hand-built settings object all bypass binding, validation, and reload,
and they scatter one section's shape across the codebase. Declare the options type, bind it to
its section, and let DI hand out the populated instance.

## Choose the source

Pick the home by the value's nature, not by convenience:

| Value                                                                        | Home                                                             |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Non-secret, environment-specific (URLs, tenant ids, pool ids, feature flags) | Deployment configuration, set by infrastructure-as-code          |
| Non-secret, a static default                                                 | `appsettings.json`                                               |
| Secret                                                                       | A secret store; never `appsettings.json`, never a committed file |
| A single developer's local value                                             | The local runner's mechanism (user secrets, app-host parameters) |

Deployed values supplied by infrastructure mean a deploy is the only step; a required manual
settings edit per environment is a defect waiting to happen. Do not invent a settings section
for a value the platform already provides, and do not commit a placeholder that cannot work —
a clear startup failure is more honest than a plausible-looking wrong value.

Name section names, policy names, and scope strings as constants on the options or policy
type so wiring and endpoints cannot drift apart.

## The options type

One sealed class per section, with the annotations that state what a valid configuration looks
like sitting beside the properties they constrain:

```csharp
public sealed class PaymentOptions
{
    public const string SectionName = "Payment";

    [Required]
    public required string ApiKey { get; set; }

    [Required, Url]
    public required string BaseUrl { get; set; }

    [Range(1, 300)]
    public int TimeoutSeconds { get; set; } = 30;
}
```

`required` guards the code side: a consumer cannot forget to set the property. The annotations
guard the configuration side, where the value can simply be absent at runtime. They cover
different failures, so keep both.

A single public parameterized constructor is supported, so records and `init`-only types bind
directly.

Two limits fail silently, so they are worth knowing up front:

- Only public read/write **properties** bind; a field is ignored.
- Only mutable collections bind. `IReadOnlyList<T>` and `IReadOnlyDictionary<TKey, TValue>` are
  never populated — bind to `List<T>` or `Dictionary<TKey, TValue>` and expose the read-only
  view to consumers.

## Bind

```csharp
services
    .AddOptions<PaymentOptions>()
    .BindConfiguration(PaymentOptions.SectionName)
    .ValidateOnStart();
```

`BindConfiguration` reads the registered `IConfiguration` itself, so an extension method needs
no `IConfiguration` parameter and callers never pass configuration around.

Use `ValidateOnStart()` for anything the application cannot run without. Options resolve
lazily, so without it a missing or invalid value surfaces at first use — possibly under load,
where it is hardest to diagnose — instead of at startup where it is obvious.

## Validate

Annotations on the options type are the default. Add a rule they cannot express — anything about
the relationship between two properties — with `.Validate(predicate, message)`:

```csharp
services
    .AddOptions<PaymentOptions>()
    .BindConfiguration(PaymentOptions.SectionName)
    .Validate(
        o => o.BaseUrl.StartsWith("https://", StringComparison.OrdinalIgnoreCase),
        "Payment:BaseUrl must use https.")
    .ValidateOnStart();
```

Annotations still need a validator, and there are two ways to supply one.
`.ValidateDataAnnotations()` reflects over the attributes at runtime; the source generator emits
the same checks as code, which is why it is the choice that survives trimming and Native AOT.
Attribute an empty partial `IValidateOptions<T>`:

```csharp
[OptionsValidator]
public partial class ValidatePaymentOptions : IValidateOptions<PaymentOptions>
{
}
```

The attribute only generates the validator. Register it, or nothing validates:

```csharp
services.AddSingleton<IValidateOptions<PaymentOptions>, ValidatePaymentOptions>();
```

Validation covers the options type's own properties. Apply `[ValidateObjectMembers]` to a nested
options property and `[ValidateEnumeratedItems]` to a collection property to recurse into them;
without the attribute, rules on the nested type are never evaluated.

## Consume it

| Need                                                     | Inject                                                                         |
| -------------------------------------------------------- | ------------------------------------------------------------------------------ |
| One resolved value, singleton lifetime                   | `IOptions<T>`                                                                  |
| A consistent snapshot for one request or scope           | `IOptionsSnapshot<T>`                                                          |
| Reacts to reload in a long-lived service                 | `IOptionsMonitor<T>`                                                           |
| A framework options type configured by a non-DI delegate | `AddOptions<ThatFrameworkOptions>(name).Configure<IOptions<T>>((o, t) => ...)` |

Do not read `IOptions<T>.Value` in a singleton constructor when reload matters — that freezes
the first value. The last row is the usual answer for authentication and similar handlers: the
framework builds its options outside DI, so configure its named options and let DI resolve the
settings.

## Environment variables

Environment variables map onto sections with a double underscore: `Payment__ApiKey` becomes
`Payment:ApiKey`. A single `:` is not a valid environment-variable name on Linux, which is why
the separator is doubled. This is the normal way a platform injects a section's values without
a settings file, so a configuration key that must be settable in the deployed environment
should be reachable this way.

## Trimming and Native AOT

The Microsoft.Extensions.Configuration.Binder **source generator** replaces the reflection in
`ConfigurationBinder` with generated property setters, so `Get<T>()`, `Bind()`, and
`BindConfiguration()` stay trim-safe. It is enabled automatically when the project sets
`PublishAot`; anywhere else, set `EnableConfigurationBindingGenerator` explicitly.

The generated binder is not identical to the reflection binder: it does not convert a value
through a custom type's `TypeConverter`. Where an options property is a custom type that has
one, bind a `string` and convert it inside the options type instead.

Hand-written `Configuration["A:B"]` reads are therefore not the AOT workaround people assume
they are; reach for them only for a genuinely single primitive where an options type would be
noise.

When you believe a constraint rules out a framework mechanism, verify it before designing
around it:

- Build with `EnableTrimAnalyzer`/`EnableAotAnalyzer` (or `PublishAot`) and read the
  `IL2026`/`IL3050` output.
- To confirm the binder generator is the thing keeping a call clean, build with
  `-p:EnableConfigurationBindingGenerator=false`. If warnings appear only then, the generator
  was doing the work and the manual workaround is unnecessary.

For the full trim/AOT workflow — warning codes, annotation fixes, CI validation — use the
`dotnet-aot-library-validation` skill when it is available; this reference covers only the
configuration and options surface. The verification habit itself is general, though: an
unverified platform limit that leads to a hand-rolled substitute is worse than the substitute
being unnecessary, because it encodes a false constraint into the design and everyone
downstream inherits it.

## Composition

```csharp
// Program.cs — what the application is made of
builder.Services.AddApiAuthentication();
builder.Services.AddOrdering();
builder.Services.AddApiCors();

// Authentication/AuthenticationExtensions.cs — how each concern is configured
public static IServiceCollection AddApiAuthentication(this IServiceCollection services)
{
    services
        .AddOptions<CognitoOptions>()
        .BindConfiguration(CognitoOptions.SectionName)
        .ValidateOnStart();
    services.AddSingleton<IValidateOptions<CognitoOptions>, ValidateCognitoOptions>();

    services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme).AddJwtBearer();
    services
        .AddOptions<JwtBearerOptions>(JwtBearerDefaults.AuthenticationScheme)
        .Configure<IOptions<CognitoOptions>>((options, cognito) =>
        {
            options.Authority = cognito.Value.Issuer;
            options.Audience = cognito.Value.Audience;
        });

    return services;
}
```

Give each concern its own `AddX` extension — authentication, authorization policies, CORS, JSON,
telemetry — in a folder named for the concern, with the options type beside it. `Program.cs`
invokes that setup and should read as a list of what the application is made of; it is not the
place where each concern's options are configured. Do not create a separate configuration or
identity project until a second consumer exists.
