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

---

## Notes

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
