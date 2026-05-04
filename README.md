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
