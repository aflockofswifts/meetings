# A Flock of Swifts
![Flock](materials/flock.jpg)
We are a group of people excited by the Swift language. We meet each Saturday morning to share and discuss Swift-related topics. 

All people and all skill levels are welcome to join.  
**RSVP**: https://www.meetup.com/A-Flock-of-Swifts/

## Archives

- [2020 Meetings](2020/README.md)
- [2021 Meetings](2021/README.md)
- [2022 Meetings](2022/README.md)
- [2023 Meetings](2023/README.md)
- [2024 Meetings](2024/README.md)
- [2025 Meetings](2025/README.md)

## 2026.08.29

### Discussion notes

- Josh shared [Gate-All-Around, Transistor Architecture Designed for the Future of Logic Devices](https://www.youtube.com/watch?v=ST_1krgYni4), an introduction to the transistor architecture being adopted for future logic processes.
- In [Running iOS Background Tasks Reliably, Part 1](https://calcopilot.app/blog/posts/running-ios-background-tasks-reliably-part1/), Josh highlighted that `BGTaskScheduler` provides opportunities rather than fixed execution times. The article recommends keeping refresh work short, coordinating normal completion and expiration so `setTaskCompleted(success:)` is called exactly once, and anchoring replacement requests to the last run instead of repeatedly pushing `earliestBeginDate` into the future. Its device telemetry also showed that launches depend heavily on charging, device use, force-quitting, reboot state, and how recently the app was opened.
- Josh reviewed [Apple Foundation Models: Hybrid AI with Dynamic Profiles](https://peterfriese.dev/blog/2026/hybrid-ai-apple-foundation-models-gemini). Dynamic profiles can hide model-selection policy behind the Foundation Models API, using `tokenCount(for:)` and `contextSize` to keep suitable prompts on device while routing larger ones to a cloud model such as Gemini. This keeps model-specific instructions, token limits, and routing decisions out of the call site.
- Two SwiftUI layout articles addressed increasingly resizable Apple-platform interfaces. [Responding to geometry changes in SwiftUI](https://nilcoalescing.com/blog/RespondingToGeometryChangesInSwiftUI/) recommends deriving the smallest useful value in `onGeometryChange`, so intermediate measurements do not cause unnecessary state updates, and warns against feedback loops in which the updated state changes the measured geometry. [Building adaptive SwiftUI layouts with `containerRelativeFrame()`](https://nilcoalescing.com/blog/BuildingAdaptiveSwiftUILayoutsWithContainerRelativeFrame/) covers matching a container dimension, dividing it into equal portions with count and span, and calculating a custom proportional size.
- Josh shared [withContinuousObservation in Swift](https://livsycode.com/swift/withcontinuousobservation-in-swift/), which introduces the iOS 27 API for observing dependencies outside a SwiftUI view. Unlike one-shot `withObservationTracking`, it automatically re-registers dependencies after updates and continues until its `ObservationTracking.Token` is cancelled or released.
- In [Stalking the Wily Hacker: 40 years later](https://www.youtube.com/watch?v=656058JxTM0), Cliff Stoll revisits the 75-cent Unix accounting discrepancy that led him through a year-long investigation of a network intruder.
- Josh reviewed [item-based alerts and confirmation dialogs in SwiftUI](https://tanaschita.com/swiftui-alert-identifiable-data/). The iOS 27 overloads bind presentation directly to an optional `Identifiable` value, keeping the selected data and presentation state in one source of truth and resetting the binding to `nil` on dismissal.
- Josh shared an [analysis of Apple's M6 chip](https://www.tomsguide.com/computing/cpus/i-analyzed-apples-new-2nm-m6-chip-here-is-why-m1-holdouts-finally-need-to-upgrade). The article describes a 2 nm process, a three-tier 12-core CPU, expanded local-AI hardware, and higher memory bandwidth, and argues that the gains are most compelling for Intel, M1, and M2 Mac owners rather than recent M4 or M5 buyers.

### Links shared

| Preview | Shared by | Link | Description |
|---|---|---|---|
| [<img src="https://i.ytimg.com/vi/ST_1krgYni4/hqdefault.jpg" width="160" alt="Gate-All-Around transistor architecture video preview">](https://www.youtube.com/watch?v=ST_1krgYni4) | Josh | [Gate-All-Around, Transistor Architecture Designed for the Future of Logic Devices](https://www.youtube.com/watch?v=ST_1krgYni4) | Introduces the gate-all-around transistor architecture used in advanced logic processes. |
| [<img src="https://calcopilot.app/img/blog/diagrams/light/part1-trigger-funnel.png" width="160" alt="iOS background task scheduling article preview">](https://calcopilot.app/blog/posts/running-ios-background-tasks-reliably-part1/) | Josh | [Running iOS Background Tasks Reliably, Part 1](https://calcopilot.app/blog/posts/running-ios-background-tasks-reliably-part1/) | Reports practical `BGTaskScheduler` lessons about request replacement, expiration races, energy budgets, device state, and scheduling telemetry. |
| [<img src="https://peterfriese.dev/_astro/OG-afm-alf-hybrid.BmsqFFsM.png" width="160" alt="Foundation Models Dynamic Profiles article preview">](https://peterfriese.dev/blog/2026/hybrid-ai-apple-foundation-models-gemini) | Josh | [Apple Foundation Models: Hybrid AI with Dynamic Profiles](https://peterfriese.dev/blog/2026/hybrid-ai-apple-foundation-models-gemini) | Uses Dynamic Profiles to route requests between Apple's on-device model and Gemini according to context size and model-specific instructions. |
| [<img src="https://nilcoalescing.com/static/blog/RespondingToGeometryChangesInSwiftUI/banner.zwvTgro2-ShJfWEIE54VkayfExPXCqge45aKcCJWXYo.png" width="160" alt="SwiftUI geometry changes article preview">](https://nilcoalescing.com/blog/RespondingToGeometryChangesInSwiftUI/) | Josh | [Responding to geometry changes in SwiftUI](https://nilcoalescing.com/blog/RespondingToGeometryChangesInSwiftUI/) | Shows how to use `onGeometryChange` for adaptive layouts while limiting state changes to meaningful derived values. |
| [<img src="https://nilcoalescing.com/static/blog/BuildingAdaptiveSwiftUILayoutsWithContainerRelativeFrame/banner.yMzxQszjA_N5EQ4M73nNKTCWc_TkqfZb1BCaQaTzkv4.png" width="160" alt="SwiftUI containerRelativeFrame article preview">](https://nilcoalescing.com/blog/BuildingAdaptiveSwiftUILayoutsWithContainerRelativeFrame/) | Josh | [Building adaptive SwiftUI layouts with `containerRelativeFrame()`](https://nilcoalescing.com/blog/BuildingAdaptiveSwiftUILayoutsWithContainerRelativeFrame/) | Explains matching container dimensions, count-and-span sizing, and custom proportional sizing for resizable interfaces. |
| [<img src="https://livsycode.com/wp-content/uploads/2024/08/SocialMediaPostCover.png" width="160" alt="Swift continuous observation article preview">](https://livsycode.com/swift/withcontinuousobservation-in-swift/) | Josh | [withContinuousObservation in Swift](https://livsycode.com/swift/withcontinuousobservation-in-swift/) | Introduces iOS 27 continuous Observation tracking, including dependency discovery, token lifetime, actor isolation, and SwiftData use. |
| [<img src="https://i.ytimg.com/vi/656058JxTM0/hqdefault.jpg" width="160" alt="Cliff Stoll DEF CON talk preview">](https://www.youtube.com/watch?v=656058JxTM0) | Josh | [Stalking the Wily Hacker: 40 years later](https://www.youtube.com/watch?v=656058JxTM0) | Cliff Stoll revisits the Unix accounting anomaly that began his year-long pursuit of a network intruder. |
| [<img src="https://tanaschita.com/og/swiftui-alert-identifiable-data.png" width="160" alt="SwiftUI item-based alerts article preview">](https://tanaschita.com/swiftui-alert-identifiable-data/) | Josh | [Presenting alerts and confirmation dialogs from identifiable data in SwiftUI](https://tanaschita.com/swiftui-alert-identifiable-data/) | Explains the iOS 27 item-binding overloads that combine presentation state with the selected `Identifiable` value. |
| [<img src="https://cdn.mos.cms.futurecdn.net/fN8sCqbHysgzpTBxtJ5oXD-2000-80.jpg" width="160" alt="Apple M6 chip article preview">](https://www.tomsguide.com/computing/cpus/i-analyzed-apples-new-2nm-m6-chip-here-is-why-m1-holdouts-finally-need-to-upgrade) | Josh | [Why M1 holdouts may want to upgrade to Apple's M6 chip](https://www.tomsguide.com/computing/cpus/i-analyzed-apples-new-2nm-m6-chip-here-is-why-m1-holdouts-finally-need-to-upgrade) | Reviews the M6 CPU tiers, local-AI hardware, memory bandwidth, and which Mac generations stand to benefit most from upgrading. |

## 2026.08.22

### Discussion notes

- Peter followed up on the group's strict-concurrency migration issue. He found that `SwiftUI.View` is still marked `@preconcurrency`, so actor-isolation violations inside a view can be downgraded from errors to warnings even in Swift 6, while region-based isolation violations remain errors. Peter suspected SwiftUI's continuing dependency on pre-concurrency Combine APIs. Josh recommended keeping business logic out of SwiftUI's `.task` modifier because its work is scoped to view visibility rather than view-model lifetime; for sibling view models, he preferred a narrowly defined communication channel supplied by their parent.

```swift
import SwiftUI

class NonSendable { }

struct Sink {
    let sink: @Sendable () -> Void
}

struct SwiftUIView: View {
    @State private var toggle = false

    @State private var nonSendable: NonSendable

    init(_ ns: NonSendable) {
        _nonSendable = .init(wrappedValue: ns)
    }

    var body: some View {
        Text(/*@START_MENU_TOKEN@*/"Hello, World!"/*@END_MENU_TOKEN@*/)
            .task {
                /* Actor isolation errors are downgraded to a warning */
                // Main actor-isolated property 'toggle' can not be mutated from a Sendable closure
                let _ = Sink {
                    toggle.toggle()
                }

                /* Region isolation errors are not downgraded */
                // Sending 'nonSendable' risks causing data races
                 await trySend(ns: nonSendable)
            }
    }

    nonisolated func trySend(ns: NonSendable) async { }

}
```

- Josh revisited SIMD with [Simple Instructions, Weird Algorithms](https://www.youtube.com/watch?v=ryfbBB3pHfI), which applies SIMD to a brute-force, quadratic N-body simulation. He emphasized that vector instructions are only part of the optimization: data-oriented design can replace an array of particle objects with separate contiguous arrays for positions and velocities, reducing cache misses and making SIMD loads and stores more efficient. The group contrasted a CPU's dependency-limited instruction stream with a GPU's ability to hide memory latency by running many parallel operations.
- The [ContentBuilder Explained](https://fatbobman.com/en/posts/contentbuilder-explained) article expanded on the prior meeting's result-builder discussion. Decoupling content structure from leaf-type validation avoids the combinatorial overload search caused by deeply nested `ViewBuilder` containers and produces nearly constant type-checking time in the article's benchmarks. The tradeoff is that some expressions no longer resolve through view-specific overloads, so code may require a trailing closure, an explicit `EmptyView`, or a small convenience overload.
- Josh reviewed [Headless Xcode: From Prompt to Simulator with MCP](https://artemnovichkov.com/blog/headless-xcode-from-prompt-to-simulator-with-mcp). Xcode 27 can persist an agent's permission and expose build, preview-rendering, and simulator tools without keeping the IDE open. Josh noted that an MCP server and its tool descriptions consume model context on every request, so teams should enable it when capabilities such as rendering preview PNGs justify that cost.
- Josh then argued that many agent workflows can use Apple's [Xcode command-line tools](https://developer.apple.com/documentation/xcode/xcode-command-line-tool-reference?changes=_8,_8) without MCP. `simctl` controls simulators, `devicectl` controls registered physical devices, and `xcodebuild` builds, archives, and signs applications. The tools can install and launch apps, capture screens, inject notifications, override status bars and appearance, simulate locations and routes, and collect sysdiagnoses. Alex described older GUI/CLI signing discrepancies and AppCode's historical need to launch a hidden Xcode instance; Peter said his current CI and release pipeline runs entirely from the command line. Jake described orphaned simulator assets protected by System Integrity Protection that may require recovery or safe mode to remove.
- In [iOS 27: StateReporter](https://antongubarenko.substack.com/p/ios-27-statereporter), Josh highlighted the new StateReporting framework for attaching application state to MetricKit and Instruments diagnostics. Stable metadata identifies meaningful states for aggregation, while volatile metadata such as progress can change without fragmenting metrics into many distinct states. He recommended reporting human-scale interactions and transitions rather than per-frame updates.
- Josh presented the modern [DataDetector API](https://antongubarenko.substack.com/p/ios-26-data-detector), which replaces the awkward `NSString` and `NSRange` model of `NSDataDetector` with a Swift-native asynchronous sequence over `StringProtocol`. It returns `Range<String.Index>` values without copying substrings and can detect URLs, phone numbers, email addresses, dates, addresses, money, measurements, flights, shipment tracking numbers, and other semantic values.
- Josh reviewed [multi-step animations with `PhaseAnimator`](https://nilcoalescing.com/blog/PhaseAnimationsInSwiftUI/). Phase animation provides an idiomatic way to sequence semantic animation states, works with physics-based animations whose completion time is not predetermined, and respects the user's Reduce Motion setting.
- [The `@State` Macro: What Xcode 27 Stops Compiling](https://blakecrosley.com/blog/state-macro-xcode-27) covers source incompatibilities introduced when Xcode 27 replaces SwiftUI's `@State` property wrapper with a back-deployed macro. A property cannot both have a declaration-site default and be assigned in an initializer, and some previously synthesized memberwise initializers must now be written explicitly.
- Peter used Apple's [`DataDetector` documentation](https://developer.apple.com/documentation/datadetection/datadetector) to clarify that match kinds are extensible static members on a struct rather than exhaustive enum cases. Josh connected that design to Apple's preference for extensible static values and explained that a caseless enum is a cleaner namespace than an instantiable struct; a struct namespace should at least make its initializer private.
- Josh explored a reusable asynchronous action abstraction backed by Observation. Making the type and its extensions `nonisolated` fixed default-main-actor problems, but passing a `KeyPath` through the `@Sendable` closure required by `Observations.untilFinished` still produced a sendability error even when the value was `Sendable`. Peter noted that `untilFinished` requires iOS 26 or later. Josh concluded that a custom subject may be a cleaner implementation than forcing this abstraction through Observation.
- Josh introduced Swift macros by distinguishing attached `@` macros from freestanding `#` macros and the public declaration from the compiler-executed expansion implementation. Macro expansion should be deterministic; SwiftSyntax exposes the syntax tree, while `MacroExpansionContext` supplies source locations, diagnostics, and fix-its. The swift-syntax repository's [`ObservableMacro.swift`](https://github.com/swiftlang/swift-syntax/blob/main/Examples/Sources/MacroExamples/Implementation/ComplexMacros/ObservableMacro.swift) demonstrates a complex macro with member, member-attribute, and accessor roles, while its URL macro shows how compile-time validation can turn a failable runtime initializer into a checked literal. Ray recommended [Swift AST Explorer](https://swift-ast-explorer.com) for interactively mapping source text to syntax-tree nodes.
- The closing macro design exercise aimed to synchronize selected `@Observable` properties between macOS and iOS over Bonjour. Josh separated an `@Replicable` type macro from opt-in `@Replicated` property markers and initially reduced the network operation to an arbitrary side effect, making the macro contract testable before integrating Bonjour. He used an agent to explore the design but rejected suggestions that would replace or collide with `@Observable`; the remaining design questions include stable keys, deduplication, service injection, and whether replication represents singleton or per-instance state.

### Links shared

| Preview | Shared by | Link | Description |
|---|---|---|---|
| [<img src="https://i.ytimg.com/vi/ryfbBB3pHfI/hqdefault.jpg" width="160" alt="SIMD N-body simulation video preview">](https://www.youtube.com/watch?v=ryfbBB3pHfI) | Josh | [Simple Instructions, Weird Algorithms](https://www.youtube.com/watch?v=ryfbBB3pHfI) | Uses an N-body simulation to explain SIMD execution and the effect of memory layout on performance. |
| [<img src="https://og.fatbobman.com/card/contentbuilder-explained-en.webp" width="160" alt="SwiftUI ContentBuilder article preview">](https://fatbobman.com/en/posts/contentbuilder-explained) | Josh | [ContentBuilder Explained](https://fatbobman.com/en/posts/contentbuilder-explained) | Explains how SwiftUI's `ContentBuilder` separates construction from validation to improve type-checking performance, with benchmarks and source-compatibility tradeoffs. |
| [<img src="https://artemnovichkov.com/images/headless-xcode-from-prompt-to-simulator-with-mcp/cover.png" width="160" alt="Headless Xcode MCP article preview">](https://artemnovichkov.com/blog/headless-xcode-from-prompt-to-simulator-with-mcp) | Josh | [Headless Xcode: From Prompt to Simulator with MCP](https://artemnovichkov.com/blog/headless-xcode-from-prompt-to-simulator-with-mcp) | Demonstrates Xcode 27's headless MCP server, exported agent skills, preview rendering, and simulator-driven app verification. |
| [<img src="https://developer.apple.com/tutorials/developer-og.jpg" width="160" alt="Xcode command-line documentation preview">](https://developer.apple.com/documentation/xcode/xcode-command-line-tool-reference?changes=_8,_8) | Josh | [Xcode command-line tool reference](https://developer.apple.com/documentation/xcode/xcode-command-line-tool-reference?changes=_8,_8) | Apple's reference for command-line build, simulator, device, and development tools. |
| [<img src="https://substackcdn.com/image/fetch/$s_!DP84!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa29a9438-a03c-435f-8346-f5ab572ebb00_1254x1254.png" width="160" alt="iOS StateReporter article preview">](https://antongubarenko.substack.com/p/ios-27-statereporter) | Josh | [iOS 27: StateReporter](https://antongubarenko.substack.com/p/ios-27-statereporter) | Introduces StateReporting for correlating MetricKit and Instruments performance data with application states and structured metadata. |
| [<img src="https://substackcdn.com/image/fetch/$s_!AF0H!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F18ea23f1-39e0-44d3-b8ef-7f76ebafe415_1254x1254.png" width="160" alt="iOS DataDetector article preview">](https://antongubarenko.substack.com/p/ios-26-data-detector) | Josh | [iOS 26: DataDetector](https://antongubarenko.substack.com/p/ios-26-data-detector) | Shows the Swift-native asynchronous API for finding semantic values in strings. |
| [<img src="https://nilcoalescing.com/static/blog/PhaseAnimationsInSwiftUI/banner.8h9FjIJsPjECQw1m_E-RZKXNuM4JckoUOzclXW5hpl4.png" width="160" alt="SwiftUI PhaseAnimator article preview">](https://nilcoalescing.com/blog/PhaseAnimationsInSwiftUI/) | Josh | [Creating multi-step animations with PhaseAnimator in SwiftUI](https://nilcoalescing.com/blog/PhaseAnimationsInSwiftUI/) | Builds repeating and event-driven sequences from phase values and per-phase animation transitions. |
| [<img src="https://blakecrosley.com/og/blog/state-macro-xcode-27.png" width="160" alt="Xcode 27 State macro article preview">](https://blakecrosley.com/blog/state-macro-xcode-27) | Josh | [The `@State` Macro: What Xcode 27 Stops Compiling](https://blakecrosley.com/blog/state-macro-xcode-27) | Identifies two source patterns that stop compiling when Xcode 27 reimplements SwiftUI's `@State` as a macro. |
| [<img src="https://developer.apple.com/tutorials/developer-og.jpg" width="160" alt="DataDetector documentation preview">](https://developer.apple.com/documentation/datadetection/datadetector) | Peter | [`DataDetector`](https://developer.apple.com/documentation/datadetection/datadetector) | Apple's API documentation for the namespace and types used by the DataDetection framework. |
| No preview | Josh | [`ObservableMacro.swift`](https://github.com/swiftlang/swift-syntax/blob/main/Examples/Sources/MacroExamples/Implementation/ComplexMacros/ObservableMacro.swift) | SwiftSyntax's example implementation of a complex Observation macro with multiple attached-macro roles. |
| [<img src="https://swift-ast-explorer.com/images/ogp_image.png" width="160" alt="Swift AST Explorer preview">](https://swift-ast-explorer.com) | Ray | [Swift AST Explorer](https://swift-ast-explorer.com) | Visualizes Swift syntax trees and interactively highlights the node corresponding to selected source code. |

## 2026.08.15

### Discussion notes

- Ray shared the Swift project's [July 2026 edition of What's new in Swift](https://www.swift.org/blog/whats-new-in-swift-july-2026/), a curated digest of project and community releases, videos, and discussions. He also shared Apple's WWDC26 session [Build real-time apps and services with gRPC and Swift](https://www.youtube.com/watch?v=CCFxlFF9XRI). In a follow-up message, he referred to “Balancing High and Low-Level Programming in Swift” as the link he had wanted.
- Peter suggested that Ed use Xcode's command-line build tools from VS Code when he only needs to build; Ed noted that Xcode previews are still valuable. Chitaranjan then shared [a post about an Xcode mode for trusted AI agents](https://x.com/_julianschiavo/status/2086880132640428080?s=20) that can retain permissions and reduce repeated prompts.
- Ray shared the [updated Embedded Swift vision](https://forums.swift.org/t/updated-embedded-swift-vision/88931), which broadens the Swift features available to embedded programs while retaining a predictable implementation model.
- Peter recommended [Graphite](https://graphite.com) for stacked changes, then shared GitHub's documentation for [stacked pull requests](https://docs.github.com/en/pull-requests/how-tos/stacked-pull-requests). Josh next shared a [size comparison for the proposed TerraFab AI infrastructure project](https://www.facebook.com/evtopcars/posts/a-new-size-comparison-shows-just-how-ambitious-terafab-could-be-the-proposed-ai-/1040558538897812/), and Peter followed with the open-source [git-spice](https://abhinav.github.io/git-spice/) branch-stacking tool.
- Josh shared [Claude Now Watermarks Its Text. How Do You Even Do That?](https://www.youtube.com/watch?v=3FhxdhVMJoU), and Georgi followed with Google DeepMind's [SynthID](https://deepmind.google/models/synthid/) tools for watermarking and identifying AI-generated content.
- Josh shared Antoine van der Lee's [`@preconcurrency`: Incremental migration to concurrency checking](https://www.avanderlee.com/concurrency/preconcurrency-checking-swift/), which presents the attribute as a temporary way to suppress `Sendable`-related diagnostics from imported modules during migration.
- Ray shared Daring Fireball's [critique of Anthropic's explanation of Claude's text watermarking](https://daringfireball.net/linked/2026/08/11/anthropic-claude-watermarks).
- Josh introduced [How to stream SSE with URLSession in Swift](https://onmyway133.com/posts/how-to-stream-sse-with-urlsession-in-swift/). Carlyn shared the [`SSEListener.swift` implementation from APItizer](https://github.com/carlynorama/APItizer/blob/main/Sources/APItizer/SSEListener.swift) that she had experimented with previously.
- Josh shared [Controlling Orphans in SwiftUI Text](https://fatbobman.com/en/posts/controlling-orphans-in-swiftui-text/), which examines SwiftUI's automatic avoidance of orphaned final words and an undocumented `avoidsOrphans` environment value for controlling that behavior.
- Josh shared [Type-safe and user-friendly error handling in Swift 6](https://theswiftdev.com/type-safe-and-user-friendly-error-handling-in-swift-6/) and posted a helper that transforms a typed error by routing the operation through `Result.mapError`:

### Type throws require annoations
```swift
func mapError<Value, Failure: Error, TransformedFailure: Error>(
        _ operation: @autoclosure () throws(Failure) -> Value,
        transFormError: (Failure) -> TransformedFailure
    ) throws(TransformedFailure) -> Value {
        try Result { () throws(Failure) -> Value in
            try operation()
        }
        .mapError(transFormError)
        .get()
    }
```

- Here the do block must have thee throws annotation

```swift
enum Completion<Failure: Error> {
    case finished, cancelled, error(Failure)
}

nonisolated extension AsyncSequence {
    func subscribe(
        isolation: isolated (any Actor)? = #isolation,
        onComplete: @escaping (Completion<Failure>) -> Void,
        _ perform: @escaping (Element) async -> Void
    ) -> Task<Void, Never> {
        Task {
            _ = isolation
            do throws(Failure) {
                for try await element in self {
                    guard !Task.isCancelled else { return onComplete(.cancelled) }
                    await perform(element)
                }
                onComplete(.finished)
            } catch {
                onComplete(.error(error))
            }
        }
    }
}
```

- Josh closed by sharing Apple's [AccessorySetupKit documentation](https://developer.apple.com/documentation/accessorysetupkit/), which covers privacy-preserving discovery and configuration of accessories.

### Links shared

| Preview | Shared by | Link | Description |
|---|---|---|---|
| No preview | Ray | [What's new in Swift: July 2026 Edition](https://www.swift.org/blog/whats-new-in-swift-july-2026/) | Swift.org's curated digest of releases, videos, and discussions from the Swift project and community. |
| [<img src="https://i.ytimg.com/vi/CCFxlFF9XRI/hqdefault.jpg" width="160" alt="WWDC26 gRPC and Swift video preview">](https://www.youtube.com/watch?v=CCFxlFF9XRI) | Ray | [WWDC26: Build real-time apps and services with gRPC and Swift](https://www.youtube.com/watch?v=CCFxlFF9XRI) | Apple Developer session about building real-time apps and services with gRPC and Swift. |
| No preview | Chitaranjan | [Xcode mode for trusted AI agents](https://x.com/_julianschiavo/status/2086880132640428080?s=20) | Post about allowing trusted AI agents to work in Xcode without repeatedly requesting the same permissions. |
| [<img src="https://global.discourse-cdn.com/swift/original/1X/0a90dde98a223f5841eeca49d89dc9f57592e8d6.png" width="160" alt="Swift Forums preview">](https://forums.swift.org/t/updated-embedded-swift-vision/88931) | Ray | [Updated Embedded Swift vision](https://forums.swift.org/t/updated-embedded-swift-vision/88931) | Forum post describing a shift toward supporting more Swift features in Embedded Swift while preserving a predictable implementation model. |
| [<img src="https://staging-graphite-splash.vercel.app/og.png" width="160" alt="Graphite code review preview">](https://graphite.com) | Peter | [Graphite](https://graphite.com) | Code-review tooling for GitHub that includes workflows for stacked changes. |
| [<img src="https://docs.github.com/assets/cb-345/images/social-cards/pull-requests.png" width="160" alt="GitHub stacked pull requests preview">](https://docs.github.com/en/pull-requests/how-tos/stacked-pull-requests) | Peter | [Stacked pull requests](https://docs.github.com/en/pull-requests/how-tos/stacked-pull-requests) | GitHub's guide to breaking a large change into a chain of smaller dependent pull requests that can be reviewed and merged independently. |
| No preview | Josh | [TerraFab size comparison](https://www.facebook.com/evtopcars/posts/a-new-size-comparison-shows-just-how-ambitious-terafab-could-be-the-proposed-ai-/1040558538897812/) | Facebook post comparing the scale of the proposed TerraFab AI infrastructure project. |
| [<img src="https://abhinav.github.io/git-spice/assets/images/social/index.png" width="160" alt="git-spice preview">](https://abhinav.github.io/git-spice/) | Peter | [git-spice](https://abhinav.github.io/git-spice/) | Open-source tool for managing and navigating stacks of Git branches. |
| [<img src="https://i.ytimg.com/vi/3FhxdhVMJoU/hqdefault.jpg" width="160" alt="Claude text watermarking video preview">](https://www.youtube.com/watch?v=3FhxdhVMJoU) | Josh | [Claude Now Watermarks Its Text. How Do You Even Do That?](https://www.youtube.com/watch?v=3FhxdhVMJoU) | Video examining Claude's text watermarking and how text produced by a model might be identified. |
| No preview | Georgi | [SynthID](https://deepmind.google/models/synthid/) | Google DeepMind's technology for watermarking and identifying AI-generated content. |
| [<img src="https://swiftlee-banners.herokuapp.com/imagegenerator.php?title=%40preconcurrency%3A+Incremental+migration+to+concurrency+checking" width="160" alt="Swift preconcurrency article preview">](https://www.avanderlee.com/concurrency/preconcurrency-checking-swift/) | Josh | [`@preconcurrency`: Incremental migration to concurrency checking](https://www.avanderlee.com/concurrency/preconcurrency-checking-swift/) | Explains how `@preconcurrency` temporarily suppresses `Sendable`-related diagnostics from imported modules during migration. |
| No preview | Ray | [Anthropic Posts “How Claude Marks AI-Generated Content” Without Explaining How Claude Marks AI-Generated Content](https://daringfireball.net/linked/2026/08/11/anthropic-claude-watermarks) | Daring Fireball's criticism of Anthropic's explanation of Claude's text watermarking. |
| No preview | Josh | [How to stream SSE with URLSession in Swift](https://onmyway133.com/posts/how-to-stream-sse-with-urlsession-in-swift/) | Shows how to consume Server-Sent Events as a continuous unidirectional HTTP stream using `URLSession` and Swift concurrency. |
| [<img src="https://opengraph.githubassets.com/81ff94a9fa764d5be1a95e12b5e67cf3a632b36439354804a131f561da126ac1/carlynorama/APItizer" width="160" alt="APItizer SSEListener preview">](https://github.com/carlynorama/APItizer/blob/main/Sources/APItizer/SSEListener.swift) | Carlyn | [`SSEListener.swift`](https://github.com/carlynorama/APItizer/blob/main/Sources/APItizer/SSEListener.swift) | Carlyn's earlier implementation of an SSE listener in the APItizer package. |
| [<img src="https://og.fatbobman.com/card/controlling-orphans-in-swiftui-text-en.webp" width="160" alt="SwiftUI text orphan control preview">](https://fatbobman.com/en/posts/controlling-orphans-in-swiftui-text/) | Josh | [Controlling Orphans in SwiftUI Text](https://fatbobman.com/en/posts/controlling-orphans-in-swiftui-text/) | Investigates SwiftUI's automatic orphan avoidance and the undocumented `avoidsOrphans` environment value. |
| [<img src="https://opengraph.githubassets.com/0bee092eb185c9e96351cadb0cafcb9172d7c61ce003441271f6c38fafc97c18/launchdarkly/swift-eventsource" width="160" alt="LaunchDarkly Swift EventSource preview">](https://github.com/launchdarkly/swift-eventsource) | Peter | [swift-eventsource](https://github.com/launchdarkly/swift-eventsource) | LaunchDarkly's Server-Sent Events client for iOS, macOS, tvOS, and watchOS. |
| No preview | Josh | [Type-safe and user-friendly error handling in Swift 6](https://theswiftdev.com/type-safe-and-user-friendly-error-handling-in-swift-6/) | Discusses typed error handling, structured diagnostics, and a hierarchical error model in Swift 6. |
| No preview | Peter | [Error Handling](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/errorhandling/) | The Swift Programming Language chapter covering error representation, propagation, handling, and assertions. |
| [<img src="https://developer.apple.com/tutorials/developer-og.jpg" width="160" alt="AccessorySetupKit documentation preview">](https://developer.apple.com/documentation/accessorysetupkit/) | Josh | [AccessorySetupKit](https://developer.apple.com/documentation/accessorysetupkit/) | Apple's framework for privacy-preserving discovery and configuration of accessories. |

## 2026.08.08

### Discussion notes

- Peter described a mixed-language-mode workspace in which a Swift 6 package produced some stricter concurrency diagnostics during migration but did not behave as expected inside a Swift 5 project. Josh recommended reproducing the setup in a minimal clean-room project and comparing its project, package, and feature settings with the real workspace. Josh also shared `-print-diagnostic-groups` for identifying a warning's group and `-Xfrontend -suppress-warning-group=GroupName` for suppressing one group when necessary.
- Josh demonstrated a weekly automation that scans the [Swift Evolution proposals](https://github.com/swiftlang/swift-evolution/tree/main/proposals), detects changes, follows linked forum discussions, and explains both what changed and why. The report surfaced accepted work involving file-wide defaults, backtraces, advanced Observation tracking, uniquely owned and fixed-size arrays, macro access to `self`, package-wide target defaults, source-location macros, and borrowing iteration over spans. Josh suggested turning the accumulated Markdown reports into a searchable and filterable site.
- Josh used [SE-0533](https://forums.swift.org/t/se-0533-generating-synchronous-overloads-of-async-functions-with-a-macro/87019) to show how an agent can summarize a long review thread and then produce concrete counterexamples. The proposal was rejected because a macro cannot always generate a valid synchronous overload when the body contains unrelated asynchronous work, actor hops, asynchronous sequence iteration, or sendability constraints. The functionality can still be implemented in a separate package, although Josh preferred a language-level `reasync` feature parallel to `rethrows`.
- In the article about AMD acquiring Taalas, Josh focused on model-specific chips that encode weights in silicon and demonstrated roughly 17,000 tokens per second. The fixed model sacrifices flexibility for throughput, but Josh suggested that the tradeoff could suit stable on-device tasks such as Siri and App Intents, with harder requests routed to cloud models.
- Peter, Ray, Juan, Mark, and Josh discussed file-wide isolation defaults and Approachable Concurrency. Source annotations can make build settings less important, but they also make isolation harder to infer from a local diff and can surprise developers when code moves between files or modules. The group recommended consistent project conventions, agent-assisted isolation checks, and better Xcode tooling that visibly reports a declaration's effective isolation.
- Josh introduced Mihaela's Apple UI Insider newsletter and its comparison of a clean-room renderer with Core Graphics, Core Text, Core Image, Core Animation, and SwiftUI. The paired results show where rendering differences emerge from compositing and antialiasing choices and include matching animation examples.
- Josh explained that the Xcode 27 `@ContentBuilder` is a type alias for `ViewBuilder` whose new variadic-generic `buildBlock` overload no longer requires every content value to conform to `View`. This enables non-view DSLs such as the article's type-safe deep-link router. He cautioned that adopting it also means supporting SwiftUI container types such as conditional content and `ForEach`; a custom result builder may be simpler and can support ordinary `for` loops.
- The Approachable Concurrency article prompted a review of how nonisolated async functions execute before and after `NonisolatedNonsendingByDefault`, and how `@concurrent` opts back into the global executor. Peter shared the meeting notes' [concurrency reference table](https://github.com/aflockofswifts/meetings#concurrency) for comparing the old and new rules.
- Josh reviewed StructuredQueries support for SQLite JSON and JSONB. He recommended strongly typed database columns for application data, but identified debug logging as a good use for JSONB: an app can persist complete network request and response bodies, and an agent can query them during diagnosis. Alex warned about cross-process writes from extensions; Josh preferred SQLite for debug builds and `OSLog`/`OSLogStore` for production reliability and privacy.
- The Liquid Glass compatibility article cataloged UIKit failures involving bar-button badges, incorrect glass colors, tab-bar mutations during dismissal, and segmented controls. Some workarounds require bridging a SwiftUI view into UIKit or substituting the other framework's component, so Josh recommended testing across OS versions and retaining these techniques for unresolved framework bugs.
- Josh described the lock-backed custom `SerialExecutor` article as educational but unsafe as written. Its recursive lock runs work inline on the current cooperative-pool thread; holding that lock across a suspension point can prevent forward progress and starve or deadlock the pool, especially on devices with few cores. For protected synchronous state he recommended `Mutex`, whose closure cannot suspend; CPU-heavy work should periodically yield or move to a dedicated thread, dispatch queue, or custom executor.
- The executor discussion distinguished Swift's cooperative tasks and executors from preemptively scheduled operating-system threads. An executor is a logical queue of work and does not map one-to-one to a thread; the runtime commonly maintains a pool sized near the available cores, while the OS can suspend and resume its underlying threads independently.
- Josh paired [Everyone Should Know SIMD](https://mitchellh.com/writing/everyone-should-know-simd) with [People Are Mad They're Told to Learn](https://www.youtube.com/watch?v=4nJ2tEPD4-k) and argued that developers should at least recognize the available forms of vector computing. Swift's built-in SIMD types perform lane-wise CPU operations; the SIMD module adds linear-algebra operations, Accelerate provides buffer-oriented routines such as vDSP, MLX targets GPU-based machine-learning workloads, and Core ML can use the Neural Engine.
- The [Halftone Performance project](https://github.com/aflockofswifts/Halftone-Performance) compared scalar, SIMD, and Accelerate implementations of the same animated dot field. The benchmark used warmups, rotated execution order, and 21 measured rounds; SIMD reduced the calculation from about 71 ms to 23 ms, while Accelerate was only modestly faster and substantially less readable. Because even 23 ms exceeds the 16.7 ms budget for 60 fps and the 8.3 ms budget for 120 fps before rendering, Josh recommended a GPU shader for production. Mark proposed caching precomputed frames, with the tradeoff of memory use and recomputation stalls after interactive changes.

### Links shared

| Preview | Shared by | Link | Description |
|---|---|---|---|
| [<img src="https://miro.medium.com/v2/resize:fit:1200/1*CJ6nMLzbUWQLSS_r7Hik6A.png" width="160" alt="Lock-backed Swift serial executor preview">](https://soumyamahunt.medium.com/stop-using-unchecked-sendable-2e00bd6cb122) | Josh | [Stop using `@unchecked Sendable`](https://soumyamahunt.medium.com/stop-using-unchecked-sendable-2e00bd6cb122) | Demonstrates a custom `SerialExecutor` built on a recursive lock. The group treated it as an instructive executor example but warned that running inline and locking across suspension points can violate Swift Concurrency's forward-progress contract. |
| No preview | Josh | [Chrome: What's New](chrome://whats-new/) | Chrome's internal release-highlights page. This browser-only link is not accessible as a public web page. |
| No preview | Josh | [Everyone Should Know SIMD](https://mitchellh.com/writing/everyone-should-know-simd) | Presents a reusable five-step SIMD pattern: broadcast constants, process vector-width chunks, perform parallel operations, reduce or store the result, and finish with a scalar tail. A Ghostty example demonstrates the approach in Zig. |
| [<img src="https://i.ytimg.com/vi/4nJ2tEPD4-k/hqdefault.jpg" width="160" alt="People Are Mad They're Told to Learn video preview">](https://www.youtube.com/watch?v=4nJ2tEPD4-k) | Josh | [People Are Mad They're Told to Learn](https://www.youtube.com/watch?v=4nJ2tEPD4-k) | The PrimeTime commentary responding to debate around Mitchell's argument that developers should understand basic SIMD concepts. |
| [<img src="https://og.fatbobman.com/card/liquid-glass-a-field-guide-to-uikit-compatibility-pitfalls-en.webp" width="160" alt="Liquid Glass UIKit compatibility preview">](https://fatbobman.com/en/posts/liquid-glass-a-field-guide-to-uikit-compatibility-pitfalls/) | Josh | [Liquid Glass: A Field Guide to UIKit Compatibility Pitfalls](https://fatbobman.com/en/posts/liquid-glass-a-field-guide-to-uikit-compatibility-pitfalls/) | Catalogs Liquid Glass compatibility problems and workarounds involving `UIBarButtonItem`, `UITabBarController`, `WKWebView`, and steppers across iOS 26 and iOS 27. |
| [<img src="https://imagedelivery.net/6_EEbfI_pxOPJCtc6OUKCg/f98e9205-4e50-482b-9ccc-0f246a987c00/public" width="160" alt="StructuredQueries JSON support preview">](https://www.pointfree.co/blog/posts/220-type-safe-json-and-jsonb-in-structuredqueries) | Josh | [Type-safe JSON and JSONB in StructuredQueries](https://www.pointfree.co/blog/posts/220-type-safe-json-and-jsonb-in-structuredqueries) | Introduces StructuredQueries 0.35.0 support for storing and querying SQLite JSON and JSONB with schema-safe functions, including the `json_each` table-valued function. |
| [<img src="https://nsvasilev.com/posts/demystifying-thread-hopping-with-swift-6-2-approachable-concurrency.png" width="160" alt="Swift approachable concurrency preview">](https://www.nsvasilev.com/posts/approachable_concurrency/) | Josh | [Demystifying Thread Hopping with Swift 6.2 Approachable Concurrency](https://www.nsvasilev.com/posts/approachable_concurrency/) | Explains how `NonisolatedNonsendingByDefault` changes the execution of nonisolated async functions, how `@concurrent` opts into the global executor, and what the resulting execution chain looks like. |
| [<img src="https://artemnovichkov.com/images/using-swiftui-contentbuilder-with-non-view-types/cover.png" width="160" alt="SwiftUI ContentBuilder router preview">](https://artemnovichkov.com/blog/using-swiftui-contentbuilder-with-non-view-types) | Josh | [Using SwiftUI's ContentBuilder with Non-View Types](https://artemnovichkov.com/blog/using-swiftui-contentbuilder-with-non-view-types) | Uses Xcode 27's expanded `@ContentBuilder` to assemble a type-safe deep-link router from non-`View` values, then recreates the syntax for deployment targets as old as iOS 17. |
| [<img src="https://appleuiinsider.com/images/issue-01/apple-ui-stack-hero-slm.png" width="160" alt="Apple UI rendering stack preview">](https://appleuiinsider.com/issues/the-map-drawn-twice/) | Josh | [Issue 1: The Map, Drawn Twice](https://appleuiinsider.com/issues/the-map-drawn-twice/) | Maps the responsibilities of Core Graphics, Core Text, Core Image, Core Animation, and SwiftUI by rendering the same scenes through a clean-room engine and Apple's frameworks. |
| [<img src="https://substackcdn.com/image/fetch/$s_!FSby!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67a15605-b600-4aa7-8634-9c4a39bdd877_1672x941.png" width="160" alt="Gemini and Google Cloud analysis preview">](https://newsletter.semianalysis.com/p/gemini-is-cooked-but-gcp-is-cooking) | Josh | [Gemini is Cooked but GCP is Cooking](https://newsletter.semianalysis.com/p/gemini-is-cooked-but-gcp-is-cooking) | Argues that leadership changes and researcher departures have weakened DeepMind's frontier-model prospects while freeing Google Cloud to direct more compute toward external customers and TPU sales. |
| [<img src="https://image.theregister.com/5284365.jpg" width="160" alt="AMD and Taalas AI accelerator preview">](https://www.theregister.com/systems/2026/08/06/amd-acquires-ai-chip-startup-taalas-to-boost-inference-performance-by-etching-models-into-silicon/5284344) | Josh | [AMD acquires AI chip startup Taalas to boost inference performance by etching models into silicon](https://www.theregister.com/systems/2026/08/06/amd-acquires-ai-chip-startup-taalas-to-boost-inference-performance-by-etching-models-into-silicon/5284344) | Reports on AMD's acquisition of Taalas, whose model-specific chips place weights directly in silicon for very high inference throughput at the cost of needing a chip respin for substantial model changes. |
| [<img src="https://global.discourse-cdn.com/swift/original/1X/0a90dde98a223f5841eeca49d89dc9f57592e8d6.png" width="160" alt="Swift Forums preview">](https://forums.swift.org/t/se-0533-generating-synchronous-overloads-of-async-functions-with-a-macro/87019) | Josh | [SE-0533: Generating synchronous overloads of async functions with a macro](https://forums.swift.org/t/se-0533-generating-synchronous-overloads-of-async-functions-with-a-macro/87019) | Review thread for the rejected proposal to have an attached macro synthesize synchronous overloads of asynchronous Swift functions. |
| No preview | Josh | [Swift Evolution proposals](https://github.com/swiftlang/swift-evolution/tree/main/proposals) | Source repository used by Josh's weekly automation to identify proposal changes and follow their motivation through linked reviews and discussions. |
| No preview | Peter | [Concurrency reference table](https://github.com/aflockofswifts/meetings#concurrency) | Meeting-notes reference comparing Swift concurrency execution behavior under the relevant isolation and language-mode settings. |
| No preview | Josh | [Halftone Performance](https://github.com/aflockofswifts/Halftone-Performance) | Sample project and benchmark comparing scalar, SIMD, and Accelerate implementations of an animated halftone dot field. |

## 2026.08.01

### Discussion notes

- Allen described using Claude and ChatGPT to organize decades of archived files into a book, identify themes, and draft an index and summaries. Josh recommended the Codex desktop app for work that needs to read and create many local files. Ray suggested using an LLM for research and organization while keeping the finished prose in Allen's own voice, and shared iA Writer's authorship annotations for distinguishing human- and AI-written text.
- Josh followed up on Allen's pendulum project with [Why Perfect Math Still Can't Predict the Future](https://www.youtube.com/watch?v=f0YubvdhQnU). The video uses double pendulums to show how tiny differences in initial conditions produce chaotic divergence, then maps crossing time against the two starting angles to reveal a fractal boundary. Allen connected the visualization to his earlier Mandelbrot work, Conway's Game of Life, and array-processor simulations.
- In [VFX Artists React to Bad & Great CGi 235](https://www.youtube.com/watch?v=Wf0i1dmxrNg), Josh highlighted John Whitney's use of a mechanical anti-aircraft computer to create the title animation for *Vertigo*. The example prompted discussion of analog computation, slide rules, and the long history of computer graphics before programmable digital hardware.
- Josh used [Training Sand to Think: Artificial General Intelligence & Future of Physics](https://www.youtube.com/watch?v=Mw60FH5iflI) to discuss scaling and power laws in AI. His takeaway was that exponential trends can look slow initially and then accelerate sharply, making recent progress in mathematical and scientific reasoning relevant to forecasts of future capability.
- In [Architecture, AI agents, and product empathy with Robert C. Martin](https://www.youtube.com/watch?v=RxxxGkFIUJ0), Josh highlighted the argument that agentic development moves programmers up another abstraction layer, from writing code toward architecture and module boundaries, while still requiring knowledge of the layer below. The group also discussed the recommendation that beginners first learn programming fundamentals without agents before treating them as power tools.
- The same interview introduced the [Change Risk Anti-Patterns score](https://testing.googleblog.com/2011/02/this-code-is-crap.html), which combines cyclomatic complexity and test coverage to estimate change risk. Josh suggested that agents could score and rewrite overly complex functions and noted an opportunity for a Swift tool built on the Swift AST. Juan and Ray pointed out that the metric does not account for side effects or shared mutable state, which can make a function difficult to reason about even when its control flow is simple.
- Josh walked through [Blend modes in SwiftUI](https://nilcoalescing.com/blog/BlendModesInSwiftUI/). Color modes such as `multiply`, `screen`, `hue`, and `color` combine pixel channels, while Porter-Duff modes such as `sourceAtop` and `destinationOut` can use alpha as a pixel-level mask or eraser. `compositingGroup()` creates the boundary that limits which previously rendered views participate in a blend.
- Juan described using blend modes to compose arbitrary SF Symbols into new icons at runtime. Josh showed an interactive sample app that an agent generated from the article in a few minutes, with adjustable layers, explanations, and source code, as an example of using small generated tools to learn an API. He noted that custom SwiftUI shaders can go beyond the framework's fixed blend operations, although their implementation is still written in Metal.
- In [Keeping SwiftData behind a boundary](https://tanaschita.com/swiftdata-persistence-boundaries/), Josh recommended isolating SwiftData or Core Data in a persistence module and exposing plain, `Sendable` value types to the rest of the app. This keeps views and view models testable and makes it easier to substitute in-memory, file, cloud, or other database implementations. Ray compared the approach with Point-Free's SQLiteData; the group agreed that direct queries in views can be reasonable for small apps but scale poorly across larger codebases and teams.
- [Markdown links can do what?](https://jacobzivandesign.com/technology/links_in_swiftui_markdown_do_what/) prompted a review of SwiftUI's `openURL` environment value. Replacing the local handler lets an app route internal links, record analytics, or decline handling so the system can open the URL. Josh clarified for Juan that this is an action handler, not network middleware like `URLProtocol`, and recommended logging network traffic in debug builds so coding agents can inspect request failures and payloads directly.
- Josh reviewed [iOS 27: UIBarMinimization](https://antongubarenko.substack.com/p/ios-27-uibarminimization), which covers SwiftUI and UIKit APIs for collapsing Liquid Glass tab bars while the user scrolls through content and restoring them when the scroll direction reverses.
- Josh used [How to free up Xcode disk space safely with an AI Agent](https://www.avanderlee.com/ai-development/how-to-free-up-xcode-disk-space-safely-with-an-ai-agent/) as a caution about installing narrowly scoped agent skills without evaluating the actual workflow. A useful cleanup skill may need to understand Xcode, Bazel and Android caches, active Git worktrees, corporate storage policy, and recoverability. He recommended periodically auditing installed skills, removing unused context, recording failures, and updating personal skills when a workaround becomes repeatable.
- Josh explained [SE-0538: `Disconnected`](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0538-disconnected.md) by contrasting it with `Sendable` and `sending`. `Sendable` is a property of a type, while `sending` applies at a function boundary when region-based isolation proves that a particular value has no other reachable references. A `Disconnected<Value>` preserves that guarantee while the value is stored in a collection or actor; consuming `take()` later produces a `sending` value that can cross an isolation boundary. Ray connected the terminology to the disconnected regions introduced by [SE-0414: Region based isolation](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0414-region-based-isolation.md).
- Josh encouraged using agents to explain proposals from a specific point of confusion and proposed a recurring skill that summarizes new Swift Evolution activity. Juan questioned the name `Disconnected`; Ray noted its precedent in region-based isolation, where a value is disconnected from every isolation domain.
- To illustrate why technical claims should be tested rather than repeated, Josh built a small SwiftUI experiment around a task that weakly captures `self` and then awaits an instance method. The weak capture does not prevent the async instance method from retaining `self` for its full duration because `self` is an implicit, strongly held argument to every instance method. This can delay `deinit` and therefore delay cancellation initiated from `deinit`.
- Josh's preferred fix was to avoid an async instance method when the work does not use instance state: keep the task body local or move the operation to a static or free function, retain only the cancellation operation that is needed, and make custom long-running work check cancellation. Frank noted that system suspension points such as `Task.sleep` already throw when cancelled. The closing discussion distinguished overridable, dynamically dispatched `class` methods from non-overridable `static` methods and favored composition over inheritance for most application business logic.
```swift
import SwiftUI
import Playgrounds
import Combine

@main struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

struct ContentView: View {
    var body: some View {
        NavigationStack {
            NavigationLink("Push me") { DetailView() }
        }
        .frame(width: 400, height: 400, alignment: .center)
    }
}

struct DetailView: View {
    @StateObject var viewModel = ViewModel()
    var body: some View {
        Text("Hello, world!")
            .padding()
    }
}

@Observable
final class ViewModel: ObservableObject {
    var subscription: AnyCancellable?
    init() {
        let id = String(describing: ObjectIdentifier(self)).suffix(4)
        print("\(id) \(#function)")
        subscription = .init(Task { [weak self] in
            try Task.checkCancellation()
            await self?.instanceMethod()
        }.cancel)
    }
    isolated deinit {
        let id = String(describing: ObjectIdentifier(self)).suffix(4)
        subscription?.cancel()
        print("\(id) \(#function)")
    }
    func instanceMethod() async {
        do {
            try await Task.sleep(for: .seconds(10))
        } catch {
            let id = String(describing: ObjectIdentifier(self)).suffix(4)
            print("\(id) \(error.localizedDescription)")
        }
    }
}
```

### Links discussed

| Preview | Shared by | Link | Description |
|---|---|---|---|
| No preview | Ray | [Authorship in iA Writer](https://ia.net/writer/support/editor/authorship) | Explains how iA Writer records and displays the origin of text, including passages written by a person, pasted from elsewhere, or generated with AI. |
| [<img src="https://i.ytimg.com/vi/f0YubvdhQnU/hqdefault.jpg" width="160" alt="Double-pendulum chaos video preview">](https://www.youtube.com/watch?v=f0YubvdhQnU) | Josh | [Why Perfect Math Still Can't Predict the Future](https://www.youtube.com/watch?v=f0YubvdhQnU) | Visualizes sensitive dependence on initial conditions in double-pendulum systems, including the fractal structure of crossing-time maps. |
| [<img src="https://i.ytimg.com/vi/Wf0i1dmxrNg/hqdefault.jpg" width="160" alt="VFX artists video preview">](https://www.youtube.com/watch?v=Wf0i1dmxrNg) | Josh | [VFX Artists React to Bad & Great CGi 235](https://www.youtube.com/watch?v=Wf0i1dmxrNg) | Includes a segment on John Whitney's mechanical-computer animation for the title sequence of *Vertigo*. |
| [<img src="https://i.ytimg.com/vi/Mw60FH5iflI/hqdefault.jpg" width="160" alt="AI and physics lecture preview">](https://www.youtube.com/watch?v=Mw60FH5iflI) | Josh | [Training Sand to Think: Artificial General Intelligence & Future of Physics](https://www.youtube.com/watch?v=Mw60FH5iflI) | A Perimeter Institute lecture connecting AI scaling trends with mathematical reasoning, scientific discovery, and the future of physics. |
| [<img src="https://i.ytimg.com/vi/RxxxGkFIUJ0/hqdefault.jpg" width="160" alt="Robert Martin interview preview">](https://www.youtube.com/watch?v=RxxxGkFIUJ0) | Josh | [Architecture, AI agents, and product empathy with Robert C. Martin](https://www.youtube.com/watch?v=RxxxGkFIUJ0) | Interview about programming abstraction levels, architecture, agentic development, education, and maintaining technical judgment. |
| No preview | Josh | [This Code is CRAP](https://testing.googleblog.com/2011/02/this-code-is-crap.html) | Introduces the Change Risk Anti-Patterns score derived from cyclomatic complexity and automated-test coverage. |
| No preview | Josh | [Blend modes in SwiftUI](https://nilcoalescing.com/blog/BlendModesInSwiftUI/) | Explains SwiftUI's color and Porter-Duff blend modes and how `compositingGroup()` limits their rendering scope. |
| No preview | Josh | [Keeping SwiftData behind a boundary](https://tanaschita.com/swiftdata-persistence-boundaries/) | Demonstrates separating persistence implementation details from domain models and application code. |
| No preview | Josh | [Markdown links can do what?](https://jacobzivandesign.com/technology/links_in_swiftui_markdown_do_what/) | Shows how SwiftUI Markdown links interact with the `openURL` environment action and custom link handling. |
| No preview | Josh | [iOS 27: UIBarMinimization](https://antongubarenko.substack.com/p/ios-27-uibarminimization) | Covers the APIs and behaviors for minimizing tab bars as content scrolls. |
| No preview | Josh | [How to free up Xcode disk space safely with an AI Agent](https://www.avanderlee.com/ai-development/how-to-free-up-xcode-disk-space-safely-with-an-ai-agent/) | Presents an agent skill for identifying and safely reclaiming space used by Xcode artifacts. |
| No preview | Josh | [SE-0538: `Disconnected`](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0538-disconnected.md) | Proposes a wrapper that preserves a value's disconnected isolation region through storage and later yields the value as `sending`. |
| No preview | Josh | [SE-0414: Region based isolation](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0414-region-based-isolation.md) | Defines compiler analysis for safely transferring non-`Sendable` values between isolation domains when their regions are disconnected. |

## 2026.07.25

### Discussion notes

- Allen showed a pendulum simulation and asked how to diagnose its slowdown. Josh suggested adding performance logs, having an agent run the app and analyze the logs for bottlenecks, fixing the command-line build so the agent can work independently, and saving a long build procedure as a reusable skill. For a SwiftUI implementation made from many separate `Path` values, Josh suggested testing `drawingGroup()` to reduce the number of rendered layers. Mark proposed adding the Coriolis effect so the simulation could show how changing Earth's rotation affects the pendulums.
- Mihaela shared [SwiftUI After 7 Years: A Story of Mediocrity](https://www.youtube.com/watch?v=3XaHHFOZeJg) and argued that SwiftUI should be treated as one tool in Apple's larger UI palette rather than a replacement for UIKit, AppKit, Core Animation, SceneKit, or SpriteKit. She described using Core Animation directly for custom editor and pivot-grid interfaces that would have been harder to build in higher-level frameworks.
- Josh agreed that the video raises valid concerns about SwiftUI's source-of-truth model, navigation and animation bugs, backward-compatibility differences, collection performance, and uneven cross-platform behavior. His recommendation was to start with SwiftUI where it fits, measure the result, and bridge to UIKit or AppKit for the parts where performance or control matters.
- Peter noted that the Apple Wallet team was reportedly still using Objective-C within the last few years. Josh added that Apple's framework APIs do not always share one style or architecture because the company is composed of teams working with different constraints and histories.
- Josh walked through [Building adaptive non-modal panels in SwiftUI](https://nilcoalescing.com/blog/BuildingAdaptiveNonModalPanelsInSwiftUI/). The panel API mirrors native SwiftUI conventions with presentation bindings, detents, and selection, illustrating why reusable components should use familiar names, contracts, and composable modifiers even if that public shape is refined only after the feature works.
- The panel implementation prompted discussion of injecting scene geometry through the environment, using a custom `Layout` to reconcile content size with detents, caching layout work, and combining panel dragging with content gestures. Peter warned that frequently changing environment values can invalidate large descendant subtrees; Josh recommended avoiding that pattern in hot or repeated content and measuring before deciding whether UIKit is a better fit.
- Josh noted that `UIGestureRecognizerRepresentable` is available when SwiftUI gesture composition is not sufficient. For Apple Maps-style panels whose controls move, fade, or blur interactively with a drag, he said UIKit may be simpler because the presentation can be updated imperatively with the gesture.
- The group discussed designing for arbitrary window widths rather than assuming portrait-only presentation. Standard sheets remain preferable when they provide the required behavior; custom partial-width panels are useful for maps, iPad layouts, and macOS interfaces where preserving surrounding content matters.
- Josh used [Geometry, compositing and drawing groups in SwiftUI](https://nilcoalescing.com/blog/GeometryCompositingAndDrawingGroupsInSwiftUI/) to distinguish three rendering tools:
  - `geometryGroup()` gives a subtree one geometric transform, which can fix components whose text, background, or keyboard-driven movement animates out of sync.
  - `compositingGroup()` applies opacity, shadows, and other effects to the composed result rather than separately to each child of a non-rendering container such as `HStack`.
  - `drawingGroup()` rasterizes a subtree into one texture, reducing layer and compositing costs for many `Path` or vector elements.
- Jake, Mark, Peter, Frank, Juan, Mihaela, and Josh explored the tradeoffs of rasterization. A drawing group must be regenerated when any flattened content changes and may look pixelated when scaled, so independently changing foreground, subject, and background content should be split into separate groups. Shadows may need different placement depending on whether they belong to each element or the composed whole.
- Josh presented `Canvas` as a more explicit alternative to `drawingGroup()`: it renders into one target, can resolve another SwiftUI view into a texture once, and can stamp that texture repeatedly. This is useful when the number or placement of elements is dynamic, while `drawingGroup()` is convenient for flattening an existing declarative subtree.
- Mihaela connected these modifiers to Core Animation's layer model and an older `shouldRasterize` butterfly demonstration. She and Josh explained that textures are pixel buffers transformed and composited by the GPU; flattening can reduce texture memory and repeated blending, but it removes independent interactivity from the flattened elements.
- Peter said a newsletter with small examples would be useful. Mihaela described work on a newsletter and eventual book intended to explain the Core Animation, Core Graphics, Core Image, and Core Text foundations that leak through SwiftUI's abstractions.
- Josh discussed [One TaskGroup, Two Live Streams: a Swift 6 LLM Benchmark](https://medium.com/@wesleymatlock/one-taskgroup-two-live-streams-a-swift-6-llm-benchmark-9e45b2ed2af0). The example uses a task group for parallel model streams and an actor to aggregate telemetry safely. Josh contrasted actor isolation and its executor hops and reentrancy concerns with `Mutex`, which can be preferable for high-frequency state accessed from synchronous as well as asynchronous code.
- Mihaela noted that Mitchell points coding agents at the Swift compiler when documentation is insufficient. Josh recommended the same technique because Swift is open source: an agent can inspect the implementation and explain how a concurrency primitive works.
- In [Previews and MCP](https://cuteios.dev/2026/07/14/previews-and-mcp/), Josh highlighted using Xcode's MCP server from a purpose-built program rather than only from an AI agent. The program communicates through the protocol's JSON requests and standard streams, reaches Xcode through XPC, and can invoke preview-related Xcode tools.
- Josh used [Verse: A New Scripting Language? In THIS Economy?](https://www.youtube.com/watch?v=ebqKYLKjL6U) to compare Verse's functional design with Swift. Verse makes effects such as reading, writing, allocation, failure, and purity part of a function's contract; that gives the compiler information it may use for enforcement and optimizations such as memoization. The group also discussed arrays and maps as related indexed containers and described a monad as a context such as `Optional`, `Array`, or a publisher whose contained values can be transformed while preserving the context.
- Mihaela shared [Mitchell's split-pane demonstration](https://x.com/mitchellh/status/2071688415524049208) and her own Core Animation implementation inspired by it. Her approach builds the layout and animation engine in Core Animation, then places AppKit interaction views over the relevant regions; the same engine can be driven from other UI frameworks. She recommended starting a custom control at the Core Animation layer and adding only the higher-level interaction surfaces it needs.
- The closing discussion touched on memory management in Zig and Swift. Mihaela described Zig's allocator-passing model as allowing more local control over memory-management choices and wished Swift offered similar flexibility; Josh pointed to proposals such as `UniqueBox` while noting that garbage collection is unlikely.

### Links discussed

| Preview | Shared by | Link | Description |
|---|---|---|---|
| [<img src="https://i.ytimg.com/vi/3XaHHFOZeJg/maxresdefault.jpg" width="160" alt="SwiftUI After 7 Years video preview">](https://www.youtube.com/watch?v=3XaHHFOZeJg) | Mihaela | [SwiftUI After 7 Years: A Story of Mediocrity](https://www.youtube.com/watch?v=3XaHHFOZeJg) | Video assessing SwiftUI after seven years, focusing on data flow, layout reliability, API stability, missing features, and performance. |
| [<img src="https://nilcoalescing.com/static/blog/BuildingAdaptiveNonModalPanelsInSwiftUI/banner.duudt5lWsdy6Fa9y6ev9vS7wex5DrInbWrNJDQlrfvI.png" width="160" alt="Adaptive non-modal SwiftUI panels preview">](https://nilcoalescing.com/blog/BuildingAdaptiveNonModalPanelsInSwiftUI/) | Josh | [Building adaptive non-modal panels in SwiftUI](https://nilcoalescing.com/blog/BuildingAdaptiveNonModalPanelsInSwiftUI/) | Shows how to build a detent-based, non-modal SwiftUI panel that adapts between a bottom panel in portrait and an edge-aligned panel in landscape. |
| [<img src="https://nilcoalescing.com/static/blog/GeometryCompositingAndDrawingGroupsInSwiftUI/banner.U6Rkng1WUujC0H3y8o1f0ogeNyf9JoJpItCJ3xYvZUQ.png" width="160" alt="SwiftUI geometry and rendering groups preview">](https://nilcoalescing.com/blog/GeometryCompositingAndDrawingGroupsInSwiftUI/) | Josh | [Geometry, compositing and drawing groups in SwiftUI](https://nilcoalescing.com/blog/GeometryCompositingAndDrawingGroupsInSwiftUI/) | Explains how `geometryGroup()`, `compositingGroup()`, and `drawingGroup()` affect distinct stages of SwiftUI animation and rendering, and when to use each. |
| [<img src="https://miro.medium.com/v2/resize:fit:1200/0*rRI-osGc45lrdmmd.png" width="160" alt="Swift 6 LLM benchmark preview">](https://medium.com/@wesleymatlock/one-taskgroup-two-live-streams-a-swift-6-llm-benchmark-9e45b2ed2af0) | Josh | [One TaskGroup, Two Live Streams: a Swift 6 LLM Benchmark](https://medium.com/@wesleymatlock/one-taskgroup-two-live-streams-a-swift-6-llm-benchmark-9e45b2ed2af0) | A Swift 6 strict-concurrency design that merges live model inference and telemetry into one ordered event stream using an actor and a structured task group. |
| No preview | Josh | [Previews and MCP](https://cuteios.dev/2026/07/14/previews-and-mcp/) | Amy's guide to communicating with Xcode's MCP bridge and using its `RenderPreview` tool to fetch SwiftUI preview snapshots. |
| [<img src="https://i.ytimg.com/vi/ebqKYLKjL6U/maxresdefault.jpg" width="160" alt="Verse scripting language video preview">](https://www.youtube.com/watch?v=ebqKYLKjL6U) | Josh | [Verse: A New Scripting Language? In THIS Economy?](https://www.youtube.com/watch?v=ebqKYLKjL6U) | Logan discusses learning programming languages in the AI era and Verse's expected role in replacing Blueprints in Unreal Engine 6. |
| No preview | Mihaela | [Mitchell's split-pane demonstration](https://x.com/mitchellh/status/2071688415524049208) | Demonstration that inspired Mihaela's Core Animation implementation of an animated, interactive split-pane layout. |

## 2026.07.18

### Articles shared by Josh

| Preview | Article | Summary |
|---|---|---|
| [<img src="https://nilcoalescing.com/static/blog/UnstableDefaultEnvironmentValuesInSwiftUI/banner.vttbL7tdbkl_VoUSyW5uIWGrqkw3k6XrLk0rOXxsvt4.png" width="160" alt="Unstable SwiftUI environment defaults preview">](https://nilcoalescing.com/blog/UnstableDefaultEnvironmentValuesInSwiftUI/) | [The hidden cost of unstable SwiftUI environment defaults](https://nilcoalescing.com/blog/UnstableDefaultEnvironmentValuesInSwiftUI/) | Explains why a reference-type `@Entry` fallback that creates a fresh instance on every access can trigger unnecessary SwiftUI view updates, and how to make the default stable. |
| [<img src="https://alexanderweiss.dev/blog/2026-07-12-the-anatomy-of-a-reusable-swiftui-view/opengraph-image" width="160" alt="Reusable SwiftUI view preview">](https://alexanderweiss.dev/blog/2026-07-12-the-anatomy-of-a-reusable-swiftui-view) | [The Anatomy of a Reusable SwiftUI View](https://alexanderweiss.dev/blog/2026-07-12-the-anatomy-of-a-reusable-swiftui-view) | Builds a reusable rating control whose API follows native SwiftUI conventions, including bindings, view-builder labels, environment-driven styles, and accessibility actions. |
| [<img src="https://nilcoalescing.com/static/blog/EquatablePropertiesInObservableClasses/banner.7UFUeuYJlNvQ4hBrMwFjjBgC4bjSgTKIYsAkrmDCzLA.png" width="160" alt="Equatable Observable properties preview">](https://nilcoalescing.com/blog/EquatablePropertiesInObservableClasses/) | [Equatable properties in `@Observable` classes](https://nilcoalescing.com/blog/EquatablePropertiesInObservableClasses/) | Shows how adding `Equatable` to custom value types stored in `@Observable` properties lets generated setters avoid notifying observers when a new value equals the old one. |
| — | [SwiftUI Best Practices, straight from Apple's Xcode 27 Agent Skill](https://www.avanderlee.com/ai-development/swiftui-best-practices-xcode-27-agent-skill/) | Distills guidance from Apple's SwiftUI agent skill, including extracting separate view types to create narrower invalidation boundaries and passing views only the data they read. |
| [<img src="https://substackcdn.com/image/fetch/$s_!wOfj!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fpbs.substack.com%2Fmedia%2FHMDvSVCbAAAfJY1.jpg" width="160" alt="Splitting large SwiftUI views preview">](https://emredegirmenci.substack.com/p/splitting-large-swiftui-views-in) | [Splitting Large SwiftUI Views in the Apple's way](https://emredegirmenci.substack.com/p/splitting-large-swiftui-views-in) | Recommends extracting subviews into separate `View` types instead of using computed properties, and clarifies where `@ViewBuilder` fits. |
| — | [User Diagnostics Reports: Solving app bugs faster with AI Agents](https://www.avanderlee.com/debugging/introducing-diagnostics-improved-debugging-and-user-support/) | Describes structured diagnostic reports that combine logs, crash details, and app context so support teams and AI agents can diagnose user-reported problems more quickly. |
| [<img src="https://livsycode.com/wp-content/uploads/2024/08/SocialMediaPostCover.png" width="160" alt="iOS launch performance agent skill preview">](https://livsycode.com/swiftui/ios-launch-performance-agent-skill/) | [The iOS Launch Performance Agent Skill](https://livsycode.com/swiftui/ios-launch-performance-agent-skill/) | Presents a focused agent skill for classifying launch scenarios, locating the expensive startup phase, separating critical work from deferrable work, and validating improvements with evidence. |
| [<img src="https://livsycode.com/wp-content/uploads/2024/08/SocialMediaPostCover.png" width="160" alt="anyAppleOS in Swift 6.4 preview">](https://livsycode.com/swift/swift-6-4-adds-anyappleos-for-cleaner-availability-checks/) | [`anyAppleOS` in Swift 6.4](https://livsycode.com/swift/swift-6-4-adds-anyappleos-for-cleaner-availability-checks/) | Introduces Swift 6.4's `anyAppleOS` availability grouping for APIs that arrive at the same version across Apple platforms, reducing repetitive platform lists. |
| — | [Previews and MCP](https://cuteios.dev/2026/07/14/previews-and-mcp/) | Explores Xcode 27 beta 3's MCP tools and the `RenderPreview` workflow, including JSON-RPC communication and the sandbox/XPC constraints involved in building a SwiftUI preview gallery. |
| [<img src="https://docs.developer.apple.com/tutorials/developer-og.jpg" width="160" alt="External agents and Xcode preview">](https://developer.apple.com/documentation/xcode/giving-external-agents-access-to-xcode) | [Giving external agents access to Xcode](https://developer.apple.com/documentation/xcode/giving-external-agents-access-to-xcode) | Apple's guide to enabling Xcode's MCP server for external agents and configuring tools such as Codex with `xcrun mcpbridge`. |
| [<img src="https://preview.redd.it/foundation-models-context-size-update-in-xcode-beta-3-v0-9rc9pzwlnich1.png?auto=webp&s=f56816d5710170421a2c5a36840c41f632a5376c" width="160" alt="Foundation Models context size screenshot">](https://www.reddit.com/r/swift/comments/1ut8e9u/foundation_models_context_size_update_in_xcode/) | [Foundation Models context size update in Xcode beta 3](https://www.reddit.com/r/swift/comments/1ut8e9u/foundation-models_context_size_update_in_xcode/) | Screenshot and discussion reporting that the on-device Foundation Models `contextSize` increased from 4,096 to 8,192 in iOS 27 beta 3. |
| [<img src="https://i.ytimg.com/vi/zZ5-KVDIaPg/hqdefault.jpg" width="160" alt="Haskell is DONE video preview">](https://www.youtube.com/watch?v=zZ5-KVDIaPg) | [Haskell is DONE](https://www.youtube.com/watch?v=zZ5-KVDIaPg) | The PrimeTime video commentary on current Haskell community news and debate. |

### Other relevant links from the chat

| Shared by | Link | Relevance |
|---|---|---|
| Josh | [SE-0420: Inheritance of actor isolation](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0420-inheritance-of-actor-isolation.md#L210-L218) | Swift Evolution proposal for optional `isolated` parameters and the `#isolation` default argument, allowing async functions to inherit their caller's actor isolation. |
| Peter | [ordo-one Benchmark package configuration](https://github.com/ordo-one/benchmark/blob/main/Benchmarks/Package.swift) | Example SwiftPM benchmark suite using the `ordo-one/benchmark` package and separate executable benchmark targets. |
| Frank | [Swift Collections Benchmark](https://github.com/apple/swift-collections-benchmark) | Apple's tool for collecting and visualizing performance data for Swift data structures and collection algorithms. |
| Carlyn | [Torvalds apologizes and takes a break from Linux](https://itsfoss.com/torvalds-takes-a-break-from-linux/) | Article shared during a side discussion about technical leadership, community conduct, and taking responsibility for communication. |
| Carlyn | [Lean Programming Language](https://lean-lang.org) | Programming language and proof assistant used for machine-checked mathematics and formal verification. |
| Carlyn | [mathlib4](https://github.com/leanprover-community/mathlib4) | The community-maintained mathematical library for Lean 4. |
| Ray | [`Narrowed Any` pitch discussion — John McCall's post](https://forums.swift.org/t/pitch-narrowed-any/86369/50) | A Swift Forums moderation note about the emerging policy for LLM-assisted contributions, emphasizing that authors remain personally responsible for accuracy and risks such as laundering misinformation. |

## 2026.07.11

### Discussion notes

- Alex asked about building Swift server executables for x86 Linux from Apple Silicon. The group discussed Swift's Static Linux SDK, musl, static linking, Docker, GitHub Actions, CI cost, and whether compiling objects locally and linking in an x86 environment could shorten the inner loop.
- Jack demoed work on an iPod Touch emulator in QEMU. He used AI assistance to add a Broadcom Wi-Fi driver, then tracked a DNS/Safari issue to an old entitlement/Seatbelt configuration problem. The group discussed older iOS internals, TLS compatibility, jailbreaking, and how to approach an AI-authored open-source pull request responsibly.
- Praveen asked about Kotlin Multiplatform from an iOS team's perspective. Mihaela, Gage, Alex, Josh, and Juan compared KMP with native Swift, Swift-on-Android, generated API clients, shared contracts, and agent-assisted porting between Android, iOS, and web codebases.
- The API-contract discussion covered OpenAPI, GraphQL, gRPC, protobuf optionality, Thrift, JSON schema, and decoding incidents caused by weak or reused client/server contracts.
- Alex described FreeFeed, an open-source small social network, and the app he is building for it. The group also discussed older private social networks, including Path and its role in pushing iOS toward clearer Contacts permission prompts.
- Josh demoed a SwiftUI `UIViewRepresentable` that hosts a `UICollectionView` with a compositional list layout and a diffable data source. The demo focused on observing `@Observable` state with `Observations.untilFinished`, subscribing to `AsyncSequence` changes, retaining task cancellation, avoiding retain cycles, and keeping task work on the current actor with `#isolation`.
- During the collection view discussion, Mihaela emphasized the continued usefulness of `UITableView`, `UICollectionView`, and diffable data sources. Alex described moving a text-heavy social feed from SwiftUI to UIKit collection views to remove scrolling stutters.
- Josh showed how an agent caught edge cases in Pokemon evolution data that a simpler hand-written traversal missed, including branching paths and cycles. The group tied that back to contracts, test-driven agent loops, and using developer judgment to reshape generated code into the preferred style.
- Josh closed with links about custom SwiftUI bindings, iOS performance myths, iOS 27 RAW image processing, and HDR/gamma perception.

### Links shared in chat

| Shared by | Preview | Link | Description |
|---|---|---|---|
| Alex | [<img src="https://api.microlink.io/?url=https%3A%2F%2Fmusl.libc.org&screenshot=true&meta=false&embed=screenshot.url" width="160" alt="musl libc preview">](https://musl.libc.org) | [musl libc](https://musl.libc.org) | Lightweight C standard library for Linux used by Swift's Static Linux SDK for fully static Linux executables. |
| Alex / Carlyn | [<img src="https://api.microlink.io/?url=https%3A%2F%2Fwww.swift.org%2Fdocumentation%2Farticles%2Fstatic-linux-getting-started.html&screenshot=true&meta=false&embed=screenshot.url" width="160" alt="Swift Static Linux SDK preview">](https://www.swift.org/documentation/articles/static-linux-getting-started.html) | [Getting Started with the Static Linux SDK](https://www.swift.org/documentation/articles/static-linux-getting-started.html) | Swift.org guide to building fully statically linked Linux executables, including x86_64 and ARM64 musl SDK targets. |
| Carlyn | [<img src="https://opengraph.githubassets.com/10d193ebf38e2eef247f1ad2bc78b8eb8ad43c6559559f5ecb46fd7f924b884b/carlynorama/GHActionsForOpenUSD" width="160" alt="GHActionsForOpenUSD preview">](https://github.com/carlynorama/GHActionsForOpenUSD) | [GHActionsForOpenUSD](https://github.com/carlynorama/GHActionsForOpenUSD) | Reusable GitHub Actions for OpenUSD, shared during the CI and cached-build discussion. |
| Jack | [<img src="https://api.microlink.io/?url=https%3A%2F%2Fdevos50.github.io%2Fblog%2F2022%2Fipod-touch-qemu%2F&screenshot=true&meta=false&embed=screenshot.url" width="160" alt="iPod Touch QEMU preview">](https://devos50.github.io/blog/2022/ipod-touch-qemu/) | [Emulating an iPod Touch 1G and iPhoneOS 1.0 using QEMU](https://devos50.github.io/blog/2022/ipod-touch-qemu/) | Blog post about emulating early iPod Touch hardware in QEMU, the project Jack extended with Wi-Fi support. |
| Alex | [<img src="https://avatars.githubusercontent.com/u/11790426?s=280&v=4" width="160" alt="FreeFeed GitHub preview">](https://github.com/FreeFeed) | [FreeFeed on GitHub](https://github.com/FreeFeed) | GitHub organization for the FreeFeed social network projects. |
| Alex | [<img src="https://opengraph.githubassets.com/294b184fb9bc670a3750cd396e7cc529e816189972e8550054edfe3b35c0bc4e/FreeFeed/freefeed-server" width="160" alt="FreeFeed server preview">](https://github.com/FreeFeed/freefeed-server) | [FreeFeed/freefeed-server](https://github.com/FreeFeed/freefeed-server) | Open-source FreeFeed server repository. |
| Alex | [<img src="https://api.microlink.io/?url=https%3A%2F%2Ffreefeed.net&screenshot=true&meta=false&embed=screenshot.url" width="160" alt="FreeFeed preview">](https://freefeed.net) | [FreeFeed](https://freefeed.net) | Small social network Alex discussed while describing his native client and notification proxy. |
| Peter | [<img src="https://docs.developer.apple.com/tutorials/developer-og.jpg" width="160" alt="Apple Observation documentation preview">](https://developer.apple.com/documentation/observation/observations/untilfinished%28_%3A%29) | [Observations.untilFinished(_:)](https://developer.apple.com/documentation/observation/observations/untilfinished%28_%3A%29) | Apple documentation for constructing an async sequence from tracked observation changes. |
| Mihaela | [<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Path_logo.svg/1280px-Path_logo.svg.png" width="160" alt="Path social network preview">](https://en.wikipedia.org/wiki/Path_%28social_network%29) | [Path (social network)](https://en.wikipedia.org/wiki/Path_%28social_network%29) | Defunct private social network that came up during the discussion of small social apps and Contacts permissions. |
| Peter | [<img src="https://opengraph.githubassets.com/0aea4c6deebe639a488415c6ea89c3b23591507354fe39562a10d8ec42b6911a/swiftlang/swift-evolution" width="160" alt="SE-0431 preview">](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0431-isolated-any-functions.md) | [SE-0431: `@isolated(any)` Function Types](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0431-isolated-any-functions.md) | Swift Evolution proposal relevant to Josh's task-isolation workaround and the `#isolation` discussion. |
| Josh | [<img src="https://nilcoalescing.com/static/blog/CustomBindingsInSwiftUIClosuresVsSubscripts/banner.BdbPRPL9pIe8lXcpnCJMwifP1lw9bHbHgcu5emHCUY4.png" width="160" alt="Custom SwiftUI bindings preview">](https://nilcoalescing.com/blog/CustomBindingsInSwiftUIClosuresVsSubscripts/) | [Custom bindings in SwiftUI: closures vs subscripts](https://nilcoalescing.com/blog/CustomBindingsInSwiftUIClosuresVsSubscripts/) | Nil Coalescing article about closure-based bindings, subscript-based bindings, and SwiftUI view updates. |
| Josh | [<img src="https://livsycode.com/wp-content/uploads/2024/08/SocialMediaPostCover.png" width="160" alt="Modern iOS performance myths preview">](https://livsycode.com/blog/modern-ios-performance-myths-episode-1/) | [Modern iOS Performance Myths: Episode 1](https://livsycode.com/blog/modern-ios-performance-myths-episode-1/) | Livsy Code article/podcast notes on iOS performance tradeoffs and common misconceptions. |
| Josh | [<img src="https://i0.wp.com/9to5mac.com/wp-content/uploads/sites/6/2026/07/raw9.jpg?resize=1200%2C628&quality=82&strip=all&ssl=1" width="160" alt="RAW 9 preview">](https://9to5mac.com/2026/07/06/apple-overhauls-raw-photo-processing-with-ios-27-showcases-impressive-results/) | [Apple overhauls RAW photo processing with iOS 27](https://9to5mac.com/2026/07/06/apple-overhauls-raw-photo-processing-with-ios-27-showcases-impressive-results/) | 9to5Mac article on Apple's RAW 9 processing pipeline and ML-based denoising/detail improvements. |
| Josh | [<img src="https://i.ytimg.com/vi/6hAVA6_Sczs/maxresdefault.jpg" width="160" alt="HDR video preview">](https://www.youtube.com/watch?v=6hAVA6_Sczs) | [The Lie You Were Sold About HDR](https://www.youtube.com/watch?v=6hAVA6_Sczs) | YouTube video about HDR, gamma, brightness perception, and display limits. |

### Observation demo

Josh shared this source code for the `UICollectionView` / Observation demo:

```swift
import SwiftUI
import UIKit

struct PokemonListView: UIViewRepresentable {
    var pokemon: [Pokemon]

    func makeUIView(context: Context) -> UICollectionView {
        context.coordinator.collectionView
    }

    func updateUIView(_ uiView: UICollectionView, context: Context) {
        context.coordinator.pokemon = pokemon
    }

    func makeCoordinator() -> Coordinator {
        .init()
    }
}

@MainActor
extension PokemonListView {
    enum Section: Int, CaseIterable {
        case all
    }

    @Observable
    @MainActor
    final class Coordinator {
        var pokemon: [Pokemon] = []
        @ObservationIgnored let collectionView: UICollectionView
        @ObservationIgnored private let subscriptions = Subscriptions()
        private typealias Item = Pokemon
        private typealias ListCellRegistration = UICollectionView.CellRegistration<UICollectionViewListCell, Item>
        private typealias DataSource = UICollectionViewDiffableDataSource<Section, Item>
        private typealias SnapShot = NSDiffableDataSourceSnapshot<Section, Item>

        init() {
            let layout = UICollectionViewCompositionalLayout.list(using: .init(appearance: .plain))

            collectionView = UICollectionView(frame: .zero, collectionViewLayout: layout)

            let listRegistration = ListCellRegistration { cell, _, item in
                var configuration = cell.defaultContentConfiguration()
                configuration.text = item.name.japanese
                configuration.secondaryText = item.description
                cell.contentConfiguration = configuration
            }

            let dataSource = DataSource(collectionView: collectionView) { [listRegistration] collectionView, indexPath, item in
                collectionView.dequeueConfiguredReusableCell(
                    using: listRegistration,
                    for: indexPath,
                    item: item
                )
            }

            subscriptions += values(of: \.pokemon).subscribe { [dataSource] pokemon in
                var snapshot = SnapShot()
                snapshot.appendSections([.all])
                snapshot.appendItems(pokemon, toSection: .all)
                dataSource.apply(snapshot, animatingDifferences: true)
            }
        }
    }
}

nonisolated extension AsyncSequence where Failure == Never {
    func subscribe(
        isolation: isolated (any Actor)? = #isolation,
        _ perform: @escaping (Element) async -> Void
    ) -> Task<Void, Never> {
        Task {
            _ = isolation
            for await element in self {
                guard !Task.isCancelled else { return }
                await perform(element)
            }
        }
    }

    func subscribe<Reference: AnyObject>(
        isolation: isolated (any Actor)? = #isolation,
        unretained reference: Reference,
        _ perform: @escaping (Reference, Element) -> Void
    ) -> Task<Void, Never> {
        Task { [weak reference] in
            _ = isolation
            for await element in self {
                guard !Task.isCancelled, let reference else { return }
                perform(reference, element)
            }
        }
    }
}

extension Observation.Observable where Self: AnyObject {
    func values<Value: Sendable>(
        of keyPath: KeyPath<Self, Value>
    ) -> some AsyncSequence<Value, Never> {
        Observations.untilFinished { [weak self] in
            self.map { .next($0[keyPath: keyPath]) } ?? .finish
        }
    }

    func newValues<Value: Sendable>(
        of keyPath: KeyPath<Self, Value>
    ) -> some AsyncSequence<Value, Never> {
        values(of: keyPath).dropFirst()
    }
}

nonisolated final class Subscriptions {
    private var cancellations: [() -> Void] = []

    deinit {
        for cancel in cancellations {
            cancel()
        }
    }

    static func += <Value, Failure>(lhs: Subscriptions, rhs: Task<Value, Failure>) {
        lhs.cancellations.append(rhs.cancel)
    }
}
```

### Pokemon evolution traversal

Josh also shared the source used in the Pokemon evolution-path discussion:

```swift
import Foundation

nonisolated extension Pokemon {
    static let firstEvolutions: [[Pokemon]] = Self
        .all
        .compactMap { pokemon -> [Pokemon]? in
            guard pokemon.evolution.previous == nil else { return nil }
            var visited: Set<Int> = []
            return Array(sequence(first: pokemon) { pokemon in
                guard let proposed = (pokemon
                    .evolution
                    .next
                    .first?
                    .targetID
                ).flatMap({ Self.pokemonByID[$0] }) else {
                    return nil
                }
                return visited.insert(pokemon.id).inserted ? pokemon : nil
            })
        }

    static let evolutions: [[Pokemon]] = {
        var visited: Set<Int> = []

        func evolutions(from pokemon: Pokemon) -> [[Pokemon]] {
            visited.insert(pokemon.id)
            let children = pokemon
                .evolution
                .next
                .compactMap { id in
                    Self.pokemonByID[id.targetID]
                        .flatMap { visited.contains($0.id) ? nil : $0 }
                }
            return children.isEmpty
                ? [[pokemon]]
                : children.flatMap { nextPokemon in
                    evolutions(from: nextPokemon).map { [pokemon] + $0 }
                }
        }

        return Self
            .all
            .lazy
            .compactMap { pokemon -> [[Pokemon]]? in
                visited.removeAll()
                return pokemon.evolution.previous == nil
                    ? evolutions(from: pokemon)
                    : nil
            }
            .flatMap(\.self)
    }()

    static let evolutionPaths: [[Pokemon]] = Self
        .all
        .compactMap { pokemon -> [[Pokemon]]? in
            guard pokemon.evolution.previous == nil else { return nil }
            return Self.allEvolutionPaths(from: pokemon)
        }
        .flatMap { $0 }

    private static func allEvolutionPaths(
        from pokemon: Pokemon,
        visited: Set<Int> = []
    ) -> [[Pokemon]] {
        let visited = visited.union([pokemon.id])
        let nextPokemon = pokemon
            .evolution
            .next
            .compactMap { Self.pokemonByID[$0.targetID] }
            .filter { !visited.contains($0.id) }

        guard !nextPokemon.isEmpty else { return [[pokemon]] }

        return nextPokemon.flatMap { nextPokemon in
            Self
                .allEvolutionPaths(from: nextPokemon, visited: visited)
                .map { [pokemon] + $0 }
        }
    }
}
```

## 2026.07.04

### Discussion notes

- Mihaela shared Aleahim's "Humans Don't Work at GitHub" article, which drew reactions from Josh, Bob, Chitaranjan, Frank, and Ray.
- Jack mentioned "greg hockenberry"; Bob and Ray followed with links to Craig Hockenberry's Mastodon profile and a Mastodon post.
- Josh shared a sequence of Swift and SwiftUI links covering SwiftUI internals, SwiftUI animation bugs, toolbar APIs, Swift Testing traits, privacy manifests, dynamic colors, loading state ownership, HDR images, and iOS 27 SDK requirements.
- Color management came up through Bob's Craig Hockenberry book link, Mihaela's color-space list, Josh's Apple HDR images documentation link, and Georgi's Android color video.
- Josh then shared a set of AI, math, formal methods, hardware, Mac gaming, and generative-media resources, including Lean, mathlib4, 3Blue1Brown, Dwarkesh Patel, Theo, Figma, Snazzy Labs, and World Science Festival videos.

### Color spaces shared by Mihaela

```text
deviceRGB — Device RGB (DeviceRGB)
deviceCMYK — Device CMYK (DeviceCMYK)
deviceGray — Device Gray (DeviceGray)
displayP3 — Display P3 (DisplayP3)
extendedSRGB — Extended-range sRGB (ExtendedSRGB)
linearSRGB — Linear-light sRGB (LinearSRGB)
extendedLinearSRGB — Extended-range linear sRGB (ExtendedLinearSRGB)
rec2020 — Rec.2020 / BT.2020 (Rec2020)
```

### Links shared by Josh

| Preview | Link | Description |
|---|---|---|
| [<img src="https://aleahim.com/images/blog/the-swiftui-oracle/hero.jpg" width="160" alt="The SwiftUI Oracle preview">](https://aleahim.com/blog/the-swiftui-oracle/) | ["The SwiftUI Oracle: Measuring a Clean Room Against the Real Thing"](https://aleahim.com/blog/the-swiftui-oracle/) | Aleahim article about testing a clean-room SwiftUI-style engine against real SwiftUI with differential tests and a headless oracle harness. |
| [<img src="https://og.fatbobman.com/card/debugging-notes-on-two-swiftui-animation-bugs-en.webp" width="160" alt="SwiftUI animation bugs preview">](https://fatbobman.com/en/posts/debugging-notes-on-two-swiftui-animation-bugs/) | [Debugging Notes on Two SwiftUI Animation Bugs](https://fatbobman.com/en/posts/debugging-notes-on-two-swiftui-animation-bugs/) | Fatbobman debugging notes on two SwiftUI animation issues, including an iOS 27 rebuild case and an `Image` rendering glitch in `List`. |
| [<img src="https://swiftwithmajid.com/public/glassy-toolbar.png" width="160" alt="SwiftUI toolbar preview">](https://swiftwithmajid.com/2026/06/23/taking-control-of-toolbar-items-in-swiftui/) | [Taking control of toolbar items in SwiftUI](https://swiftwithmajid.com/2026/06/23/taking-control-of-toolbar-items-in-swiftui/) | Swift with Majid article on newer SwiftUI toolbar APIs for controlling toolbar appearance and behavior. |
| [<img src="https://d3rccdn33rt8ze.cloudfront.net/email-assets/pf-email-header.png" width="160" alt="Point-Free preview">](https://www.pointfree.co/blog/posts/217-proposing-task-local-test-traits-for-swift-testing) | [Proposing task-local test traits for Swift Testing](https://www.pointfree.co/blog/posts/217-proposing-task-local-test-traits-for-swift-testing) | Point-Free post about proposing task-local test traits for Swift Testing and feeding ideas from Point-Free libraries back into Swift. |
| [<img src="https://tanaschita.com/og/ios-privacy-manifests.png" width="160" alt="Privacy manifests preview">](https://tanaschita.com/ios-privacy-manifests/) | [Understanding privacy manifests in iOS](https://tanaschita.com/ios-privacy-manifests/) | Guide to iOS privacy manifests, third-party SDK disclosures, and required-reason APIs. |
| [<img src="https://substackcdn.com/image/fetch/$s_!8qXX!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28f9bc60-227e-41b0-9072-1e038ee362cf_1254x1254.png" width="160" alt="Dynamic Color Init preview">](https://antongubarenko.substack.com/p/dynamic-color-init) | [Dynamic Color Init](https://antongubarenko.substack.com/p/dynamic-color-init) | Anton Gubarenko Substack post about making colors reflect the current color scheme. |
| No preview | [Where Should Loading State Live In Swiftui](https://azamsharp.com/2026/06/24/where-should-loading-state-live-in-swiftui.html) | AzamSharp post on where loading state should live in SwiftUI. |
| [<img src="https://docs.developer.apple.com/tutorials/developer-og.jpg" width="160" alt="Apple Developer Documentation preview">](https://developer.apple.com/documentation/uikit/supporting-hdr-images-in-your-app) | [Supporting HDR images in your app](https://developer.apple.com/documentation/uikit/supporting-hdr-images-in-your-app) | Apple Developer Documentation on loading, displaying, editing, and saving HDR images using SwiftUI and Core Image. |
| [<img src="https://cdn.hashnode.com/uploads/covers/5fe8ca6cc0c31a41479b568a/3f10d727-bb96-4c70-9dae-47a19250d8f3.jpg" width="160" alt="iOS 27 SDK requirements preview">](https://blog.makwanbk.com/ios-27-sdk-3-major-requirements-that-migh-break-your-app) | [iOS 27 SDK: 3 Major Requirements That Might Break Your App](https://blog.makwanbk.com/ios-27-sdk-3-major-requirements-that-migh-break-your-app) | Article about SDK-enforced iOS 27 requirements that may affect launch behavior or App Store submission. |
| [<img src="https://lean-lang.org/static/png/banner.png" width="160" alt="Lean preview">](https://lean-lang.org/) | [Lean Programming Language](https://lean-lang.org/) | Official site for Lean, an open-source programming language and proof assistant for formally verified code. |
| [<img src="https://opengraph.githubassets.com/ed37388e373c69d48b87bf8a0bcbefb832bc38165a5a1944836bae34cc5d9991/leanprover-community/mathlib4" width="160" alt="mathlib4 preview">](https://github.com/leanprover-community/mathlib4) | [leanprover-community/mathlib4](https://github.com/leanprover-community/mathlib4) | GitHub repository for the Lean 4 mathematics library. |

### YouTube videos shared by Josh

| Preview | Video | Description |
|---|---|---|
| [<img src="https://i.ytimg.com/vi/ypO0q_8zhWw/hqdefault.jpg" width="160" alt="OpenAI efficiency video preview">](https://www.youtube.com/watch?v=ypO0q_8zhWw) | [Why is OpenAI so much more efficient?](https://www.youtube.com/watch?v=ypO0q_8zhWw) | YouTube video by Theo - t3.gg on OpenAI efficiency. |
| [<img src="https://i.ytimg.com/vi/iFYF_e1GSGI/hqdefault.jpg" width="160" alt="AI reasoning video preview">](https://www.youtube.com/watch?v=iFYF_e1GSGI) | [The Uncomfortable Truth About AI "Reasoning" \| World Science Festival](https://www.youtube.com/watch?v=iFYF_e1GSGI) | World Science Festival video about AI reasoning. |
| [<img src="https://i.ytimg.com/vi/bLSLN96Gn-w/hqdefault.jpg" width="160" alt="Designing Math video preview">](https://www.youtube.com/watch?v=bLSLN96Gn-w) | [Designing Math ft. Grant Sanderson (3Blue1Brown) I Config 2026](https://www.youtube.com/watch?v=bLSLN96Gn-w) | Figma video with Grant Sanderson on designing math explanations. |
| [<img src="https://i.ytimg.com/vi/TfyPshgMbug/hqdefault.jpg" width="160" alt="AI and math video preview">](https://www.youtube.com/watch?v=TfyPshgMbug) | [Grant Sanderson (3Blue1Brown) - AI and the future of math](https://www.youtube.com/watch?v=TfyPshgMbug) | Dwarkesh Patel video with Grant Sanderson on AI and mathematics. |
| [<img src="https://i.ytimg.com/vi/oIk3R-sMX5o/hqdefault.jpg" width="160" alt="Chip design video preview">](https://www.youtube.com/watch?v=oIk3R-sMX5o) | [Chip design from the bottom up - Reiner Pope](https://www.youtube.com/watch?v=oIk3R-sMX5o) | Dwarkesh Patel video with Reiner Pope about chip design. |
| [<img src="https://i.ytimg.com/vi/3ZlPEsiaGiQ/hqdefault.jpg" width="160" alt="Mac gaming video preview">](https://www.youtube.com/watch?v=3ZlPEsiaGiQ) | [Apple Just Fixed Mac Gaming and Said Nothing](https://www.youtube.com/watch?v=3ZlPEsiaGiQ) | Snazzy Labs video about Apple's Mac gaming improvements. |
| [<img src="https://i.ytimg.com/vi/iv-5mZ_9CPY/hqdefault.jpg" width="160" alt="AI images and videos preview">](https://www.youtube.com/watch?v=iv-5mZ_9CPY) | [But how do AI images and videos actually work? \| Guest video by Welch Labs](https://www.youtube.com/watch?v=iv-5mZ_9CPY) | 3Blue1Brown video explaining how AI image and video generation works. |

### Other links shared in chat

| Shared by | Preview | Link | Description |
|---|---|---|---|
| Mihaela | [<img src="https://aleahim.com/images/blog/humans-dont-work-at-github/hero.jpg" width="160" alt="Humans Don't Work at GitHub preview">](https://aleahim.com/blog/humans-dont-work-at-github/) | [Humans Don't Work at GitHub](https://aleahim.com/blog/humans-dont-work-at-github/) | Aleahim article about a GitHub account/workflow problem where automated enforcement left no apparent human appeal path. |
| Bob | [<img src="https://files.mastodon.social/accounts/avatars/000/423/566/original/61c6e28824186686.jpeg" width="160" alt="Craig Hockenberry Mastodon profile preview">](https://mastodon.social/@chockenberry) | [Craig Hockenberry on Mastodon](https://mastodon.social/@chockenberry) | Mastodon profile for Craig Hockenberry. |
| Ray | [<img src="https://files.mastodon.social/media_attachments/files/116/789/845/449/447/062/original/d61596d4a895e437.png" width="160" alt="Craig Hockenberry Mastodon post preview">](https://mastodon.social/@chockenberry/116789845717297219) | [Craig Hockenberry Mastodon post](https://mastodon.social/@chockenberry/116789845717297219) | Mastodon post by Craig Hockenberry with an attached image and a thank-you note to someone at Apple keeping something alive. |
| Bob | No preview | [Making Sense of Color Management](https://www.amazon.com/Making-Sense-Color-Management-Hockenberry/dp/1937557502) | Amazon listing for Craig Hockenberry's color management book. |
| Georgi | [<img src="https://i.ytimg.com/vi/r8NeG0wmFXM/hqdefault.jpg" width="160" alt="Understanding color video preview">](https://www.youtube.com/watch?v=r8NeG0wmFXM) | [Understanding color (Google I/O '17)](https://www.youtube.com/watch?v=r8NeG0wmFXM) | Android Developers video shared as "Color from the Android side." |

## 2026.06.27

### Links shared in chat

#### Josh: Apple pricing and upcoming M7
| Link | Description |
|---|---|
| [Apple Explains Why It Raised Prices](https://www.macrumors.com/2026/06/25/apple-explains-why-it-raised-prices/) | MacRumors reports that Apple raised prices across Macs, iPads, Apple TV, HomePod, and Vision Pro, citing AI-driven pressure on memory and storage component costs. |
| [2027 Macs Expected to Use M7 Chips](https://www.macrumors.com/2026/06/25/2027-macs-m7-chips/) | A Bloomberg-sourced roadmap suggesting Apple may skip high-end M6 Pro and M6 Max chips, accelerating M7 Pro and M7 Max Macs for on-device AI and GPU-heavy workloads. |

#### AI tools
| Shared by | Link | Description |
|---|---|---|
| Peter | [OpenRouter Fusion](https://openrouter.ai/fusion) | Peter asked about OpenRouter's Fusion page, which appears to be an interface for starting model-fusion runs or experiments across available OpenRouter models. |

#### SwiftUI and layout
| Shared by | Link | Description |
|---|---|---|
| Josh Homann / Josh | [SwiftUI Is One Graph, Over 40+ Years of Engineering](https://aleahim.com/blog/swiftui-is-one-graph/) | Deep dive arguing that SwiftUI is a demand-driven attribute graph, tying state identity, lazy invalidation, layout negotiation, coalesced layers, and animation back to Apple's lower-level rendering stack. |
| Carlyn | [SwiftUI Layout Explained](https://talk.objc.io/collections/swiftui-layout-explained) | Carlyn recommended this Swift Talk series as a concrete companion to "just a graph": objc.io reimplements pieces of SwiftUI layout from scratch, covering view protocols, frames, alignment, stacks, layout priority, and grids. |

#### Other shares
| Shared by | Link / Note | Description |
|---|---|---|
| Ray | [In the Weights](https://www.intheweights.com) | Ray shared the In the Weights site|
| Ray Fix | [Dropping the requirement for C++-only bootstrapping](https://forums.swift.org/t/dropping-the-requirement-for-c-only-bootstrapping/87739) | Swift Forums announcement that mandatory parts of the Swift compiler can now be implemented in Swift, dropping the old requirement that the compiler bootstrap from a pure C++ host toolchain. |

### Articles Discussed
| Thumbnail | Description |
|---|---|
| [<img src="https://aleahim.com/images/blog/swiftui-is-one-graph/hero.jpg" width="160" alt="SwiftUI graph thumbnail">](https://aleahim.com/blog/swiftui-is-one-graph/) | [Argues that SwiftUI is best understood as a single demand-driven attribute graph rather than a view tree diffing system, with disposable view values sitting on top of decades of lower-level Apple rendering infrastructure.](https://aleahim.com/blog/swiftui-is-one-graph/) |
| [<img src="https://livsycode.com/wp-content/uploads/2024/08/SocialMediaPostCover.png" width="160" alt="_UIPortalView thumbnail">](https://livsycode.com/uikit/exploring-_uiportalview-live-view-replication-without-copying-or-snapshots/) | [Explores the private UIKit `_UIPortalView` and its `CAPortalLayer` backing, explaining how live layer mirroring can support picture-in-picture, reflections, transitions, and Liquid Glass-style effects while warning about private API risk.](https://livsycode.com/uikit/exploring-_uiportalview-live-view-replication-without-copying-or-snapshots/) |
| [Swift 6.4: What's New in Concurrency](https://www.avanderlee.com/concurrency/swift-6-4-whats-new-in-concurrency/) | [Surveys Swift 6.4 concurrency changes, including async `defer`, task cancellation shields, warnings for ignored throwing tasks, typed throwing task initializers, `AsyncResult`, weak `let`, and explicit non-Sendable types.](https://www.avanderlee.com/concurrency/swift-6-4-whats-new-in-concurrency/) |
| [<img src="https://swiftjectivec.com/assets/images/logo.png" width="160" alt="Swiftjective-C thumbnail">](https://www.swiftjectivec.com/siri-ai-for-ios027/) | [Looks at how iOS 27 Siri integrations connect to apps through App Entities, IndexedEntity, app schemas, on-screen awareness, and data handoff through App Intents.](https://www.swiftjectivec.com/siri-ai-for-ios027/) |
| [<img src="https://iosapptemplates.com/img/blog/app-intents-swiftui-siri-shortcuts-spotlight/app-intents-swiftui-siri-shortcuts-spotlight-cover.svg" width="160" alt="App Intents thumbnail">](https://iosapptemplates.com/blog/app-intents-swiftui-siri-shortcuts-spotlight/) | [A SwiftUI planning guide for exposing useful product actions through App Intents across Siri, Shortcuts, Spotlight, widgets, and the Action Button while keeping intents thin and entity-driven.](https://iosapptemplates.com/blog/app-intents-swiftui-siri-shortcuts-spotlight/) |
| [<img src="https://substackcdn.com/image/fetch/$s_!Ji45!,f_auto,q_auto:best,fl_progressive:steep/https%3A%2F%2Fantongubarenko.substack.com%2Ftwitter%2Fsubscribe-card.jpg%3Fv%3D544402036%26version%3D9" width="160" alt="Anton Substack thumbnail">](https://antongubarenko.substack.com/wwdc26-swiftui-group-lab-2nd-qanda) | [The open Substack tab currently renders as a page-not-found for Anton Gubarenko's iOS development Substack, so the link is retained here without inferring article content beyond the available page metadata.](https://antongubarenko.substack.com/wwdc26-swiftui-group-lab-2nd-qanda) |
| [<img src="https://nilcoalescing.com/static/blog/AsyncImageImprovementsInSwiftUIOnIOS27/banner.vM8Mp6-r4VlvIwdjKUcMPM576Rn94UQHh9e4d-UYhdo.png" width="160" alt="AsyncImage thumbnail">](https://nilcoalescing.com/blog/AsyncImageImprovementsInSwiftUIOnIOS27/) | [Explains iOS 27's new `AsyncImage` support for `URLRequest`, allowing custom headers, cache policies, and timeouts, plus a hierarchy-wide `asyncImageURLSession(_:)` modifier.](https://nilcoalescing.com/blog/AsyncImageImprovementsInSwiftUIOnIOS27/) |
| [<img src="https://iosapptemplates.com/img/blog/metrickit-swiftui-performance-after-launch/metrickit-swiftui-performance-after-launch-cover.svg" width="160" alt="MetricKit thumbnail">](https://iosapptemplates.com/blog/metrickit-swiftui-performance-after-launch/) | [A practical guide to using MetricKit after launch to monitor SwiftUI app performance in the field, connect diagnostics to product states, and build release performance budgets.](https://iosapptemplates.com/blog/metrickit-swiftui-performance-after-launch/) |
| [LinkedIn post by Dave Verwer](https://www.linkedin.com/posts/daveverwer_what-is-it-im-supposed-to-say-some-personal-share-7475301426106347520-f6Wb/) | [Dave Verwer shares that Swift Package Index has joined Apple and that he will be working on Swift packages at Apple, with follow-up discussion noting the SPI blog will continue.](https://www.linkedin.com/posts/daveverwer_what-is-it-im-supposed-to-say-some-personal-share-7475301426106347520-f6Wb/) |

### Josh's article skill
Josh's skill to automatically scan email and social media for articles and rate them based on their match with existing topics: [swift-article-roundup](materials/swift-article-roundup/)

### Swift flatMapLatest and share fixes
These proposals have [PRs](https://github.com/apple/swift-async-algorithms/pulls) but no confirmed release.


### @State still not fixed in iOS 27
The new macro is a half fix; viewmodels still run init on every pass through body, but now SwiftUI discards the new viewmodels and only observes the first viewmodel.
```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        TimelineView(.periodic(from: .now, by: 3)) { context in
            let _ = print("-----------\(Date.now)-----------")
            V().padding(40)
        }
    }
}

struct V: View {
    var vm = VM(Self.annotateWithSeconds("naked var"))
    @State var vm0 = VM(Self.annotateWithSeconds("@State"))
    @ViewModel var vm1 = VM(Self.annotateWithSeconds("@ViewModel"))
    var body: some View {
        Text(vm.text)
        Text(vm0.text)
        Text(vm1.text)
    }
    static func annotateWithSeconds(_ text: some StringProtocol) -> String {
        "\(text) \(Date.now.formatted(.dateTime.second()))"
    }
}

@Observable
final class VM {
    var text: String
    init(_ text: String) {
        self.text = text
        print("Init \(text)")
    }
    deinit {
        print("Deinit \(text)")
    }
}


@propertyWrapper
struct ViewModel<Wrapped: AnyObject & Observable>: DynamicProperty {
    @State private var reference: Reference
    var wrappedValue: Wrapped {
        reference.value
    }
    var projectedValue: Bindable<Wrapped> {
        reference.bindable
    }
    init(wrappedValue make: @autoclosure @escaping () -> Wrapped) {
        _reference = State(wrappedValue: Reference(make))
    }
}

extension ViewModel {
    final class Reference {
        private var viewModel: Wrapped?
        private let makeViewModel: () -> Wrapped
        lazy var value: Wrapped = makeViewModel()
        lazy var bindable = { Bindable(value) }()
        init(_ make: @escaping () -> Wrapped) {
            makeViewModel = make
        }
    }
}
```
## 2026.06.20

### Decorators with @dynamicMemberLookup
```swift
import Foundation

@dynamicMemberLookup
struct UniquelyIdentifiable<WrappedValue>: Identifiable {
    var value: WrappedValue
    let id: UUID = .init()
    subscript<Value>(dynamicMember keyPath: KeyPath<WrappedValue, Value>) -> Value {
        value[keyPath: keyPath]
    }
}

struct Name {
    var given: String
}

let name = Name(given: "Josh")
let uniqueName = UniquelyIdentifiable(value: name)
print(uniqueName.given)
```

### Articles Discussed
| Thumbnail | Description |
|---|---|
| [<img src="https://api.microlink.io/?url=https%3A%2F%2Fgithub.com%2Fswiftlang%2Fswift-evolution%2Fblob%2Fmain%2Fproposals%2F0533-reasync-macros.md&screenshot=true&meta=false&embed=screenshot.url" width="160" alt="SE-0533 reasync macros thumbnail">](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0533-reasync-macros.md) | [Swift Evolution SE-0533 proposes an `@Reasync` macro that generates synchronous overloads from `async` functions, reducing duplicated APIs and keeping sync/async variants aligned from a single implementation.](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0533-reasync-macros.md) |
| [<img src="https://api.microlink.io/?url=https%3A%2F%2Fblog.jacobstechtavern.com%2Fp%2Fios-27-launch-time&screenshot=true&meta=false&embed=screenshot.url" width="160" alt="iOS 27 launch time thumbnail">](https://blog.jacobstechtavern.com/p/ios-27-launch-time) | [An Instruments-focused performance deep dive into Apple’s claimed 30% launch-time improvement in iOS 27, with attention to dyld, startup costs, and how developers can reason about launch bottlenecks in real apps.](https://blog.jacobstechtavern.com/p/ios-27-launch-time) |
| [<img src="https://api.microlink.io/?url=https%3A%2F%2Ffatbobman.com%2Fen%2Fposts%2Ffrom-size-class-to-available-space%2F&screenshot=true&meta=false&embed=screenshot.url" width="160" alt="Available space article thumbnail">](https://fatbobman.com/en/posts/from-size-class-to-available-space/) | [Explains why `horizontalSizeClass` is no longer a reliable proxy for width in newly resizable iPhone environments, and argues that SwiftUI layout decisions should move toward actual available space instead of device-style assumptions.](https://fatbobman.com/en/posts/from-size-class-to-available-space/) |
| [<img src="https://api.microlink.io/?url=https%3A%2F%2Ftanaschita.com%2Fswift-defer-async%2F&screenshot=true&meta=false&embed=screenshot.url" width="160" alt="Async defer thumbnail">](https://tanaschita.com/swift-defer-async/) | [Shows how Swift 6.4 allows asynchronous work inside `defer`, making cleanup code easier to keep next to resource acquisition while still guaranteeing it runs when the scope exits.](https://tanaschita.com/swift-defer-async/) |
| [<img src="https://api.microlink.io/?url=https%3A%2F%2Fwww.sagarunagar.com%2Fblog%2Fswiftui-prominent-tab-is-not-a-floating-action-button%2F&screenshot=true&meta=false&embed=screenshot.url" width="160" alt="Prominent tab thumbnail">](https://www.sagarunagar.com/blog/swiftui-prominent-tab-is-not-a-floating-action-button/) | [A design-focused SwiftUI article arguing that `.prominent` emphasizes a navigation destination, not an action button, and that using it like a floating action button breaks long-standing tab-bar expectations.](https://www.sagarunagar.com/blog/swiftui-prominent-tab-is-not-a-floating-action-button/) |

### @State is still broken?
```swift
import SwiftUI
import Combine

@Observable
final class ViewModel: ObservableObject {
    var name: String
    init(name: String) {
        self.name = name
        print("Init \(name)")
    }
    deinit {
        print("deinit \(name)")
    }
}

struct V1: View {
    @State var viewModel: ViewModel
    var body: some View {
        Text(viewModel.name)
    }
}
struct V2: View {
    @StateObject var viewModel: ViewModel
    var body: some View {
        Text(viewModel.name)
    }
}
struct ContentView: View {
    var body: some View {
        TimelineView(.explicit(sequence(first: Date.now, next: { $0 + 5}))) { time in
            V1(viewModel: .init(name: "State \(time.date)"))
            V2(viewModel: .init(name: "StateObject \(time.date)"))

        }
    }
}
```

## 2026.06.13

### WWDC 2027 Favorites
| Person | Favorite | Link |
|---|---|---|
| Alex | Rewatch group labs: Camera and Photos technologies | [<img src="https://img.youtube.com/vi/fn4F09dQb3s/hqdefault.jpg" width="120" alt="YouTube thumbnail">](https://www.youtube.com/live/fn4F09dQb3s?si=S_7dKKC4_6UHGZgC&t=116) |
| Alex | Compose advanced graphics effects with SwiftUI | [<img src="https://img.youtube.com/vi/HTDU2HKqM8c/hqdefault.jpg" width="120" alt="YouTube thumbnail">](https://www.youtube.com/watch?v=HTDU2HKqM8c) |
| Frank | Foundation Models are now open source |  |
| Frank | `@State` macro |  |
| Mihaela | CoreAI |  |
| Bob | Evaluations framework | [Apple Developer Documentation](https://developer.apple.com/documentation/evaluations) |
| Juan | SwiftData updates for `groupby` and `fetchresults` |  |
| Juan | Multimodal input for Foundation Models |  |
| Peter | `@State` |  |
| Peter | Xcode previews on multiple devices |  |
| Ed | Firebase AI integration | [Firebase docs](https://firebase.google.com/docs/ai-logic/apple-foundation-models-framework/get-started?api=dev) |
| Ed | RealityKit 3 |  |
| Carlyn | PaperKit | [<img src="https://devimages-cdn.apple.com/wwdc-services/images/9B2E82C5-4DDF-4B9A-9459-328D8E297696/10929/10929_wide_250x141_2x.jpg" width="120" alt="PaperKit thumbnail">](https://developer.apple.com/videos/play/wwdc2026/372) |
| Josh | Apple’s EU announcement | [Apple Newsroom](https://www.apple.com/newsroom/2026/06/due-to-dma-siri-ai-delayed-in-eu-for-ios-27-and-ipados-27/) |
|

### Articles discussed
| Thumbnail | Description |
|---|---|
| [<img src="https://nilcoalescing.com/static/blog/InitializingObservableClassesWithTheStateMacroInXcode27/banner.JK1OXwnQB21bdUROhOdM19nntAH1Sp1uA-kON2POmhk.png" width="160" alt="@State macro thumbnail">](https://nilcoalescing.com/blog/InitializingObservableClassesWithTheStateMacroInXcode27/) | [Explains how `@State` becoming a macro in Xcode 27 changes `@Observable` class initialization, including lazy initial values and avoiding unnecessary model recreation.](https://nilcoalescing.com/blog/InitializingObservableClassesWithTheStateMacroInXcode27/) |
| [<img src="https://opengraph.githubassets.com/dc18eafdf4a93ddbab3e43e3261a68d9c7ef692e7a7d0bd2a6c63a2af59be408/swiftlang/swift-evolution" width="160" alt="Swift Evolution thumbnail">](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0400-init-accessors.md) | [Swift Evolution SE-0400: init accessors, which let computed properties participate in definite initialization and support cleaner initialization patterns for wrappers and macros.](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0400-init-accessors.md) |
| [<img src="https://www.swiftjectivec.com/assets/images/UIKit2026_1.jpg" width="160" alt="UIKit additions thumbnail">](https://www.swiftjectivec.com/ios-27-notable-uikit-additions/) | [A tour of notable UIKit additions in iOS 27, including practical API changes and examples for modern UIKit apps.](https://www.swiftjectivec.com/ios-27-notable-uikit-additions/) |
| [<img src="https://api.microlink.io/?url=https%3A%2F%2Fpdf.aleahim.com&amp;screenshot=true&amp;meta=false&amp;embed=screenshot.url" width="160" alt="MarkdownPDF Playground thumbnail">](https://pdf.aleahim.com) | [MarkdownPDF Playground renders Markdown to PDF directly in the browser using a pure-Swift engine compiled to WebAssembly.](https://pdf.aleahim.com) |
| [<img src="https://www.swift.org/assets/images/bringing-goodnotes-to-web-with-swift/blog-hero@2x.png" width="160" alt="Goodnotes Swift WebAssembly thumbnail">](https://www.swift.org/blog/bringing-goodnotes-to-web-with-swift/) | [Goodnotes explains how it brought its Swift codebase to the web with WebAssembly, sharing ink rendering and note-taking logic across platforms.](https://www.swift.org/blog/bringing-goodnotes-to-web-with-swift/) |

## 2026.06.06
WWDC predictions: https://mjtsai.com/blog/2026/06/04/wwdc-2026-preview/
WWDC Wishlist: https://mjtsai.com/blog/2026/06/03/wwdc-2026-wish-lists/
WWDC Events: https://github.com/twostraws/wwdc
My Secret Plot to Kill SwiftUI: https://blog.jacobstechtavern.com/p/my-secret-plot-to-kill-swiftui

Juan's SwiftData Observation: https://github.com/juanarzola/fetch-descriptor-observer

## 2026.05.30

## Mihaela's shares:
| Image / Link | Summary |
|---|---|
| [![Kiraa](https://yt3.googleusercontent.com/7XuP7dgwCUS8KD1RJbC2vTzRG1dc9HPWcXuJ4Jk9OVA4-0O2XbXQl64ni2aPa9nV8BmhWaHEuA=s900-c-k-c0x00ffffff-no-rj)](https://www.youtube.com/@kiraa_ai)<br>[Kiraa](https://www.youtube.com/@kiraa_ai) | YouTube channel by Errol Brandt focused on practical, skeptical analysis of AI and technology for business decision-makers. The channel pushes back on AI hype, with videos about AI economics, cloud AI, Apple/ARM hardware, open source, token usage, and the Kiraa engine. |
| [![TileDown/tile-down](https://opengraph.githubassets.com/2649206901e23afd023cc6f32595fe4541f40767822d6c7a8b6fc1402776e4ae/TileDown/tile-down)](https://github.com/TileDown/tile-down)<br>[TileDown/tile-down](https://github.com/TileDown/tile-down) | A Swift static site generator called `tiledown`. It parses a constrained Markdown profile into typed tiles, then renders static HTML/CSS and optional browser JavaScript. It supports CommonMark/GFM basics, build-time math-to-SVG, charts, Mermaid, RSS, article PDFs, theming, and a local preview CLI. |
| [![mihaelamj/cupertino-desktop](https://opengraph.githubassets.com/e3cf2880fabac460cb7296c4ad70c18ca398002458f50931255522c2397fc4f7/mihaelamj/cupertino-desktop)](https://github.com/mihaelamj/cupertino-desktop)<br>[mihaelamj/cupertino-desktop](https://github.com/mihaelamj/cupertino-desktop) | Early-stage native Apple-platform app for browsing Apple Developer documentation, Swift Evolution

## Articles discussed:
| Image / Link | Summary |
|---|---|
| [![Monads are Easy](https://krishna.github.io/uploads/monads-are-easy/hero.png)](https://krishna.github.io/posts/monads-are-easy/)<br>[Monads are Easy](https://krishna.github.io/posts/monads-are-easy/) | Explains monads using a concrete warehouse/book-scanning analogy. The post frames a monad as something that can wrap a value and flatten nested containers via `flatMap`, then tests that idea against arrays, optionals, results, custom structs, and JSON. |
| [![Replacing Bash with Swift in an AI Harness](https://alejandromp.com/development/blog/replacing-bash-with-swift-in-an-ai-harness/poster.jpeg)](https://alejandromp.com/development/blog/replacing-bash-with-swift-in-an-ai-harness/)<br>[Replacing Bash with Swift in an AI Harness](https://alejandromp.com/development/blog/replacing-bash-with-swift-in-an-ai-harness/) | Describes replacing a Bash tool in an AI coding harness with embedded Swift via SwiftScript. The author argues this creates a more controlled runtime than shell execution, while still needing clear sandboxing boundaries for real security. |
| [![Protecting sensitive content when screen sharing and remote control are active](https://developer.apple.com/tutorials/developer-og.jpg)](https://developer.apple.com/documentation/swiftui/protecting-sensitive-content-when-screen-sharing)<br>[Protecting sensitive content when screen sharing and remote control are active](https://developer.apple.com/documentation/swiftui/protecting-sensitive-content-when-screen-sharing) | Apple documentation on detecting active screen capture, mirroring, and remote-control sessions. It recommends using SwiftUI’s `isSceneCaptured` or UIKit’s `sceneCaptureState` to selectively redact sensitive content, notify users, or disable risky actions while balancing privacy with usability. |
| [![Hide SwiftUI Views from Screenshot](https://kyleye.top/images/swiftui-hidden-from-capture/cover.png)](https://kyleye.top/posts/swiftui-hidden-from-capture/)<br>[Hide SwiftUI Views from Screenshot](https://kyleye.top/posts/swiftui-hidden-from-capture/) | Investigates how to hide specific SwiftUI views from screenshots and screen recordings without wrapping them in a secure text field. The post traces the approach through CALayer capture flags, SwiftUI renderer internals, `privacySensitive(false)`, and private redaction reasons, with caveats about SPI and security limits. |
| [![Type-Driven Design in Swift: Better Money Formatting](https://miro.medium.com/v2/resize:fit:1200/1*lFNvzXmlwyuHYjnrPy7LmQ.png)](https://medium.com/@uwaisalqadri/type-driven-design-in-swift-better-money-formatting-4667b823fe6c)<br>[Type-Driven Design in Swift: Better Money Formatting](https://medium.com/@uwaisalqadri/type-driven-design-in-swift-better-money-formatting-4667b823fe6c) | Argues for separating raw money values from formatted display values in Swift. The article uses currency and rounding examples to show why formatted strings should not feed calculations, then proposes domain-specific types to keep calculation data and UI presentation distinct. |

## Extending monads:
```swift
extension Sequence {
    func mapToSet<Transformed: Hashable, Failure: Error>(
        transform: (Element) throws(Failure) -> Transformed
    ) throws(Failure) -> Set<Transformed> {
        var accumulated = Set<Transformed>(minimumCapacity: underestimatedCount)
        for element in self {
            try accumulated.insert(transform(element))
        }
        return accumulated
    }
    func mapToCountedSet<Transformed, Failure: Error>(
        transform: (Element) throws(Failure) -> Transformed
    ) throws(Failure) -> [Transformed: Int] {
        var accumulated = [Transformed: Int](minimumCapacity: underestimatedCount)
        for element in self {
            try accumulated[transform(element), default: 0] += 1
        }
        return accumulated
    }
}
```

## 2026.05.23

## Articles discussed:
| Article | URL | Description |
|---|---|---|
| A Feature Flags System in Swift | https://livsycode.com/best-practices/a-feature-flags-system-in-swift/ | Walks through building a type-safe, thread-safe feature flag system in Swift, including feature definitions, priority-based sources, local overrides, and an internal QA/developer toggle screen. |
| A floating card using safeAreaBar | https://codakuma.com/floating-safe-area-bar/ | Shows how to build a bottom-pinned floating SwiftUI card using `safeAreaBar` on iOS 26, with an iOS 18 fallback based on `safeAreaInset`, material blur, and gradients. |
| ContentUnavailableView in SwiftUI - Complete Guide With Examples | https://www.sagarunagar.com/blog/contentunavailableview-swiftui/ | A practical guide to SwiftUI’s `ContentUnavailableView`, covering empty states, failed searches, recovery actions, customization, accessibility, and common mistakes. |
| Cupertino v1.1.0: my Apple docs index was 30% lies and I didn't know | https://aleahim.com/blog/cupertino-v1-1-0-poison-cleanup/ | Describes debugging and cleaning a corrupted Apple documentation search index, including crawler poison cases, CDN/SPA failure modes, audit checks, and release-version lessons. |
```

### Using idiomatic views in SwiftUI to build a chat app:
```swift
@Observable
final class ViewModel {
    var items: [Item] = []
    var input = ""
    func send() {
        items.append(.init(title: input, isUser: true))
        items.append(.init(title: "Hello", isUser: false))
    }
}

struct V: View {
    var viewModel = ViewModel()
    var body: some View {
        List {
            ForEach(viewModel.items.reversed()) { item in
                let image = item.isUser ? "bubble.left" : "bubble.right"
                Label(item.title, systemImage: image)
                    .listRowSeparator(.hidden)
                    .padding(.horizontal, 20)
                    .containerRelativeFrame(.horizontal, alignment: item.isUser ? .leading : .trailing)
                    .scaleEffect(y: -1)

            }
        }
        .listStyle(.plain)
        .safeAreaBar(edge: .top) {
            HStack {
                @Bindable var binding = viewModel
                TextField("Send a message", text: $binding.input)
                    .frame(minHeight: 40)
                    .padding(.horizontal, 16)
                    .onSubmit(viewModel.send)
                    .glassEffect()
                Button {
                    viewModel.send()
                } label: {
                    Image(systemName: "arrow.up")
                        .font(.title.weight(.semibold))
                        .padding(6)
                        .tint(Color(uiColor: .systemBackground))
                }
                .glassEffect(.regular.tint(Color.accentColor).interactive(), in: Circle())
            }
            .padding(.horizontal, 16)
            .scaleEffect(y: -1)
        }
        .scaleEffect(y: -1)
    }
}
```


## 2026.05.16

### Concurrency

|  | &lt; Swift 6.2 | Swift 6.2+ |
| --- | --- | --- |
| `struct`, `enum`, `func`, `class` | `nonisolated` | `@MainActor` |
| `actor` | `isolated` to `actor` | `isolated` to `actor` |
|  |  |  |
| `func synchronous()` | `nonisolated(nonsending)` | `nonisolated(nonsending)` |
| `func nonsynchronous() async` | `nonisolated`(sending) | `nonisolated(nonsending)` |
| run in background | `nonisolated func f() async` | `@concurrent func f() async` |


### Executive Summary

This session focused heavily on Swift isolation, actor semantics, memory management, and SwiftUI state behavior. Participants discussed actor isolation control, async result support, ARC internals, and the practical realities of SwiftUI reevaluation. There was also discussion of zombie objects, pointer APIs, and classic software design patterns.

### Swift Concurrency & Isolation

- Swift isolation documentation:
  https://developer.apple.com/documentation/swift/isolation()

- Actor isolation control proposal:
  https://github.com/swiftlang/swift-evolution/blob/main/proposals/0313-actor-isolation-control.md

- Async result support proposal:
  https://github.com/swiftlang/swift-evolution/blob/main/proposals/0530-async-result-support.md

- Discussion topics:
  - Actor isolation semantics
  - Async result handling
  - Reevaluation behavior in SwiftUI
  - State propagation through modifiers

### SwiftUI

- Formatting values in SwiftUI:
  https://serialcoder.dev/text-tutorials/swiftui/formatting-values-in-swiftui-text-and-textfield/?utm_source=substack&utm_medium=email

- SwiftUI state deep dive:
  https://www.nsvasilev.com/posts/swiftui-state/?utm_source=substack&utm_medium=email

- Reusable SwiftUI views:
  https://matteomanferdini.com/swiftui-reusable-views/?ck_subscriber_id=2978341758&utm_source=convertkit&utm_medium=email&utm_campaign=SwiftLee%20Weekly%20-%20Issue%20323%20-%2021730246

- Discussion topic:
  - What portions of a view hierarchy reevaluate when modifier state changes

### Memory Management & Pointers

- Swift ARC internals:
  https://livsycode.com/swift/swift-arc-from-zombie-objects-to-side-tables/?ck_subscriber_id=2978341758&utm_source=convertkit&utm_medium=email&utm_campaign=SwiftLee%20Weekly%20-%20Issue%20323%20-%2021730246

- OpaquePointer documentation:
  https://developer.apple.com/documentation/swift/opaquepointer

- Discussion topics:
  - Zombie objects
  - `unowned` vs `unowned(unsafe)`
  - Pointer mutation
  - Debugging memory issues

## Apple Platform Development

- WatchConnectivity reliability discussion:
  https://tarek-builds.dev/p/watchconnectivity-was-failing-40-of-the-time-so-i-stopped-using-it/?utm_source=substack&utm_medium=email

## Software Engineering

- Software design patterns:
  https://en.wikipedia.org/wiki/Software_design_pattern

- Prior A Flock of Swifts references:
  https://github.com/aflockofswifts/meetings/tree/main/2025#20250329
  https://github.com/aflockofswifts/meetings/tree/main/2025#presentation-gof-design-patterns-in-swift

---

## 2026.05.09

### Executive Summary

This session focused on Swift-based web tooling, Core Animation fundamentals, and developer infrastructure topics including Docker and Apple documentation workflows. 

Participants shared resources related to static site generation, animation timing curves, and practical references for Core Animation behavior. 

Josh ran a code-along where we used UICollectionView to power a large collection of items.

### Swift Web & Static Site Generation

- Toucan Sites (Swift-based static site generator):
  https://toucansites.com

- Related site:
  https://aleahim.com

### Apple Documentation & Developer Resources

- Apple documentation mirror/search:
  https://sosumi.ai

- Core Animation Programming Guide:
  https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/CoreAnimation_guide/Introduction/Introduction.html

- Reacting to layer changes:
  https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/CoreAnimation_guide/ReactingtoLayerChanges/ReactingtoLayerChanges.html#//apple_ref/doc/uid/TP40004514-CH7-SW6

### Animation & Motion

- Cubic Bézier curve visualizer:
  https://cubic-bezier.com/#.17,.67,.83,.67

- Discussion topics:
  - Animation timing curves
  - Core Animation behavior
  - Layer updates and rendering

### Infrastructure & Tooling

- TechWorld with Nana:
  https://www.youtube.com/@TechWorldwithNana

- Discussion topics:
  - DevOps
  - Docker learning resources
  - DockerCon talks and historical conference content

---

## 2026.05.02

### Executive Summary

This session explored creative tooling (including voice-controlled presentations and video generation), Swift networking evolution, and practical career development advice. There was also discussion around Core Animation, compositional layouts, and real-world app development. A recurring theme was focusing on building and refining real projects as a path to growth.

### Job Interviews

Josh H. presented about interviewing and preparing for interviews.

#### Types of questions

- Bio - provide additional context not just a repeat of the resume
- Behavioral - prepare about experience you had where you made a mistake and how you overcame it
- Technical Deep Dive - prepare something interesting and with sufficient depth
- System Design
- Practical
- Knowledge (know the APIs)
- Data structures and Algorith - Yes, you need this.
- AI? How to use tooling effectively

#### Reasons for rejection

You should always do a post mortem of the interview. 

- Just not the right person for the job (it happens, move on)
- They liked someone else better (maybe ask about positions in another dept if big company)
- Behavioral (they didn't want to work with you)
- Technical (you didn't have the skill)
- Something else

### Swift & Architecture

- Swift networking vision (accepted):
  https://github.com/swiftlang/swift-evolution/blob/main/visions/networking.md

- Discussion topics:
  - OpenAPI as the primary interface layer
  - Standardizing underlying networking primitives (HTTP, TLS, observability)
  - `swift-http-types` as a shared foundation

### SwiftUI, UIKit & UI Development

- Apple training tutorial:
  https://developer.apple.com/tutorials/app-dev-training/getting-started-with-today

- Compositional layout tutorial:
  https://www.kodeco.com/5436806-modern-collection-views-with-compositional-layouts

- Core Animation demo:
  https://github.com/mihaelamj/CubeIn3DWithCoreAnimation

- UIKit reference:
  https://www.oreilly.com/library/view/programming-ios-14/9781492092162/

- Core Animation book:
  https://www.oreilly.com/library/view/ios-core-animation/9780133440744/

### Creative Tools & Media

- Voice-controlled presentation system:
  https://tow.com/2026/05/02/how-i-controlled-my-slides-with-my-voice-live-at-deep-dish-swift/
  https://tow.com/2026/04/03/action-phrase-voice-control-for-live-production/

- Remotion (video generation):
  https://www.remotion.dev

- WWDC session reference (3D body pose & segmentation):
  https://www.youtube.com/watch?v=WWDC23-placeholder

### Apps & Projects

- Fieldnote (plant journal app):
  https://apps.apple.com/us/app/fieldnote-plant-journal/id6757382315

- Core takeaway:
  - Focus on improving real apps and iterating on existing work
  - Study patterns used in your own projects

### Learning & Career Development

- Interview preparation:
  https://interviewing.io/blog/we-co-wrote-the-official-sequel-to-cracking-the-coding-interview-introducing-beyond-ctci

- Discussion topics:
  - Pattern recognition in interviews
  - Practicing with mock interviews
  - Balancing preparation with full-time work

- Notable ideas:
  - “Best version of you”
  - Emphasis on adaptability and learning across domains (UI, data, graphics)

### Miscellaneous

- Privacy-focused cell phone provider:
  http://calyx.org

- Protocol stack reference:
  https://en.wikipedia.org/wiki/Protocol_stack

- Ed's Lil Finder Guy (Etsy):
  https://www.etsy.com/listing/4489125113/lil-finder-guy-magnetic-poseable-mini

---

## 2026.04.25

### Executive Summary

This session focused on SwiftUI patterns (notably `.refreshable` and task cancellation), growing interest in AI “agent skills” ecosystems, and security considerations in AI systems. There was also discussion around mentorship, career development, and practical engineering wisdom. Several reusable SwiftUI samples and concurrency patterns were shared.

### SwiftUI & Concurrency

- SwiftUI samples:
  https://www.hackingwithswift.com/samples/swiftui

- Refreshable + task cancellation discussion:
  https://antongubarenko.substack.com/p/swiftui-refreshable-task-cancellation?utm_source=substack&utm_medium=email

- Example: `.refreshable` with `defer` for state cleanup

```swift
    struct ContentView: View {
        @State private var items = [1,2,3]
        @State private var isRefreshing = false

        var body: some View {
            NavigationStack {
                ScrollView {
                    VStack {
                        let _ = Self._printChanges()
                        let cells = ForEach(items, id: \.self) { item in
                            Label("List item number \(item)", systemImage: "star.fill")
                        }
                        if isRefreshing {
                            cells.redacted(reason: .placeholder)
                        } else {
                            cells
                        }
                    }
                }
                .refreshable {
                    isRefreshing = true
                    defer { isRefreshing = false }
                    let newItems = [4,5,6]
                    do {
                        for newItem in newItems {
                            items.append(newItem)
                            try await Task.sleep(for: .seconds(1))
                        }
                    } catch {
                        print(error)
                    }
                }
            }
        }
    }
```

- Notable takeaway:
  - “`defer {}` always works” (practical pattern for state cleanup)

### AI & Agent Skills

- Core Data agent skill:
  https://github.com/AvdLee/Core-Data-Agent-Skill

- Swift agent skills collection:
  https://github.com/twostraws/swift-agent-skills

- Mozilla on AI security and zero-day risks:
  https://blog.mozilla.org/en/privacy-security/ai-security-zero-day-vulnerabilities/

### Data & Persistence

- SQLite Data (Point-Free):
  https://github.com/pointfreeco/sqlite-data

### Apple Ecosystem

- Tim Cook community letter:
  https://www.apple.com/community-letter-from-tim/

- Apple developer event:
  https://developer.apple.com/events/view/8D4G7DD8LR/dashboard?ck_subscriber_id=2978341758&utm_source=convertkit&utm_medium=email&utm_campaign=SwiftLee%20Weekly%20-%20Issue%20320%20-%2021464229

### Learning & Media

- Video resources:
  https://www.youtube.com/watch?v=p3NdQL9DND0&list=PLBn01m5Vbs4CYoNYe55G1kijxeNza9SMe&index=10
  https://www.youtube.com/watch?v=ddOFVcZ2X6M
  https://www.youtube.com/watch?v=SQ-bn9iC5gw
  https://www.youtube.com/watch?v=INlzHNbQ9Eg

### Community & Mentorship

- Swift mentorship program:
  https://www.swift.org/mentorship/

- Discussion topics:
  - Mentorship opportunities
  - Interview preparation challenges
  - Balancing full-time work with career growth

### Lil Finder Guy (Etsy) from Ed!
  https://www.etsy.com/listing/4489125113/lil-finder-guy-magnetic-poseable-mini


---

## 2026.04.18

### Executive Summary

This session blended discussion of conference talks (notably Deep Dish Swift), SwiftUI architecture challenges, and advanced state management patterns. A strong theme was the difficulty of animation and motion design in SwiftUI, along with ongoing friction around `@StateObject`, view lifecycle, and UIKit feature gaps. Participants also shared a large collection of Swift articles, architecture references, and tooling resources, alongside some accessibility considerations and AI knowledge tools.

### Conferences & Talks

- Deep Dish Swift:
  https://deepdishswift.com
  https://www.youtube.com/@DeepDishSwift/streams

- Notable talks discussed:
  - *Playing the Long Game as an Indie Developer* — Adam Tow  
  - *Mistakes I Made In Alamofire 5* — Jon Shier  
  - *AltStore: From Hacky Side Project to Legitimate App Store* — Riley Testut  
  - *Surviving in Low Connectivity* — David Beck  
  - *Reverse Engineering the macOS Genie Animation* — Chad Etzel  

- try! Swift:
  https://www.youtube.com/@trySwiftConference  
  https://tryswift.jp/en/

### SwiftUI & State Management

- SwiftUI `Transaction`:
  https://developer.apple.com/documentation/SwiftUI/Transaction

- Keyframe animations:
  https://developer.apple.com/documentation/swiftui/keyframetimeline

- Lazy initialization and `@StateObject`:
  https://fatbobman.com/en/posts/lazy-initialization-state-in-swiftui/
  https://developer.apple.com/documentation/swiftui/stateobject/init(wrappedvalue:)

- Discussion topics:
  - Lifecycle challenges with `@StateObject`
  - View recreation pitfalls
  - Lack of UIKitDynamics equivalent in SwiftUI
  - Difficulty of motion design even before implementation

### Example: `@StateObject` Initialization Pattern

```swift
    struct V: View {
        @State var isOn = true
        var body: some View {
            A(viewModel: VM())
        }
    }

    public struct A: View {
        @StateObject var viewModel: VM
        public init(viewModel makeViewModel: @escaping @autoclosure () -> VM) {
            _viewModel = .init(wrappedValue: makeViewModel())
        }
        public var body: some View {
            Text(viewModel.name)
        }
    }

    public final class VM: ObservableObject {
        var name = "Josh"
        init() {
            print("expensive work")
        }
    }
```

### Swift Architecture & Patterns

- MVVM guidance:
  https://github.com/efremidze/swift-architecture-skill/blob/main/swift-architecture-skill/references/mvvm.md#view-guidance

- Package traits in Xcode:
  https://www.massicotte.org/blog/package-traits-in-xcode/

- Interface Segregation Principle in iOS:
  https://swiftandmemes.com/interface-segregation-principle-in-ios-how-to-prevent-protocol-from-becoming-a-prison/?utm_source=substack&utm_medium=email

### SwiftUI & UI Development

- Building a List replacement:
  https://swiftwithmajid.com/2026/04/06/building-list-replacement-in-swiftui/

- SwiftUI preview testing:
  https://mobilea11y.com/blog/swiftui-preview-testing/?utm_source=substack&utm_medium=email

- Swift Charts discussion (limitations and accessibility concerns)

### Foundation & System APIs

- URL resource values:
  https://developer.apple.com/documentation/foundation/urlresourcevalues

- iOS file system overview:
  https://tanaschita.com/ios-file-system-overview/?utm_source=substack&utm_medium=email

- FormatStyle references:
  https://formatstyle.guide/number/
  https://goshdarnformatstyle.com/numeric-styles/

### AI & Knowledge Tools

- Grove AI Knowledge Base:
  https://apps.apple.com/us/app/grove-ai-knowledge-base/id6759467865?mt=12

### Miscellaneous

- Swift Blog Carnival (tiny languages):
  https://christiantietze.de/posts/2026/04/swift-blog-carnival-tiny-languages

- Jevons paradox:
  https://en.wikipedia.org/wiki/Jevons_paradox

- Cupertino MCP documentation project:
  https://github.com/mihaelamj/cupertino


---

## 2026.04.11

### Executive Summary

This session focused on modern Swift architecture patterns, emerging Apple ML tooling (MLX), and increasing overlap between Swift development and AI workflows. There was notable interest in coordinator-based navigation in SwiftUI, LLM tooling integration, and evolving Swift language features such as Codable redesign discussions.

### SwiftUI & Architecture

- Coordinator pattern for SwiftUI navigation:
  https://medium.com/@wesleymatlock/swiftui-coordinator-pattern-navigation-without-navigationlink-d9ebc5a3388b

- Mihaela M. shared a production-style coordinator implementation:
  https://github.com/mihaelamj/nsspainapi/tree/main/Packages/Sources/SharedModels/Coordinators

- Example navigation project:
  https://github.com/joshuajhomann/PokemonNavigation

### Swift Evolution

- New Codable prototype discussion on Swift Forums:
  https://forums.swift.org/t/new-codable-prototype-available-for-feedback/85186

### Machine Learning & AI

- Apple MLX project:
  https://opensource.apple.com/projects/mlx/

- MLX Swift bindings:
  https://github.com/ml-explore/mlx-swift

- OpenAI Codex use cases for native Apple apps:
  https://developers.openai.com/codex/use-cases/native-ios-macos-apps?utm_source=substack&utm_medium=email

- Andrej Karpathy discussion and notes:
  https://x.com/karpathy/status/2039805659525644595
  https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

### Knowledge Systems & Tooling

- Obsidian-based LLM knowledge system:
  https://github.com/kepano/obsidian-skills

### Miscellaneous

- Privacy-focused services:
  https://calyx.org

- Video resource:
  https://www.youtube.com/watch?v=31OyQa_3gZU

---

## 2026.04.04

### Summary

This session covered a wide range of Swift-adjacent topics, including SwiftUI animation techniques, concurrency discussions, and emerging graphics approaches like Gaussian splatting. Participants shared numerous high-quality resources spanning SwiftUI, Metal, system-level tools, retro computing, and Apple history. There was also discussion of development tooling, emulation environments, and cross-platform workflows.

### Swift & SwiftUI

- Josh H. shared a guide on the SwiftUI Animatable protocol:
  https://www.sagarunagar.com/blog/swiftui-animatable-protocol-guide/?utm_source=substack&utm_medium=email

- Additional SwiftUI text rendering insights:
  https://nilcoalescing.com/blog/AdjustingLineHeightInSwiftUIOniOS26/?utm_source=substack&utm_medium=email

- Ray F. shared updates on Swift:
  https://www.swift.org/blog/whats-new-in-swift-march-2026/

### Concurrency

- Discussion of concurrency models and tradeoffs:
  https://livsycode.com/swift/thread-vs-queue-vs-actor/?utm_source=substack&utm_medium=email

### Graphics & Metal

- Gaussian splatting exploration:
  https://www.unrealtwin.com/gallery/derelict-corridor

- Overview of Gaussian splatting:
  https://medium.com/data-science/a-comprehensive-overview-of-gaussian-splatting-e7d570081362

- Metal-based implementation:
  https://github.com/scier/MetalSplatter

### Tools & Libraries

- PAR2 command line tools:
  https://github.com/Parchive/par2cmdline

- Swift logging server:
  https://github.com/krugazor/SwiftLoggerServer

- SwiftBasic project:
  https://github.com/jeradesign/SwiftBasic

- Cadova (creative coding / graphics tool):
  https://github.com/tomasf/Cadova

### Apple Ecosystem & History

- WWDC video index (including delisted content):
  https://nonstrict.eu/wwdcindex/

- Steve Jobs archive downloads:
  https://stevejobsarchive.com/publications/download

- Apple: The First 50 Years (book):
  https://books.apple.com/us/book/apple/id6749329845

- Remastered 1984 Apple ad:
  https://www.youtube.com/watch?v=ErwS24cBZPc

### Development & Systems

- Ubuntu installation references (Carlyn C.):
  https://documentation.ubuntu.com/desktop/en/24.04/tutorial/install-ubuntu-desktop/
  https://linuxsimply.com/linux-basics/os-installation/dual-boot/ubuntu-on-mac/
  https://www.youtube.com/watch?v=KIgxEEzT9ek
  https://linuxiac.com/linux-swap-explained-do-you-need-it/
  https://www.youtube.com/watch?v=aUbHiKVRAAw

- macOS recovery issue troubleshooting:
  https://mrmacintosh.com/how-to-fix-the-recovery-server-could-not-be-contacted-error-high-sierra-recovery-is-still-online-but-broken/

### Emulation & Retro Computing

- iPod emulator:
  https://mitchivin.github.io/ipod/

- OpenEmu:
  https://openemu.org

- Virtual II:
  https://www.virtualii.com

- Merlin cross-development tools:
  https://www.brutaldeluxe.fr/products/crossdevtools/merlin/

### App Release Announcement!

Ed developed a new protein visualizing Vision Pro app:

- VisionProtein:
  https://visionprotein.com

---

## 2026.03.28

### Executive Summary

This session centered on upcoming Apple events (WWDC26), Swift evolution (including Swift 6.3 and networking discussions), and the growing intersection of Swift with AI agent tooling. There was also active discussion around concurrency primitives, AsyncStream use cases, and emerging libraries. Participants shared resources spanning accessibility tooling, long-running AI application design, and developer ecosystem events.

### Apple Ecosystem & Events

- WWDC 2026:
  https://developer.apple.com/wwdc26/

- Self Service Repair (official Apple parts):
  https://selfservicerepair.com/en-US/home

- Community-driven WWDC events:
  https://communitykit.social/
  https://www.meetup.com/core-coffee-a-catch-up-for-ios-and-macos-developers/events/313900770

- Conferences:
  https://swiftsonicconf.com
  https://omt-conf.com

### Swift Evolution

- Swift 6.3 release:
  https://www.swift.org/blog/swift-6.3-released/

- Swift networking vision:
  https://github.com/swiftlang/swift-evolution/blob/main/visions/networking.md?utm_source=substack&utm_medium=email

- Yielding accessors proposal:
  https://github.com/swiftlang/swift-evolution/blob/main/proposals/0474-yielding-accessors.md

- SwiftUI environment value (`appearsActive`):
  https://developer.apple.com/documentation/swiftui/environmentvalues/appearsactive

### Concurrency & Async Patterns

- TaskGate (concurrency utility):
  https://github.com/mattmassicotte/TaskGate?utm_source=substack&utm_medium=email

- Queue implementation discussion:
  https://github.com/mattmassicotte/Queue/blob/main/Sources/Queue/AsyncQueue.swift

- Discussion topics:
  - AsyncStream for server-sent events (SSE)
  - Cross-platform networking challenges (macOS/Linux)

### AI & Agent Tooling

- Blender MCP integration:
  https://github.com/ahujasid/blender-mcp

- Google Stitch:
  https://stitch.withgoogle.com

- Anthropic long-running app design:
  https://www.anthropic.com/engineering/harness-design-long-running-apps

- Agent skill selection framework:
  https://www.avanderlee.com/ai-development/a-9-step-framework-for-choosing-the-right-agent-skill/?utm_source=substack&utm_medium=email

- iOS Accessibility Agent Skill:
  https://github.com/dadederk/iOS-Accessibility-Agent-Skill?ck_subscriber_id=2978341758&utm_source=convertkit&utm_medium=email&utm_campaign=SwiftLee%20Weekly%20-%20Issue%20314%20-%2020983352

- Sentry skill tooling:
  https://warden.sentry.dev/
  https://github.com/getsentry/skills/tree/main/plugins/sentry-skills/skills/skill-scanner

## Tooling & Issues

- Firebase / Xcode compatibility issue:
  https://github.com/firebase/firebase-ios-sdk/issues/15974


  ---


## 2026.03.21

You can now script the browser using Swift.

- https://github.com/m1guelpf/swift-playwright
  


### Concurrency Notes
  
- https://soumyamahunt.medium.com/what-you-should-know-before-migrating-from-gcd-to-swift-concurrency-74d4d9b2c4e1
- https://github.com/mattmassicotte/Queue
  

### Avoid Spacers

  https://nerdyak.tech/development/2023/04/06/avoid-swiftui-spacers-in-stacks.html
  

### Adding a timeout to an async function

```swift
  enum TimeoutError: Error {
    case timedOut
  }
  
  func withTimeout<T: Sendable>(_ duration: Duration, 
                                operation: @Sendable @escaping () async throws -> T) async throws -> T {
    try await withThrowingTaskGroup(of: T.self) { group in
  
      // Task 1: your actual work
      group.addTask {
        try await operation()
      }
  
      // Task 2: timeout
      group.addTask {
        try await Task.sleep(for: duration)
        throw TimeoutError.timedOut
      }
  
      let result = try await group.next()!
      group.cancelAll()
      return result
    }
  }
```

### Copy-On-Write COW

Dicussed copy on write and how it preserves value semantics and isolation.

- https://livsycode.com/swift/copy-on-write-in-swift-semantics-misconceptions-and-a-custom-implementation/

- https://async.techconnection.io/talks/swift-connection/swift-connection-2024/rick-van-voorden-swift-cowbox-easy-copy-on-write-semantics-for-swift-structs
  
- https://github.com/Swift-CowBox/Swift-CowBox

- https://www.hackingwithswift.com/example-code/language/what-is-copy-on-write


## VisionPro App for Visualizing Proteins

Ed's VisionPro app is available for pre-order and shipping on April 1!

- https://visionprotein.com


## Understanding Lifetime

To prepare us to understand some of the new Swift Evolution proposals, Josh took
us on a playground quick tour through:

- consuming
- consume
- borrowing
- copy
- inout
- mutating
- sending


```swift
  struct V {
      var w: String
      init(w: String) {
          self.w = w
      }
      func make(_ x: consuming String) -> String {
          x.append("a")
          print(x)
          return consume x
      }
      func a(_ x: String) {
          var y = x
          y.append("a")
          print(y)
      }
      func b(_ x: borrowing String) {
          var y = copy x
          y.append("a")
          _ = x
      }
      func c(_ x: inout String) {
  
      }
      mutating func f() {
          w = ""
      }
      consuming func close() -> String {
          ""
      }
      func r(_ x: sending NSView) -> NSView {
          consume x
      }
  }
  
  let r = "a"
  let v = V(w: r)
  print(r)
  let s = "hello"
  v.a(s)
  v.make(r)
  print(r)
```  

---


## 2026.03.14


### Faster Grep

This has come up a few times.  "rg" is a command line tool that works
faster than awk and grep and automatically respects .git rules. It is 
open source (MIT) and written in Rust.

- https://github.com/BurntSushi/ripgrep
  
### Model Agnostic Agent

- https://opencode.ai
  

### APNs

  Apple APN 
  - https://developer.apple.com/documentation/usernotifications/sending-notification-requests-to-apns
  

  https://developer.apple.com/documentation/storekit/implementing-promotional-offers-in-your-app
  
### Apple: The First 50 Years

- https://amzn.to/4lwJHt5
  

### iTrace

Handwriting practice app from Alex!

- https://apps.apple.com/us/app/itrace-handwriting-practice/id645416621
  

### iRelay

Send commands to an AI agent from iMessage from Mihaela!

- https://github.com/mihaelamj/iRelay

How it works:
  
```
iPhone (iMessage) → Mac (iRelay daemon) → Claude Code → response → iMessage
```

### Apple Neo

- https://hardcoresoftware.learningbyshipping.com/p/239-mac-neo-and-my-afternoon-of-reflection
  

### AI Agent Kanban Tool - Symphony

- https://github.com/openai/symphony?tab=readme-ov-file
  

### Chris Lattner and Modular

Brief history of LLVM. Modular and Mojo. LLVM for AI chips.  

- https://youtu.be/dYk-bt9BFIs?t=4326

  
"People who ignore this [AI] will be left behind."

### Differential Fuzzing

- https://github.com/graydon/dac-wasm
  
### Pictures of Apple Silicon M1 Die

- https://x.com/Locuza_/status/1450271726827413508/photo/1
  
### Aticles of Interest

- https://www.sagarunagar.com/blog/geometry-in-swiftui/
- https://medium.com/@oscarberggren082/swiftui-charts-caused-major-stutter-in-my-app-replacing-it-with-path-fixed-everything-9b15059efeae
- https://sundayswift.com/posts/building-a-high-performance-list-framework/
- https://azamsharp.com/2026/03/04/mvvm-and-cost-of-old-patterns.html

---

### 2026.03.07

### Memory Safety

- https://youtu.be/oV6mC8Rt1kY?si=OyGoIeS2cjFAIztA
  

### Foundation Generable

- https://developer.apple.com/documentation/foundationmodels/generable
  

Making reproducible outputs:

- https://developers.openai.com/cookbook/examples/reproducible_outputs_with_the_seed_parameter/
  

Model personalization

- https://developer.apple.com/documentation/coreml/model-personalization
  

### Tools: Git, VS Code, Worktrees

- https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens
- https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github
- https://git-scm.com/docs/git-worktree
- Keyboard Maestro recommended by Bob


### Metatopic: Learning

- https://www.simplypsychology.org/learning-kolb.html
- https://ldaustralia.org/information-resources/response-to-intervention/
  
---

## 2026.02.28
  
2026-02-28 09:48:07 From Josh Homann to Everyone:
  https://www.youtube.com/watch?v=69Gw7aoWMMI
  
2026-02-28 09:53:15 From SWEET Institute to Everyone:
  What are is your opinion on server driven UI?

### Dynamic Animator

Josh reminded us that dynamic animator is part of UIKit.
  
- https://github.com/joshuajhomann/DynamicAnimatorAttachment
- https://github.com/joshuajhomann/DynamicRadialGravity

Mihaela reminds us that these things can be done with Core Animation.

```swift
  let spring = CASpringAnimation(keyPath: "position.y")
  spring.fromValue = layer.position.y
  spring.toValue = layer.position.y + 200
  
  
  spring.mass = 1.0
  spring.stiffness = 100
  spring.damping = 10
  spring.initialVelocity = 0
  
  
  spring.duration = spring.settlingDuration
  
  
  layer.add(spring, forKey: "springMove")
  layer.position.y += 200 // update model layer
```

Carlyn reminds us of other affordances in SwiftUI

- https://developer.apple.com/documentation/swiftui/view/visualeffect(_:)
- https://www.hackingwithswift.com/quick-start/swiftui/how-to-add-metal-shaders-to-swiftui-views-using-layer-effects
  

### A Google PM Vibe Codes Palantir

From Josh. Not really Swift related, but speaks to the idea of having a clear goals and specifying what you want a product to be.
  
- https://www.youtube.com/watch?v=rXvU7bPJ8n4


### Strings, Regex and Benchmarking

We looked at different implementations of string replacement. At first we thought 
Swift string was the winner but then Tobias noticed that the units were milliseconds
instead of microseconds.

-  https://www.swift.org/blog/benchmarks/

Related is the topic of "new" serialization.

- https://forums.swift.org/t/the-future-of-serialization-deserialization-apis/78585

RG is a fast version of Grep: https://github.com/BurntSushi/ripgrep
  
Alex reminds us that regular expressions can be hard.

- https://pdw.ex-parrot.com/Mail-RFC822-Address.html
  
Helpful for learning regex.

- https://regex101.com
  
And a great WWDC video from Michael Ilseman

- https://developer.apple.com/videos/play/wwdc2022/110357/

  
### WendyOS

A Swift First embedded operating system (linux distro)

- https://forums.swift.org/t/wendyos-a-swift-first-embedded-linux-distro/84478
  

### Cool conferences coming

- Nvidia https://www.nvidia.com/gtc/
- siggraph https://s2026.siggraph.org
  
---

## 2026.02.21

We talked a bunch about different AI tools and got an interesting demo from Tobias about
a Mac app he wrote for keeping track of web articles.

- https://ghuntley.com/ralph/

Talked about using Codex and Claude with worktrees.  It lets you try out a bunch of 
solutions in parallel.

- https://code.claude.com/docs/en/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees 
  
### Natural Language

Just for fun project by Carlyn to do proper title case for a given style guide.  

- https://github.com/carlynorama/StyleGuided
  
  
### Testing Shareplay

Ed wants to test his Vision Pro app without buying another Vision Pro.

- https://medium.com/@xinyichen0321/the-easiest-way-to-test-shareplay-on-visionos-apps-7bf8a1753d8e
 

### The Popularity of Swift

This month, Swift is just ahead of COBOL at position 21.

- https://www.tiobe.com/tiobe-index/
  
  
### Articles of Interest

Josh brought up some articles to read.

Copy-on-write pattern.

- https://www.sagarunagar.com/blog/copy-on-write-swift

Building a toast component. Good interview topic because it gets to
if you understand the view hierarchy.

- https://livsycode.com/swiftui/building-a-toast-component-in-swiftui

More on Observable.

- https://swiftandmemes.com/how-to-migrate-to-observable-without-breaking-your-app
  

---

## 2026.02.14

### Swift Arctic Conference

Frank was back from https://arcticonference.com which was a great conference. Not recorded but some of the speakers indicated that they would post their talks. One of those was ElementaryUI which Josh shared a link to.

- https://elementary.codes

### AI, Engineering, and Industry Updates

**Josh Homann shared:** 
- https://shumer.dev/something-big-is-happening
- https://openai.com/index/new-result-theoretical-physics/
- https://openai.com/index/introducing-gpt-5-3-codex-spark/
- https://openai.com/index/harness-engineering/


Josh feels that the industry is at a major transition and early adopters will benefit.

Ed Arenberg shared:

- https://www.cerebras.ai/chip
- https://www.cerebras.ai/system

Carlyn raised concerns about AI being over-hyped in a *crypto-bro-style* way. There are indications that it is having a significant negative impact on open-source projects.

- https://theshamblog.com/an-ai-agent-published-a-hit-piece-on-me/

Also,

- https://tante.cc/2026/02/14/diffusion-of-responsibility/

Ray shared anecdotal experiences about AI being useful but not getting to a full solution. He also raised some concerns about "The Point Free Way"--a new skills constellation that has strict license requirements.

### Bioinformatics and Protein Structures

Ed gave a demo of his VisionPro app that he has been building with Xcode 26.3 and claude code. It gives rich visualizations of large proteins and even unfolds them visually.  It reads in proteins in pdb format shows them.

**carlyn shared:** - https://rothemundlab.caltech.edu

**Ed Arenberg shared:** 

- https://pdb101.rcsb.org
- https://www.rcsb.org
- https://files.wwpdb.org/pub/pdb/doc/format_descriptions/Format_v33_Letter.pdf

**Josh Homann shared:** 
- https://github.com/Androp0v/BioViewer

Discussion included: - Ribbon diagrams - PDB file structure and
specification (\~170 pages) - Protein visualization tools

### Fonts

https://typeof.net/Iosevka/


### Swift topic for next time

Alex shared:

https://github.com/swiftlang/swift-evolution/blob/main/proposals/0504-task-cancellation-shields.md

---

## 2026.02.07

### AI, Tooling, and Agentic Coding
- **Josh Homann** shared Apple documentation on allowing agentic coding tools to access Xcode:  
  https://developer.apple.com/documentation/xcode/giving-agentic-coding-tools-access-to-xcode

- **Josh Homann** shared OpenAI’s announcement of the Codex app:  
  https://openai.com/index/introducing-the-codex-app/

- **carlyn** shared a discussion on Mastodon arguing that AI can be a barrier to innovation because it relies on existing code patterns rather than enabling fundamentally new ideas:  
  https://mastodon.social/@mrtoto@mrtoto.net/116029868243712977  
  **Ray Fix** reacted positively to the discussion.

- **Josh Homann** shared an article on Kimi K2.5 and its free API:  
  https://medium.com/data-science-in-your-pocket/kimi-k2-5-free-api-b4ce65a14dd3

- **Josh Homann** shared an Ars Technica article describing multiple Claude AI agents collaborating to create a new C compiler:  
  https://arstechnica.com/ai/2026/02/sixteen-claude-ai-agents-working-together-created-a-new-c-compiler/

- **carlyn** shared a post from Adafruit’s Limor Fried discussing AI usage:  
  https://mastodon.social/@adafruit@fosstodon.org/116029624511670210

- **Josh Homann** shared Steve Yegge’s essay “Welcome to Gas Town”:  
  https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04

- **Chitaranjan sahu** shared a post emphasizing that the future is not about AI replacing programmers, but about people who think clearly about systems moving faster while others generate low-quality output at scale:  
  https://x.com/ryolu_/status/2019089085034586239

### Swift, Performance, and Language Topics
- **Ray Fix** shared a talk titled *How Apple Replaces Entire Frameworks* by Bryce Bostwick:  
  https://www.youtube.com/watch?v=SuQGQ1vh9k0

- **Ray Fix** shared the related GitHub repository *SwizzleEverything*:  
  https://github.com/brycebostwick/SwizzleEverything/

- **Ray Fix** shared the talk *Closing the Performance Gap Between Swift and C* by Paul Toffoloni:  
  https://www.youtube.com/watch?v=-pbd2wkdpD8

- **Ray Fix** shared *Swift in the Browser with ElementaryUI* by Simon Leeb:  
  https://www.youtube.com/watch?v=OmQ881sOTIc  
  **carlyn** asked how ElementaryUI relates to ElementaryOS.

- **Ray Fix** shared *Introducing the Swift SDK for Android* by Marc Prud’hommeaux:  
  https://www.youtube.com/watch?v=mZNIAuQ7s7k

- **Josh Homann** shared references on method swizzling and dynamic method replacement in Swift:
  - Swift underscored attributes documentation:  
    https://github.com/swiftlang/swift/blob/main/docs/ReferenceGuides/UnderscoredAttributes.md
  - Swift Forums discussion on dynamic method replacement:  
    https://forums.swift.org/t/dynamic-method-replacement/16619

### Swift Ecosystem, Blogs, and Resources
- **Josh Homann** shared the Point-Free website. They have a new version of The Composable Architecture (TCA 2.0) and a bunch of skills that implement "The Point-Free Way"
  https://www.pointfree.co

- **Josh Homann** shared a YouTube video about a scientist's view of AI:  
  https://www.youtube.com/watch?v=PctlBxRh0p4

- **carlyn** shared a Psychology Today article on curiosity deficits:  
  https://www.psychologytoday.com/us/blog/the-curiosity-deficit

- **Josh Homann** shared the SwiftSonic conference Sessionize page:  
  https://sessionize.com/swiftsonic-26

- **Josh Homann** shared the SwiftSonic conference website:  
  https://swiftsonicconf.com

- **Chitaranjan sahu** shared a tweet by Chris Lattner related to LLVM and compiler topics:  
  https://x.com/clattner_llvm/status/2020107665566036122?s=20

- **Josh Homann** shared an article on tiered caching in Swift:  
  https://kylebrowning.com/posts/tiered-caching-in-swift/?utm_source=substack&utm_medium=email

- **Josh Homann** shared a Levels.fyi job listing:  
  https://www.levels.fyi/jobs?locationSlug=united-states&jobId=141351424356164294

- **Josh Homann** shared a GitHub repository for SwiftUI Agent skills:  
  https://github.com/AvdLee/SwiftUI-Agent-Skill?utm_source=substack&utm_medium=email

- **Josh Homann** shared a Captain SwiftUI Substack article on observation and SwiftUI complexity:  
  https://captainswiftui.substack.com/p/objectively-better-observably-trickier?utm_campaign=post-expanded-share&utm_medium=post%20viewer&triedRedirect=true

- **Josh Homann** shared a SwiftDifferently article on SwiftUI performance:  
  https://www.swiftdifferently.com/blog/swiftui/swiftui-performance-article?utm_source=substack&utm_medium=email

- **Josh Homann** shared an article on exploring Xcode using MCP tools and external clients:  
  https://rudrank.com/exploring-xcode-using-mcp-tools-cursor-external-clients

- **Josh Homann** shared the XcodeBuild MCP project website:  
  https://www.xcodebuildmcp.com

- **Tobias** mentioned *xclaude* and shared the related GitHub plugin:  
  https://github.com/conorluddy/xclaude-plugin


## 2026.01.31

### Swift Blog
  - Announcing the Swift Windows Workgroup  
    https://www.swift.org/blog/announcing-windows-workgroup/
  - What’s New in Swift — January 2026  
    https://www.swift.org/blog/whats-new-in-swift-january-2026/

### Stanford CS193p      

- https://cs193p.stanford.edu

Continues to be useful. Interesting how course content has shifted over the years.

### Other University Courses
  - MIT OpenCourseWare  
    https://ocw.mit.edu
  - MIT 6.001 — *Structure and Interpretation of Computer Programs* (Spring 2005)  
    https://ocw.mit.edu/courses/6-001-structure-and-interpretation-of-computer-programs-spring-2005/
  - MIT 6.0001 — *Introduction to Computer Science and Programming in Python*  
    https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/
  - Coursera Instructor Page (Alex)  
    https://www.coursera.org/instructor/~873260
  - Scala Functional Programming Course  
    https://www.coursera.org/learn/scala-functional-programming
  - Scala Specialization  
    https://www.coursera.org/specializations/scala

### SwiftUI*
  - SwiftUI Lab (older but still useful)  
    https://swiftui-lab.com

### Swift, Architecture, and App Design
- Swift Actors pitfalls  
  https://www.fractal-dev.com/blog/swift-actors-pitfalls
- objc.io talk — *Solving the View Model Problem (Part 1)*  
  https://talk.objc.io/episodes/S01E476-solving-the-view-model-problem-part-1
- Liquid Glass Toast  
  https://writetodisk.com/liquid-glass-toast/


### Philosophy, Cognition, and AI
- Ordinary Language Philosophy  
  https://en.wikipedia.org/wiki/Ordinary_language_philosophy
- Embodied Cognition  
  https://en.wikipedia.org/wiki/Embodied_cognition  
  (Related to *An Immense World* by Ed Yong)

### Security, Privacy, and Tooling
- Discussion on risks of tools with email access
- Recommendation to use a fully separate “burner computer” for sensitive experimentation
- UTM (virtual machines on macOS)  
  https://mac.getutm.app


### Moltbook - A dicussion board for agents.
- https://www.moltbook.com  

- Speaking of burner computers and the need for virtual machines. 
  https://www.reddit.com/r/accelerate/comments/1qrr3he/a_real_security_problem_just_showed_up_on/

---

## 2026.01.24

### Consciousness and AI

Josh shares that Anthropic's CEO talks about how AI is growing exponentially. That changes everything.

- https://www.youtube.com/watch?v=Ckt1cj0xjRM

Some links from Ray:

- https://www.preposterousuniverse.com/podcast/2026/01/05/339-ned-block-on-whether-consciousness-requires-biology/
- https://philarchive.org/rec/BLOCOM-3
  
Carlyn recommends “An Immense World” by Ed Yong
  
- https://en.wikipedia.org/wiki/An_Immense_World

Josh hypothesises that language might not matter in a year's time.

### Android and Swift

There is a post on the Swift blog:

https://www.swift.org/blog/exploring-the-swift-sdk-for-android/

Also,
  
- https://github.com/skiptools/skip

###  Ralph

Small mini-projects that can fit into context that runs in a loop.

- https://ghuntley.com/ralph/
- https://www.youtube.com/watch?v=RpvQH0r0ecM
- https://github.com/snarktank/ralph
  
### Figma and AI

- https://help.figma.com/hc/en-us/articles/35280808976151-Figma-MCP-collection-MCP-collection-overview

---


## 2026.01.17

### AI Tooling, Agents, and Codex
- **Josh Homann** shared resources related to AI coding tools and agent workflows:
  - Claude Cowork introduction  
    https://support.claude.com/en/articles/13345190-getting-started-with-cowork
  - OpenCode  
    https://opencode.ai
  - OpenAI Codex repository (shared twice during the meeting)  
    https://github.com/openai/codex
  - Codex Skill Manager  
    https://github.com/Dimillian/CodexSkillManager
  - Curated list of agent skills  
    https://github.com/heilcheng/awesome-agent-skills?tab=readme-ov-file

### Swift Concurrency & Logging
- **Peter Wu** raised a question about **global actor lifecycle**, and specifically:
  - Lifecycle of custom (unowned) executors owned by a global actor.

### Logging

Josh noted that requiring an async context for clients wanting to use analytics is a high hurdle. Better off to just use locks / mutex and have synchronous method calls.

- **Mihaela MJ** shared a gist related to the discussion:  
  https://gist.github.com/mihaelamj/ca6b3955f47217d976111b9164d8d927

- Apple’s Swift logging library:  
  https://github.com/apple/swift-log/tree/main

### Cupertino & MCP Integration
- **Mihaela MJ** shared her Cupertino repository that got a mention on https://iosdevweekly.com/

- https://github.com/mihaelamj/cupertino

- **Josh Homann** showed how to add Cupertino to Codex via MCP:

```
  codex mcp add cupertino -- /usr/local/bin/cupertino serve
```

### Hardware Hacking & Security

- **Mihaela MJ** mentioned Flipper Zero, followed by the official site:  
  https://flipper.net
- **Carlyn** shared several articles related to car hacking and replay/CAN injection attacks:
  - Wired article on a tiny hacking device:  
    https://www.wired.com/2015/08/hackers-tiny-device-unlocks-cars-opens-garages/
  - Replay attack discussion:  
    https://tcm-sec.com/intro-to-car-hacking-replay-attacks/
  - Ars Technica on CAN injection attacks:  
    https://arstechnica.com/information-technology/2023/04/crooks-are-stealing-cars-using-previously-unknown-keyless-can-injection-attacks/


### Haiku's from Ed (or possibly his AI)

```
    All speech is Haiku
    No other way to converse
    Words are poetic
```

```
    PR obsolete
    Just let AI fix it all
    No more code reviews
```

```
    Humans make Haiku
    AI just steals from people
    Creativity
```

```
    Zooming with AIs
    No more humans required
    Meetings so lonely
```

---

## 2026.01.10

### Highlights & Discussion

- The **Pipe** project was shared and discussed, including recent architectural changes (shared by Peter Wu):
  - Repository: https://github.com/PeterWu9/Pipe
  - Pipe is no longer an `AsyncSequence`.
  - Pipe now vends an `AsyncStream`.
  - Additional updates were pushed incorporating feedback from Josh Homann.

- A concurrency observation was raised that `async let` does not always result in parallel execution in practice (noted by Peter Wu).

### Articles to Read

- Several resources on approachable Swift concurrency and recent community discussion were shared (by Josh Homann):
  - https://fuckingapproachableswiftconcurrency.com/en/?utm_source=substack&utm_medium=email
  - https://thosewhoswift.substack.com/p/those-who-swift-issue-248

- An article exploring a new way of working with Metal shaders in SwiftUI was shared (by Josh Homann):
  - https://medium.com/@victorbaro/metalgraph-a-new-way-of-working-with-metal-shaders-for-swiftui-bed1cf1a2b81

- Visual and dataflow programming nostalgia was discussed, referencing tools such as Max/MSP/Jitter and PureData (shared by carlyn).

- A code analytics and exploration tool was recommended (shared by carlyn):
  - DeepWiki: https://deepwiki.com

### AI and Robots
  - Hugging Face LeRobot (shared by Ed Arenberg): https://github.com/huggingface/lerobot
  - NVIDIA Isaac Sim (shared by carlyn): https://developer.nvidia.com/isaac/sim

### Skills! (via Josh Homann):
  - https://github.com/anthropics/skills
  - https://github.com/Dimillian/Skills
  - https://www.linkedin.com/posts/ajvanderlee_introducing-the-swift-concurrency-ai-agent-activity-7414656677767069697-qnXN/

- A broader philosophical discussion touched on the idea that English (human-readable text) is becoming a programming language (remark by Georgi Dagnall), and that some modern “AI” systems resemble markdown-driven plugin frameworks (observed by carlyn).

## 2025.01.03

### Build times

We discusses using [tuist](https://docs.tuist.dev/en/) to reduce build times by pre compiling.  
[Video](https://youtu.be/wCVPWJvJGng?si=Eo5lNP0JQoI8xx6N) shared by ChitaRanjan


### Pipe
We reviewed the various implementations of pipe from last year and discussed how to iterate over the pipe:
```swift
public final class Pipe<Value: Sendable>: Sendable, AsyncSequence {
    public typealias Stream = AsyncStream<Element>
    public typealias AsyncIterator = Stream.AsyncIterator
    public typealias Element = Value
    private let lockedContinuations: Mutex<[UUID: Stream.Continuation]>
    private let replayCount: Int
    public init(replay: Int = 0) {
        replayCount = replay
        lockedContinuations = .init([:])
    }
    deinit {
        lockedContinuations.withLock { continuations in
            continuations.values.forEach { $0.finish() }
        }
    }
    public func send(_ value: Value) {
        lockedContinuations.withLock { continuations in
            continuations.values.forEach { $0.yield(value) }
        }
    }

    public func makeAsyncIterator() -> AsyncIterator {
        let (stream, continuation) = Stream.makeStream(of: Element.self,
                                                       bufferingPolicy: .bufferingNewest(replayCount))
        let id = UUID()
        continuation.onTermination = { [weak self] _ in
            self?.lockedContinuations.withLock { $0[id] = nil }
        }
        lockedContinuations.withLock { $0[id] = continuation }
        return stream.makeAsyncIterator()
    }
}
```

A sequence is just an iterator factory and a for loop is syntactic sugar for making an iterator and looping over it (async or not):
```swift
let pipe = Pipe<Int>()
let array = [1, 3, 5, 7, 9]

Task {
    for value in array { }
    var i = array.makeIterator()
    while let value = i.next() {

    }
    for await value in pipe {
        print(value)
    }
    var iterator = pipe.makeAsyncIterator()
    while let value = await iterator.next() {
        print(value)
    }
}

```

### Context engineering
We discussed context engineering as outlined in [this video](https://www.youtube.com/watch?v=VvkhYWFWaKI) and [these notes](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md)
We discussed how to refine the prompt from december to produce better code by not cluttering the context window:
* [Software requirements GPT](https://chatgpt.com/g/g-nixs0I0zV-software-requirements-specification-generator) shared by Carlyn
* [How coding agents explore your codebase](https://www.intent-systems.com/learn/intent-layer) shared by ChitaRanjan
* [Does the iOS code matter?](https://blog.jacobstechtavern.com/p/the-year-swiftui-died) blog post shared by Josh
