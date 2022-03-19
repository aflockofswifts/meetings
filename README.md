# A Flock of Swifts

We are a group of people excited by the Swift language. We meet each Saturday morning to share and discuss Swift-related topics. 

All people and all skill levels are welcome to join. 

## 2022.03.26

- **RSVP**: https://www.meetup.com/A-Flock-of-Swifts/

---

## 2022.03.19

### Swift 5.6

We discussed the features in Swift 5.6 in Xcode 13.3.

https://www.swift.org/blog/swift-5.6-released/


- Another way to think about `any` is "box" because it make explicit there is a boxing cost to using protocols as a "base-class".

We talked about method dispatch.
https://blog.allegro.tech/2014/12/swift-method-dispatching.html


### Swift 5.7 and beyond

Proposals we focus on include improvements `some` and `any`. We also looked at the syntax shortening proposal for `if let name = name {}` to `if let name {}` 

### Implementing Search

Caleb was looking for some advice about how to speed up his fuzzy search performance.

```swift
final class CardSearchViewModel: ObservableObject {
    @Published var searchTerm: String = ""
    @Published private(set) var cards: [Card] = []
    init(
        cardSearchService: CardSearchServiceProtocol = CardSearchService()
    ) {

        $searchTerm
            .debounce(for: .seconds(1), scheduler: DispatchQueue.main)
            .receive(on: DispatchQueue.global(qos: .userInitiated))
            .removeDuplicates()
            .map { searchTerm -> AnyPublisher<[MagicCard], Never> in
                searchTerm.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
                ? Just([]).eraseToAnyPublisher()
                : cardSearchService
                    .search(query: searchTerm)
                    .replaceError(with: [])
                    .eraseToAnyPublisher()
            }
            .switchToLatest()
            .map { $0.map(Card.init(magicCard:)) }
            .receive(on: DispatchQueue.main)
            .assign(to: &$cards)
    }
}
```

Manu mentioned: Premature optimization is the Root of Evil 
https://okaleniuk.medium.com/premature-optimization-is-the-root-of-all-evil-is-the-root-of-evil-a8ab8056c6b


---

## 2022.03.12

* We discussed use of the `@MainActor` tag for functions and closures as well as the `MainActor` singleton.
### Autoclosures
  * We revisited why you cannot write `XCTAssertTrue(await someAsyncFunction())
  * We looked at the signature for XCTAssertTrue:
  ```swift
  public func XCTAssertTrue(_ expression: @autoclosure () throws -> Bool, _ message: @autoclosure () -> String = "", file: StaticString = #filePath, line: UInt = #line)
  ```
  * We discussed what an `@autoclosure` is and why we would want to use one by looking by making an analog of the `??` operator:
  ```swift
    infix operator ?!

    func ?!<Value>(_ lhs: Value?, rhs: Value) -> Value {
        guard let lhs = lhs else { return rhs }
        return lhs
    }
  ```
  * We saw that the purpose of `@autoclosure` to is to defer expensive work (and possibly only perform it under certain conditions).  We saw that `XCTAssertTrue` wants to capture the error for its `@autoclosure` and reasoned that this is why the function is written with an `@autoclosure`
  * We then wrote a function with `Result` to solve the `@autoclosure` problem:
  ```swift
  extension Result where Failure == Error {
    init(awaiting operation: () async throws -> Success) async {
        do {
            self = .success(try await operation())
        } catch {
            self = .failure(error)
        }
    }
  }
  ```
  * we looked at a more declarative solution:
  ```swift
    class Tests_macOS: XCTestCase {

        func testA() async throws {
            try await
                after { try await a() }
                assert: { XCTAssertTrue($0) }
        }

    }

    func after<Value>(
        _ operation: () async throws -> Value,
        assert: (Value) throws -> Void
    ) async rethrows -> Void {
        let value = try await operation()
        try assert(value)
    }
  ```
  * We didn't make it to the final one line version, but its listed here:
  ```swift
  func a() async throws -> Bool {
    true
  }

  class Tests_macOS: XCTestCase {
      func testA() async throws {
          try await assertTrue(eventually: a)
      }
  }

  func assertTrue(
      eventually operation: () async throws -> Bool,
      _ message: @autoclosure () -> String = "",
      file: StaticString = #filePath,
      line: UInt = #line
  ) async throws {
      try await after(operation, assert: { XCTAssertTrue($0, message(), file: file, line: line)})
  }

  func after<Value>(
      _ operation: () async throws -> Value,
      assert: (Value) throws -> Void
  ) async rethrows -> Void {
      let value = try await operation()
      try assert(value)
  }
  ```

## 2022.03.05

More followup discussion of the coordinator pattern and deep linking. 

### FileAccess Protocol and Actors

Put file access behind an abstraction:

```swift
protocol FileAccess {
    func write(path: [String], data: Data) async throws
    func read(path: [String]) async throws -> Data
    func move(source: [String], destination: [String]) async throws
    func copy(source: [String], destination: [String]) async throws
    func enumerate(path: [String]) async throws -> AsyncStream<String>
    func delete(path: [String]) async throws
    func exists(path: [String]) async throws -> Bool
    func createDirectory(path: [String]) async throws
}
```

Then we can implement a concrete type:

```swift
actor NativeFileAccess: FileAccess {
  
  enum Error: Swift.Error {
    case couldNotEnumerate(String)
  }
  
  
  let root: URL
  
  init() {
    let path =
    NSSearchPathForDirectoriesInDomains(.documentDirectory,
                                        .userDomainMask, true)[0]
    root = URL(fileURLWithPath: path)
  }
  
  func write(path: [String], data: Data) async throws {
    try await Task {
      try data.write(to: root.appending(components: path))
    }.value
  }
  
  func read(path: [String]) async throws -> Data {
    try await Task {
      try Data(contentsOf: root.appending(components: path))
    }.value
  }
  
  func enumerate(path: [String]) async throws -> AsyncStream<String> {
    let location = root.appending(components: path)
    guard let enumerator = FileManager.default.enumerator(atPath: location.path) else {
      throw Error.couldNotEnumerate(location.absoluteString)
    }
    return AsyncStream(String.self) { continuation in
      Task {
        for element in enumerator {
          guard let nsString =  element as? NSString else { continue }
          let file = String(nsString)
          continuation.yield(file)
        }
        continuation.finish()
      }
    }
  }
}

private extension URL {
  func appending(components: [String]) -> URL {
    components.reduce(self) { $0.appendingPathComponent($1) }
  }
}
```

And it can be tested:

```swift
import XCTest
@testable import FileAccess

class FileAccessTests: XCTestCase {

  func checkThrows(method: () async throws -> Void) async {
    do {
      try await method()
    } catch {
      XCTFail("method throws")
    }
  }

  func testRoundTrip() async throws {
    
    let fileAccess = NativeFileAccess()
    
    let payload = try XCTUnwrap("Hello".data(using: .utf8))
    try await fileAccess.write(path: ["hello.txt"], data: payload)
    let readback = try await fileAccess.read(path: ["hello.txt"])
    XCTAssertEqual(readback, payload)
        
    await checkThrows {
     try await fileAccess.write(path: ["..", "..", "hello.txt"], data: payload)
    }
    
    // Alternate approach
    let r = await Task { try await fileAccess.read(path: ["nope.txt"]) }.result
    XCTAssertThrowsError(try r.get())
        
    let files = try await fileAccess.enumerate(path: []).reduce(into: []) { $0.append($1) }
    XCTAssertEqual(["hello.txt"], files)
  }
}
```

### Unsafe Pointers

Josh gave a quick demo of unsafe pointers and unsafe buffer pointers.

---

## 2022.02.26

We talked about a variety of topics including app navigation, deep linking and coordinators.

Rainer gave a demo of UIKit debugging tool called chisel by Facebook.

---

## 2022.02.19

### Rendering to pdf and printers
We discussed printing to pdf and printer contexts using:
* UIGraphicsPDFRendererContext: https://developer.apple.com/documentation/uikit/uigraphicspdfrenderercontext
* UIPrintPageRenderer: https://developer.apple.com/documentation/uikit/uiprintpagerenderer
* UIPrinterPickerController: https://developer.apple.com/documentation/uikit/uiprinterpickercontroller

### Leveling
We discussed leveling and compensation:
* https://medium.com/building-carta/engineering-levels-at-carta-d33db2a55a20
* www.levels.fyi
* https://www.amazon.com/dp/B08RMSHYGG
* https://staffeng.com

### Declarative Tests
Josh presented a project showing declarative testing: https://github.com/joshuajhomann/DeclarativeTests

## 2022.02.12

### App Privacy

Discussion about app privacy and how there is now an option to turn on URL logging for apps under settings :: general :: privacy down at the bottom.  You can also use a proxy to get at the urls and inspect the data.

Proxies:

- https://www.charlesproxy.com
- https://proxyman.io


Discussion about parental IT. Remote desktop via Facetime FTW.

### Core Data and Testing

Continued work on https://github.com/rayfix/DatabaseFacade  What we coded live is committed there.

Things we covered:

- actor basics
- The cost of making an actor conform to a protocol
- Type safe fetch requests
- Managing fetch request controller lifetimes
- Debugging concurrency issues with `-com.apple.CoreData.ConcurrencyDebug 1`
- Writing unit tests
- Making persistent stores in-memory containers
- Unit testing core data


---

## 2022.02.05

### Git and Git Ignore

Xcode has git integration that lets you look at pull requests. John has a problem with pagination and can only list up to "i" in his list of 89 repos.

Some other git clients:

- https://git-tower.com (@stuffmc's client of choice)
- https://gitup.co (Free, open source, works great on giant repos.)
- Sublime Merge
- Fork
- p4merge
- A text editor

Length side discussion about how git ignore files are processed.  You can see what your global git settings are with `git config --global -l`

Here is John's .gitignore for Xcode projects:

https://github.com/jeradesign/0common/blob/main/gitignore_xcode_appcode


### Reveal Followup

Rainer followed up with what Reveal shows for a SwiftUI app using the Stanford University card game project. It might not be all that useful for debugging SwiftUI but is interesting because it lets you see some of the private implementation.

### Programmatically controlling `UIScrollView`

You are probably better off not swizzling the implementation but using the gesture recognizer delegate to resolve conflicts.

https://developer.apple.com/documentation/uikit/uigesturerecognizerdelegate


### AttributedString

New in iOS 15 there is an attributed string class that you should know about.

Check out: https://developer.apple.com/documentation/foundation/attributedstring

The markdown interpreter that it supports is here: https://developer.apple.com/documentation/foundation/attributedstring/markdownparsingoptions/interpretedsyntax


Aside. A cool markdown program is MacDown: https://macdown.uranusjr.com  (It is free, open source MIT.)


### Hacking Database Facade

Ray forked Josh's Database Facade project with an alternative (but very reusable?) approach. It has the big downside that it requires the client of the service to think about the lifetime of the watcher object rather than the service worrying about it.  We started converting the service to an actor.  We made it part of the way but it is finished in the forked version of the repo.  The fork can be found here: https://github.com/rayfix/DatabaseFacade

Here is the basic idea WatchValues type:

```swift
import CoreData
import Combine

// Protocol to let you turn core data types into value types.
protocol ValueTypeConvertable {
  associatedtype ValueType
  func valueType() throws -> ValueType
}

// A private fetched results controller delegate that can publish
private final class FetchEngine<ValueType, CoreDataType>: NSObject, NSFetchedResultsControllerDelegate where CoreDataType: ValueTypeConvertable, CoreDataType.ValueType == ValueType
{
  private let controller: NSFetchedResultsController<NSFetchRequestResult>
  weak var target: WatchedCoreDataValues<ValueType, CoreDataType>?
  
  init(fetchRequest: NSFetchRequest<NSFetchRequestResult>, context: NSManagedObjectContext) {
    controller = NSFetchedResultsController<NSFetchRequestResult>(fetchRequest: fetchRequest,
                                                                  managedObjectContext: context,
                                                                  sectionNameKeyPath: nil,
                                                                  cacheName: nil)
    super.init()
  }
  
  func start(target: WatchedCoreDataValues<ValueType, CoreDataType>) {
    self.target = target
    controller.delegate = self
    try? controller.performFetch()
  }

  private func transform(_ objects: [NSFetchRequestResult]) -> [ValueType] {
    return objects
      .compactMap { $0 as? CoreDataType }
      .compactMap { try? $0.valueType() }
  }
  
  fileprivate
  func controllerDidChangeContent(_ controller: NSFetchedResultsController<NSFetchRequestResult>) {
    guard let objects = controller.fetchedObjects else { return }
    target?.results.send(transform(objects))
  }
  
  func initialValues() -> [ValueType] {
    guard let results = try? controller.managedObjectContext.fetch(controller.fetchRequest) else {
      return []
    }
    return transform(results)
  }
}

final class WatchedCoreDataValues<ValueType, CoreDataType>: ObservableObject
  where CoreDataType: ValueTypeConvertable, CoreDataType.ValueType == ValueType
{
  var publisher: AnyPublisher<[ValueType], Never> {
    return results
      .prepend(fetcher.initialValues())
      .eraseToAnyPublisher()
  }
  
  fileprivate let results = PassthroughSubject<[ValueType], Never>()
  
  private let fetcher: FetchEngine<ValueType, CoreDataType>
  init(fetchRequest: NSFetchRequest<NSFetchRequestResult>, context: NSManagedObjectContext) {
    fetcher = FetchEngine(fetchRequest: fetchRequest, context: context)
    fetcher.start(target: self)
  }
}
```

Having to main


---

## 2022.01.29

I forgot to capture the zoom chat log this week.  Whoops.  Topics included:

- Lots of new Versions of Swift coming (5.6, 5.7, ... 6.0)
- Bumping versions, John showed that Xcode has a checkbox to automatically bump version numbers
- Use a service layer with your MVVM
- App code
- Default View Models should be `@MainActor final class ObervableObject`
- Don't use @Published outside of View Models, just use an `AnyPublisher` that you can recieve on the Main thread.
- Snow in Boston

### Reveal

Rainer Standke demo'ed the Reveal app.  Works best with UIKit and requires a framework that presumably does a lot of swizzling to make it work.  It tends to be faster and more robust than the Xcode solution.

### Force Directed Graph

We implemented the link drawing and dragging methods today.

```swift
let links = Path { drawing in
              for link in viewModel.linkSegments() {
                drawing.move(to: link.0)
                drawing.addLine(to: link.1)
              }
            }
        
context.stroke(links, with: .color(white: 0.9),
               lineWidth: viewModel.linkWidthModel)
```

We talked about setting the transforms and being careful not to write to @Published from the canvas draw method. (It causes an assertion during rotation in this sample.)

![Demo of Force Directed Graph](https://raw.githubusercontent.com/rayfix/ForceDirectedGraph/main/FDG.gif)

A link to the repo: https://github.com/rayfix/ForceDirectedGraph

---

## 2022.01.22

### Security Vulerability in Safari?

Bill was wondering about a recent vulnerability in Safari.  John Brewer shared the following link: https://arstechnica.com/information-technology/2022/01/safari-and-ios-bug-reveals-your-browsing-activity-and-id-in-real-time/

### iOS 15 Adoption

The age old question of what versions of iOS to support. If you are making a new app, you should strongly consider supporting only the latest OS. The decision should be guided by the specific audience however.

Some related links:

- https://www.macrumors.com/2022/01/13/ios-15-installation-rates/
- https://mixpanel.com/trends/#report/ios_15

### Becoming an Expert

This question comes up from time to time. Here are some suggestions in no particular order (Google for links):

- Attend these meetings and ask questions
- Pick a topic and learn everything you can about it - then present it!
- Advanced Swift by objc.io
- Functional Swift by objc.io
- The Stanford iOS course, updated every year, now with SwiftUI
- RayWenderlich.com
- 100 days of Swift, Hacking with Swift
- Read the Swift.org forums

### Resistors!

John Brewer showed us his app for reading resistors!

https://ResistorVision.com


### Canvas and TimelineView Demo

Converting the ForceDirectedGraph app to use Canvas and TimelineView.

We implemented the node drawing:

```swift
struct GraphView: View { 
  @ObservedObject var viewModel: GraphViewModel

  var body: some View {
    TimelineView(.animation) { timeline in
      Canvas { context, size in
        viewModel.canvasSize = size
        let _ = viewModel.updateSimulation()
        print(timeline.date)
        context.transform = viewModel.modelToView
        
        for node in viewModel.graph.nodes {
          let ellipse = viewModel.modelRect(node: node)
          context.fill(Path(ellipseIn: ellipse), with: .color(Palette.color(for: node.group)))
        }
      }
    }
  }
}
```

These rely on transforms that are computed in the view model when the canvas dimensions are known:

```swift
  var canvasSize: CGSize = .zero {
    didSet {
      let minDimension = min(canvasSize.width, canvasSize.height)
      
      modelToView = CGAffineTransform.identity
        .translatedBy(x: (canvasSize.width - minDimension) * 0.5,
                      y: (canvasSize.height - minDimension) * 0.5)
        .scaledBy(x: minDimension, y: minDimension)
      viewToModel = modelToView.inverted()
      
    }
  }
```

We need to make sure we are transformed into the correct spaces.


```swift
  func modelRect(node: Node) -> CGRect {
    let inset = -Constant.nodeSize / (modelToView.a * 2)
    return CGRect(origin: node.position, size: .zero)
      .insetBy(dx: inset, dy: inset)
  }
```

We will continue the discussion next week.

---

## [2022.01.15](2022.01.15)

### Converting Combine to async/await

Continuing the example from last week, Josh converted the Magic app over to use async/await instead of a combine publisher.  We could then compare and contrast the strenths and weaknesses of each approach.  async/await has a much more imperative feel.  For example `debounce` is a combine publisher and works just by calling that and remembering to switching to the latest publisher. By contast, with async/await, you have to spell it out `Task.sleep(nanoseconds:)` and a `Task.cancel` at the right place.

---

## [2022.01.08](2022-01-08)

Happy New Year!  It was a first meeting of the year lots of people turned out.

### Proposal Discussion: any

This proposal was accepted yesterday. It is a fairly simple syntax change but perhaps paves the way for more advanced automatic type erasure. 

Here is the [acceptance announcement with modifications](https://forums.swift.org/t/accepted-with-modifications-se-0335-introduce-existential-any/54504).


### Discussion: Performance Predictability

Ray guided a summary discussion on Joe Groff's forum post about expected improvements to the ARC programming model and performance predictability.  The original post is here: [https://forums.swift.org/](https://forums.swift.org/t/a-roadmap-for-improving-swift-performance-predictability-arc-improvements-and-ownership-control/54206)

The walk-through presentation [PerformanceRoadmapPitchSummary](materials/PerformanceRoadmapPitchSummary.pdf).

### Privacy and App Submission

When you are submitting an app, you need to worry about third party dependencies (such as analytics and crash reporters) that phone home.  You need to include those privacy policies in your submission.

You might wish to check your app using a proxy such as Charles or proxyman.
 https://proxyman.io

Manu wrote a book about privacy for app developers
 https://link.springer.com/book/10.1007/978-1-4842-4291-9 


### Modern SwiftUI Magic

Josh revisited an old SwiftUI project (searching cards from the game Magic) from years ago and looked to modernize it.  Some things we did:

- Use `AsyncImage` removing an entire package dependency.
- Use `LazyVGrid` inside a `ScrollView` instead of `List`
- Use `searchable` view modifier (inside a `NavigationView`) instead of doing something custom.

These changes make the user interface look great on different size devices including iPads and Macs.

The original repo is here: https://github.com/joshuajhomann/Magic-Browser-SwiftUI

We looked at how the app uses **Combine** in the view model to map search terms to a publisher of Card types.  Next week Josh will show how this can be updated to the new async/await world.


## Archives

- [2020 Meetings](2020/README.md)
- [2021 Meetings](2021/README.md)
