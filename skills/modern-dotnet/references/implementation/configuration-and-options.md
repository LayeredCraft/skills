# Configuration and Options

Configuration is data, not code. Read each value once into a typed options object and consume
it where it is needed; do not spread `Configuration[...]` reads through startup code or
handlers. This reference covers where a value belongs, how to bind it, and what to do when
trimming or Native AOT looks like it rules a mechanism out.

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

## Bind through the options system

```csharp
services
    .AddOptions<PaymentOptions>()
    .BindConfiguration(PaymentOptions.SectionName)
    .Validate(o => !string.IsNullOrWhiteSpace(o.ApiKey), "Payment:ApiKey must be configured.")
    .ValidateOnStart();
```

`BindConfiguration` reads the registered `IConfiguration` itself, so an extension method needs
no `IConfiguration` parameter and callers never pass configuration around.

Use `ValidateOnStart()` for anything the application cannot run without. Options resolve
lazily, so without it a missing or invalid value surfaces at first use — possibly under load,
where it is hardest to diagnose — instead of at startup where it is obvious.

## Validate

- One or two simple checks: an inline `.Validate(predicate, message)` is enough.
- Many options types, or declarative rules: put `[Required]` (and friends) on the options type
  and attribute a partial `IValidateOptions<T>` with `[OptionsValidator]`. The generator emits
  the validation code, so it stays trim-safe.

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
`BindConfiguration()` stay trim-safe. It is on by default in projects that publish with Native
AOT; in a context where it is not, set `EnableConfigurationBindingGenerator` explicitly.

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
        .Validate(o => !string.IsNullOrWhiteSpace(o.Issuer), "Cognito:Issuer must be configured.")
        .ValidateOnStart();

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
