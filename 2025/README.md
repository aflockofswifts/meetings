# A Flock of Swifts - 2025

## 2025.12.27

### Review of **What’s New in Swift**:
  - https://www.swift.org/blog/whats-new-in-swift-december-2025/
  - Swift underscored attributes such as `@_transparent`, `@inline(always)`, and `@_disfavoredOverload`
  - Swift underscored attributes guide:  
    https://github.com/swiftlang/swift/blob/main/docs/ReferenceGuides/UnderscoredAttributes.md
  - Swift Collections: https://github.com/apple/swift-collections

### Tooling Discussed
- Tooling ecosystem discussions:
  - JetBrains IDEs and IntelliJ IDEA:
    - https://www.jetbrains.com/idea/
  - SKIE for Kotlin Multiplatform ↔ Swift interop:
    - https://skie.touchlab.co

### Improving the `with` function

The original version:

```swift
@discardableResult public func with<Item>(_ item: Item, update: (inout Item) throws -> Void) rethrows -> Item {
    var copy = item
    try update(&copy)
    return copy
}
```

The improved version using inlinable and consuming:
    
```swift
@inlinable
@discardableResult
public func with<T>( _ value: consuming T, update: (inout T) throws -> Void) rethrows -> T {
    var taken = consume value
    try update(&taken)
    return taken
}
```

The semantics beween the two are subtly different. The first is copy-initialize, the second is take/move-initialize. It always prevents the copy which is closer to what we wanted to do originally but couldn't without the consuming/consume language features.

---

## 2025.12.20

### Swift Evolution
- Discussion of Swift Evolution topics, including **extensible enums**:
  - https://github.com/swiftlang/swift-evolution/blob/main/proposals/0487-extensible-enums.md
- Discussion around **OptionSet**, bit masking, and performance-sensitive code:
  - https://developer.apple.com/documentation/swift/optionset
- Exploration of compile-time behavior and inspection using **SIL**:
  - `swiftc -emit-sil MyFile.swift > MyFile.sil`
  - Compiler exploration via Godbolt

### Tooling and Workflow
- Tooling and workflow discussions:
  - CLI workflows vs Xcode UI (CLI often faster and clearer)
  - Xcode system prompts repo: https://github.com/artemnovichkov/xcode-26-system-prompts
  - Swift install instructions: https://www.swift.org/install/macos/
- Educational resources shared:
  - Updated Stanford CS193p course: https://cs193p.stanford.edu
  - Point-Free SQLiteData episode (re-shared)

### Offline Maps
  - Mapbox offline maps: https://docs.mapbox.com/android/maps/guides/offline/
  - HERE SDK: https://www.here.com/platform/here-sdk
  - MapKit region caching considerations
  - FAA VFR and IFR charts:
    - https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/vfr/
    - https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/ifr/

### Compensation Levels
  - Compensation data discussion via https://www.levels.fyi/2025/
  - Computer History Museum and software history resources


### Advent of Code
  - Advent of Code 2025: https://adventofcode.com/2025/day/1

```swift
func output(from input: String) -> Int {
    let lines = input.split(separator: "\n")
    var position = 50
    var count = 0
    for line in lines {
        let value = Int(line
            .replacing("L", with: "-")
            .replacing("R", with: "")
        )!
        position += (value + 100)
        position %= 100
        count += position == 0 ? 1 : 0
    }
    return count
}
    
func output2(from input: String) -> Int {
    sequence(state: Scanner(string: input)) { scanner -> Int? in
        let sign = scanner.scanCharacter() == "L" ? -1 : 1
        guard let value = scanner.scanInt() else { return nil }
        return sign * value
    }
    .reduce(into: (position: 50, count: 0)) { accumulated, next in
        accumulated.position += next + 100
        accumulated.position %= 100
        accumulated.count += accumulated.position == 0 ? 1 : 0
    }
    .count
}
```

---

# 📅 December 13, 2025 — AI-Driven App Scaffolding & Specs

**Themes:** Agent-driven development, specifications, modern Swift tooling

- Discussion of an article highlighting a large productivity gap between AI power users and others, motivating interest in AI-assisted development workflows.  
  - https://venturebeat.com/ai/openai-report-reveals-a-6x-productivity-gap-between-ai-power-users-and
- Ongoing focus on the **vibe-tvmaze** project:  
  - https://github.com/aflockofswifts/vibe-tvmaze
- Proposal to use an **AGENTS.md** file as a formal, machine-readable specification for code generation.
- Detailed app specification discussed:
  - Universal app targeting **iOS, iPadOS, macOS Catalyst, and visionOS**
  - Search TV shows via the **TVMaze API**
  - Two primary views: **Search** (with recent history) and **Favorites**
  - Favorites support for both shows and episodes, including reordering and swipe-to-delete
  - Show detail view with episode list and favorite toggles
  - Episode detail view with favorite toggles
  - Deep linking via show ID or episode ID (push notifications or custom URL scheme)
  - Offline caching support
  - Full testability
  - Analytics service capturing all user interactions (mock backend initially)
  - Modern Swift features: structured concurrency, `@Observable`; **no Combine**
  - Project generation via **xcodegen**
- Demonstration and discussion of **Codex CLI** usage (`brew install codex`) and fully automated app scaffolding.
- Brief troubleshooting of authentication and MCP startup issues.
- Additional links and side discussions:
  - Point-Free SQLiteData episode: https://www.pointfree.co/episodes/ep347-tour-of-sqlitedata-basics
  - Mermaid vs Graphviz (`dot`)
  - Claude agents and tools documentation
- General agreement that **clear specs dramatically improve AI-driven development**.

---

## 2025.12.13

### Vibe coding an app

Motivated by  - https://venturebeat.com/ai/openai-report-reveals-a-6x-productivity-gap-between-ai-power-users-and we explored vibe coding by asking chatGPT to write an AGENTS.md file with this 30 second voice prompt:

```swift
I want you to write a AGENTS.md file to generate a universal iOS, iPadOS, visionOS and macOS Catalyst app that allows the user to search for TV shows using the TV maze API from https://www.tvmaze.com/api . The app should have two tabs or sidebar items: one for search and the other for favorites. The search tab should have recent history.  The favorites tab should show favorite shows and favorite episodes. The favorite tab should support re-ordering and swipe actions to delete items. Tapping on a show result in either view should show an episode list for the show with a button to toggle the favorite for the show. Tapping on an episode should open the details for that episode a button to toggle the favorite for the episode. The app should support deep linking by either show ID or episode ID in a push notification or custom URL scheme. The data should be cached for offline access.  The entire app needs to be testable. There should be an analytics service that reports analytic events for all user interactions. The analytics can go to a mock analytic service for now.  The app should use the latest swift language features including structured concurrency and the @Observable macro.  The app should not use combine.  Use xcodegen to create a project.
```

We discussed asking chatGPT for how to install Codex and XcodeGen and then use codex to execute the above prompt.

The resulting code can be found [here](https://github.com/aflockofswifts/vibe-tvmaze)

  - https://venturebeat.com/ai/openai-report-reveals-a-6x-productivity-gap-between-ai-power-users-and


## 2025.12.06

### Resources Shared

- *The Programmer’s Brain* (Manning): https://www.manning.com/books/the-programmers-brain  

- *Ten Faces of Innovation* (IDEO): https://www.ideo.com/journal/the-ten-faces-of-innovation

- Refactoring Guru: https://refactoring.guru/design-patterns

### SwiftLint Plugins

- Jamie asked whether anyone uses SwiftLint’s Xcode BuildToolPlugin:  
  https://github.com/SimplyDanny/SwiftLintPlugins

Continued discussion about `Action` abstraction from last week.

---

## 2025.11.29

### Conference Talk Suggestions (Frank)

Frank shared a YouTube playlist of Server Side Swift talks:

- Playlist of suggested talks — https://www.youtube.com/playlist?list=PLTFt3GGfH3hl2rTYswjVXCaNvXmafQ3bt

Individual talks mentioned from that playlist:

- Usability Meets Performance in Swift — Ben Cohen  
- How To Approach Approachable Concurrency — Matt Massicotte  
- Observability in Server-Side Swift — Si Beaumont & Moritz Lang  

We touched briefly on server-side Swift technologies:

- Swift Temporal SDK (general discussion)  
- Swift gRPC  
- Frank noted the talk in question was actually about this library:  
- grpc-swift-2 — https://github.com/grpc/grpc-swift-2

### Mihaela’s “cupertino” Project (“Josh in a Box”)

Mihaela shared her `cupertino` project, jokingly described as “Josh in a box.”

- cupertino — https://github.com/mihaelamj/cupertino

### Build Tooling: XcodeGen

Xcode project generation came up as a way to keep projects maintainable and reproducible.

- XcodeGen — https://github.com/yonaskolb/XcodeGen

### Transcription Models: Parakeet

Frank recommended **Parakeet** as a good model for transcription, useful for meeting recordings and similar audio tasks.

### Action Abstractions in Reactive Frameworks

Josh shared links to `Action` abstractions from popular reactive Swift libraries as references for modeling user actions and side effects:

- ReactiveSwift `Action` — https://github.com/ReactiveCocoa/ReactiveSwift/blob/master/Sources/Action.swift  
- RxSwiftCommunity `Action` — https://github.com/RxSwiftCommunity/Action

An implementation using `AsyncSequence`:
```swift
nonisolated final class Action<Input, Output, Failure: Error> {
    var isEnabled: some AsyncSequence<Bool, Never> {
        isEnabledSubject
    }
    var isExecuting: some AsyncSequence<Bool, Never> {
        isExecutingSubject
    }
    var results: some AsyncSequence<Result<Output, Failure>, Never> {
        resultsPipe
    }
    var outputs: some AsyncSequence<Output, Never> {
        resultsPipe.compactMap { try? $0.get() }
    }
    var errors: some AsyncSequence<Failure, Never> {
        resultsPipe.compactMap {
            switch $0 {
            case .success: nil
            case .failure(let error): error
            }
        }
    }
    private let isExecutingSubject = AsyncSubject<Bool>(false)
    private let isEnabledSubject = AsyncSubject<Bool>(false)
    private let resultsPipe = AsyncPipe<Result<Output, Failure>>()
    private let transform: @Sendable (Input) -> AnyAsyncSequence<Output, Failure>
    private let lockedWorkTask = Mutex<Task<Void, Never>?>(nil)
    private let lockedEnabledTask = Mutex<Task<Void, Never>?>(nil)
    init(
        enabledIf: some AsyncSequence<Bool, Never>,
        transform: @escaping @Sendable (Input) -> some AsyncSequence<Output, Failure>
    ) {
        self.transform = { input in
            AnyAsyncSequence(transform(input))
        }
        let enabledTask = Task { [isExecutingSubject, isEnabledSubject] in
            for await value in combineLatest(isExecutingSubject, enabledIf) {
                isEnabledSubject.send(!value.0 && value.1)
            }
        }
        lockedEnabledTask.withLock { $0 = enabledTask }
    }
    convenience init(transform: @escaping @Sendable (Input) -> some AsyncSequence<Output, Failure>) {
        self.init(
            enabledIf: [true].async,
            transform: transform
        )
    }
    deinit{
        lockedWorkTask.withLock(\.self)?.cancel()
        lockedEnabledTask.withLock(\.self)?.cancel()
    }
    func callAsFunction(_ input: sending Input) {
        guard isEnabledSubject.currentValue else { return }
        isExecutingSubject.currentValue = true
        let workTask = Task {
            defer { isExecutingSubject.currentValue = false }
            let values = transform(input)
            do {
                for try await value in values {
                    resultsPipe.send(.success(value))
                }
            } catch let error as Failure {
                resultsPipe.send(.failure(error))
            } catch {
                fatalError("Unhandled error: \(error)")
            }
        }
        lockedWorkTask.withLock {
            $0 = workTask
        }
    }
    func cancel() {
        lockedWorkTask.withLock(\.self)?.cancel()
        if isEnabledSubject.currentValue {
            isEnabledSubject.send(true)
        }
    }
}

extension Action where Input == Void {
    func callAsFunction() {
        self(())
    }
}
extension Action: Sendable where Output: Sendable, Failure: Sendable { }

```

Usage
```swift
@Observable
final class ContentViewModel {
    var text: String = ""
    private(set) var progress: Double = 0
    private(set) var isProgressVisible = false
    private(set) var isButtonDisabled = false
    private(set) var isUploading = false
    private(set) var tapButton: Action<Void, Double, Never>

    private let subscriptions = Subscriptions()
    init() {

        let textIsNonEmpty = AsyncPipe<Bool>()

        tapButton = .init(enabledIf: textIsNonEmpty) { _ in
            var progress = 0
            return AsyncStream<Int> {
                defer { progress += 1 }
                try? await Task.sleep(for: .milliseconds(50))
                return progress <= 100 ? progress : nil
            }.map {
                Double($0) / 100.0
            }
        }

        subscriptions += values(of: \.text)
            .map(\.isEmpty)
            .map(!)
            .subscribe(onNext: textIsNonEmpty.send)

        subscriptions += tapButton
            .outputs
            .assign(on: self, to: \.progress)

        subscriptions += tapButton
            .isExecuting
            .assign(on: self, to: \.isUploading)

        subscriptions += tapButton
            .isEnabled
            .map { !$0 }
            .assign(on: self, to: \.isButtonDisabled)

        subscriptions += tapButton
            .isExecuting
            .filter(!)
            .map { _ in (0.0, "")}
            .assign(on: self, to: \.progress, \.text)
    }
}


struct ContentView: View {
    @ViewModel var viewModel = ContentViewModel()
    var body: some View {
        VStack {
            TextField("Upload file", text: $viewModel.text)
                .disabled(viewModel.isUploading)
            Button {
                viewModel.tapButton()
            } label: {
                ZStack(alignment: .center) {
                    Text("Upload…")
                        .opacity(viewModel.isUploading ? 0 : 1)
                    ProgressView()
                        .opacity(viewModel.isUploading ? 1 : 0)
                        .controlSize(.small)
                }
            }
            .disabled(viewModel.isButtonDisabled)
            VStack {
                Text("\(viewModel.progress.formatted(.percent.precision(.fractionLength(0))))")
                ProgressView("downloading…", value: viewModel.progress, total: 1)
            }
            .opacity(viewModel.isUploading ? 1 : 0)
        }
        .padding()
    }
}
```

Supporting types
```swift
nonisolated final class AsyncSubject<Element>: AsyncSequence {
    typealias Failure = Never
    private let input: AsyncStream<Element>.Continuation
    private let output: AnyAsyncSequence<Element, Never>
    private let lockedValue: Mutex<Element>
    var currentValue: Element {
        get {
            lockedValue.withLock(\.self)
        }
        set {
            lockedValue.withLock { $0 = newValue }
            input.yield(newValue)
        }
    }
    init(_ initialValue: Element) {
        lockedValue = .init(initialValue)
        let (output, input) = AsyncStream.makeStream(of: Element.self, bufferingPolicy: .bufferingNewest(1))
        self.input = input
        self.output = AnyAsyncSequence(output.share())
        self.input.yield(initialValue)
    }

    func makeAsyncIterator() -> AnyAsyncSequence<Element, Never>.AsyncIterator {
        output.makeAsyncIterator()
    }

    func send(_ value: Element) {
        currentValue = value
    }
    func finish() {
        input.finish()
    }
}

extension AsyncSubject: Sendable where Element: Sendable { }

nonisolated final class AsyncPipe<Element>: AsyncSequence {
    private let input: AsyncStream<Element>.Continuation
    private let output: AnyAsyncSequence<Element, Never>

    init() {
        let (output, input) = AsyncStream.makeStream(of: Element.self, bufferingPolicy: .bufferingNewest(0))
        self.input = input
        self.output = AnyAsyncSequence<Element, Never>(output.share())
    }

    func makeAsyncIterator() -> AnyAsyncSequence<Element, Never>.AsyncIterator {
        output.makeAsyncIterator()
    }

    func send(_ value: Element) {
        input.yield(value)
    }
    func finish() {
        input.finish()
    }
}

extension AsyncPipe: Sendable where Element: Sendable { }

nonisolated struct AnyInfallibleAsyncSequence<Element>: AsyncSequence {
    struct AsyncIterator: AsyncIteratorProtocol {
        private let _next: () async -> Element?
        init<I: AsyncIteratorProtocol>(_ base: consuming I) where I.Element == Element, I.Failure == Never {
            self._next = { await base.next(isolation: #isolation) }
        }
        mutating func next() async -> Element? { await _next() }
    }

    private let _makeAsyncIterator: () -> AsyncIterator

    init<S: AsyncSequence>(_ base: S) where S.Element == Element, S.Failure == Never {
        self._makeAsyncIterator = {
            AsyncIterator(base.makeAsyncIterator())
        }
    }

    func makeAsyncIterator() -> AsyncIterator { _makeAsyncIterator() }
}

nonisolated struct AnyAsyncSequence<Element, Failure: Error>: AsyncSequence {
    struct AsyncIterator: AsyncIteratorProtocol {
        private let _next: (isolated (any Actor)?) async -> Result<Element?, Failure>
        init<Base: AsyncIteratorProtocol>(
            _ base: consuming Base
        ) where Base.Element == Element, Base.Failure == Failure {
            self._next = { isolation in
                do {
                    let element = try await base.next(isolation: isolation)
                    return .success(element)
                } catch let error as Failure {
                    return .failure(error)
                } catch {
                    fatalError("Unexpected error type: \(error)")
                }
            }
        }
        mutating func next(isolation actor: isolated (any Actor)?) async throws(Failure) -> Element? {
            try await _next(actor).get()
        }
    }

    private let _makeAsyncIterator: () -> AsyncIterator

    init<Base: AsyncSequence>(_ base: Base) where Base.Element == Element, Base.Failure == Failure {
        self._makeAsyncIterator = {
            AsyncIterator(base.makeAsyncIterator())
        }
    }

    func makeAsyncIterator() -> AsyncIterator {
        _makeAsyncIterator()
    }
}

```
---

## 2025.11.22

### Conference Playlists

- Swift Connection 2025 playlist — <https://www.youtube.com/playlist?list=PLZsRQnRG-mlIkHsjeax_cRq6kAclNrWBF>

- Pragma Conf 2025 playlist — <https://www.youtube.com/playlist?list=PLAVm70iJlMuvTihK1OzK9S4Vzw_KO71b0>

### Individual talks (Swift Connection 2025)

- Quentin Fasquel — *The Wonderful World of Private APIs*
- Thomas Durand — *Crafting Reusable SwiftUI Components the Same Way Apple Does* — <https://www.youtube.com/watch?v=eS1DIEnfXvk&list=PLZsRQnRG-mlIkHsjeax_cRq6kAclNrWBF&index=20>
- Josh Holtz & Zach Brass — *A Talk... Two Ways* — <https://www.youtube.com/watch?v=3uZHL-Oco9I&list=PLZsRQnRG-mlIkHsjeax_cRq6kAclNrWBF&index=6>
- Maxim Cramer — *Designing for the Post-Screen Era*
- Gui Rambo — *Inside Liquid Glass: How iOS 26 Synthesizes Refractive UI*

### Individual talks (Pragma Conf 2025)

- Chris Eidhof — *The Attribute Graph: SwiftUI’s Invisible Hand*
- Johannes Fahrenkrug — *AI from Scratch: Let's Build & Train a Perceptron in Swift*
- Arkadiusz Świętnicki — *Joys and challenges of a sightless coder*
- Matteo Rattotti & Konstantin Erokhin — *The sacred secret behind our App's speed*

### Ed's Demo of On-Device AI

Apple technote: managing on‑device model context window

- TN3193 — *Managing the On-Device Foundation Model’s Context Window* — <https://developer.apple.com/documentation/technotes/tn3193-managing-the-on-device-foundation-model-s-context-window>

- `TranslationSession` API — <https://developer.apple.com/documentation/translation/translationsession>

- **Swift Log**, **Swift Metrics**, **Swift Distributed Tracing** — packages support swapping custom implementations.

### Concurrency pattern: bridging callbacks to `AsyncStream`

Mihaela shared a neat adapter for streaming location updates via `AsyncStream` while cleaning up on termination.

```swift
class LocationManager {
    var onLocationUpdate: ((Location) -> Void)?
}

extension LocationManager {
    var locationUpdates: AsyncStream<Location> {
        AsyncStream { continuation in
            self.onLocationUpdate = { location in
                continuation.yield(location)
            }

            continuation.onTermination = { @Sendable _ in
                self.onLocationUpdate = nil
            }

            self.startUpdating()
        }
    }
}

// Usage
for await location in locationManager.locationUpdates {
    print("New location: \(location)")
}
```

---

## 2025.11.15

### MCP for Apple Documentation

Mihaela has a new exciting project that compiles Apple docs and provides access to AI agents.

- https://github.com/mihaelamj/appledocsucker

### Async Functions

Took a deep dive into async function.

Some low level details about how async wrote:
- https://developer.apple.com/videos/play/wwdc2021/10254/
- https://www.youtube.com/watch?v=H_K-us4-K7s

In Swift 6.2, the caller decides where (what executor) a function finishes on.

The old way:

```swift
func getCities(completion: @escaping @Sendable (Int) -> Void) {
    DispatchQueue.global(qos: .utility).async {
        let response = 1
        DispatchQueue.main.async { [completion] in
            completion(response)
        }
    }
}
```

Can be translated to this:

```swift
func getCities() async -> Int {
    await withCheckedContinuation { continuation in
        DispatchQueue.global(qos: .utility).async {
            let response = 1
            continuation.resume(returning: response)
        }
    }
}
```

A more modern actor approach bridging the old world:

```swift
actor NetworkService {
    private var header: [String: String] = [:]
    static func getCities() async -> Int {
        // Continuation captures this state
        var a = 0
        try? await Task.sleep(for: .seconds(1))
        let b = await withCheckedContinuation { continuation in
            DispatchQueue.global(qos: .utility).async {
                let response = 1
                continuation.resume(returning: response)
            }
        }
        // Continuation returns here
        print(a)
        return b
    }
    @available(*, deprecated)
    nonisolated static func getCities(completion: @escaping @Sendable (Int) -> Void) {
        Task {
            completion(await getCities())
        }
    }
}
```

Non-isolated behavior: https://docs.swift.org/compiler/documentation/diagnostics/nonisolated-nonsending-by-default/


### Embedded Swift

Sadly, I was in and out during most of Carlyn's presentation. She talked about
several projects and things including embedded swift the ESP 32 C6 and hacking conference badges. She also talked about Swift and LoRa and implementing a 
Harware Abstraction Layer for Swift.


### Swift Everywhere

Related to this, Josh mentioned that Android tools are now available for Swift for free.

- https://skip.tools/blog/skip-fuse-free-for-indies/

---

## 2025.11.08

### Using Shazam API

Rainer discovered that Shazam requires 12 second samples or its performance is very poor.
  
### Making Previews Work

There are strange interactions with Previews and third party packages. Josh notes that you can steer around these problems by
making your code modular and not depending at all on any
external package.

This lead to a discussion about architecture.

![Architecture](images/architecture1.png)

```swift
@MainActor final class ViewModelFactory {
    private let services: Services
    func makeDocumentViewModel(from id: Document.ID) -> DocumentViewModel{
        .init(
            id: id,
            analyticsService: services.analyticsService,
            documentManager: services.documentManager
        )
    }
}

@EnvironmentObject private var viewModelFactory
var body: some View {
    Child(viewModel: viewModelFactory.makeChildViewModel(from: viewmodel.document.id))
}
```
  
### Article Roundup

Mihaela recommends this podcast. Lots of interesting stuff about server side swift:

- https://www.youtube.com/@SwiftToolkit


Josh showed us a lot of interesting articles:

- https://antongubarenko.substack.com/p/optimize-your-apps-speed-and-efficiency
- https://swiftdevjournal.com/posts/swiftui-frequent-view-updates/
- https://gioscalzo.com/blog/demystifying-ai-coding-agents-in-swift/
- https://forums.swift.org/t/roadmap-for-improving-the-type-checker/82952
- https://www.avanderlee.com/optimization/analysing-build-performance-xcode/

From SwiftLeeds.

- https://www.youtube.com/playlist?list=PL-wmxEeX64YTpDbpfszWMV76oZZO3wxZH
  
### More Conference Videos

From Frank to talk about next week!

- Swift Connection: https://www.youtube.com/playlist?list=PLZsRQnRG-mlIkHsjeax_cRq6kAclNrWBF 
  
- Pragma: https://www.youtube.com/playlist?list=PLAVm70iJlMuvTihK1OzK9S4Vzw_KO71b0

---

## 2025.11.01


### Graphics tooling: Affinity & SwiftDraw

Quick exchange on vector/bitmap tooling that can fit developer workflows.

- **Links**
  - Affinity downloads — <https://www.affinity.studio/download>  
  - SwiftDraw (Swift vector drawing library) — <https://github.com/swhitty/SwiftDraw>


### Apple performance/efficiency session & follow-ups

Peter flags an Apple session; later chat touches view identity/diffing in SwiftUI.

- Apple session: *Performance & Efficiency* — <https://www.youtube.com/watch?v=yXAQTIKR8fk>  
- “Meet with Apple / 212” — <https://developer.apple.com/videos/play/meet-with-apple/212>  
- SwiftUI diffing deep-dive article — <https://fatbobman.com/en/posts/understanding-swiftui-view-update-mechanism/>

### Linking discussion (static vs dynamic) in Xcode

static vs dynamic linking practices; notes about embedding dylibs and verifying app bundle contents.


### SwiftUI view identity: preserving state across branches

Mihaela posts code illustrating how identity changes across `if` branches can reset state, and how a single identity preserves it.

- https://fatbobman.com/en/posts/understanding-swiftui-view-update-mechanism/

### SwiftUI

It is possible to implement your own ShapeStyle conformances. Alex created his own color type HSL

- https://developer.apple.com/documentation/swiftui/shapestyle

### Swift on Android

- https://www.swift.org/blog/nightly-swift-sdk-for-android/
- https://www.swift.org/android-workgroup/

### Data modeling & migrations: SQLiteData

- https://swiftpackageindex.com/pointfreeco/sqlite-data/1.3.0/documentation/sqlitedata


Specifically we walked through creation of a database.

- https://swiftpackageindex.com/pointfreeco/sqlite-data/1.3.0/documentation/sqlitedata/preparingdatabase

---

## 2025.10.25


### Swift on Android & Cross-Platform UI
- **Ray Fix:** Swift Android Workgroup  
  https://www.swift.org/android-workgroup/
- **Mihaela MJ:** Skip (write in Swift, run on iOS/Android)  
  https://skip.tools
- **Josh Homann:** Swift Android examples  
  https://github.com/swiftlang/swift-android-examples
- **Josh Homann:** OpenSwiftUI project  
  https://github.com/OpenSwiftUIProject/OpenSwiftUI
- **Alex:** swift-cross-ui  
  https://github.com/stackotter/swift-cross-ui


### Xcode / Distribution
- **Josh Homann:** Distributing binary frameworks as Swift packages (Xcode)  
  https://developer.apple.com/documentation/xcode/distributing-binary-frameworks-as-swift-packages

### Symbols, Fonts & Rendering
- **Alex:** SFSymbolBuilder  
  https://github.com/bealex/SFSymbolBuilder

- **Josh Homann:** Font anatomy (Material guidelines)  
  https://m2.material.io/design/typography/understanding-typography.html#type-properties

### Monospaced Fonts

- **Peter Wu:** SwiftUI monospaced digits  
  https://developer.apple.com/documentation/swiftui/font/monospaceddigit()
- TextRenderer (SwiftUI)  
  https://developer.apple.com/documentation/swiftui/textrenderer

### Retro Books & Articles
- **Josh Homann:** Programming iOS 14 (Matt Neuburg)  
  https://www.amazon.com/Programming-iOS-14-Controllers-Frameworks/dp/1492092177
- **Mihaela MJ:** iOS Core Animation: Advanced Techniques (Nick Lockwood)  
  https://www.amazon.com/iOS-Core-Animation-Advanced-Techniques-ebook/dp/B00EHJCORC
- **Mihaela MJ:** Core Animation Simplified (O’Reilly)  
  https://www.oreilly.com/library/view/core-animation-simplified/9780321617835/
- NOTE: You might be able to check out some of these books from your library!

### Articles

- **Josh Homann:** “Swift Concurrency — what I wish someone had told me”  
  https://www.linkedin.com/pulse/swift-concurrency-what-i-wish-someone-had-told-me-valente-pimentel--xqb5f/

- **Josh Homann:** Singletons and Concurrency
  https://www.massicotte.org/singletons

---

## 2025.10.18

### Server‑Side Swift / Middleware

- **Mihaela MJ:** OpenAPI Logging middleware  
  https://github.com/mihaelamj/OpenAPILoggingMiddleware

- **Mihaela MJ:** Bearer token auth middleware  
  https://github.com/mihaelamj/BearerTokenAuthMiddleware

- **Mihaela MJ:** Swift OpenAPI “extreme packaging” example  
  https://github.com/mihaelamj/swift-openapi-extremepackaging-example


### Conferences & Communities
- **Frank Lefebvre:** CocoaConferences aggregator  
  https://cocoaconferences.com

### Symbols & Vector Design Tools

Alex created a script to produce custom SF symbols. He is working on possibly open sourcing it.

Vector drawing: Figma, Sketch, Affinity Designer, Inkscape

- https://inkscape.org

## Articles & Reading

- **Ray Fix:** Advanced Codable (“No‑Drama Codable”)  
  https://nothingtocommitworkingtreeclean.com/advanced_codable.html


## AI Model Sizes & Local Models
- **Bob DeLaurentis:** (from web search) “Claude 3.5 Sonnet ~175B params; Claude 4 ~1.7T (unverified).”
- **Josh Homann:** “I run the 20B GPT‑OSS on ollama.”
- **Mihaela MJ:** OpenAI GPT‑OSS intro  
  https://openai.com/index/introducing-gpt-oss/

---


## 2025.10.11

### Swift & Apple APIs
- **Josh Homann:** Swift diagnostics — nonisolated / non-sending by default  
  https://docs.swift.org/compiler/documentation/diagnostics/nonisolated-nonsending-by-default/
- **Ray Fix:** Swift Evolution: Module Selectors proposal  
  https://github.com/swiftlang/swift-evolution/blob/main/proposals/0491-module-selectors.md
- **Josh Homann:** SpeechAnalyzer API  
  https://developer.apple.com/documentation/speech/speechanalyzer
- **Peter Wu:** Mutex docs  
  https://developer.apple.com/documentation/synchronization/mutex

### Swift Packages & Libraries
- **Mihaela MJ:** Point‑Free Clocks  
  https://github.com/pointfreeco/swift-clocks

### UUID Extras Package

- **Ray Fix:** UUIDExtras (v7 UUID package)  
  https://github.com/rayfix/UUIDExtras  👍

### ViewModels are just a Function
- **Josh Homann:** RxTvMaze  
  https://github.com/joshuajhomann/RxTvMaze/tree/master


### Foundation Models

- **Josh Homann:** Profiling Foundation Models  
  https://artemnovichkov.com/blog/foundation-models-profiling-with-xcode-instruments

- **Josh Homann:** iOS 26 Foundation Model framework overview  
  https://antongubarenko.substack.com/p/ios-26-foundation-model-framework-f6d

```swift
.task {
    do {
        let instructions =
        """
        You are a screen writer pitching ideas for a screenplay.
        Your response should be a synopsis of the plot followed by a bulleted list
        of major characters with a brief biography.
        """
        let options = GenerationOptions(sampling: .greedy)
        let session = LanguageModelSession(instructions: instructions)
        session.prewarm()
        let prompt = "Write a murder mystery set on a train"
        let response = try await session.respond(to: prompt,
                           generating: ScreenPlaySynopsis.self, options: options)
        print(response)
    } catch {
        print(error)
    }
}
```

---

## 2025.10.04

### Algorithms & Interview Prep
- **Josh Homann**: Cracking the Coding Interview  
  https://www.amazon.com/Cracking-Coding-Interview-Programming-Questions/dp/0984782850  
- **Josh Homann**: neetcode YouTube channel  
  https://www.youtube.com/c/neetcode  
- **Josh Homann**: Leetcode  
  https://leetcode.com  
- **Peter Wu**: The Algorithm Design Manual  
  https://www.amazon.com/Algorithm-Design-Manual-Steven-Skiena/dp/1849967202  
- **Alex**: *Just for fun — Algorithms (big books)*  
  https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/  
  https://www.amazon.com/Computer-Programming-Volumes-1-4B-Boxed/dp/0137935102  
- **Tobias**: Swift Collections Heap documentation  
  https://swiftpackageindex.com/apple/swift-collections/1.2.1/documentation/heapmodule/heap  
- **Joe Mestrovich**: Swift Algorithm Club (Kodeco)  
  https://github.com/kodecocodes/swift-algorithm-club  
- **Josh Homann**: Swift API Design Guidelines  
  https://www.swift.org/documentation/api-design-guidelines/  
- **Josh Homann**: Advent of Code  
  https://adventofcode.com  
- **Josh Homann**: SymbolSearch project  
  https://github.com/joshuajhomann/SymbolSearch  
 

### Global Actor Example

```swift
@globalActor
actor MyActor {
    static let shared = MyActor()
    private init() { }
}
```  
### AI & Tools

- **Josh Homann**: SwiftLog  
  https://github.com/apple/swift-log 
- **Josh Homann**: Reactive ViewModels Simplified video  
  https://www.youtube.com/watch?v=uTLG_LgjWGA  
- **Josh Homann**: SwiftUI file exporter reference  
  https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:document:contenttype:defaultfilename:oncompletion:)  
- **Josh Homann**: Claude for mobile demo  
  https://www.youtube.com/watch?v=NnYLzGMk8Tg&t=750s  
- **Josh Homann**: OpenAI GPT OSS 20B & 120B models  
  https://huggingface.co/openai/gpt-oss-120b  
- **Peter Wu**: Claude Code origin video  
  https://www.youtube.com/watch?v=Yf_1w00qIKc  
- **Peter Wu**: Claude Code best practices walk-through  
  https://www.youtube.com/watch?v=6eBSHbLKuN0&t=956s  
- **Josh Homann**: TechCrunch article on local AI models with iOS 26  
  https://techcrunch.com/2025/10/03/how-developers-are-using-apples-local-ai-models-with-ios-26/  
- **Peter Wu**: objc.io Environment & Preference Updates episode  
  https://talk.objc.io/episodes/S01E409-environment-preference-updates

### Using Foundation Models

An example from Josh Homann.

```swift
import FoundationModels
let instructions =
"""
    All recipes should be vegan. Start every answer with a bulleted list of ingredients followed by a description of the dish followed by a numbered list of instructions.
"""
let options = GenerationOptions(temperature: 5.0)
let session = LanguageModelSession(instructions: instructions)

let prompt = "create a recipe for Mapo Tofu"
let response = try await session.respond(to: prompt, options: options)
print(response.content)
```  

## 2025.09.27

### AI Generated History

Allen used Claude to go through all of the pages documents that had a high level UML-like diagram of his
design turn them into a movie.

### Gestures

There are things that you still cannot do with pure SwiftUI.

- https://developer.apple.com/documentation/uikit/uigesturerecognizerdelegate    
- https://swiftwithmajid.com/2024/12/17/introducing-uigesturerecognizerrepresentable-protocol-in-swiftui/


### UI Design

Be careful about using SF symbol as images because they lose their original type-based semantics.

Consider using scaled metric: https://developer.apple.com/documentation/swiftui/scaledmetric

#### Liquid Glass
    
- https://developer.apple.com/documentation/SwiftUI/Applying-Liquid-Glass-to-custom-views
    

```swift
    Text("Hello, World!")
        .font(.title)
        .padding()
        .glassEffect(.regular.tint(.orange).interactive())
```

### App Intents

Interesting impromptu discussion with Joe leading about how he uses app intents in some of his apps. Here are some resources:

- https://developer.apple.com/documentation/appintents/adopting-app-intents-to-support-system-experiences    
- https://developer.apple.com/videos/play/wwdc2025/275


### Trip Advisor Moving to from MVVM-C to TCA

Shared by Rainer.

https://medium.com/tripadvisor/the-evolution-of-native-engineering-at-tripadvisor-part-1-577cc0e36ec8


### Article Roundup from Peter

In depth coverage of how SwiftUI view updates.

- https://fatbobman.com/en/posts/understanding-swiftui-view-update-mechanism/

Also from Josh:

- https://medium.com/@matgnt/swiftui-redraw-system-in-depth-attributes-recomputation-diffing-and-observation-66b469fdcada

Async algorithm share:

https://github.com/apple/swift-async-algorithms/blob/main/Evolution/0016-share.md

### Article Roundup from Josh

A bunch of shortcuts to produce things like screenshots that you can include in git commits.

- https://lickability.com/blog/github-markdown-shortcuts/

An IDE for Shortcuts on macOS.
    
- https://www.jellycuts.com

It is suprising just how slow NSImage is. If you are on the Mac, make sure you are using CGImage.

- https://macguru.dev/fast-thumbnails-with-cgimagesource/

If you use the command line, this is how you can create code completion for zsh.    

- https://swifttoolkit.dev/posts/argument-parser-gems
    
This is a deep dive on how rendering in iOS works.

- https://github.com/EthanArbuckle/ios-rendering-docs
  
Matt Mssicotte's take on when to use actors. (Which Josh doesn't seem to agree with but found it to be an interesting post.)

- https://www.massicotte.org/actors

---

## 2025.09.20


### To OpenAI or Not

Carlyn talked about when it makes sense to generate your APIs using OpenAPI.

- https://www.whynotestflight.com/excuses/how-do-i-get-hummingbird-to-work-with-the-openapi-plugins/
  
Some other options (resources):

-  https://loopback.io
-  https://fastapi.tiangolo.com

### Talking Architecture  

  Recreating Stateobject: https://fatbobman.com/en/posts/lazy-initialization-state-in-swiftui/

![Architecture](images/architecture1.png)

### Memory Safety

Ray F. did an exploration of the new Swift 6.2 strict memory enforcement.

- https://github.com/swiftlang/swift-evolution/blob/main/proposals/0458-strict-memory-safety.md

We started by enabling checking in the package.

```swift
// swift-tools-version: 6.2
```

And in the target:

```swift


.target(name: "uuid-exploration"),
        swiftSettings: [.strictMemorySafety(), .treatAllWarnings(as: .error)])
```

You can enable from the command line or as an argument in your Xcode project's build:

```none
  -strict-memory-safety
```
  
Then we fixed the warnings (errors) by adding `unsafe` to every place that required it.

```swift
unsafe withUnsafeMutableBytes(of: &random) { raw in
    let result = unsafe SecRandomCopyBytes(kSecRandomDefault, 10, raw.baseAddress!)
    precondition(result == errSecSuccess)
}
```

### Exploring a Design System 

Going back to the homework from Josh.

- https://www.swiftbysundell.com/articles/building-a-design-system-at-genius-scan/
  

HTML/CSS are very good about separating semantics and style. SwiftUI, similarly can be decomposed into different parts.


As example consider this view which is all about content:

```swift
struct ContentView: View {
    var body: some View {
        List {
            ForEach(0..<10) { i in
                LabeledContent {
                    Text("Title")
                        .font(.body)
                        .foregroundStyle(.red)
                    Text("Subtitle")
                    Text("Subsubtitle")
                    Text("Subsubsubtitle")
                } label: {
                    Label("hello", systemImage: "star.fill")
                }
                .labeledContentStyle(.verticalHierarchicalText)
            }
        }
    }
}
```

The style is applied with a custom modifier and can be defined like so:

```swift  
struct HierarchicalLabeledContentStyle: LabeledContentStyle {
    var orientation: Axis = .horizontal
    var spacing: Double = .zero
    enum Constant {
        static let fontFromIndex: [Int: Font] = [ 1 : .body, 2: .caption2, 3 : .caption]
        static let shapeStyleFromIndex: [Int: AnyShapeStyle] = [ 1 : AnyShapeStyle(.primary), 2: nyShapeStyle(.secondary), 3 : AnyShapeStyle(.tertiary)]
    }

    func makeBody(configuration: Configuration) -> some View {
        let layout = switch orientation {
          case .horizontal: AnyLayout(HStackLayout(spacing: spacing))
          case .vertical: AnyLayout(VStackLayout(alignment: .leading, spacing: spacing))
        }
        HStack(spacing: 10) {
          configuration.label
                .alignmentGuide(.listRowSeparatorLeading) { $0[.trailing] + 10 }
  
            layout {
                var index = 0
                ForEach(subviews: configuration.content) { subview in
                    subview.font(Constant.fontFromIndex[index] ?? .footnote)
                        .foregroundStyle(Constant.shapeStyleFromIndex[index] ?? AnyShapeStyle(.quaternary))
                    let _ = index += 1
                }
            }
        }
    }
}
```

To allow for ergonomic auto-completing modifiers:

```swift
extension LabeledContentStyle where Self == HierarchicalLabeledContentStyle {
    static var horizontal: Self {
        Self(orientation: .horizontal)
    }
    static var verticalHierarchicalText: Self {
        Self(orientation: .vertical)
    }
    static func verticalHierarchicalText(spacing: Double) -> Self {
        Self(orientation: .vertical, spacing: spacing)
    }
}
```
---

## 2025.09.13

### Apple Security & Updates
  
- https://security.apple.com/blog/memory-integrity-enforcement/  
 
### Projects & Apps
- **Ed Arenberg**: Emoji Game Helper app (App Store link)  
  https://apps.apple.com/us/app/emoji-game-helper/id6749472749  

### Links & References
- **Josh Homann**: iPhone URL Scheme reference  
  https://developer.apple.com/library/archive/featuredarticles/iPhoneURLScheme_Reference/Introduction/Introduction.html#//apple_ref/doc/uid/TP40007899-CH1-SW1  
- Square link  
  https://squareup.com  
- **Ed Arenberg**: Mobile app design inspiration  
  https://dribbble.com/tags/mobile-app-design  


### Swift & Interpreter
- **Josh Homann**: Swift Interpreter article  
  https://www.bitrig.app/blog/swift-interpreter
- https://github.com/SwiftyLua/SwiftyLua


### Containers & Servers

Carlyn led a presentation on containers.

- Podman on macOS (shared twice)  
  https://www.whynotestflight.com/excuses/podman-how-do-i-get-and-edit-an-image-on-macos/  
- HelloServer repo  
  https://github.com/carlynorama/HelloServer  
- HummingbirdExamples repo  
  https://github.com/carlynorama/HummingbirdExamples/  


### Other container references
- **Georgi Dagnall**: New Docker tutorial (same channel)  
  https://www.youtube.com/watch?v=zFa9_K8BS8I   
- **carlyn**: YouTube reference (containers)  
  https://www.youtube.com/watch?v=SXwC9fSwct8

--

## 2025.09.06

### Retro-computing

John Brewer informed us that Microsoft released the source code BASIC for the 6502.

- https://github.com/microsoft/BASIC-M6502

It is about 8000 lines and compiles for multiple platforms, including the Apple II, Commodore PET and others.


### UUID

Universal Unique IDs are an important part of application development are defined by RFC 4122 and is being updated in RFC 9562. See https://www.rfc-editor.org/rfc/rfc9562.html

The Foundation implementation is version 4 of RFC 4122 and contains 120 bits of randomness. Ray walked us through an extension that implements version 7 which uses Unix-based time so that UUIDs can be sorted in order.

The first thing we did was make a setter from a raw UInt128.  The first implementation looks like this:

```swift
extension UUID {
  @inlinable init(_ value: UInt128) {
    let v: uuid_t =
      (UInt8(value >> 120 & 0xff),
       UInt8(value >> 112 & 0xff),
       UInt8(value >> 104 & 0xff),
       UInt8(value >> 96 & 0xff),
       UInt8(value >> 88 & 0xff),
       UInt8(value >> 80 & 0xff),
       UInt8(value >> 72 & 0xff),
       UInt8(value >> 64 & 0xff),
       UInt8(value >> 56 & 0xff),
       UInt8(value >> 48 & 0xff),
       UInt8(value >> 40 & 0xff),
       UInt8(value >> 32 & 0xff),
       UInt8(value >> 24 & 0xff),
       UInt8(value >> 16 & 0xff),
       UInt8(value >> 8 & 0xff),
       UInt8(value & 0xff))
    self = UUID(uuid: v)
  }
}
```

Turns out that this is only valid for little endian platforms (which is most everything these days) but might fail on an embedded platform.  Here is the final version:

```swift
import Foundation
    
extension UUID {
      
  var version: Int {
    Int((uuid.6 & 0xf0) >> 4)
  }
      
  enum Variant {
     case ncs, rfc9562, guid, future
   }
       
   var variant: Variant {
       switch (uuid.8 >> 4) & 0xf {
       case 0x0 ... 0x7: .ncs
       case 0x8 ... 0xb: .rfc9562
       case 0xc ... 0xd: .guid
       case 0xe ... 0xf: .future
       }
   }
      
  init(_ value: UInt128) {
    var bigEndian = value.bigEndian
    let t = withUnsafeBytes(of: &bigEndian) { raw -> uuid_t in
      raw.load(as: uuid_t.self)
    }
    self = UUID(uuid: t)
  }
      
  var value: UInt128 {
    var source = uuid
    var destination: UInt128 = 0        
    _ = withUnsafeBytes(of: &source) { src in
      withUnsafeMutableBytes(of: &destination) { dst in
        src.copyBytes(to: dst)
      }
    }        
    return Int(littleEndian: 42) == 42 ? destination.byteSwapped : destination
  }

  static func v7() -> UUID {
      let timestamp = UInt128(Date().timeIntervalSince1970 * 1000)
      var random = UInt128.zero
      withUnsafeMutableBytes(of: &random) { raw in
        let result = SecRandomCopyBytes(kSecRandomDefault, 10, raw.baseAddress!)
        assert(result == 0)
      }
        
      var value = UInt128(0x7000_0000_000000000000)
      value |= (timestamp & ((UInt128(1) << 48) - 1)) << 80
      value |= (random & ((UInt128(1) << 76) - 1))
        
      // Patch in the variant
      value &= ~(UInt128(0b11) << 62) // clear the two bits
      value |=  (UInt128(0b10) << 62) // set to 10
        
      return UUID(value)
    }
      
  var unixMilliseconds: UInt64? {
     guard version == 7 else { return nil }
     return UInt64((value >> 80) & ((UInt128(1) << 48) - 1))
   }
      
  var timestamp: Date? {
    guard let unixMilliseconds else { return nil }
    return Date(timeIntervalSince1970: TimeInterval(unixMilliseconds) / 1000.0)
  }
}

```

We also wrote some tests:

```swift
import Testing
import Foundation
@testable import uuid_exploration
    
@Suite struct UUIDTests {
  @Test func version() {
    let uuid = UUID()
    #expect(uuid.version == 4)
    #expect(uuid.timestamp == nil)
  }
      
  @Test func initialize() {
    let x = UUID(1)
    #expect(x.uuidString == "00000000-0000-0000-0000-000000000001")
    #expect(x.value == 1)
        
    let y = UUID(0x112233445566778899AABBCCDDEEFF00)
    #expect(y.uuidString == "11223344-5566-7788-99AA-BBCCDDEEFF00")
    #expect(y.value == 0x112233445566778899AABBCCDDEEFF00)
  }
      
  @Test func generateUUID7() {
    let uuid = UUID.v7()
    #expect(uuid.version == 7)
    print(uuid.uuidString)
    print(uuid.timestamp!)
  }
}
```

We also tested with this web service:

- https://uuid7.com


### Making a Random Label

From Josh:

```swift
print(String(Int.random(in: 0..<Int.max), radix: 36).uppercased())
```

Alternatively:

```swift
print(ObjectIdentifier(a).debugDescription)
```

### Homework

From Josh. Read up on this for next week:

- https://www.swiftbysundell.com/articles/building-a-design-system-at-genius-scan/


---

## 2025.08.30

## Numerics Release 1.1 

This release introduces relaxed addition (that can use FMA instructions) for an order of magnitude performance gain.

https://github.com/apple/swift-numerics/releases/tag/1.1.0  

## Issues & Debugging
- **Joe**: *With iOS 26 I get Xcode console messages for “Attribute Graph: cycle detected through attribute” when using the new tab bar bottom accessory. Anyone else seeing these?*  


## Sendable, Sending, and Nonsending

- **Josh Homann**: Article: Sendable / Non-Sending discussion  
  https://fatbobman.com/en/posts/sendable-sending-nonsending/  

## Global Actor Example
- **Josh Homann**: Example of global actor  

```swift
@globalActor
actor MyActor {
    static let shared = MyActor()
    private init() { }
}
```  

## Containers

- **carlyn**: *I’ve started using containers! Will say more next week when I’m more confident.*  
  
https://www.whynotestflight.com/excuses/podman-how-do-i-get-and-edit-an-image-on-macos/  


## Subscriptions & Assign

- **Josh Homann**: Subscriptions class  

```swift
nonisolated final class Subscriptions {
    private var disposables: [() -> Void] = []
    deinit { disposables.forEach { $0() } }
    static func += <Value> (lhs: Subscriptions, rhs: Task<Value, some Error>) {
        lhs.disposables.append(rhs.cancel)
    }
}
```  

- **Josh Homann**: Generic `assign` function  

```swift
func assign<each Value, Target: AnyObject>(
        on target: Target,
        to keyPaths: repeat ReferenceWritableKeyPath<Target, each Value>
    ) -> Task<Void, Never> where Element == (repeat each Value) {
        subscribe(referencing: target) { target, values in
            for (value, keyPath) in repeat (each values, each keyPaths) {
                target[keyPath: keyPath] = value
            }
        }
    }
```  

## Text Rendering

- **Josh Homann**: Custom Renderer for text blur effect  

```swift
struct Renderer: TextRenderer {
    var time: TimeInterval
    func draw(layout: Text.Layout, in context: inout GraphicsContext) {
        let glyphs = layout.lazy.flatMap(\.self).flatMap(\.self)
        let currentTime = sin(time)
        for (offset, glyph) in glyphs.enumerated() {
            var context = context
            let blur = abs(Double(offset) * currentTime)
            context.addFilter(.blur(radius: blur))
            context.translateBy(x: 0, y: Double(offset) * 5 * currentTime)
            context.draw(glyph)
        }
    }
}
```  

- **Josh Homann**: Example `ContentView` using `TimelineView`  

```swift
struct ContentView: View {
    var body: some View {
        VStack {
            Image(systemName: "globe")
                .imageScale(.large)
                .foregroundStyle(.tint)
            TimelineView(.animation) { context in
                Text("Hello, world!")
                    .font(.largeTitle)
                    .textRenderer(Renderer(time: context.date.timeIntervalSince1970))
            }
        }
        .padding()
    }
}
```

---

## 2025.08.23

### Payments 

It is wise to not do encryption and payment systems yourself.

- **Josh Homann**: Stripe  https://stripe.com/

### Authentication

- **Ray FASWebAuthenticationSession OAuth*  
- **Ray Fix**: Credit card input UI inspirations  https://dribbble.com/tags/credit-card-input  
- **Josh Homann**: Auth0  
  https://auth0.com  

### Passwords & Security Tools
- **carlyn**: *OnePassword, BitWarden, LastPass … used them all but I still like the built-in password manager*  
- **carlyn**: *Bitwarden is freemium open-source*  
- **Josh Homann**: Apple recovery contact guide  
  https://support.apple.com/en-us/102608  
- **Bob DeLaurentis**: Diceware password method  
  https://en.wikipedia.org/wiki/Diceware  
- **Josh Homann**: CryptoKit docs  
  https://developer.apple.com/documentation/cryptokit/  
- **Bob DeLaurentis**: Secure features in Notes app  
  https://support.apple.com/guide/security/secure-features-in-the-notes-app-sec1782bcab1/web  

### ARKit
- **Josh Homann**: Scene Reconstruction Provider  
  https://developer.apple.com/documentation/ARKit/SceneReconstructionProvider  

### Swift Observation Extensions

Using observed to replace combine.

- **Josh Homann**: Shared `Observation.Observable` extension snippet:  

```swift
extension Observation.Observable where Self: AnyObject {
    func values<Value: Sendable>(of keyPath: KeyPath<Self, Value>) -> some AsyncSequence<Value, Never> {
        Observations.untilFinished { [weak self] in
            self.map { .next($0[keyPath: keyPath]) } ?? .finish
        }
    }
    func newValues<Value: Sendable>(of keyPath: KeyPath<Self, Value>) -> some AsyncSequence<Value, Never> {
        values(of: keyPath).dropFirst()
    }
}
```  

- **Josh Homann**: Example `@Observable` Person class:  

```swift
@Observable
@MainActor
final class Person: Sendable {
    var name = "Joshua"
    var age = 25
    init() {
        let a = newValues(of: \.name)
        Task {
            try await Task.sleep(for: .seconds(1))
            name = "Mark"
        }
        Task {
            for await name in a {
                print(name)
            }
        }
    }
}
```

---

## 2025.08.16

### Hummingbird Adventures from Carlyn
- https://github.com/carlynorama/HummingbirdExamples/tree/main/04_front_end_work/welomeToTheCircus/Sources/welcomeToTheCircus/HTMLMakers  
- https://github.com/carlynorama/HummingbirdExamples/  
- https://github.com/carlynorama/SimplerServer  


If you need a static site generator:

  https://github.com/twostraws/Ignite 

### JavaScript in Swift

- **Josh Homann**: nshipster article  https://nshipster.com/javascriptcore/  

A live example:

```swift
import JavaScriptCore

let context = JSContext()
let squareScript = """
var a = 1;
function square(number) {
    return number * number;
}
"""
context?.evaluateScript(squareScript)
let square = context?.objectForKeyedSubscript("square")
print(square?.call(withArguments: [2]).toDouble())
```  

- WKWebView reference  
  https://developer.apple.com/documentation/webkit/wkwebview/evaluatejavascript(_:completionhandler:)  
- SwiftUI WebView reference  
  https://developer.apple.com/documentation/webkit/webpage/calljavascript(_:arguments:in:contentworld:)  


### Protobuf & WWDC
- **Alex**: Apple Protobuf generator  https://github.com/apple/swift-protobuf  
- **Chitaranjan sahu**: WWDC 2023 video  https://developer.apple.com/videos/play/wwdc2023/10171/  

### App Store Guidelines & Hybrid Apps

- **John Brewer**: External Javascript in hybrid apps (StackOverflow links)  
  https://stackoverflow.com/questions/43517892/apple-store-guidelines-external-javascript-files-in-hybrid-mobile-application  
  https://stackoverflow.com/questions/43503259/convert-server-generated-site-to-phonegap-cordova-app/43504441#43504441 
### References & Utilities

- **Josh Homann**: SwiftUI TabView for page controller snippet:  

```swift
TabView {
    // ... views ...
}
.tabViewStyle(.page(indexDisplayMode: .always))
```  

- **Chitaranjan sahu**: SwiftLint repo  
  https://github.com/realm/SwiftLint  
  
### Swift Evolution
- **Ray Fix**: Inline Array Sugar proposal accepted
  https://github.com/swiftlang/swift-evolution/blob/main/proposals/0483-inline-array-sugar.md

---

## 2025.08.09

### AI Chat

- **Peter Wu**: *I highly recommend Claude code — the $20 is worth it*  
- **Alex**: https://ollama.com  
- **Chitaranjan sahu**: https://lmstudio.ai/ (*Download and run models on your computer*)
- **Frank Lefebvre**: *There’s MLX too, optimized for Apple Silicon*  
  https://github.com/ml-explore/mlx  
- **Josh Homann**: Swift Composable Architecture examples  
  https://github.com/pointfreeco/swift-composable-architecture?tab=readme-ov-file#examples

### Speaking of AI 

- **Josh Homann**: News link  
  https://www.benzinga.com/markets/tech/25/08/46949685/zuck-poaching-effect-pushes-openai-to-announce-1-5-million-bonus-for-all-employees-even-new-hires-says-tech-entrepreneur  

### Interface talk

- **Josh Homann**: Minimum touch targets by platform  
  https://developer.apple.com/design/human-interface-guidelines/accessibility 

### Bartosz Milewski Category Theory
- **Peter Wu**: Category Theory for Programmers  
  https://bartoszmilewski.com/2014/10/28/category-theory-for-programmers-the-preface/  

### Cool Stuff

- **Josh Homann**: SwiftUI Backports  
  https://github.com/shaps80/SwiftUIBackports  
- **Josh Homann**: Silent memory leak fix  
  https://medium.com/@egzonpllana/how-i-stopped-a-silent-memory-leak-in-my-ios-app-282aef170df5  
- **Peter Wu**: Past project demonstrated RAII
  https://github.com/aflockofswifts/meetings/tree/main/2024#20240406  


### Memory & System APIs
- **Frank Lefebvre**: *About available memory: on iOS (and all other platforms except macOS) you can use `os_proc_available_memory()`*  


### Async & Extensions
- **Peter Wu**: AsyncSequence assign example  
  https://github.com/sideeffect-io/AsyncExtensions/blob/main/Sources/Operators/AsyncSequence+Assign.swift  

### Assembly Discussion
- **Josh Homann**: Assembly for Swift developers  
  https://arturgruchala.com/assembler-for-swift-developers/?utm_source=substack&utm_medium=email 
- **carlyn**: Helpful tool  
  https://cpulator.01xz.net  
- **carlyn**: Video resource  
  https://www.youtube.com/watch?v=in-UY_EyI14&list=PL2EF13wm-hWAlQe87UB2HV0SVhBXFpXbn  

### Swift Evolution — `@Observable`
  https://github.com/swiftlang/swift-evolution/blob/main/proposals/0475-observed.md  

```swift
import Swift
import Observation

@Observable
final class Person: Sendable {
    var name = "John"
    var age = 30
    init(name: String = "John", age: Int = 30) {
        self.name = name
        self.age = age
    }
}

extension Observation.Observable where Self: Sendable & AnyObject {
    func changes<Value: Sendable>(in transform: @escaping @Sendable (Self) -> Value) -> some AsyncSequence<Value, Never> {
        Observations.untilFinished { [weak self] in
            if let self {
                return .next(transform(self))
            } else {
                return .finish
            }
        }
    }
}

let p = Person()
let names = p.changes { $0.name }

Task {
    for await name in names {
        print(name)
    }
}

Task {
    try await Task.sleep(for: .seconds(1))
    p.name = "Jane"
    try await Task.sleep(nanoseconds: 0)
    p.name = "Jim"
}
```  

---

## 2025.08.05

### Swift Async Algorithms

Sharing async streams begins a new round of development.

- *Swift Async Algorithms Proposal: Broadcast*  
  https://forums.swift.org/t/swift-async-algorithms-proposal-broadcast-previously-shared/61210 — via **Robert G.**

- *Kickoff of a New Season of Development for AsyncAlgorithms*  
  https://forums.swift.org/t/kickoff-of-a-new-season-of-development-for-asyncalgorithms-share/81447 — via **Ray F.**

- *Open Pull Requests for Swift Async Algorithms*  
  https://github.com/apple/swift-async-algorithms/pulls — via **Josh H.**


### Observation & Perception

- *Perception 2.0 (Point-Free blog)*  
  https://www.pointfree.co/blog/posts/180-perception-2-0-an-updated-back-port-of-swift-s-observation-framework — via **Ray F.**

- *PerceptionCheckingTests.swift from Point-Free*  
  https://github.com/pointfreeco/swift-perception/blob/main/Tests/PerceptionTests/PerceptionCheckingTests.swift — via **Peter W.**


### Swift Evolution & Diffing

- *SE-0240: Ordered Collection Diffing*  
  https://github.com/swiftlang/swift-evolution/blob/main/proposals/0240-ordered-collection-diffing.md — via **Josh H.**

### Keyframe Animations

From Alex:

```swift
KeyframeTrack(\.x) {
    MoveKeyframe(0)
    LinearKeyframe(0, duration: appearDuration)
    let keyframes = spiralKeyframes(cos, targetAngle: a, targetRadius: r, duration: flyDuration)
    KeyframeTrackContentBuilder.buildArray(keyframes)
}
```

Comment:  
> "This line allows me to use runtime-generated array of keyframes inside track content builder: `KeyframeTrackContentBuilder.buildArray()`"


### SwiftUI & UI Tutorials

- *Landmarks: Building an App with Liquid Glass*  
  https://developer.apple.com/documentation/swiftui/landmarks-building-an-app-with-liquid-glass — via **Josh H.**

- *Chris Eidhof: How SwiftUI’s Rendering Works*  
  https://youtu.be/dCSf9nR6SOQ?si=G6_9HW5sPjEPGMSb — via **Chitaranjan S.** 


### Open Source Projects

- *TrackWeight app on GitHub*  
  https://github.com/KrishKrosh/TrackWeight — via **Chitaranjan S.**

- *Core Motion CMotionManager Docs*  
  https://developer.apple.com/documentation/coremotion/cmmotionmanager — via **Josh H.**

- *Redline GitHub Repo*  
  https://github.com/robb/Redline — via **Josh H.** 


## How Default Actor Isolation introduces problems and how to fix them 

- *Default Actor Isolation (Fatbobman)*  
  https://fatbobman.com/en/posts/default-actor-isolation/ — via **Josh H.**

---

## 2025.07.26

### Swift Composable Architecture (TCA)
- https://github.com/pointfreeco/swift-composable-architecture – John B.
- https://www.youtube.com/watch?v=efGCznIDVb4 – Bob D.
- https://www.youtube.com/watch?v=XWZmgbylTpc – Bob D.

### Community & Chat Groups
- https://ios-developers.io – Josh H.
- https://discord.gg/dVbEFjbU – carlyn
- https://www.meetup.com/Learn-Swift-Boston/ – Peter W.

### Swift Language & Features
- https://www.swiftbysundell.com/articles/let-vs-var-for-swift-struct-properties/ – Peter W.
- https://docs.swift.org/swift-book/documentation/the-swift-programming-language/declarations/#In-Out-Parameters - Peter W.
- https://developer.apple.com/documentation/realitykit/realityview/init(make:update:)-666xr – John B.
- https://github.com/swiftlang/swift-evolution/blob/main/visions/embedded-swift.md – John B.

### Swift & C++ Interop
- https://developer.apple.com/videos/play/wwdc2023/10172/ – John B.
- https://github.com/carlynorama/SoManyWaysToInclude – carlyn
- https://github.com/carlynorama/CxxInteropLibrary – carlyn
- https://github.com/carlynorama/CppInteropSimplestXCode – carlyn
- https://www.swift.org/documentation/cxx-interop/) – carlyn
- https://github.com/carlynorama/another-swift-cmake-examples – carlyn
- https://bazel.build – carlyn
- https://crascit.com/professional-cmake/ – carlyn
- https://www.youtube.com/watch?v=m0DwB4OvDXk – carlyn

### Swift Embedded / Pico Projects
- https://github.com/carlynorama/swift-pico-w-hello/blob/e180cf9b99b042ef16589ed881d48489124ea731/XX-BadgeFirmware/HAL/LanguageSupport.swift#L12 – carlyn
- https://github.com/carlynorama/swift-pico-w-hello/tree/main/08-StrippedDownBlink – carlyn

### MCP (Model Context Protocol)
- https://github.com/Cocoanetics/SwiftMCP – Chitaranjan S.
- https://www.youtube.com/watch?v=ANOpQiLG7Q0 – Chitaranjan S.
- https://www.youtube.com/watch?v=qjHf_S_PxSw – Chitaranjan S.
- https://crascit.com/professional-cmake/ – carlyn
- https://www.youtube.com/watch?v=m0DwB4OvDXk – carlyn

## Swift Concurrency
- https://developer.apple.com/videos/play/wwdc2025/268 – John B.
- https://developer.apple.com/videos/play/wwdc2025/270 – John B.

### Mesh Gradients in SwiftUI
- https://developer.apple.com/videos/play/wwdc2024/10151 – carlyn
- https://medium.com/@rishixcode/animated-mesh-gradient-in-swiftui-e1c2e11ed6bf – carlyn

```swift
struct MeshGradientView: View {
    @State var isAnimating = false
    
    var body: some View {
        MeshGradient(width: 3, height: 3, points: [
            [0.0, 0.0], [0.5, 0.0], [1.0, 0.0],
            [0.0, 0.5], [isAnimating ? 0.1 : 0.8, 0.5], [1.0, isAnimating ? 0.5 : 1],
            [0.0, 1.0], [0.5, 1.0], [1.0, 1.0]
        ], colors: [
            .purple, .indigo, .purple,
            isAnimating ? .mint : .purple, .blue, .blue,
            .purple, .indigo, .purple
        ])
        .edgesIgnoringSafeArea(.all)
        .onAppear() {
            withAnimation(.easeInOut(duration: 3.0).repeatForever(autoreverses: true)) {
                isAnimating.toggle()
            }
        }
    }
}
```

### UIKit & Transparent Tab Bars

From Joe:

```swift
Found what I needed to get my UIKit (storyboard and UIViewControllerRepresentables) to work with the transparent tab bar in iOS 18 and iOS 26 
    
    .ignoresSafeArea(.all, edges: .bottom)
    .toolbarBackgroundVisibility(.hidden, for: .tabBar)
```

### AI Agent IDE & ChatGPT Commentary

- https://kiro.dev/blog/introducing-kiro/ – Robert G.
- https://www.wheresyoured.at/the-haters-gui/ – John B.

### Misc Tools
- https://getunblocked.com – Mihaela MJ / Peter W.


---


## 2025.07.12


### CMake Examples

- https://github.com/carlynorama/another-swift-cmake-examples
    

### Waiting for Observations

The new Observations API is still not available in the current Xcode beta 3.

- https://forums.swift.org/t/observations-for-await-compilation-error/80508/7
    

### Emoji Game

Josh talked about a solution for the new apple emoji game.  The correspondance problem 
between emoji images and word solutions probably requires an LLM.

You can solve the word problem independently. An old game that Josh used a trie to 
solve the Boggle game. 

- https://github.com/joshuajhomann/Boggle-SwiftUI
    

A more generalized type of trie useful for the emoji game is a "compressed suffix trie" which can quickly match substrings.


### Cancelling TaskGroup

Peter investigating the subtleties of TaskGroup and cancellation.

- https://www.avanderlee.com/concurrency/task-groups-in-swift/

> “Since a TaskGroup is a structured concurrency primitive, cancellation is automatically propagated through all of its child-tasks (and their child tasks).”    

- https://developer.apple.com/documentation/swift/taskgroup 


### Solutions for Different Layout

These blog posts go into quite a bit of depth about how things work.
  
- https://fatbobman.com/en/posts/how-to-detect-text-truncation-in-swiftui/
    
Another solution is to create a variant of Text that never truncates and use it in combination with ViewThatFits.
    

### AI and XcodeBuild

From Chitaranjan:

- https://github.com/cameroncooke/XcodeBuildMCP

---

## 2025.07.05


### Embedded Swift

Frank Lefebvre is teaching a workshop on embedded Swift. Here is a link to 
some of the materials he has used.

- https://github.com/franklefebvre/EmbeddedSwiftWorkshop

Carlyn suggests starting with something simpler than Swift. (i.e. Vendor environments tends to be highly streamlined.)

- https://www.arduino.cc
- https://www.adafruit.com

Also, for board design:

- https://www.kicad.org

### A cool clock design with 48 stepper motors. Alex is experimenting building something like it and showed:

- https://store.moma.org/products/clockclock-24


Another motor based art project  from Carlyn
- https://www.youtube.com/watch?v=1ZPJ0U_kpNg


### Question about customizing the output of DoCC

Here are some general resources:

- https://danielsaidi.com/blog/2022/04/27/building-multi-platform-documentation-with-docc
- https://forums.swift.org/t/customizing-the-look-and-feel-of-swift-docc-render/58858
- https://www.youtube.com/watch?v=8KoIXbm0nv4
  
(Sounds like Carlyn is hoping to inspect the AST and build a custom DOCC backend. The most relevant
one supplied by Bob.)

- https://www.createwithswift.com/publishing-docc-documention-as-a-static-website-on-github-pages/


Carlyn's docc notes:

- https://www.whynotestflight.com/excuses/docc-notes-on-getting-started/

### Puzzles

YYUR, YYUB, ICUR YY4ME
    
There is a new puzzle game that Apple released in the news App.  It requires you to drag emoji
combination.


### New Coding Language Model

The idea is that instead of a sequential context window, it uses a diffusion model
to come up with the global structure of the program.

- https://9to5mac.com/2025/07/04/apple-just-released-a-weirdly-interesting-coding-language-model/
    

### Vibe Coding in Xcode 26

We made an experimental Inventory app on macOS 26 and Xcode 26.  

Some thoughts:
- It put together mostly working code.
- It made some unfortunate design decisions (user defaults storage, monolithic file to store everything)
- We were able to correct the problems though it did put some things in the wrong file and forgot to  inject all of the dependencies.
    

---

## 2025.06.28


### New Beta Available

There is a new beta available for 26. 

- https://www.xcodes.app
- https://github.com/XcodesOrg/xcodes
    
For new toolchains there is an excellent tool called Swiftly:
    
- https://github.com/swiftlang/swiftly
  

### Optimizing Animation  

Allen had a question about animating sticks and spheres using SceneKit.  The spheres are animating
smoothly while the sticks attached to the spheres would jump into place at the end. The question was
how to make it smooth.  The issue was that he was rendering the sticks using billboards. The consensus 
recommendation was to use simple geometry (e.g. hexagonal rod) to render the sticks and let the system
handle it for you.

Aside: SceneKit has been deprecated in favor of Reality kit.

- https://developer.apple.com/videos/play/wwdc2025/288/


### Result Building Arrays and Sets    
    

Josh notes that in many of his projects he defines a result builders to declaratively define
arrays.

Here is the result builder:

- https://github.com/swiftlang/swift-evolution/blob/main/proposals/0289-result-builders.md
    

Here is how you do it for array:

```swift
@resultBuilder
struct ArrayBuilder<Element> {
    typealias Expression = Element
    typealias Component = Array<Element>
    
    static func buildBlock(_ components: Component...) -> Component {
        buildArray(components)
    }
    static func buildExpression(_ expression: Expression) -> Component {
        [expression]
    }
    static func buildExpression(_ expression: Expression?) -> Component {
        expression.map { [$0] } ?? []
    }
    static func buildOptional(_ component: Component?) -> Component {
        component ?? []
    }
    static func buildEither(first component: Component) -> Component {
        component
    }
    static func buildEither(second component: Component) -> Component {
        component
    }
    static func buildArray(_ components: [Component]) -> Component {
        components.flatMap { $0 }
    }
    static func buildLimitedAvailability(_ component: Component) -> Component {
        component
    }
}
```

An extension improves the ergonomics.

```swift
extension Array {
    static func build(@ArrayBuilder<Element> _ make: () -> Self) -> Self {
        make()
    }
}
```

You can use it like this:

```swift
var b = true
var c: Int? = nil
let a = Array<Int>.build {
    1
    2
    c
    if b {
        3
    }
    if #available(iOS 26.0, *) {
        4
    }
}
```

Another compelling use case for result builders is declarative tests:
    
- https://github.com/joshuajhomann/DeclarativeTests
    

### Either and Functional Programming

A functional library for swift:

 - https://bow-swift.io
    
 - https://github.com/bow-swift/bow/blob/master/Sources/Bow/Data/Either.swift
    

### Layout and SwiftUI

- https://www.semanticscholar.org/paper/A-System-for-Efficient-and-Flexible-One-Way-in-C%2B%2B-Hudson/9609985dbef43633f4deb88c949a9776e0cd766b
- https://talk.objc.io/collections/swiftui-layout-explained  

### Swift and Certification

If you have background in CS, it is hard to beat Paul Hegerty's class even thought it is a little old.

- https://cs193p.stanford.edu

A starting point for a lot of people:

- https://www.hackingwithswift.com
    

There are degrees you can get through coursera and udacity but consensus says a github account with the portfolio project is great. Meta has a
certificate as well.

- https://www.coursera.org/degrees    
- https://www.udacity.com
- https://www.coursera.org/professional-certificates/meta-ios-developer
    

### AI Coding

- Cursor ai: https://www.youtube.com/watch?v=oOylEw3tPQ8
- Reverse-Engineering Xcode's Coding Intelligence prompt https://peterfriese.dev/blog/2025/reveng-xcode-coding-intelligence/


### Sharing GRDB


- https://github.com/pointfreeco/sharing-grdb
- https://www.pointfree.co/blog/posts/168-sharinggrdb-a-swiftdata-alternative
- https://www.pointfree.co/episodes/ep313-point-free-live-sharinggrdb
    

All of the free episodes for pointfree are here:

- https://www.pointfree.co/episodes/free


### Link Roundup    
    

- https://www.createwithswift.com/exploring-a-new-visual-language-liquid-glass/?utm_source=substack&utm_medium=email
- https://developer.apple.com/design/human-interface-guidelines/
- https://www.donnywals.com/exploring-tab-bars-on-ios-26-with-liquid-glass/?utm_source=substack&utm_medium=email
- https://nilcoalescing.com/blog/StretchyHeaderInSwiftUI/?utm_source=substack&utm_medium=email    
- https://steipete.me/posts/2025/automatic-observation-tracking-uikit-appkit    
- https://christianselig.com/2025/05/godot-ios-interop/


### Android Swift Workgroup

- https://forums.swift.org/t/announcing-the-android-workgroup/80666
    

### Foundation Models
    

- https://onevcat.com/2025/06/foundation-models/
- https://azamsharp.com/2025/06/18/the-ultimate-guide-to-the-foundation-models-framework.html
    

---

## 2025.06.21

### Embedded Swift

Ray is embarking on a Embedded Swift hobby project to build a one button remote that toggles the mute on his Sony TV. He is using an ESP32C6 dev kit from espressif.

- https://developer.espressif.com/blog/build-embedded-swift-application-for-esp32c6/

There is some good documentation for Embedded Swift:

- https://www.swift.org/get-started/embedded/
    

Swiftly is a good tool for managing toolchains:

- https://github.com/swiftlang/swiftly


A previous exploration by Carlyn:

- https://github.com/carlynorama/swift-pico-w-hello


### AI and Machine Learning

Software 3.0 by Andrej Karpathy

- https://www.youtube.com/watch?v=LCEmiRjPEtQ

More talks:

- https://www.youtube.com/@AndrejKarpathy/videos


Also,

- https://www.3blue1brown.com/topics/neural-networks


### Get a job
    
- https://www.levels.fyi/heatmap/
    

### ExtensionKit

- https://www.massicotte.org/extensionkit-intro?utm_source=substack&utm_medium=email    
- https://mastodon.social/@mattiem/114665149298651073


### Expensive Runtime    

- https://medium.com/ios-ic-weekly/swift-dynamiccast-in-swifts-runtime-0d41b244c8f0
    

### What's new in SwiftUI

Josh took us through many of the SwiftUI changes presented by Paul Hudson.

- https://www.hackingwithswift.com/articles/278/whats-new-in-swiftui-for-ios-26
    

With the new Liquid Glass theme, you might want to checkout the HIG again.

- https://developer.apple.com/design/human-interface-guidelines
    

### Learning Metal

Josh tells Ed to watch this!

- https://www.youtube.com/watch?v=vO0M4c9mb2E


Also, squircles...
    
---


## 2025.05.31

We discussed some other meetups:
  * https://links.iosdevhappyhour.com
  * https://lu.ma/core-coffee
We discussed solving the [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) problem and how the particulars of Swift's String implementation make this different than the solutions in other languages.
We discussed comparing normalized strings:
```swift
let chars: [Character] = ["a", "ä"]
extension Character {
    func isSemanticallyEquivalent(to other: Character) -> Bool {
//        String(self).compare(String(other), options: [.diacriticInsensitive, .caseInsensitive, .widthInsensitive], locale: .current) == .orderedSame
        String(self).folding(options: [.diacriticInsensitive, .caseInsensitive, .widthInsensitive], locale: .current) == String(other).folding(options: [.diacriticInsensitive, .caseInsensitive, .widthInsensitive], locale: .current)
    }
}
print(chars[0].lowercased() == chars[1].lowercased())
print(chars[0].isSemanticallyEquivalent(to: chars[1]))
```swift
Then how to solve the problem: First the indexing solution which shows how RandomAccessCollection works.  YUou should no use this solution in any language since index math is unsafe:
```swift
extension RandomAccessCollection where Element == Character  {
    var isPalindrome: Bool {
        let backwards = reversed()
        var front = indices.first
        var back = backwards.indices.first
        while let unwrappedFront = front, let unwrappedBack = back {
            front = self[unwrappedFront...].firstIndex(where: \.isLetter)
            back = backwards[unwrappedBack...].firstIndex(where:\.isLetter)
            guard let unwrappedFront = front, let unwrappedBack = back  else { return true }
            guard self[unwrappedFront].isSemanticallyEquivalent(to: backwards[unwrappedBack]) else {
                return false
            }
            front = front.map { self.index(after: $0) }
            back = back.map { backwards.index(after: $0)}
        }
        return true
    }
}
```
Next the iterator solution:
```swift
extension BidirectionalCollection where Element == Character {
    var isPalindrome2: Bool {
        var frontIterator = makeIterator()
        var backIterator = reversed().makeIterator()
        var matchCount = 0
        let length = count / 2
        while let front = frontIterator.next(where: \.isLetter), let back = backIterator.next(where: \.isLetter), matchCount < length  {
            guard front.isSemanticallyEquivalent(to: back) else {
                return false
            }
            matchCount += 1
        }
        return true
    }
}

private extension IteratorProtocol where Element == Character {
    mutating func next(where predicate: (Character) -> Bool) -> Character? {
        while let next = next(){
            if predicate(next){
                return next
            }
        }
        return nil
    }
}
```
And finally the functional solution:
```swift
extension String {
    var isPalindrome3: Bool {
        zip(
            lazy.compactMap { $0.isLetter ? $0 : nil },
            reversed().lazy.compactMap { $0.isLetter ? $0 : nil }
        ).prefix(count/2).allSatisfy { $0.isSemanticallyEquivalent(to: $1) }
    }
}
```
## 2025.05.24

Discussion about testing, specifically about testing Combine. 

- https://developer.apple.com/documentation/combine/processing-published-elements-with-subscribers  
- https://github.com/FlineDev/ErrorKit

Carlyn gave us a Swift testing demo and it is awesome. We also went over how to get code coverage 
numbers in Xcode.    
    
- https://developer.apple.com/documentation/testing/migratingfromxctest

Josh talked about how many

- https://www.hyrumslaw.com
    
10:33:45 From Peter Wu to Everyone:
    For larger code bases codecov is nice that you can see the lines not covered in a PR https://about.codecov.io
    

A previous project from Josh (before concurrency) forming a nice example about how to get the buisness logic out of your tests.

- https://github.com/joshuajhomann/DeclarativeTests
  

### Discussion of AI and Coding Tools

- https://openai.com/index/introducing-codex/    
- https://repoprompt.com
- https://pre-commit.com/
- https://aider.chat
    
11:05:51 From carlyn to Everyone:
    https://www.cookiecutter.io
    
### New Swift Playground

From Bob: This is newly released from Marcin Krzyzanowski: a third-party 
“Swift Playground”. https://notepadexe.com/ Looks like fun.
    
---

## 2025.05.17


### Discussion on Apple Developer Ecosystem

- General longing for the simple early days and the wonders of getting new stuff at WWDC.
- Apple behind in server tech? Swift could be a great solution.
- Widgets are not in a great state. Hoping for improvements at WWDC. (Problems around multiprocessing and controlling when they wake up.)    

### Swift Proposals

- https://github.com/swiftlang/swift-evolution/blob/main/proposals/0481-weak-let.md
    

#### Progress

- https://forums.swift.org/t/pitch-progress-reporting-in-swift-concurrency/78112    
- https://forums.swift.org/t/review-sf-0023-progress-reporting-in-swift-concurrency/79474

### Using OpenAPI Generator

- https://developer.apple.com/videos/play/wwdc2023/10171/
- https://www.swift.org/blog/introducing-swift-openapi-generator/
    

### Keyboard Avoidance

- https://www.fivestars.blog/articles/swiftui-keyboard/

### Dependency Management PointFree

A demo of using the dependency management system from pointfree

- https://swiftpackageindex.com/pointfreeco/swift-dependencies/main/documentation/dependencies


### Dependency Management 

Alex showed us a dependency injection tool he created.

- https://swiftpackageindex.com/bealex/Macaroni

### Programming Font

- https://en.wikipedia.org/wiki/PragmataPro
- https://github.com/fabrizioschiavi/pragmatapro
- https://github.com/shytikov/pragmasevka
    

### Swift Easter Egg: Jabberwocky

- https://github.com/swiftlang/swift/blob/44c5f9f4596dcb4d85cc2c61930851508df6c513/benchmark/single-source/CodableTest.swift#L72
    

---

## 2025.05.10


### Upcoming Events

- https://github.com/twostraws/wwdc
- https://communitykit.social/schedule.html


### Swift Concurrency is Awesome
- https://mastodon.social/@Migueldeicaza/114446205671894351
  

### Distributed Actors    

Looking for examples.

- https://www.swift.org/blog/distributed-actors/
    
Example (non-production, proof of concept): https://github.com/franklefebvre/DistributedActors-FrenchKit
    
- https://developer.apple.com/documentation/xpc


### Experiments with containerRelativeFrame    

- https://developer.apple.com/documentation/swiftui/view/containerrelativeframe(_:alignment:)
    

```           
available length = ((container length - safe area) - (spacing x (count - 1))       
column length = available length / count
       
view length = (column length x span) + ((span - 1) x spacing)
```

Here is the code we experimented with:

```swift
    struct ContentView: View {
        var body: some View {
      ScrollView(.horizontal) {
       LazyHStack(spacing: 100) {
        ForEach(0..<20) { item in
         Rectangle()
          .fill([Color.red, .green, .blue][item % 3])
    //      .aspectRatio(3.0 / 2.0, contentMode: .fit)
          .frame(height: 100)
    //      .overlay(Color.yellow.opacity(0.5))
          
          .containerRelativeFrame(
           .horizontal, count: 3, span: 1, spacing: 100)
    //      .overlay(Color.blue.opacity(0.5))
        }
       }
      }
    //  .safeAreaPadding(.horizontal, 20.0)
        }
    }
    
    #Preview {
        ContentView()
    }
```
    

### What is a Crash?

A cool low level exploration:

- https://blog.jacobstechtavern.com/p/what-is-a-crash
    

---

## 2025.05.03

### What's New in Swift 6.1

- https://www.hackingwithswift.com/articles/276/whats-new-in-swift-6-1
    

### Deep Dish Videos

- https://www.youtube.com/@DeepDishSwift/streams
- https://deepdishswift.com/#schedule
  
### Swift Mocking

A mocking library announced at Deep Dish from Peter's company fetch-rewards!

- https://swiftpackageindex.com/fetch-rewards/swift-mocking    
- https://github.com/fetch-rewards/swift-mocking


### SSE Server Streaming Events

- https://github.com/launchdarkly/swift-eventsource    
- https://github.com/Recouse/EventSource

Carlyn's experiments on the subject.

- https://github.com/carlynorama/APItizer/blob/main/Sources/APItizer/SSEListener.swift

---

## 2025.04.26


### Concurrency Changes

    https://swiftpackageindex.com/fetch-rewards/swift-mocking
    

Peter took us on a blog post tour:

- https://www.avanderlee.com/concurrency/swift-6-2-concurrency-changes/
 

### Better Sounds

Exploring the sounds that are available:

```
    import AVFoundation
    var greeting = "Hello, playground"
    
    let systemSoundIDs: [SystemSoundID] = Array(1000...4000).map { SystemSoundID($0)}
    
    for id in systemSoundIDs {
    //    AudioServicesPlaySystemSoundWithCompletion(id) {
    //        print(id)
    //        return
    //    }
        AudioServicesPlaySystemSound(id)
        AudioServicesPropertyID(systemSoundIDs[0])
    }
```

Tutorial for creating system sounds (with a funny ending):    
    
- https://www.youtube.com/watch?v=TjmkmIsUEbA
    

Haptics might be a useful semantic way to get some sounds:

- https://developer.apple.com/documentation/corehaptics/delivering-rich-app-experiences-with-haptics


### Backups

"321" - Three copies of your data, two formats, one offsite.

"Just use Backblaze."

---

## 2025.04.19

### Using Ignite

Paul Hudson's static website builder, Ignite, continues to be awesome to use. Mihaela 

- https://aleahim.com

Talked about how to use your own custom domain.

- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site

Useful for debugging DNS issues:

https://dnschecker.org/    


### try! Swift Tokyo Conference

- https://www.youtube.com/@trySwiftConference/videos
  

Along with some of Frank's picks:

- https://www.youtube.com/watch?v=eQefdC2xDY4    
- https://www.youtube.com/watch?v=xtXaxMlFI6M&pp=0gcJCX4JAYcqIYzv
    

Learning Regex:    
- https://regexcrossword.com
- https://regex101.com
    
Example: let regex = /^([1-9]\d{0,2}(\,\d{3})*|([1-9]\d*))(\.\d{2})?$/
    
From Apple:

- https://developer.apple.com/videos/play/wwdc2022/110357
- https://developer.apple.com/videos/play/wwdc2022/110358


### Why Chris Eidhof avoids Group
    
- https://chris.eidhof.nl/post/why-i-avoid-group/
    
SwiftUI works more consistently if you have a single stable view at the root of your hierarchy.

### SwiftUI and Identity    

```swift
// Single identity
// .clear option becomes a no-op 
ViewWithState()
    .background(flag ? .red : .clear)
    .animation(.easeInOut(duration: 2), value: flag)
```

As Josh points out, you still get the space taken.

```swift    
struct ContentView: View {
    var body: some View {
        VStack {
            Image(systemName: "globe")
                .imageScale(.large)
                .foregroundStyle(.tint)
            Text("Hello, world!").opacity(0.0)
            Text("a")
        }
        .padding()
    }
}
```

### New Development Environments (Design tools)


- https://createwithplay.com

Firebase

- https://www.firebasestudio.vip
- https://firebase.google.com

### Learning Xcode Instruments

A new cohort of the epic instruments workshop is going to run in May:
- https://swift-virtuoso.com
    
### Presentation: Removing Combine

Josh started a presentation about the tooling that you can build in order 
to ditch import Combine.

Tools we reviewed this week:

- Subject
- Subscriptions
- ViewModel

One more abstraction to build next week and we will be ready to convert apps.

Source code TBD.

---

## 2025.04.12

### Async Discussion

When should you dispatch to the background?

No clear rule. Measure. An example from Josh:

```swift
import SwiftUI

@Observable
@MainActor
final class VM {
    var names: [String] = []
    func sort() async {
        async let sortedNames = { [names] in
            names.sorted()
        }()
        names = await sortedNames
    }
}
```

Peter brings up the point about re-entrancy. That leads to a discussion
about implementing switch map.

https://rxmarbles.com

- FlatMap in Combine is Merge Map
- FlatMap in AsyncAlgorithms is concatMap

There are many ways to flatten such as exhaustMap.

- https://rxjs.dev/api/operators/exhaustMap

Here is a manual way of doing it:

```swift
@Observable
@MainActor
final class VM {
    var names: [String] = []
    var sortTask: Task<[String], Error>?
    func sort() async {
        sortTask?.cancel()
        let sortTask = Task.detached { [names] in
            try await Task.sleep(for: .seconds(1))
            return names.sorted()
        }
        self.sortTask = sortTask
        do {
            names = try await sortTask.value
        } catch {
            switch error {
            case is CancellationError: print("task was canceled")
            default: print(error.localizedDescription)
            }
        }
    }
}
```

### Xcode Preview Bug

Ed filed feedback on Xcode previews always flipping back to their default (half screen) size.


### Benchmarking

How can you be sure that a better abstraction isn't slowing down your code too much. How can you
measure it?  It is a hard problem.

### Swift Evolution Proposal Review


#### Yielding Accessors

- https://github.com/swiftlang/swift-evolution/blob/main/proposals/0474-yielding-accessors.md


#### Observed

- https://github.com/swiftlang/swift-evolution/blob/main/proposals/0475-observed.md


### Swift Forums

There is a lot of detailed, amazing information on them.  Peter wonders where they get the time
to make these long, detailed posts.

You can find the pitches (pre-proposal stage) on the forums:

https://forums.swift.org/c/evolution/pitches/5


---

## 2025.04.05

### Discussion on SwiftData

Some key debugging tips:

- https://www.avanderlee.com/debugging/core-data-debugging-xcode/
    

You can see the underlying SQL commands: `-com.apple.CoreData.SQLDebug 1`
    
- https://developer.apple.com/documentation/swiftdata/adding-and-editing-persistent-data-in-your-app  
    
10:12:17 From Josh Homann to Everyone:
    https://www.hackingwithswift.com/quick-start/swiftui/how-to-dismiss-the-keyboard-for-a-textfield
    
10:13:21 From Josh Homann to Everyone:
    https://developer.apple.com/documentation/uikit/synchronizing-documents-in-the-icloud-environment
    
10:18:42 From Ray Fix to Everyone:
    https://www.pointfree.co/blog/posts/168-sharinggrdb-a-swiftdata-alternative
    

New in iOS 18 there are notifications for SwiftData that you can lisen to.

- https://developer.apple.com/documentation/swiftdata/modelcontext/notificationkey

Recommended reading for SwiftData:

- https://fatbobman.com/en/tags/SwiftData/

### Modular Apps
    
Mihaela MJ is working on a modular framework. Here is a working sample project

https://github.com/mihaelamj/Formidabble

### Design Patterns

It is always possible to convert between level and edge based events.

```swift
    Publishers.Merge(
        NotificationCenter.default.publisher(for: NSApplication.willResignActiveNotification).map { _ in false },
        NotificationCenter.default.publisher(for: NSApplication.willBecomeActiveNotification).map { _ in true }
    )
    .prepend(true)
```

Looking deeper at Patterns with Josh (such as the iterator pattern):


```swift
extension Sequence {
  static func +<Right: Sequence>(lhs: Self, rhs: Right) -> ConcatenatedSequence<Self, Right, Element> {
    ConcatenatedSequence(leftSequence: lhs, rightSequence: rhs)
  }
}
    
struct ConcatenatedSequence<Left: Sequence<Value>, Right: Sequence<Value>, Value>: Sequence {
  typealias Element = Value
  var leftSequence: Left
  var rightSequence: Right
  func makeIterator() -> Iterator {
      .init(leftIterator: leftSequence.makeIterator(), rightIterator: rightSequence.makeIterator())
  }
  struct Iterator: IteratorProtocol {
      typealias Element = Value
      var leftIterator: Left.Iterator
      var rightIterator: Right.Iterator
      mutating func next() -> Value? {
          leftIterator.next() ?? rightIterator.next()
      }
  }
}
    
let a = [1,2,3] + Set([4,5,6])
for value in a {
    print(value)
}
``` 

```swift
extension Sequence {
  static func +(lhs: Self, rhs: some Sequence<Element>) -> some Sequence<Element> {
    sequence(
        state: (
                leftIterator: lhs.makeIterator(),
                rightIterator: rhs.makeIterator()
        )
    ) { state in
          state.leftIterator.next() ?? state.rightIterator.next()
    }
}
```    

---

## 2025.03.29

### Instruments

A new video tutorial from Apple about instruments. 90 minutes long.

- https://developer.apple.com/tutorials/instruments

### Swift 6: What am I missing?

If you go to the evolution website:

- https://www.swift.org/swift-evolution/
    
You can apply the filters "Implemented" and then the versions you are interested in
such as Swift 6, Swift 6.1, Swift 6.2 to see what features are available.

### Vibe Coding

An interesting article (via Josh) about a potential future for the industry.

- https://irace.me/vibe

Gemini 2.5 model is new model that does a lot of stuff correctly that other models don't seem to be able to.

- https://www.youtube.com/watch?v=RxCZhltR9Cw
    
Someone mentioned that Claude is good for interactive Vibe coding.

### Presentation: GoF: Design Patterns in Swift

Josh H. presented about the classic "Gang of Four" Design patterns--it is a common lexicon that can be used
to communicate with other developers or even machines using prompts.


#### Creational Patterns

These focus on object creation mechanisms, promoting better encapsulation and system independence.
    
- **Factory Method:** Defines an interface for creating objects, letting subclasses decide the class to instantiate.
- **Abstract Factory:** Provides an abstract factory class that creates families of related objects.
- **Builder:** Separates object construction from its representation, enabling different representations through the same process.
- **Prototype:** Creates objects by cloning existing instances rather than using constructors.
- **Singleton:** Ensures a class has only one instance and provides global access to it.
    
#### Structural Patterns

These focus on how classes and objects can be composed to form larger structures.

- **Adapter:** Converts an interface to another, allowing incompatible classes to work together.
- **Decorator:** Dynamically adds responsibilities to objects by wrapping them in decorator classes.
- **Proxy:** Acts as a placeholder for an object, controlling access and handling tasks like lazy loading.
- **Facade:** Provides a simplified interface to a complex system, reducing exposed complexity.
- **Composite:** Treats individual and composite objects uniformly, useful for tree structures.
- **Flyweight:** Shares data among multiple objects to reduce memory usage.
    

#### Behavioral Patterns
    
These focus on how classes interact and the responsibilities of objects within a system.

- **Strategy:** Encapsulates algorithms, allowing selection at runtime based on conditions.
- **Observer:** Establishes a one-to-many dependency, notifying dependents of state changes.
- **State:** Changes object behavior when its internal state changes.
- **Chain of Responsibility:** Passes requests along a chain of handlers until one handles it.
- **Command:** Encapsulates requests as objects for operations like logging and undo/redo.
- **Iterator:** Accesses aggregate elements sequentially without exposing the structure.
- **Mediator:** Reduces coupling between classes by encapsulating interactions.
- **Memento:** Captures and restores object state, useful for undo/redo functionality.
- **Visitor:** Adds methods to objects without changing their classes, useful for operations across sets of objects.
- **Template Method:** Defines an algorithm skeleton in a base class, letting subclasses implement specific steps.
    

### Other Patterns

Peter mentioned a pattern that he has been looking into

- https://swiftology.io/articles/typestate/
 

Alex mentioned one of his favorites: "Inversion of Control 🙂"

---

## 2025.03.22

### Discussion

Ray shared a recent experience with upgrading XCTest to Swift Testing.
The migration was straightforward in Xcode and there is a good migration
guide.

- https://developer.apple.com/documentation/testing/migratingfromxctest
    

### Swift Evolution

Related to Swift testing, this proposal means you can use a short description with spaces and punctuation 
as the name of your test:

- https://github.com/swiftlang/swift-evolution/blob/main/proposals/0451-escaped-identifiers.md

Josh also taked about a new addition to the language which lets you better hide implementation details.
  
- https://github.com/swiftlang/swift-evolution/blob/main/proposals/0409-access-level-on-imports.md


### Swift Packages    

Talked about modularization.

You can set the library type to statically or dynamically link packages. 

https://developer.apple.com/documentation/packagedescription/product/library(name:type:targets:)
    

CoreData in packages needs to be handled specially: https://ishabazz.dev/blog/2020/7/5/using-core-data-with-swift-package-manager
    

### Other discussion
    
From Ed returning integers as a blob of bytes:

```swift
extension FixedWidthInteger {
  var data: Data {
    let data = withUnsafeBytes(of: self) { Data($0) }
    return data
  }
}
```

From Josh (another way to deserialize)

```swift
enum JSON {
    indirect case array([JSON])
    indirect case dictionary([String: JSON])
    case boolean(Bool)
    case number(Double)
    case string(String)
    case null
}
    
extension JSON: Decodable {
    init(from decoder: Decoder) throws {
        self = try Result { try decoder.singleValueContainer() }
            .flatMap { container in
                container.decodeNil()
                    ? .success(JSON.null)
                    : Result { JSON.boolean(try container.decode(Bool.self)) }
                        .flatMapError { _ in Result { JSON.number(try container.decode(Double.self)) } }
                        .flatMapError { _ in Result { JSON.string(try container.decode(String.self)) } }
                        .flatMapError { _ in Result { JSON.array(try container.decode([JSON].self)) } }
                        .flatMapError { _ in Result { JSON.dictionary(try container.decode([String: JSON].self)) } }
             }.get()
    }
}
```    

---

## 2025.03.15

### Discussion 

How to cleanup space on your disk.

#### Daisydisk
- https://apps.apple.com/us/app/daisydisk/id411643860?mt=12
- https://daisydiskapp.com    


#### Hyperspace to delete duplicates

- https://hypercritical.co/hyperspace/

#### OmniDiskSweeper

- A free app from OmniGroup: 

- https://www.omnigroup.com/more
    
### Presentation: Recent Swift Evolution Topics

MutableSpan: https://github.com/swiftlang/swift-evolution/blob/main/proposals/0467-MutableSpan.md

To understand borrowing and consuming we looked at some of the 

```swift
static func embiggened(_ value: [Int]) -> [Int] {
    var mutableValue = value
    for index in mutableValue.indices {
        mutableValue[index] += 1
    }
    return mutableValue
}

static func embiggened(byBorrowing value: borrowing [Int]) -> [Int] {
    var mutableValue = copy value
    for index in mutableValue.indices {
        mutableValue[index] += 1
    }
    return mutableValue
}
static func embiggen(byExclusiveBorrow value: inout [Int]) {
    for index in value.indices {
        value[index] += 1
    }
}
static func embiggen(byConsuming value: consuming [Int]) -> [Int] {
    for index in value.indices {
        value[index] += 1
    }
    return consume value
}
    
let a = [1, 2, 3]
let b = embiggen(byConsuming: a)
print(a,b)
```    

### Presentation: Replacing Combine with Modern Concurrency

Josh continued with a topic from last week about how to replace combine
with modern Swift concurrency. This week Josh created a `Pipe` abstraction
to allow multiple observers of a sent value (much like notification center).

```swift
import Foundation
import Synchronization
    
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


---

## 2025.03.08

### Instruments

James Dempsey has a new online course that teaches the ins and outs of Apple Instruments:

- https://swift-virtuoso.com

Also, there is a new Processor Trace Instrument that uses low level hardward on the M4 and iPhone 16 to collect very detailed metrics about performance.

https://developer.apple.com/documentation/xcode/analyzing-cpu-usage-with-processor-trace?changes=la
    

### OpenAI on Xcode
Chatgpt Xcode: https://help.openai.com/en/articles/10119604-work-with-apps-on-macos
    

### Running a VM on macOS

    macOS VM: https://arstechnica.com/gadgets/2022/07/how-to-use-free-virtualization-apps-to-safely-test-the-macos-ventura-betas/
    

### Syncing across devices
    
- NSUnibiquitousKeyValueStore https://developer.apple.com/documentation/foundation/nsubiquitouskeyvaluestore
- CKAsset to sync user data: https://developer.apple.com/library/archive/documentation/DataManagement/Conceptual/CloudKitQuickStart/AddingAssetsandLocations/AddingAssetsandLocations.html#//apple_ref/doc/uid/TP40014987-CH6-SW2
    

### URL Encoding Game State    

Ways to crunch down the JSON so it can be URL encoded.

- https://www.whynotestflight.com/excuses/how-do-custom-encoders-work/    
- https://github.com/SomeRandomiOSDev/CBORCoding
- https://cbor.io/impls.html
- https://msgpack.org

Using a server:    

A large infrastructure:

- https://www.swift.org/blog/how-swifts-server-support-powers-things-cloud/


Smaller deployments:

- https://fosdem.org/2025/schedule/event/fosdem-2025-4592-your-first-aws-lambda-function/
- https://rambo.codes/posts/2021-12-06-using-cloudkit-for-content-hosting-and-feature-flags


### Industry Compensation

- https://newsletter.pragmaticengineer.com/p/trimodal    
- https://www.levels.fyi/t/software-engineer?countryId=254
    

### Presentation (Josh): Removing @StateObject

Previously, Josh demostrated how SwiftUI can use Combine to achieve lazy initialization
and prevent repeated re-initialization of a view model of a view in a timeline view
using StateObject.

Inspired by this blog post:

- https://fatbobman.com/en/posts/lazy-initialization-state-in-swiftui/
    

Josh created a special property wrapper ViewModel that does the same thing and means 
you don't need to use StateObject or derive from Combine's ObservableObject.


```swift
import SwiftUI
import PlaygroundSupport
    
PlaygroundPage.current.setLiveView(ContentView())
    
struct ContentView: View {
    var body: some View {
        TimelineView(.periodic(from: .now, by: 3)) { _ in
            let _ = print("-----------\(Date.now)-----------")
            V()
        }
    }
}
    
struct V: View {
    var vm = VM("naked var")
    @State var vm0 = VM("@State")
    @ViewModel var vm1 = VM("@ViewModel")
    var body: some View {
        Text(vm.text)
        Text(vm0.text)
        Text(vm1.text)
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
```    

Here is the property wrapper:

```swift
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


---

## 2025.03.01


### FOSDEM

There were a lot of Swift topics presented at this years FOSDEM (Free Open Source Developers European Meeting) that have been
organized for viewing here:

- https://swiftlang.github.io/event-fosdem/

### SwiftUI Fundamentals

A new book about SwiftUI from Natalia Panferova of nilcoalecing is available. Bob DeLaurentis says that it does a great job in 
explaining some of the subtleties of the framework.

- https://books.nilcoalescing.com/swiftui-fundamentals
    

### Electronic Readers

This led to a discussion about books and apps for reading ebooks.

- Remarkable: https://remarkable.com  (https://www.amazon.com/dp/B0CZ9VFQ2P)
- Meebook ebook reader    
- https://www.amazon.ae/AZMXDVP-Meebook-P78-Adjustable-Micro-SD/dp/B09Q37DFJ7
- https://www.liquidtext.net
- Boox Palma: https://shop.boox.com/products/palma
- https://supernote.com/products/supernote-nomad



### Forward Progress and Concurrency

Led by Peter and Josh, we discussed concurrency and the tools to guarantee forward progress.

- https://github.com/swiftlang/swift-evolution/blob/main/proposals/0433-mutex.md


To visualize / test restricting cooperative thread pool:  https://alejandromp.com/development/blog/limit-swift-concurrency-cooperative-pool/

A key insight is the ability to use `LIBDISPATCH_COOPERATIVE_POOL_STRICT=1` to make sure forward progress is always being made.

This is the thread on forum that goes in-depth on lock ownership and safety in using across suspension point https://forums.swift.org/t/incremental-migration-to-structured-concurrency/54939/5
    

Assert that you are on a specific queue https://developer.apple.com/documentation/dispatch/dispatchprecondition(condition:)
    
10:33:29 From Mihaela MJ to Everyone:
    https://github.com/siteline/swiftui-introspect


### New Isolation Guarantees
    
Josh gave us a tour of proposal 0461 and how it makes things more similar between sync and async methods.

- https://github.com/swiftlang/swift-evolution/blob/main/proposals/0461-async-function-isolation.md
    

```swift
import Foundation
    
final class Q {
    func sync() {
        MyActor.assertIsolated()
        print("synchronous Q")
    }
    nonisolated func nonSync() async {
        MyActor.assertIsolated()
        print("asynchronous Q")
    }
}
    
@MyActor
final class P {
    var q = Q()
    func doStuff() async {
        q.sync()
        async let v = q.nonSync()
        let _ = await v
    }
}
    
@globalActor
actor MyActor: GlobalActor {
    static let shared = MyActor()
    private init() { }
}
    
Task {
    let p = await P()
    await p.doStuff()
}
```



### Making UI around Command line

Some useful tools!

- https://forums.swift.org/t/review-sf-0007-introducing-swift-subprocess/70337   
- https://github.com/apple/swift-argument-parser
    

Also, some code from Carlyn:

```swift
@discardableResult
func shellOneShot(_ command: some StringProtocol) throws -> String {
   let task = Process()
   let pipe = Pipe()
       
   task.standardOutput = pipe
   task.standardError = pipe
   task.arguments = ["-c", command]
       
   //task.currentDirectoryURL
   //task.qualityOfService
   //task.environment = ProcessInfo.processInfo.environment
       
   task.standardInput = nil
   task.executableURL = URL(fileURLWithPath: "/bin/zsh")
   try task.run()
       
   let data = pipe.fileHandleForReading.readDataToEndOfFile()
   let output = String(data: data, encoding: .utf8)!
       
   task.waitUntilExit()
    
   if task.terminationStatus == 0 || task.terminationStatus == 2 {
     return output
   } else {
     print(output)
     throw CustomProcessError.unknownError(exitCode: task.terminationStatus)
   }
}

@discardableResult
func runProcess(_ tool:URL, arguments:[some StringProtocol] = [], workingDirectory:URL? = nil) throws -> String {
    let task = Process()
    let pipe = Pipe()
        
    task.standardOutput = pipe
    task.standardError = pipe
    task.arguments = arguments
        
    if let workingDirectory {
        task.currentDirectoryURL = workingDirectory
    }
    //task.qualityOfService
    //task.environment
    
    task.standardInput = nil
    task.executableURL = tool
    try task.run()
        
    let data = pipe.fileHandleForReading.readDataToEndOfFile()
    let output = String(data: data, encoding: .utf8)!
        
    task.waitUntilExit()
    
    if task.terminationStatus == 0 || task.terminationStatus == 2 {
      return output
    } else {
      print(output)
      throw CustomProcessError.unknownError(exitCode: task.terminationStatus)
    }
    }

enum CustomProcessError: Error {
  case unknownError(exitCode: Int32)
}
```

### Apple Vision Pro Meeting

Apparently there was an interesting (mostly non-code meeting) by Apple last week about
how to develop "experiences" of vision pro. Ed atteneded online and John B was there in-person.
Four sessions over the course of the day.

Apparently they had a demo where they showed how to render the experience of being on the moon.

```none
    Environment metrics
    Geometry: 20K-500K total triangles
    View: -100K triangles per camera angle
    Memory: Less than 250MB total texture data
    Entities: Under 200 draw calls
    Materials: Unlit with custom shader effects
```
    
---


## 2025.02.22

### Concurrency in Legacy Code

Questions from Rainer about how to use concurrency effectively in legacy code.

We talked about where things run and how the default might change in future versions
of Swift.


Link from Peter:

- https://developer.apple.com/documentation/swift/mainactor/assertisolated(_:file:line:)

Examples from Josh:

```swift
struct A {
    //@MainActor
    nonisolated func a() {
        Task {
            MainActor.assertIsolated()
        }
    }
}

Task {
     A().a()
}


```

Instead of falling back to using Combine (which bring tech debt with it), a suggestion from Josh to make
simple abstractions to avoid creating Tasks everywhere.

    
```swift
extension AsyncSequence where Failure == Never {
    func subscribe<Unretained: AnyObject>(withUnretained object: Unretained, onNext: @escaping (Unretained, Element) -> Void) -> Task<Void, Never> {
        Task { [weak object] in
            for await value in self {
                guard let object else { return }
                onNext(object, value)
            }
        }
    }
}
```

Can be used like this:

```swift
actor A {
    var subscription: Task<Void, Never>?
     func a()  {
         let (output, input) = AsyncStream.makeStream(of: Int.self, bufferingPolicy: .bufferingNewest(1))
         subscription = output.subscribe(withUnretained: self) { unretained, value in
             print(unretained, value)    
         }
         input.yield(1)
         input.yield(2)
         input.yield(3)
    }
}
```
 
### Protocol Composition   

- https://developer.apple.com/documentation/swiftui/viewbuilder/buildeither(first:)


### File System

This came up in the context of Peter's custom image caching problem.

Some notes from Carlyn:

- https://www.whynotestflight.com/excuses/how-to-do-some-basic-file-handling/
- https://forums.swift.org/t/what-is-the-best-way-to-work-with-the-file-system/71020/17
- https://github.com/apple/swift-nio-examples/blob/4bd02d14e6309bbd722b64f6de17855326aa1145/backpressure-file-io-channel/Sources/BackpressureChannelToFileIO/FileIOChannelWriteCoordinator.swift#L17 
- https://github.com/apple/swift-nio/tree/5f60ceeca072475252ca1ad747bd1156a370fe5d/Sources/NIOFileSystem
  

Using custom executors (Josh)

- https://github.com/swiftlang/swift-evolution/blob/main/proposals/0392-custom-actor-executors.md
- https://www.swift.org/migration/documentation/swift-6-concurrency-migration-guide/incrementaladoption
    

```swift
actor LandingSite {
    private let queue = DispatchSerialQueue(label: "something")

    nonisolated var unownedExecutor: UnownedSerialExecutor {
        queue.asUnownedSerialExecutor()
    }
    
    func acceptTransport(_ transport: PersonalTransportation) {
        // this function will be running on queue
    }
}
```
    
10:35:09 From carlyn to Everyone:
    private func appendData(data: Data) throws {
        let fileHandle = try FileHandle(forWritingTo: storageUrl)
        fileHandle.seekToEndOfFile()
        fileHandle.write(data)
        fileHandle.closeFile()
      }

Creating a custom global actor:

```swift
@globalActor actor SharedActor {
  static let shared = SharedActor()
}
    
@SharedActor final class A { }
@SharedActor final class B { }
```

- Actor all implicitly conform to the Actor protocol https://developer.apple.com/documentation/swift/actor
- Swift Concurrency and Instruments https://developer.apple.com/videos/play/wwdc2022/110350

### Delphi Style Components

Starting with Package definitions. From MJ

```swift
// Dependency grouping
enum Dependencies {
    static var common: [Target.Dependency] {
        [
            .product(name: "Difference", package: "Difference"),
            .product(name: "LifetimeTracker", package: "LifetimeTracker"),
        ]
    }
}

    .target(
         name: "SharedModels",
         dependencies:
            Dependencies.common + [
                "AutomaticSettings",
            ]
    ),
```    

These ideas come from:

- https://www.swiftystack.com/curriculum
    

Related: 

```swift
@_exported import PackageName
```

For details see:

- https://github.com/swiftlang/swift/blob/main/docs/ReferenceGuides/UnderscoredAttributes.md
    

### Interesting Links
    

- New Junior Developers Can’t Actually Code: https://nmn.gl/blog/ai-and-learning
- Cybersecurity and AI https://cset.georgetown.edu/publication/cybersecurity-risks-of-ai-generated-code/
- Swift Navigation https://github.com/pointfreeco/swift-navigation
    

### Ed's Hex Tac Toe in Beta Review

Hex Tac Toe is waiting for Apple beta review.  Anyone else want to be 
on the beta, send your Apple email (DM).  I have all the ones from before.


---


## 2025.02.15

Peter worked on a caching system for an app and wanted feedback for
how it could be improved. The basic app is here:

https://github.com/PeterWu9/Recipes


A recommendation from Josh to use the headers in the HTTP response headers:

- https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
    
Also related:
- https://developer.apple.com/documentation/foundation/nsurlcache
    
- Async file reading https://losingfight.com/blog/2024/04/22/reading-and-writing-files-in-swift-asyncawait/

### SwiftUI View Builders


View builder returns some View which is a container view like `ConditionalContent`.

```swift    
struct W: View {
    let a: Int
    @ViewBuilder
    var body: some View {
        switch a {
        case ..<0: Text("Negative")
        case 0: Text("Zero")
        case 1... : Color.green
        default: EmptyView()
      }
    }
}
```
    

### SwiftUI Navigation Bug

Joe shared this SwiftUI navigation bug:

```swift
struct ContentView: View {
    var body: some View {
        NavigationStack {
            NavigationLink {
                Text("Do not tap back, you'll regret it")
                    .toolbarBackground(.visible, for: .navigationBar)
                    .toolbarBackground(Color.orange, for: .navigationBar)
                    .toolbarColorScheme(.dark, for: .navigationBar)
            } label: {
                VStack {
                    Text("First page is the sweetest")
                }               
                .padding()
            }
            .navigationTitle("First Page")
            .toolbarBackground(.visible, for: .navigationBar)
            .toolbarBackground(Color.orange, for: .navigationBar)
            .toolbarColorScheme(.dark, for: .navigationBar)
        }
    }
}
```

### Sequencing Animations    
    

Sample from Josh:

```swift
    withAnimation(animation, completionCriteria: .logicallyComplete) {
                operation()
            } completion: {
                continuation.resume()
            }
```


### Swift Blog gRPC 2
    
-  https://www.swift.org/blog/grpc-swift-2/
    

---

## 2025.02.08

### Discussions

- Creating a multi-platform framework bundle. https://developer.apple.com/documentation/xcode/creating-a-multi-platform-binary-framework-bundle/
    

- Integer generic parameters are going to be a thing. https://github.com/swiftlang/swift-evolution/blob/main/proposals/0452-integer-generic-parameters.md
    
- New InlineArray type. https://github.com/swiftlang/swift-evolution/blob/main/proposals/0453-vector.md
    
- Transferable protocol
    https://developer.apple.com/documentation/CoreTransferable/Transferable
    

### Assistive Technology

- App Intents https://developer.apple.com/videos/play/wwdc2024/10134/
- Guided Access https://www.theseniorlist.com/cell-phones/assistive-access/
- https://www.ninjaone.com/blog/ipad-kiosk-mode/
    
09:57:53 From Josh Homann to Everyone:
    Request sharing in FaceTime: https://support.apple.com/guide/iphone/request-give-remote-control-a-facetime-call-iph5d70f34a3/ios
    

### Hacking Problem
    

Puzzle from John Brewer

```swift
var test3 = [-1, 1, 2, 3, 4, -1, -9, -6, 10, 1, -5]
print(largestSumSpan(array: test3)) // [10, 1]
var test4 = [-1, 1, 2, 3, 4, -1, -9, -6, 8, 1, -5]
print(largestSumSpan(array: test4)) // [1, 2, 3, 4]
```
What is the best idiomatic Swift to handle this?

```swift    
print(missingPair([1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1]))
9
```

There is a "trick" to this one which to xor all of the bits.

Related book
    
- https://www.amazon.com/Hackers-Delight-2nd-Henry-Warren-dp-0321842685/dp/0321842685/ref=dp_ob_title_bk
    

---


## 2025.02.01

### Resources and SwiftPM

- Peter was able to make a common target that other targets could depend on.

Exciting announcement Carlyn let us know about is that Swift Build (used by Xcode)
is, as of today, an open source technology. It will support Windows and Linux.

- https://forums.swift.org/t/evolving-swiftpm-builds-with-swift-build/77596/2

Also, the official announcement:

https://www.swift.org/blog/the-next-chapter-in-swift-build-technologies/

We looked at conditional package inclusion. You can conditionalize based on
platform but it doesn't look like there are too many other options.

An example from Mihaela:

```swift
    .product(name: "ResChatHouUIKit", package: "ResChatHouUIKit", condition: .when(platforms: [.iOS])),
                    .product(name: "ResChatUIKit", package: "ResChatUIKit", condition: .when(platforms: [.iOS])),
                    .product(name: "ResChatHouAppKit", package: "ResChatHouAppKit", condition: .when(platforms: [.macOS])),
                    .product(name: "ResChatAppKitUI", package: "ResChatAppKitUI", condition: .when(platforms: [.macOS])),
                    ]
            ),
```

### Swift Playgrounds App

Now supports Swift 6.  You may need to remove previous versions.
- https://apps.apple.com/us/app/swift-playground/id1496833156?mt=12

### Hex Tac Toe

Ed is working on his game hex-tac-toe.  Lots of suggestions for how to improve.


### Other random stuff

It is an open source airdrop thing but written in Flutter:

- https://localsend.org

Josh demo'ed LLMs including deepseek on your local machine:

- https://ollama.com/library/deepseek-r1
    

You can run in from within a UI too that supports many models.

- https://chatboxai.app/en

---

## 2025.01.25

- How to share resources among multiple Swift packages.
- Continued working on Mine Sweeper

---

## 2025.01.18

### Making CoW Types Sendable

We modernized a small app to Swift 6. Making a type CoW and isolating all mutation
allows you to declare a type sendable. The mutable state is not shared so these 
properties can be marked sendable (unsafe).

### Performance

Measure the performance of a new collection type using the Swift performance package.

https://www.swift.org/blog/benchmarks/


### Mine Sweeper

Continued the mine sweeper example.

---

## 2025.01.10

### Debugging SceneKit Audio

We spent some time debugging a problem with a SceneKit app that was leaking audio players.

### Animating Text

Rainer was trying to animate text along a Bézier curve.

Josh reminded us of this project example from last year:

- https://github.com/aflockofswifts/meetings/tree/main/2024#20240518

Also, a Primer on Bézier curves: https://pomax.github.io/bezierinfo/
    

Rainer noted that the example he was trying to emulate: 

- https://github.com/objcio/S01E166-geometry-effects
  

His code here:
  
- https://github.com/minsOne/custom-ui-prototype-in-swiftui
  

### Continuing the Mine Sweeper Example

This week we looked at a serious performance problem in what we built so far.
Changing the color of a handful of tile taking almost a second to perform.

A nice video from Ben Cohen about Fast Safe Mutable State:

- https://www.youtube.com/watch?v=BXJIIQ-B4-E
    

An internal way to do in-place mutation:

- https://jano.dev/apple/2024/12/10/Modify-and-Yield.html
- https://forums.swift.org/t/modify-accessors/31872
    

But the biggest performance win was had by using a properly identifiable type in the ForEach statement of the grid.

---

## 2025.01.03

### A functional solution to Ed's game
  * Ed is making a game where he needs to match n distinct items in a row.  Josh offered a solution in functional swift:
  * We start with an assumption that we have a node, a sequence of adjacencies that can transform a node into another node, and the number of distinct items we want to match
```swift
let n = 6
let adjacency: some Sequence<(Node) -> Node?>
let node: Node
```
![layout](materials/blocks.png)
  * We can express the algorithm we want to apply as a node represents a winning state if there is a way to transform it into a sequence of n distinct elements. or more formally:
![layout](materials/existential.png)
  * Equivalently in swift:
```swift
let isWon = adjacency.contains { [node, n] adjacency in
	Set(sequence(first: node) { adjacency(node)}.prefix(n))).count == n
}
```
  * We can further express our intent with the use of explanatory variables:
```swift
let isWon = adjacency.contains { [node, n] adjacency in
    let adjacentUnique = Set(sequence(first: node) { adjacency(node)}.prefix(n))
	let isWinningRun = adjacentUnique.count == n
	return isWinningRun
}
```
* Ed asked how to get the winning nodes.  We can do this by changing the operator to `compactMap`:
```swift
let winningSets = adjacency.compactMap { [node, n] adjacency in
    let adjacentUnique = Set(sequence(first: node) { adjacency(node)}.prefix(n))
	let isWinningRun = adjacentUnique.count == n
	return isWinningRun ? adjacentUnique : nil
}
.reduce(into: Set<Node>()) { $0.formUnion($1) }
```

### Mine sweeper continued
* We updated the Layout to use a cache and added a viewModel:
```swift
@Observable
final class ViewModel: ObservableObject {
    private(set) var cells: Grid2D<Cell> = .init(rows: 8, columns: 8) { x, y in
        .init(id: x + y * 8, position: .init(x, y), color: .allCases.randomElement()!)
    }
    func tap(index: SIMD2<Int>) {
        cells[index].color = .blue
    }
}

struct Cell: Identifiable, Hashable {
    let id: Int
    let position: SIMD2<Int>
    var color: ViewModel.BoardColor
}

extension ViewModel {
    enum BoardColor: Hashable, CaseIterable {
        case red, green, blue
    }
}

struct ContentView: View {
    @StateObject private var viewModel = ViewModel()
    var body: some View {
        Board(dimension: 8) {
            ForEach(viewModel.cells.indices, id: \.self) { index in
                Group {
                    switch viewModel.cells[index].color {
                    case .red: Color.red
                    case .green: Color.green
                    case .blue: Color.blue
                    }
                }
                .onTapGesture {
                    viewModel.tap(index:  viewModel.cells[index].position)
                }
                .boardPosition(index)
            }
        }
    }
}

extension View {
    func boardPosition(_ position: SIMD2<Int>) -> some View {
        layoutValue(key: BoardPosition.self, value: position)
    }
    func boardPosition(x: Int, y: Int) -> some View {
        boardPosition(.init(x, y))
    }
}

struct Board: Layout {
    let dimension: Int

    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout Cache) -> CGSize {
        let size = proposal.replacingUnspecifiedDimensions(by: .zero)
        let minimumDimension = min(size.width, size.height)
        return .init(width: minimumDimension, height: minimumDimension)
    }

    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout Cache) {
        if cache.bounds != bounds {
            cache.bounds = bounds
            cache.cellSize = CGSize(width: bounds.width / Double(dimension), height: bounds.height / Double(dimension))
            let transform = CGAffineTransform
                .identity
                .translatedBy(x: bounds.origin.x, y: bounds.origin.y)
                .scaledBy(x: cache.cellSize.width, y: cache.cellSize.height)
            cache.grid = .init(rows: dimension, columns: dimension) { x, y in
                CGPoint(x: x, y: y).applying(transform)
            }
        }
        for view in subviews {
            let position = cache.grid[safe: view[BoardPosition.self]] ?? bounds.origin
            view.place(
                at: position,
                proposal: .init(cache.cellSize)
            )
        }
    }

    func makeCache(subviews: Subviews) -> Cache {
        .init()
    }

    struct Cache {
        var bounds = CGRect.zero
        var cellSize = CGSize.zero
        var grid: Grid2D<CGPoint> = .init(repeating: .zero, rows: 0, columns: 0)
    }
}

struct BoardPosition: LayoutValueKey {
    static let defaultValue = SIMD2<Int>.zero
}
```
