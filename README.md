# A Flock of Swifts 

We are a group of people excited by the Swift language. We meet each Saturday morning to share and discuss Swift-related topics. 

All people and all skill levels are welcome to join. 

## 2021.08.14

Join us next Saturday:

- **RSVP**: https://www.meetup.com/A-Flock-of-Swifts/

---

## 2021.08.07

This meeting was a smorgasbord of topics by group participants.

Ed had a couple of questions about building his watch app in SwiftUI.

1. How to make a piece of text scale up.  Using a geometry reader is one solution to the problem. Josh H. had a better solution.  Make font size extra large and then scale it down by setting the minimum scale factor to something really small.

```swift
Text("Hello, world!")
   .font(.system(size: 400))
   .lineLimit(1)
   .minimumScaleFactor(0.00001)
```

2. How to implement double tap in SwiftUI.  The best solution we could come up with was to use a ZStack-ed `UIHostingView` with a `UIGestureRecognizer`.

> Don't use touchesBegan and friends from `UIResponder`.  It is the old, ugly way of doing it.

We talked about syncing solutions.  You can't force an iCloud sync.

There are other solutions:

https://developer.apple.com/documentation/watchconnectivity

Probably the best way is to do the iCloud sync separately.

Firebase is a low latency solution but Ed doesn't like it because it is a large dependency with a lot of extra baggage that your app probably doesn't need.

A commercial solution noted was Pusher https://pusher.com but none seems to have had actual experience with it.

Tim showed us an app that he was making (QuickStuff) but needed to change the orientation of the video stream for Mac and iOS.

```swift
// Set the video orientation mode for Mac only
        // NOT needed when Mac Target is added!
        #if os(OSX)
            print("---> macOS")
        #elseif os(watchOS)
            print("---> watchOS")
        #elseif os(tvOS)
            print("---> tvOS")
        #elseif os(iOS)
            #if targetEnvironment(macCatalyst)
                print("---> macOS - Catalyst")
            #else
                print("---> iOS")
            // Without a Mac Target, running on Mac lands here
            //preview.connection?.videoOrientation = .landscapeLeft
            #endif
        #endif
```

Ray talked about a recent evolution pitch that will allow opaque return types to be structural types.  https://forums.swift.org/t/structural-opaque-result-types/50998

---

## 2021.07.31

In this meeting, Josh created a generic property wrapper for transforming values.  He also made the property wrapper conform to Dynamic Property which is useful in SwiftUI to make sure the body property of a view gets recomputed upon mutation. Among other tricks, he showed how to use nonmutating set with a reference type.

See previous meetings (April) for more information about property wrappers.

```
import Combine
import SwiftUI
import PlaygroundSupport
import Foundation

protocol TransformerProtcol {
    associatedtype Value
    var transform: (Value) -> Value { get }
}

struct AnyTransformer<Value>: TransformerProtcol {
    let transform: (Value) -> Value
}

enum CharacterCase { case lower, upper, capitalized }

extension TransformerProtcol {
    static func identity<Value>() -> AnyTransformer<Value> {
        .init { $0 }
    }
    static func clamp<Value: Comparable>(_ range: ClosedRange<Value>) -> AnyTransformer<Value> {
        .init { min(max($0, range.lowerBound), range.upperBound) }
    }
    static func rounded<Value: BinaryFloatingPoint>(_ rule: FloatingPointRoundingRule = .up) -> AnyTransformer<Value> {
        .init { $0.rounded(rule) }
    }
    static func normalized<Value: BinaryFloatingPoint>(magnitude: Value) -> AnyTransformer<Value> {
        .init { $0 / magnitude }
    }
    static func trimmed(_ characterSet: CharacterSet = .whitespacesAndNewlines) -> AnyTransformer<String> {
        .init { $0.trimmingCharacters(in: characterSet) }
    }
    static func cased(_ characterCase: CharacterCase) -> AnyTransformer<String> {
        .init {
            switch characterCase {
            case .lower: return $0.lowercased()
            case .upper: return $0.uppercased()
            case .capitalized: return $0.capitalized
            }
        }
    }
}

@propertyWrapper
struct Transform<Value>: DynamicProperty {
    final class Wrapper: ObservableObject {
        @Published var value: Value
        @Published var untransformedValue: Value
        private let setter: (Value) -> Value
        init(
            untransformedValue: Value,
            setter: @escaping (Value) -> Value
        ) {
            self.untransformedValue = untransformedValue
            self.setter = setter
            value = setter(untransformedValue)
        }
        func set(_ newValue: Value) {
            untransformedValue = newValue
            value = setter(newValue)
        }
    }
    @ObservedObject private var wrapped: Wrapper
    var wrappedValue: Value {
        get { wrapped.value }
        nonmutating set { wrapped.set(newValue) }
    }

    var projectedValue: Wrapper {
        wrapped
    }

    init(
        wrappedValue: Value,
        _ setter: AnyTransformer<Value>
    ) {
        let wrapper = Wrapper(untransformedValue: wrappedValue, setter: setter.transform)
        _wrapped = .init(wrappedValue: wrapper)
    }
}

final class B: ObservableObject {
    @Transform(.clamp(0...1.0)) var a = 1.5
    @Transform(.rounded()) var b = 2.7
    @Transform(.trimmed()) var c = " sdsf "
}
let b = B()
print(b.a)
print(b.b)

extension NSNotification.Name {
    static let persistedDidChange = NSNotification.Name(rawValue: "PersistedDidChange")
}

@propertyWrapper
struct Persisted<Value: Codable>: DynamicProperty {
    final class Wrapper: ObservableObject {
        @Published var value: Value
        private let defaults: UserDefaults
        private let suiteName: String?
        private let key: String
        init(
            value: Value,
            suiteName: String? = nil,
            key: String
        ) {
            defaults = suiteName.flatMap(UserDefaults.init(suiteName:)) ?? .standard
            self.key = key
            self.suiteName = suiteName
            self.value = defaults
                .data(forKey: key)
                .flatMap { try? JSONDecoder().decode(Value.self, from: $0) } ?? value

            NotificationCenter
                .default
                .publisher(for: .persistedDidChange)
                .compactMap { notification in
                    guard (notification.object as? String) == suiteName else { return nil }
                    return notification.userInfo?[key] as? Value
                }
                .assign(to: &$value)
        }
        func setAndSave(_ newValue: Value) {
            guard let data = try? JSONEncoder().encode(newValue) else { return }
            value = newValue
            defaults.set(data, forKey: key)
            NotificationCenter.default.post(.init(name: .persistedDidChange, object: suiteName, userInfo: [key: newValue]))
        }
    }
    @ObservedObject private var wrapped: Wrapper
    var wrappedValue: Value {
        get { wrapped.value }
        nonmutating set { wrapped.setAndSave(newValue) }
    }

    var projectedValue: Published<Value>.Publisher {
        wrapped.$value
    }
}
```

---

## 2021.07.24

### Overheating MacBook Pro

We started off the meeting talking about Ray's computer problems with macOS 11.4 - macOS 11.5, Zoom, Google meetup and overheating.  Update: After getting the pentalop driver to disassemble and clean the dust the 2019 MBP, the problem appears to be resolved!  There was a lot of dust stuck in the fan blades.

### Capturing Video Frames

Tim asked about the state of the art for capturing video. https://medium.com/ios-os-x-development/ios-camera-frames-extraction-d2c0f80ed05a

### Colors with themes

There was a question about how to handle colors with light and dark themes.  Josh talked about how to specify multiple colors per theme in an asset catalog as well as resolved colors: https://developer.apple.com/documentation/uikit/uicolor/3238042-resolvedcolor

### TouchRoute

Ed gave us a demo of GeoCoding and reverse geocoding.

He uses this in his app **TouchRoute**.  Five star reviews welcome!

https://apps.apple.com/us/app/touchroute/id1559820521

### Formatters

New in foundation is the ability to specify formatters.  These formatters are better typed than before.

```swift
let date = Date()
date.formatted(date: .abbreviated, time: .omitted)

let stuff = [1,2,3,4,5].map(String.init)
print(stuff.formatted(.list(type: .and)))
```

https://developer.apple.com/documentation/foundation/formatter

### Usability Feedback 

Tim Colson let us know about a group that offers free advice on user experience.

http://uxua.arizona.edu/dropin

### Extensible Options

Static member lookup in Swift 5.5 gives us the syntactic elegance and code completion of enums while making things extensible.

Imagine a library method:

```swift

protocol ItemSorting {
    func sort(_ items: [Item]) -> [Item]
}

extension Array where Element == Item {
    func sort<Method: ItemSorting>(method: Method) -> [Item] {
    method.sort(self)
    }
}
```

The library can define methods:

```swift
struct NoneItemSorting: ItemSorting {
    func sort(_ items: [Item]) -> [Item] {
        items
    }
}

extension ItemSorting where Self == NoneItemSorting {
    static var none: NoneItemSorting {
        NoneItemSorting()
    }
}
```

But clients outside the library can also define methods.

```swift
struct CrazyItemSorting: ItemSorting {
    func sort(_ items: [Item]) -> [Item] {
        print("Crazy!")
        return items
    }
}

extension ItemSorting where Self == CrazyItemSorting {
    static var crazy: CrazyItemSorting {
        CrazyItemSorting()
    }
}
```

How beautiful it looks at the call site:

```swift
[Item(name: "Hello", date: .now)].sort(method: .none)
```

---

## 2021.07.17

## Questions
  * Ray asked about the composable architecture
  * Dan asked about resources for RxSwift: 
    * Frank suggests https://freak4pc.medium.com/whats-new-in-rxswift-5-f7a5c8ee48e7 
    * Josh suggests https://rxslack.herokuapp.com
  * Emily asked about the touch area for UIButton contained in a UIBArButtonItem
     * Ed Suggested not using a UIButton as UIBarbuttonItem already expands its touch target
     * Josh Suggested using UIAppearance to style the UIBarButtonItem when contained in a UINavigationBar instead of an image: https://developer.apple.com/documentation/uikit/uiappearance and setting the backItem to "Back" int he navigation delegate: https://developer.apple.com/documentation/uikit/uinavigationcontroller/customizing_your_app_s_navigation_bar
     * Ray offered that you can expand the tap area of any view by overriding hitTest: https://developer.apple.com/documentation/uikit/uiview/1622469-hittest
  * Peter asked about composing property wrappers to make a @Published @Clamped property.  This is impossible. Josh suggested instead making @Clamped a Dynamic property. https://github.com/joshuajhomann/CustomDynamicProperties/blob/master/CustomDynamicProperties/Interval.swift

## @ViewBuilder SwiftUI API Conventions

We walked through a [blog post](https://www.fivestars.blog/articles/swiftui-patterns-view-builders/) on the Five Stars blog that talked about how SwiftUI has changed API over the last couple years with regards to ViewBuilders and trailing closures.

- Instead of a single generic view, SwiftUI now prefers @ViewBuilders
- Main content comes first and labels and secondary views second
- Takes advantage of trailing closure syntax
- `@escaping` closures for actions come last, after the view builders

Although not covered in this blog post, the latest beta has enabled these new APIs back to iOS13.

## TimelineView and CanvasView
Josh reviewed the new `TimelineView` and `Canvas` in iOS 15.  We discussed animation scheduling and the graphics context.

```swift
struct ContentView: View {
    @StateObject private var viewModel = ViewModel()
    var body: some View {
        TimelineView(.animation()) { time in
            Canvas { context, size in
                let minimumDimension = size.minimumDimension
                let delta = minimumDimension * 0.1 * sin(time.date.timeIntervalSince1970) + minimumDimension * 0.1
                let rect = CGRect(origin: .zero, size: .init(width: minimumDimension, height: minimumDimension))
                    .offsetBy(
                        dx: (size.width - minimumDimension) / 2,
                        dy: (size.height - minimumDimension) / 2
                    )
                    .insetBy(dx: delta, dy: delta)
                context.fill(
                    Path(ellipseIn: rect),
                    with: .color(.red)
                )
            }
        }
    }
}

extension CGSize {
    var minimumDimension: Double {
        min(width, height)
    }
}
```

The animation schedule is analogous to `CADisplayLink` and executes on every frame available.  This is great for animation.

The `GraphicsContext` has a bunch of features including grabbing resolved images and text so that duplicates can be draw very quickly. See the documentation for details.

---

## 2021.07.10

## R-Style Boolean Sequences in Swift

Ray presented some extensions on Sequences and Collection to make Swift work more like the statistical programming language R.  (PS: After reinstalling Big Sur 11.4, things worked a lot better. The playground that was having problems in the demo suddenly just worked. Hah.)

[Walkthrough](https://rayfix.org/2021/07/10/r-style-boolean-sequences-swift.html)

## Nasa Astronomy Image of the Day
Josh showed a [code along project](https://github.com/joshuajhomann/Nasa-Image-Of-The-Day) designed to show how to use async / await with SwiftUI in iOS 15 beta.

We dicussed:
  * The Nasa  Astronomy Picture of the Day API: https://api.nasa.gov
  * decoding the response with Quicktype: https://quicktype.io
  * cleaning up the type to remove optional elements, use strong typing for `URL`, and make the resulting struct `Identifiable` so it works in a `SwiftUI.List`
  * build a `URL` with `URLComponents`
  * making an async initializer for `Result`
  * making an async network request and decoding the response
  * switching over the images enum to handle loading, error and loaded states
  * Using the new `AsyncImage` API
  * Using the new `.task` modifier to start an async task that is automatically scoped to the lifetime of the view
  * using the new `.refreshable` modifier to implement pull to refresh  
  
![image](https://github.com/joshuajhomann/Nasa-Image-Of-The-Day/blob/master/preview.gif)

---

## 2021.07.3

## Met Museum Gallery
We continued the Met Museum app.
Fixes:
  * Fixed the problem with search results not updating by using the new `OrderedSet` in the `swift-collections` package.  We all discussed package lists and the new IDE changes for packages in XCode 13.
  * Fix the parallel download issue by using `withThrowingTaskGroup` and hoisted this logic into its own generic function:

```swift
extension Sequence {
    func asyncUnorderedMap<Value>(awaiting transform: @escaping (Element) async throws -> Value) async rethrows -> [Value] {
        try await withThrowingTaskGroup(of: [Value].self) { group in
            forEach { element in
                group.async {
                    [try await transform(element)]
                }
            }
            return try await group.reduce(into: [Value]()) { total, next in
                total.append(contentsOf: next)
            }
        }
    }
}

```
  * discussed the `.listStyle` and `.listRowSeparator` modifiers
  * created a `DetailView` and discussed when to use an `ObservableObject` vs when to use a `struct` for a viewModel
  * discussed `AttributedString` from markdown, new iOS 15 `Date` formatter and List Formatter
  * discussed new `.safeAreaInset` modifier
  * discussed new `.foregroundStyle` label styles
  * discussed new `Material` styles
Project: https://github.com/joshuajhomann/Met  

![Met](https://github.com/joshuajhomann/Met/raw/master/preview.gif)
---

## 2021.06.26

## Command line dice roll app
Peter showed his command line dice rolling app and we discussed some problems he was having compiling the app from the command line when including a swift package:  https://github.com/PPeter326/Roll

## Met Museum Gallery
Josh demoed an app using the Met API https://metmuseum.github.io .  We discussed:
  * Code generating the response with quicktype.io and manually cleaning up the generated code
  * A generic networking layer using the new `try await URLSession.shared.data(for:)` API
  * Using an `actor` for the service layer of the app
  * The new `AsyncImage` View in iOS 15
  * The new `.searchable`, `.searchCompletion` and `.onSubmit` modifiers in iOS 15
  * The new `@MainActor` annotation
  * Reviewed the `@AppStorage` property wrapper from iOS 14
  * discussed chaining `await` calls and a problem with using `withThrowingTaskGroup(of:` inside a `async`
The partial project is here: https://github.com/joshuajhomann/Met  We will finish it next week.

## Bridging await to Combine
We dicussed the differences push (Combine) vs pull (async/await), strong error typing (combine) vs weak error typing (async/await), cold publishers (the Combine structs) vs hot publishers (the Combine references and async/await), and how to bridge async functions to Combine by leveraging Future, a hot publisher.

```swift
extension Future where Failure == Error {
    convenience init(awaiting asyncTask: @escaping () async throws -> Output) {
        self.init { promise in
            async {
                do {
                    promise(.success(try await asyncTask()))
                } catch {
                    promise(.failure(error))
                }
            }
        }
    }
}
```
---

## 2021.06.19

### Izzi Pics App Feedback

Emil Safier asked our opinion on his screenshots for marketing 
his Izzi Pics app. 

https://apps.apple.com/us/app/izzipics/id1476207437?mt=8

He also has a TestFlight version available.

### Slow Watch Reminders Updates

Mark not getting good performance. Perhaps his iCloud data store needs to be reset?  It is a scary operation so caution is advised.

John James needs to get a new watch or replace his battery.  Discussion about "right to repair".

### Existential and Universal Types in Swift

A presentation from Josh about the difference between existential protocol types, generics, type erased Any*, and some types.

Universals:
  * Generic functions
  * `Any`
  * `AnyObject`, `AnyClass`
  * Concrete generic type erasers: `Any*` `AnySequence`, `AnyView`, `AnyPublisher`
Existentials:
  * existentials (SE-309): `let a: CustomStringConvertible = 1`.  Dynamically implemented by witness table.
  * `some`: `let a: some CustomStringConvertible = 1`.  Statically known at compile time.
A question from Josh A in the chat we didn't notice. (We'll discuss the answer next week):

> Hope this isn't a silly question, but why do we need "some", couldn't we do something like T<View>, like just a normal generic? Is it because we want the compiler to know the type? Or is it because there are so many different ways to satisfy the "View protocol" having a normal generic wouldn't work?

The "some type" is called a "reverse generic" because the implementation body determines the implementation.  With normal generics the caller determines the concrete type which would not work for "some View". 

### Apple Logo

Looking at the details of this code from Jordan Singer.
https://twitter.com/jsngr/status/1405232521256841219

### Fighting Xcode, Zoom, macOS

Ray had significant problems sharing his screen today. Somehow hopes to fix this for next week.

---

## 2021.06.12

### WWDC Discussion

You are probably best off using the developer app to watch the videos.  Get started here:

https://developer.apple.com/wwdc21/

Josh talked about some of the major themes and surprises from this year.

- Continued improvement to bring parity to all platforms but not do something like run Mac apps on iPad.
- Markdown support for Text
- No developments on Combine. Pushes the FRP story out by another year.

Other discussion:

- Frank's pick was Demystifying SwiftUI
- Column breakpoints!
- ARC observed lifetime vs guaranteed lifetime

We will be talking a lot more about these things in the coming weeks.

---
## 2021.06.05

* Ray will be live on the Raywenderlich podcast after WWDC.  Signup here: https://us02web.zoom.us/webinar/register/WN_Rljgpr44Twag3K9BbM3kuw

* Emily asked about showing a different viewcontroller at startup depending on Userdefaults.  We discussed using childViewControllers and setting the rootViewController programatically from the Appdelegate or the SceneDelegate
```swift
    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        let contentView = ContentView()
        if let windowScene = scene as? UIWindowScene {
            let window = UIWindow(windowScene: windowScene)
            window.rootViewController = figureOutWhichVCGoesHere()
            self.window = window
            window.makeKeyAndVisible()
        }
    }
```

* Dan's app is available on the app store.  Check it out here: https://apps.apple.com/mu/app/mygames-database/id1559848159

* Ed demoed his brother hackathon entry for buying/renting AR rendered NFT's.

* Josh demoed the problem with classes and shared mutable state that `actors` are designed to solve.  For example this code is not thread safe:
```swift
final class Poop {
    private var count: Int = 0
    private let serialQueue = DispatchQueue(label: String(reflecting: Poop.self))
    func poo() {
        count += 1
        print(count == 1 ?  "💩 is good" : "\(count) bad 💩 happened!!!!")
        count -= 1
    }
}

let poop = Poop()
for _ in 0..<10 {
    DispatchQueue.global(qos: .background).async {
        poop.poo()
    }
}
```
It can be made thread safe by adding locks or a serial `DispatchQueue`, but this results in a programmer guarantee and not a compiler guarantee:
```swift
final class Poop {
    private var count: Int = 0
    private let serialQueue = DispatchQueue(label: String(reflecting: Poop.self))
    func poo() {
        serialQueue.async { [weak self] in
            guard let self = self else { return }
            self.count += 1
            print(self.count == 1 ?  "💩 is good" : "\(self.count) bad 💩 happened!!!!")
            self.count -= 1
        }
    }
}

let poop = Poop()
for _ in 0..<10 {
    DispatchQueue.global(qos: .background).async {
        poop.poo()
    }
}
```

* We discussed the types in Swift and when to use them:
  * enum
    * Is your type heterogeneous?
    * Does your type represent discretely many states?
    * enum is a value unless you use the indirect keyword
  * struct
    * structs have value semantics
    * Copy on write for types that are implemented as references
    * Sendable thread safe by default
  * tuple
    * tuple have value semantics
    * anonymous
    * Sendable thread safe by default
  * class
    * class has reference semantics
    * Implies shared ownership
    * Allows inheritance (don’t use it for non obj C code)
    * Not thread safe unless its immutable or you guarantee safety
    * Have lifetime with init and deinit
  * actor
    * actor has reference semantics
    * Implies shared ownership
    * No inheritance
    * Thread safe and Sendable but you pay a performance cost
  * func
    * func is a reference type
    * Not thread safe; you make the guarantee with @Sendable
  * Protocol
    * protocol is abstract type
    * Prefer to using inheritance

Josh's shorthand rule for `class` vs `actor`: Use an `actor` for all of the service level objects in your app (networking, caching, location etc.) but continue to use classes for types that are owned by UI thread objects (ie viewModels) and wherever you need to inherit from Objective C or can guarantee single threaded access or immutability.

---

## 2021.05.29

We talked about getting the most out of the WWDC.
  - Download the developer app
  - Make sure to watch the Platforms state of the Union
  - Watch what's new in Swift

We spent most of the meeting working through this article by Paul Hudson:

https://www.hackingwithswift.com/articles/233/whats-new-in-swift-5-5

The newsletter https://iosdevweekly.com mentioned some videos that might also be useful to watch:

https://alejandromp.com/blog/swift-concurrency/

Apple needs to get caught up on graphics technology.

https://www.ign.com/articles/unreal-engine-5-dog-render-10-billion-polygons

---
## 2021.05.22

### Announcements

- The new book [Expert Swift](https://www.raywenderlich.com/books/expert-swift/v1.0/) is out. You can read the first four chapters for free and Ray Fix wrote two of those. Any feedback you have toward the next edition would be useful!

- Paul Hegarty's famous [CS193p iOS Stanford class](https://cs193p.sites.stanford.edu) for 2021 is out. He does an amazing job of teaching SwiftUI from the ground up. Worth watching.

### Router Pattern

Tim Colson helped us explore a navigational pattern related someone to coordinators. 

https://davidgarywood.com/writing/swiftui-router-pattern/

- Protip: To reset user defaults quickly you can just delete the app in the simulator.

### Building C++

Ed was working through some tricky build issues. One issue which we were able to solve was related to ensuring that there one definition of a symbol in C++ so the linker doesn't get duplicates.  You must declare things "extern" in shared headers.  Also, special care needs to be taken for C:

```cpp
#ifdef __cplusplus
extern "C" {
#endif

// C code here

#ifdef __cplusplus
}
#endif
```

### Coredata, Dependency Injection, Inversion of Dependencies
Josh reworked Apple's sample CoreData project to facade CoreData behind a value and function only interface, sequesting the CoreData specific logic, types and delegates behind a protocol and decoupling the rest of the app from the dependency on Coredata.  See last weeks discussiong for dependency inversionf or more details.

https://github.com/joshuajhomann/DatabaseFacade  

![DatabaseFacade](https://github.com/joshuajhomann/DatabaseFacade/blob/master/preview.gif)
---
## 2021.05.15

### Fluent SQLite

In previous weeks we have talked about using a variety of data backends for iOS models.  I demonstrated how you can use the Fluent ORM from the Vapor project to back your SwiftUI app. Here is the writeup: https://rayfix.org/2021/05/18/fluent-swiftui.html

### Inversion of Dependecies
We discussed the `D` in `SOLID`: dependency inversion and how it can we be used to facade your database implementation so that you can swap out the implementation of your caching or storage layer without affecting the rest of your app (ie swap Coredata for Fluent).
https://ducmanhphan.github.io/2020-01-15-Understanding-about-SOLID-part-5/

### Transforming a while loop into an asynchronous Publisher

Josh showed how we can take a while loop for a series of asynchronous tasks and reimagine it as a generic recursive asynchrounous function.  This is useful for tasks such as making repeated sequential network requests until the response satisfies some predicate.

```swift
import PlaygroundSupport
import Combine

extension Publishers {
  static func publishLatest<Output, Failure>(
    while predicate: @escaping (Output) -> Bool,
    make publisherFactory: @escaping (Output?) -> AnyPublisher<Output, Failure>
  ) -> AnyPublisher<Output, Failure> {
    func makeNextPublisher(from output:Output?) -> AnyPublisher<Output, Failure> {
      publisherFactory(output).map { result -> AnyPublisher<Output, Failure> in
        predicate(result)
          ? Publishers.Concatenate(
              prefix: Just(result).setFailureType(to: Failure.self),
              suffix: makeNextPublisher(from: result)
            ).eraseToAnyPublisher()
          : Empty(
              completeImmediately: true,
              outputType: Output.self,
              failureType: Failure.self
            ).eraseToAnyPublisher()
      }
      .switchToLatest()
      .eraseToAnyPublisher()
    }
    return makeNextPublisher(from: nil)
  }
}


let c = Publishers.publishLatest(
  while: { $0 < 3 },
  make: { previous in Just(previous.map { $0 + 1 } ?? 0).eraseToAnyPublisher() }
)
.sink(receiveValue: {
  print($0)
})
```

---
## 2021.05.8

### Swift 5.5

We discussed the current status of the Swift 5.5 with many of the proposals approved ahead of WWDC: https://apple.github.io/swift-evolution/

### Swift Package index

Ray showed the Swift package index and the apbility to download and test a package in a playground: https://swiftpackageindex.com. 
He also showed the collections package and the Dequeue: https://github.com/apple/swift-collections

### Rendering cell gradients
Josh A showed his project to create a messaging UI framework.  We discussed possible ways to render a gradient overlay for the entire scrollview in UIKit and in Swift UI.  Josh H suggested using a blend mode on a gradient to tint the cells like this: https://github.com/joshuajhomann/Shimmer/blob/master/Sources/Shimmer/Shimmer.swift

### MVC, Diffable DataSources and MVVM in UIKit and SwiftUI
Josh H continued his demo on modern app architecture in UIKit and SwiftUI.  We recapped what a basica imperative MVC TableView VC looks like in UIKit, what the analogous declarative version looks like by using DiffableDataSources, Combine and UIAction.  We noted that we were able to delete all of the instance variables in the declartive version because all the mutable state is now private to the init function.  

We then created a futher refinement by lifting out the busness logic to a SwiftUI inspired viewModel, and saw that we can use the same viewModel to drive both the UIKit and SwiftUI versions of this screen, giving us a single reactive declarative and immutable architecture for both UIKit and SwiftUI that is especially useful for hybrid apps that need to use both UI layers:
https://github.com/joshuajhomann/DiffableDataSources

---
## 2021.05.1

### Storekit

Emil asked about the requirements for decrypting and inspecting the receipt payload for Storekit in app purchases.  We discussed that the official Apple solution is to have your server validate the receipts against the Apple servers to avoid a possible man in the middle attack, although you can do this on device if you don't have a server and are willing to ignore Apple's security concerns.

### Parsing command line arguments

We looked at the Swift argument parser library. This was developed, among other reasons, to provide argument parsing for the Swift compiler. While most of Swift is written in C++, parts are being re-written now in Swift.

We created a simple SwiftUI app and passed arguments to it. You can find the example, and more information on this blog post:

https://rayfix.org/2021/04/24/swiftui-argument-parser.html

### Coordinators

Curits asked about how to perform deeplinking from a local notification in his app.  We discussed the MVC architecture and noted that it lacks a separate component for routing.  This problem also exists for MVVM applications in SwiftUI where the view tree is a function of the viewmodel state.  We discussed the possibility of solving this with a separate Router/Coordinator component that can be imperative for UIKit code and reactive for SwiftUI, allowing for a single unified routing architecture in a mixed app.  We looked at how you can handle deeplinks imperatively by handling 3 functions in the app delegate (didLaunch, open url, and didRecieveRemoteNotification) and funneling the results to one function that can inspect the application's keywindow rootViewController to decide how to route the link.  We dicussed the possible pitfalls of changing the navigation stack when the user is not logged in, when the user is in the middle of some content creation (typing a message for instance), or when the user does not have permission or is not authenticated.  We will explore this concept in the future as part of a broader discussion on modern ios app architecture.

---

## 2021.04.24

### Product and Rumor Talk

We talked about the new product Apple made. Ray and John pre-ordered AirTags. Ray is excited to buy an M1 iPad when it becomes available.

We discussed the quanta leaks:   
https://appleinsider.com/articles/21/04/21/stolen-quanta-documents-show-macbook-pro-with-sd-card-slot-magsafe

### UITextField vs UITextView

Josh notes UITextField is generally easier to work with because it has the target action behavior of `UIControl`.

https://developer.apple.com/documentation/uikit/uitextview
https://developer.apple.com/documentation/uikit/uicontrol

### Demonstration of Yi's apps

He showed a cool desktop picture app that uses the Unsplash API.

https://ylin.co

He showed his finance app which compared with big competitors is (1) easy to use (2) protects your privacy (3) is not a subscription model. Asked for market. 

https://savingsapp.com

Sync solution used http://www.ensembles.io

#### Feedback

We discussed market positioning and marketing and possibly using a press release as a better value proposition than advertising: http://www.prweb.com. 

- Emphasize the angle of user privacy.
- Look at https://www.mrmoneymustache.com/mmm-recommends/
- Localization https://github.com/mac-cain13/R.swift 

### Josh's picks

#### Benchmarking Swift
https://benchmarksgame-team.pages.debian.net/benchmarksgame/which-programs-are-fastest.html

#### One language to rule them all?
https://www.youtube.com/watch?v=P2yr-3F6PQo

Josh suggested watching this Uncle Bob video where Bob proposes that new programming paradigms are about subtraction and not adding features and that we may have discovered all of the programming paradigms because there is nothing else left to subtract.  The most interesting discussion is at the 13:20 mark. 

#### Lots of changes coming in Swift 5.5
https://apple.github.io/swift-evolution/

---
## 2021.04.17

### New Swift Evolution Proposals, Repos and Tools

We talked about some of the new evolution proposals and repositories available.

#### Evolution Proposals
- https://github.com/apple/swift-evolution/blob/main/proposals/0308-postfix-if-config-expressions.md
- https://github.com/apple/swift-evolution/blob/main/proposals/0309-unlock-existential-types-for-all-protocols.md
- https://github.com/apple/swift-evolution/blob/main/proposals/0310-effectful-readonly-properties.md
- https://github.com/apple/swift-evolution/blob/main/proposals/0311-task-locals.md

#### Swift Repositories

- https://github.com/apple/swift-collections

Other repos to think about using:

- https://github.com/apple/swift-numerics
- https://github.com/apple/swift-algorithms


### User Experience Resources

Read the Human Interface Guidelines (HIG).  There are also websites that explore different user interfaces 

- https://developer.apple.com/design/human-interface-guidelines/
- https://dribbble.com/shots/popular/mobile
- https://mobbin.design

### Corner Rounding

Mira had a question about label corner rounding. The discovery was that if corner rounding is added to the init of a custom collection view cell it works but if added to layoutSubviews, it does not. It is somewhat a mystery as to why this is the case

### Core Data vs ...

Curtis was wonding about https://github.com/groue/GRDB.swift as a wrapper for data.  A simpler approach may be to just store everything in a file that is saved to the documents directory.

If you are learning about CoreData you might want to check this out:

- https://www.youtube.com/watch?v=yOhyOpXvaec

Also you might want to read this:

https://davedelong.com/blog/2018/05/09/the-laws-of-core-data/

Josh A. reminded us that parse which is alive and well (and uses Mongo under the hood) 

https://docs.parseplatform.org/

### Previews for UIKit

Josh created a package that lets you preview UIKit views and view controllers using the SwiftUI preview mechanism.

https://github.com/joshuajhomann/Preview


### Table View Data Sources

Ask three questions?

1. How does it work?  (coding concern)
2. Why does it work that way? (software engineering concern)
3. Should it work that way? (deeper software engineering concern)

Josh gave a presentation about table view data sources.  His first example used standard MVC to show pokeman characters loaded in from a JSON document.  It had a searchbar to narrow down search terms.  It worked but performed expensive filter work on the main thread, had to have mutable shared state properties, and didn't animate changes.

Next, he used the diffable data source to solve the same problem.  This is a more declarative form put everything in the initializer (except for the observing publisher subscription).  It applies snapshots as the data source to achieve animation when search is activated.  The structures look more like SwiftUI.

Next week he will take this example further and show an MVVM implementation that looks a lot more like SwiftUI.
https://github.com/joshuajhomann/DiffableDataSources
---
## 2021.04.10

### Touch Route

Ed has a new app in the App Store called Touch Route. Several participated in the TestFlight. Time to get it and give him a five star review! :)

https://apps.apple.com/us/app/touchroute/id1559820521

### Swift Packages with Binary Frameworks

Ed also gave us a quick tour about how to use frameworks from SwiftPM. Important: you need to convert a .framework to an .xcframework to be usable.  The package definition DSL is just Swift code.

We also talked about various Brother printers
https://www.brother-usa.com/support/ql820nwb - Brother QL-820NWB

### Review of Property Wrappers

We worked through this example:

```swift
@propertyWrapper
struct Clamped<Value: Comparable> {
    var range: ClosedRange<Value>
    private var value: Value
    var wrappedValue: Value {
        get { value.clamped(to: range) }
        set { value = newValue }
    }
    var projectedValue: Value {
        get { value }
        set { value = newValue }
    }
    init(wrappedValue: Value, range: ClosedRange<Value>) {
        value = wrappedValue
        self.range = range
    }
}

extension Comparable {
    func clamped(to range: ClosedRange<Self>) -> Self {
        min(max(range.lowerBound, self), range.upperBound)
    }
}
```

Josh Homann has covered this in previous meetups.
https://github.com/joshuajhomann/CustomDynamicProperties

Also, Josh recommends using Snippets in Xcode as a way to expose the entire surface area of a function in one shot.

```swift
@propertyWrapper
struct <#Name#> {
  private var value: <#Wrapped#>
  var wrappedValue: <#Wrapped#> {
    get { value }
    set { value = newValue }
  }
  var projectedValue: <#Projected#> {
    get { value }
    set { value = newValue }
  }
  init(wrappedValue: <#Wrapped#>) {
    value = wrappedValue
  }
}
```

A new Swift evolution proposal 0293 has been accepted and will be in Swift 5.5.  Expect to see a lot more `@` symbols at next WWDC.

https://github.com/apple/swift-evolution/blob/main/proposals/0293-extend-property-wrappers-to-function-and-closure-parameters.md

---
## 2021.04.03

## Review of Mutable Value Semantics

Ray did a review of what mutable value semantics are in Swift using the iPad note app to draw with. Languages like Java and Python use reference semantics for performance. Languages like Haskell have value semantics but achieve it through immutability. Swift gets the best of both worlds by using reference semantics privately but then doing  copy-on-write to achieve value semantics.

Tim wrote some playground code to work through the ideas:

```swift
// Value Semantics
let a = [1,2,3]
// b just "points" to same memory as "a"
let b = a
// c just points to a
var c = a
print(a,b,c) // [1,2,3][1,2,3][1,2,3]
    // Standard Swift Types support "Mutable Value Semantics" - i.e. Copy on Write (aka "COW paradigm")
    // Uh Oh - this is a var that changes... so COW!
c.append(4)
print(a,b,c) // [1,2,3][1,2,3][1,2,3,4]

// Example with Classes (Person) 
class Person {
    var name : String
    init(name: String) {
        self.name = name
    }
}
var p1 = Person(name:"Josh1")
let p2 = Person(name:"Josh2")
let p3 = Person(name:"Josh3")
print("p1 unique=\(isKnownUniquelyReferenced(&p1))")
var people : [Person] = [p1, p2, p3]
print(people)
//  print("people unique=\(isKnownUniquelyReferenced(&people))")
print("p1 unique=\(isKnownUniquelyReferenced(&p1))")
//  let tallPeople = people
//  let smartPeople = people
```

We looked at the problem with SwiftUI and CoW types. The property wrappers `@State` and `@Published` make a local copy which prevents the copy optimization.  Instead, you can use `objectWillChange` on `ObservableObject` directly.

https://gist.github.com/rayfix/dc079e527be76f9be4a419ca2896d5ba

### Swift on Tap

Tim showed us Apple-like documentation but with examples.
https://swiftontap.com/

Frank: Swift on Tap is the work of [Alex Fine](https://github.com/alexfine).

Some SwiftUI resources worth a look:
  - https://www.avanderlee.com (Antoine van Der Lee)
  - https://kean.blog

### Importing a binary framework and vending it from SwiftPM

Ed talked about a problem he is still trying to solve. We think he will need to import the library through a bridging header of a modulemap file.

### Rumors and Discussion
https://www.macrumors.com/2020/12/22/2021-apple-tv-rumors/

### Video app pitch

Yi pitched his video app that he is just beginning with.


---
## 2021.03.27

John showed the beginning of his app: https://github.com/codger/Guess-Who which he would like to make into an interactive coding exercise.  If you'd like to contribute, propose a feature and you can present it during the meetup and crowd source the solution.

Ray demoed an issue with a CowWrapper type where it was causing unexpected allocations.  The solution will be presented in the next meeting!

Josh showed a solution to making a `UIStackView` in `UIScrollView` scroll only when the content exceeds the scrollView's height, and making the stackview equal the scrollview's height in all other cases.  This involves 10 constraints:
  * 4 position constraints on the scrollView's `frameLayoutGuide` to its parent view to position the scrollview.
  * 4 position constraints on the stackview to the scrollView's `contentLayoutGuide` to position the stackView inside the scrollview
  * 2 dimension constraints to imply the size of the stackView
    * A cross axis (horizontal for a vertical scroll) constraint that constrains the stackView's width to the scrollView's width, causing the scrollView to not scroll horizontally
    * An axis constraint (height for a vertical scrollView) that provides a minimum dimension for the stackView's axis that is equal to or greater than the scrollView's scrolling axis.  This constraint *must* not be required (the priority must be less than `.required` which has a rawValue of 1000). 

Finally, at least one view in the stack needs to be expandable.  In this example it is the spacer view.  Expandability is accomplished by setting the contentHuggingPiority of the expandable view(s) to a value lower than all of the other views in the stack for the scrolling axis (vertical).

```swift
class ViewController: UIViewController {

  override func viewDidLoad() {
    super.viewDidLoad()
    let title = UILabel()
    title.text = "Title"
    let subtitle = UILabel()
    subtitle.numberOfLines = 0
    subtitle.text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    let imageView = UIImageView(image: UIImage(systemName: "star.fill") ?? UIImage())
    imageView.contentMode = .scaleAspectFill
    imageView.heightAnchor.constraint(equalToConstant: 300).isActive = true
    let button = UIButton()
    button.backgroundColor = .black
    button.setTitle("Test", for: .normal)
    button.heightAnchor.constraint(equalToConstant: 50).isActive = true
    button.widthAnchor.constraint(equalToConstant: 100).isActive = true
    button.layer.cornerRadius = 8
    let spacer = UIView()
    spacer.translatesAutoresizingMaskIntoConstraints = false
    spacer.heightAnchor.constraint(greaterThanOrEqualToConstant: 50).isActive = true
    spacer.setContentHuggingPriority(.init(rawValue: 0), for: .vertical)
    let stack = UIStackView.init(arrangedSubviews: [
      title,
      imageView,
      subtitle,
      spacer,
      button
    ])
    stack.translatesAutoresizingMaskIntoConstraints = false
    stack.axis = .vertical
    stack.alignment = .center
    let scrollView = UIScrollView()
    scrollView.translatesAutoresizingMaskIntoConstraints = false
    scrollView.addSubview(stack)
    view.addSubview(scrollView)
    NSLayoutConstraint.activate([
      scrollView.frameLayoutGuide.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
      scrollView.frameLayoutGuide.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor),
      scrollView.frameLayoutGuide.leadingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.leadingAnchor),
      scrollView.frameLayoutGuide.trailingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.trailingAnchor),
      scrollView.contentLayoutGuide.topAnchor.constraint(equalTo: stack.topAnchor),
      scrollView.contentLayoutGuide.bottomAnchor.constraint(equalTo: stack.bottomAnchor),
      scrollView.contentLayoutGuide.leadingAnchor.constraint(equalTo: stack.leadingAnchor),
      scrollView.contentLayoutGuide.trailingAnchor.constraint(equalTo: stack.trailingAnchor),
      scrollView.widthAnchor.constraint(equalTo: stack.widthAnchor),
    ])
    let height = scrollView.heightAnchor.constraint(greaterThanOrEqualTo: stack.heightAnchor)
    height.priority = .defaultLow
    height.isActive = true
  }
}
```
---
## 2021.03.20

### Breakout sessions

Had fun with breakout sessions.  I can see how we can use these in the future.

### Setting Autolayout Constraints and whitespace

Constraints need to set the xy position and width and height of a view.  Sometimes the size has an implicit content size and you don't need to set the width and height.  You want to avoid under constraining or specifying conflicting contraints.

#### How to make whitespace at the bottom?

1. Make a constraint >= 1
2. Set vertical hugging priority to the lowest possible value (1)

### String Performance Cliff

If you load in a string with:

```swift
let value = try String(contentsOf: url)
```

You might load a string that is UTF16 or non-contiguous.  That causes a 10x slowdown.  This might be noticeable if you have a string processing app or a lot of concurrent users on a server app.

There are two functions you might want to be aware of:

```swift
    value.isContiguousUTF8  // can this string use the fast path algorithms?
    value.makeContiguousUTF8() // makes it O(1) to access the storage
```

Also, there are two overloads: `String(contentsOf: url)` and `String(contentsOf: url, encoding: .utf8)`  The first does autodetection the second assumes the encoding.  Prefer specifying it when you can as it may guarantee contiguous storage in the future. 

See https://forums.swift.org/t/confused-by-string-iteration-performance/46723/9

### Codable and code synthesis

A lot of forum discussions happening right now with relation to Codable because of the associated type proposal.

We talked about this one: https://forums.swift.org/t/why-does-subclassing-a-codable-class-produce-class-has-no-initializers/23586


### Swizzling and associated storage to track view controller leaks

Josh walked through the different types of dispatch available to Swift: static dispatch, virtual table (closely related to witness table) dispatch, and full Objective-C message dispatch.  The last is the most flexible to a frightening extent.  It allows you to swizzle (replace) system methods like `viewDidLoad` of `UIViewController` types.  Using assocated storage you can track stuff about the object including an object with a custom `deinit`.  

Code:
```Swift
extension UIViewController {

  final class OnDealloc {
    var closure: () -> Void
    init(_ closure: @escaping () -> Void) {
      self.closure = closure
    }
    deinit {
      closure()
    }
  }
  private static var associatedObjectAddress = String(reflecting: OnDealloc.self)

  @objc private func swizzledViewDidLoad() {
    let onDealloc = OnDealloc {
      print("Dealloc \(Self.self)")
    }
    objc_setAssociatedObject(self, &Self.associatedObjectAddress, onDealloc, .OBJC_ASSOCIATION_RETAIN_NONATOMIC)
    print("ViewDidLoad \(Self.self)")
    swizzledViewDidLoad()  //ViewDidLoad
  }
  private static let swizzleImplementation: Void = {
    let originalSelector = #selector(UIViewController.viewDidLoad)
    let swizzledSelector = #selector(UIViewController.swizzledViewDidLoad)

    guard let originalMethod = class_getInstanceMethod(UIViewController.self, originalSelector),
          let swizzledMethod = class_getInstanceMethod(UIViewController.self, swizzledSelector) else {
      return
    }

    method_exchangeImplementations(originalMethod, swizzledMethod)
  }()

  static func swizzle() {
    _ = swizzleImplementation
  }

}
```


---

## 2021.03.13

### What's new in Swift evolution?

#### CGFloat <-> Double

https://github.com/apple/swift-evolution/blob/main/proposals/0307-allow-interchangeable-use-of-double-cgfloat-types.md

Great if this sharp edge were fixed.  A good April 1st version of this would be to introduce `CGDouble` 🤣 

#### Actors

https://github.com/apple/swift-evolution/blob/main/proposals/0306-actors.md

Some chatter about the pattern in general: https://en.wikipedia.org/wiki/Actor_model

It is available in many languages.  (I first encountered it a decade ago in C++ Boost asio.)

## Alignment Guides

There are many ways of performing the alignment in Swift.  We looked at several ways using alignment guides.  Here was a basic example we explored.

```swift
extension HorizontalAlignment {
    enum Custom: AlignmentID {
        static func defaultValue(in context: ViewDimensions) -> CGFloat {
            context[.leading]
        }
    }
    static var custom: HorizontalAlignment = HorizontalAlignment(Custom.self)
}

 struct ContentView: View {
        var body: some View {
            VStack(alignment: .custom) {
                HStack {
                    Text("Name")
                    TextField("John J.", text: .constant(""))
                        .alignmentGuide(.custom) { context in
                            context[HorizontalAlignment.center]
                        }
                }
                HStack {
                    Text("Address")
                    TextField("1234 Main Drive", text: .constant(""))
                        .alignmentGuide(.custom) { context in
                            context[.leading]
                        }
                }
            }.padding()
        }
 }
```


## Adding Measurement Units

The `Measurement` facility in Foundation lets you add different units of the same dimension in a type safe way.  Be careful with temperature, though.  If you add `C` and `F` together it will convert to the base unit (`K`) and add those  which might not be expected.  Stay in the same units to keep the implicit conversion from happening.

```swift
import Foundation
let a = Measurement(value: 70, unit: UnitTemperature.fahrenheit)
let b = Measurement(value: 20, unit: UnitTemperature.celsius)
a + b // really hot!

a.converted(to: .kelvin) + b.converted(to: .kelvin)  // same as a + b

a + b.converted(to: .fahrenheit)  // probably what you meant, not as hot
```

## Better NSAttributedString API with Result Builder

Josh created a cool custom result builder for creating composable NSAttributedString without all of the type loss of its Objective-C / NSDictionary based API.

Package and example project:

https://github.com/joshuajhomann/AttributedStringBuilder
![image](https://github.com/joshuajhomann/AttributedStringBuilder/blob/master/preview.png?raw=true "Preview")

---
## 2021.03.06

### Demo Time

Caleb and Emily showed a new version of their app. They had some questions about handling multipart posts and general app architecture.

Josh gave us a brief survey of various app architectures.

Is SwiftUI ready for production? The answer depends on the user base you need to support.  (They are currently requiring iOS 13 because they are using Combine.)

Some links from Tim Colson
- https://kean.blog/post/appkit-is-done
- https://kean.blog/post/swiftui-layout-system

The story about how Uber almost had a disaster when they switched to Swift:
https://twitter.com/StanTwinB/status/1336890449861066753?s=20

### Push Notifications

What is the state of the art for push notifications?

https://developer.apple.com/notifications/

Many services out there. You probably don't want to roll your own unless you have to.

### Network Sniffing

- Postman
- Paw https://paw.cloud
- Charles Proxy
- Wireshark
- RESTed
- Insomnia https://insomnia.rest

Aside: Serial 2 is a great tool for sniffing USB/serial devices on macOS

https://www.decisivetactics.com/products/serial/

### LaTeX and MathML

A cool project would be to write a LaTeX parser that rendered using MathML and WKWebView. 

### Units and Codable

```swift
import Foundation
let mile = Measurement(value: 1, unit: UnitLength.miles)
let encoder = JSONEncoder()
let data = try encoder.encode(mile)
print(String(data: data, encoding: .utf8)!)
let decoded = try JSONDecoder().decode(Measurement<UnitLength>.self, 
                                       from: data)
print(decoded)
decoded.converted(to: .fathoms)
```

The archive looks like this:

```none
{"value":1,"unit":{"converter":{"constant":0,"coefficient":1609.3440000000001},"symbol":"mi"}}
```


### Capture Lists

Capture lists are a way of extending lifetime.  The capture occurs at the point of declaration so be careful about capturing values.  They can also be used to break reference cycles, but they tend to be rare.  Try to capture the minimum set of things that you need to.  If you are doing MVC, you probably don't need to inject in and capture your services.  Instead, you can use a singleton.  If you are doing MVVM or others you probably need to use the capture list.


### Getting Started

We all agree that https://cs193p.sites.stanford.edu is a great course.  The prerequisites are OOP, data structures and algorithms but you might be able to fake it even without some of those things.

### Swimbols

John demo'ed a cool tool for using symbols that outputs code.

https://apps.apple.com/us/app/swimbols/id1525226399

### Slack

LA Swift Coders has a Slack channel.

https://join.slack.com/t/swiftcodersla/shared_invite/zt-745saxp2-irO2nTquTwFDHriTmU5JBg



---

## 2021.02.27

### Discussion

Josh had a link for Ray as a follow up on his mandlebrot plot: https://www.youtube.com/watch?v=ovJcsL7vyrk&vl=en

John showed a math project manually laying out equations in SwiftUI. Asked if there is another way to do it.  Frank suggested MathML https://en.wikipedia.org/wiki/MathML which is supported by WKWebView. Others mentioned LaTeX.  

Clarissa had a question on her flipping animation. Josh suggested interactively flipping each card as a function of how far a touch has traveled by using the UIView.transform property: https://developer.apple.com/documentation/uikit/uiview/1622459-transform and then animating the transform back to `.identity` when the gesture ends. although Josh just realized that this is wrong and you need the y-axis (uiview only rotates about z) so you have to actually use CALayer's transform instead of the view's transform for this particular animation.  For instance:

```swift
import PlaygroundSupport
import UIKit

final class V: UIViewController {
  override func viewDidLoad() {
    super.viewDidLoad()
    let square = UIView()
    square.translatesAutoresizingMaskIntoConstraints = false
    square.backgroundColor = .red
    view.addSubview(square)
    NSLayoutConstraint.activate([
      square.centerXAnchor.constraint(equalTo: view.centerXAnchor),
      square.centerYAnchor.constraint(equalTo: view.centerYAnchor),
      square.widthAnchor.constraint(equalToConstant: 100),
      square.heightAnchor.constraint(equalTo: square.widthAnchor)
    ])

    let rotation: CABasicAnimation = CABasicAnimation(keyPath: "transform")

    CATransaction.begin()
    rotation.duration = 5
    rotation.fromValue = CATransform3D()
    rotation.toValue = CATransform3DMakeRotation(.pi, 0, 1, 0)
    square.layer.add(rotation, forKey: "scale")
    CATransaction.commit()
  }
}

PlaygroundPage.current.liveView = V()
```

### Intro to Measurement

TimC gave a brief intro to Foundation Measurements in an XCode playground. Asked for help with Apple's broken Custmo Unit example. Josh suggested running in Mac Playgrounds app - showed the true error. 

```swift
//
// Brief intro to Measurements
// Creation, Conversion, Custom
//

import Foundation

// Create a Measurement
var mile = Measurement(value: 1, unit: UnitLength.miles)

// Convert to another unit
var dMiles = mile.converted(to: .meters)
mile.converted(to: .yards)

// Extend UnitLength to include pool-laps conversions:
extension UnitLength {
    static let lap50m = UnitLength(symbol: "laps", converter: UnitConverterLinear(coefficient: 50))
    static let lap50y = UnitLength(symbol: "laps", converter: UnitConverterLinear(coefficient: 45.72))
    static let lap25y = UnitLength(symbol: "laps", converter: UnitConverterLinear(coefficient: 45.72/2))
}

// How many laps
var lapCount = mile.converted(to: UnitLength.lap50m)

// Make Measurement init less verbose
extension Measurement {
    init(_ v: Double, _ u: UnitType) {
        self.init(value:v, unit:u)
    }
}

// Swimmers consider 1650 yards or 1500 meters a "mile"
// These distances are shorter than an actual mile
var mileSwimY = Measurement(1650, UnitLength.yards)
var mileSwimM = Measurement(1500, UnitLength.meters)
mileSwimY.converted(to: .miles)
mileSwimM.converted(to: .miles)

// How many laps do you need to swim in different pools?

// 1500 meters in a 50 meter pool (Olympic) -> 30 laps
mileSwimM.converted(to: .lap50m)

// 1500 meters in a 50 yard pool -> ~33 laps
mileSwimM.converted(to: .lap50y)

// 1500 meters in a 25 yard pool -> ~66 laps
mileSwimM.converted(to: .lap25y)

// Actual Mile in a 25 yard pool -> ~71 laps (Tim swims 72 to end where he started)
mile.converted(to: .lap25y)

/* Create a Custom Dimension
 
 Apple example code for RadioactivityUnits does NOT compile;
    after some updates, it compiles, throws a runtime error.
 https://developer.apple.com/documentation/foundation/dimension

 class CustomRadioactivityUnit: Dimension {
    //init needs converter: argument name
    static let becquerel = CustomRadioactivityUnit(symbol: "Bq", UnitConverterLinear(coefficient: 1.0))
    static let curie = CustomRadioactivityUnit(symbol: "Ci", UnitConverterLinear(coefficient: 3.7e10))

    static let baseUnit = self.becquerel // replace with "becquerel" to compile
}

 **THANKS JoshHomann** for suggesting Mac Playgrounds app which shows the run-time error.
 
 Error: Crashing on exception: *** You must override baseUnit in your class
      Page_Contents.CustomRadioactivityUnit to define its base unit.

 Note -- obviously the static let isn't doing the job, but TimC found below works:
 */

// Working Custom Unit Dimension!
class CustomRadioactivityUnit: Dimension {
    static let becquerel = CustomRadioactivityUnit(
        symbol: "Bq", converter: UnitConverterLinear(coefficient: 1.0))
    static let curie = CustomRadioactivityUnit(
        symbol: "Ci", converter: UnitConverterLinear(coefficient: 3.7e10))
    
    override class func baseUnit() -> Self {
        becquerel as! Self // expects a *Dimension* as Self
    }
}

var rads = Measurement(1, CustomRadioactivityUnit.becquerel)
var radsC = rads.converted(to: .curie)

print("Rads=\(rads) -> curie= \(radsC) ")
```

### Intro to @propertyWrappers - JoshH

We looked at the basics of proertyWrappers and their three characteristics: 1) a required `wrappedValue`, 2) an optional `projectedValue` 3) an optional `init(wrappedValue:)`.  The only thing a propertyWrapper provides is renaming for the `wrappedValue` (`name`), the underlying struct (`_name`) and the `projectedValue` (`$name`) it is otherwise entirely equivalent to the unsugared struct, as this playground demonstrates:

```swift
import Foundation
import PlaygroundSupport

@propertyWrapper
struct Uppercased {
  private var value: String = ""
  var wrappedValue: String {
    get { value.uppercased() }
    set { value = newValue }
  }
  var projectedValue: String {
    value
  }
  init(wrappedValue: String) {
    self.wrappedValue = wrappedValue
  }
}

final class Person {
  @Uppercased var name = "josh"
  var name2 = Uppercased(wrappedValue: "peter")
  func output() {
    // name.wrappedValue
    print(name)
    // name
    print(_name)
    // name.projectedValue
    print($name)

    print(name2.wrappedValue)
    print(name2)
    print(name2.projectedValue)
  }
}

let p = Person()
p.output()
```

### Custom DynamicProperty implementations

We looked at Apple's DynamicProperty documentations and noted that the only required function has a default implmenation and that call of the propertyWrappers that implment the protocol are listed at the bottom of the page: https://developer.apple.com/documentation/swiftui/dynamicproperty  

Josh walked through the code for this project on how to build your own custom DynamicProperty.  The readme for the project has more details: https://github.com/joshuajhomann/CustomDynamicProperties  

We saw the `struct`s in swift cannot be mutated inside of a function that is not flagged as `mutating`.  We further saw that Apple skirts this restriction with `@State` by using the `nonmutating` keyword for its setter, and that we can do the same thing an achieve the same behavior by using a reference type to store our variable: the reference never changes, but the pointee can change.  If we want to communicate information about the pointee changing, we can use the `ObservedObject` protocol.


## 2021.02.20

### Discussion

This is a good system to produce animations made by designers.
https://github.com/airbnb/lottie-ios

### What are some good SwiftUI starter resources?

- https://www.raywenderlich.com
- Stanford course https://cs193p.sites.stanford.edu
- The landmarks tutorial from Apple https://developer.apple.com/tutorials/swiftui/
- Paul Hudson's 100 days of Swift / SwiftUI 
- A new tutorial from Apple https://developer.apple.com/tutorials/app-dev-training
- Newsletter by Matteo Manferdini https://matteomanferdini.com
- Another list of resources: http://bit.ly/get-started-with-swift

### Debug session: problem with gestures in a collection view

We did a group debug of Clarissa's code. The tap selector for the tap selector wasn't being called.  Josh spoted the problem: the gesture was being added to the cell's root view instead of the `contentView`.  Remember that table view cells and collection view cells have a `contentView` that you need to add your custom views and gestures to.

### Problem with Collection Views in iOS 14.4

Jumping to a particular cell seems to be broken. Mira provided a discussion link:

https://developer.apple.com/forums/thread/663156?answerId=642133022#642133022

### How do you make an app that uses landscape but only in one view

One way is to make a class derived from UIViewController that is a NonRotatingView and overrides supported orientations.  All the views
that don't rotate derive from that.

https://developer.apple.com/documentation/uikit/uiviewcontroller/1621435-supportedinterfaceorientations

### How do you make an enable button and a slider

https://gist.github.com/rayfix/11827eaf8acae38a08b2190c0db72cee

We used `onAppear` and `onChange` to sync state and a binding.

We hit a disable styling problem.  Jo mentioned this:

https://stackoverflow.com/questions/64756306/using-a-toggle-to-disable-a-slider-in-swiftui-results-in-styling-problems


---
## 2021.02.13

### Tricks and tips

John shared Xcode tips from [24 Quick Xcode Tipes article by Paul Hudson](https://www.hackingwithswift.com/articles/229/24-quick-xcode-tips)

Notable shortcuts:
  - **Command-option-control g**  - Run the last unit test.
  - **Command-option /**  - Automatic doc comment template.
  - **Command-control-shift A**  - Author's view (git blame) 

### M1 Rumors 

Bill is interested in M1 rumors, especially this one about a [Mac Mini _Pro version_ in space grey](https://www.macworld.co.uk/news/mac-trends-2021-3800044/#toc-3800044-4)!

### SwiftUI Composition

Tim Colson presented strategies for SwiftUI Composition, i.e. breaking views down into components. SwiftUI composition exercises were inspired by strategies from articles/code/videos by Joseph Pacheco and Paul Hudson. 

The code-along session style was inspired by Tim's year teaching and David Laing's [Grand Unified Theory of Documentation (Divio)](documentation.divio.com) which itself decomposes documentation into four types. Intent was a hands-on learning oriented tutorial, applying composition techniques to a task reminders view. (Unfortunately, Zoom sharing + Xcode + (2 x 4K monitors) crippled Tim's 2015 MBP 13" i7/16GB. He needs an M1x MBP 14"! 

See Tim's GitHub repo has for links and sample code:
https://github.com/timcolson/tut-swiftui-comp -- start with tag v1  `git co tags/v1`

If interested in working thru the code together, reach out to Tim. 

### Breakout rooms

We will try this next week.

---


## 2021.02.06

### Xcode Tricks and Tips

Rainer presented a list of tricks and Tips in Xcode and macOS.

- Click the "jump bar"; then start typing to do a fuzzy match.
- Command click the jump bar to get an alphabetical listing by scope.
- Command-option square brackets to move the entire line of text under the cursor up & down. This also works for partially selected lines of text.
- Define a shortcut in Xcode's key bindings to delete the line under the cursor (or partially selected lines): Command-Backsapce (Pay attention to collisions with system shortcuts ⚠️.
- Control-left/right arrow to move from captial to capital in CamelCase words
- Option-left/right arrows to move to word boundaries, command-left/right arrows to go to head and tail of the line. Hold SHIFT to also select. (Works also in all Apple text editors, i.e. TextEdit & Pages)
- Select text, Command-K to add a URL/web link in Apple text editors.
- Control-Command left/right arrows to go back & forth in file 'browser' history (Shout-out to Caleb!)
- Command Shift J reveals where a file is located in the file navigator.
- Command Shift A exposes actions on a selected piece of text
- Comment `// MARK: - Note` creates a note in the jump bar. Also `FIXME:` and `TODO:`.  The colon makes it show up in the list of jump bar items, and the `-` makes a horizontal divider line in the menu.
- Command-option square brackets moves a line or a group of lines up and down.
- Multi-cursor support: Control-Shift-click or arrow up/down
- Click the blue 'change' ribbon to see an action menu. Command-click to automatically show/hide the changes

### Other tricks:

* [Emacs keybindings](https://caiorss.github.io/Emacs-Elisp-Programming/Keybindings.html)
* [Custom Code Snippets in Xcode](https://medium.com/@hassanahmedkhan/writing-custom-code-snippets-in-xcode-9e91f8ed4207)

### xcconfig

Frank introduced us to the world of xcconfig files. You can specify these files to use in your build.  They handle comments, key values such as:

MY_SETTING = "this is debug mode"

- You can cut and past from the build configuration of Xcode.
- It understands include files to support common settings.
- You can use `include?` for optional includes used for local configuration not checked into version control.

* [Xcode Build Configuration Files article by Mattt @ NSHipster](https://nshipster.com/xcconfig/) - reference article with info similar to what Frank shared 

### SHA256

Ray demo'ed SHA256 hash generation.  Using CryptoKit makes it easy.

```swift
import UIKit
import CryptoKit

var str = "Hello, playground!"

let data = str.data(using: .utf8)!
let digest = SHA256.hash(data: data)
print(String(describing: digest))

extension Digest {
    var hexString: String {
        map { String(format: "%02x", $0) }.joined()
    }
}

let d2 = SHA512.hash(data: data)
SHA512.byteCount
print(digest.hexString)
print(d2.hexString)
```

### URL Publishing Chain Revisited

By request, Josh walked us step-by-step thru the Combine URL publishing chain in his [TeslaOwnerAPI.swift](https://github.com/joshuajhomann/tesla/blob/main/TeslaOwnerAPI/Sources/TeslaOwnerAPI/TeslaOwnerAPI.swift)

---

## 2021.01.30
Josh presented his Tesla Owner app. 
https://github.com/joshuajhomann/tesla

(Note as of 2021.02-13 app is broken due to Tesla changing the authentication process; however, the concepts are still notable!)   

FYI - Josh presenting at SwiftLA meetup - [Creation of Local Packages](https://www.meetup.com/LearnSwiftLA/events/276056318/attendees/)

Some high level notes:
* Uses a Shared URL session
* Models data quickly with Quicktype.io 
* Maps generic Errors to specific server error types
* Returns 

We looked at making a `struct` to encapsulate the unique information about an endpoint:
```swift
struct EndPoint {
  enum HTTPMethod: String {
    case post = "POST", get = "GET"
  }
  enum Parameters {
    case url([String: String]), body(Data)
  }
  var path: String
  var method: HTTPMethod
  var parameters: Parameters? = nil
  var requiresAuthentication = true
  var headers: [String: String] = Self.jsonHeaders
}

...

static func getVehicleData(id: Int) -> Self {
    .init(path: "/api/1/vehicles/\(id)/vehicle_data", method: .get)
}
```

Noted that [Moya](https://github.com/Moya/Moya ) is a more robust general solution; however, a lot can be done with plain URLSessions, as Josh expertly demo'd. 

We discussed using quicktype.io to code gen conformance to `Codable` and making server errors `Codable`:
```swift
public struct ErrorMessage: Codable {
  public var message: String
  public enum CodingKeys: String, CodingKey {
    case message = "error"
  }
}
```

We discussed the value of strongly typed errors and name shadowing Swift.Error:
```swift
  public enum Error: Swift.Error {
    case invalidURL, networkError(Swift.Error), decodingError(Swift.Error), unauthenticated, server(message: String)
    public var message: String {
      switch self {
      case let .server(message): return message
      case let .networkError(error): return error.localizedDescription
      case let .decodingError(error): return error.localizedDescription
      case .invalidURL: return "Invalid URL"
      case .unauthenticated: return "Unauthenticated"
      }
    }
    public var isVehicleUnavailableError: Bool {
      if case let .server(message) = self {
        return message.starts(with: "vehicle unavailable")
      }
      return false
    }
  }
```

We building a URL request from `URLComponents`, `URLQueryItems` and body data:
```swift
  private func makeRequest(from endPoint: EndPoint) throws -> URLRequest {
    var components = URLComponents()
    components.scheme = Constant.scheme
    components.host = Constant.host
    components.path = endPoint.path
    if case let .url(parameters) = endPoint.parameters {
      components.queryItems = parameters.map { key, value in
        .init(name: key, value: value)
      }
    }
    guard let url = components.url else {
      throw Error.invalidURL
    }
    var request = URLRequest(url: url)
    request.httpMethod = endPoint.method.rawValue
    endPoint.headers.forEach { key, value in
      request.setValue(value, forHTTPHeaderField: key)
    }
    if case let .body(data) = endPoint.parameters {
      print(String(data: data, encoding: .utf8))
      request.httpBody = data
    }
    return request
  }
```

We discussed a generic request function:
```swift
  private func request<SomeDecodable: Decodable, Output>(
    _ decoded: SomeDecodable.Type,
    from endPoint: EndPoint,
    transform: @escaping (SomeDecodable) -> Output
  ) -> AnyPublisher<Output, Error> {
    guard var request = try? makeRequest(from: endPoint) else {
      return Fail(error: .invalidURL).eraseToAnyPublisher()
    }
    if endPoint.requiresAuthentication {
      guard let token = token?.accessToken else {
        return Fail(error: .unauthenticated).eraseToAnyPublisher()
      }
      EndPoint.authenticatedHeaders(from: token).forEach { key, value in
        request.addValue(value, forHTTPHeaderField: key)
      }
    }
    return URLSession
      .shared
      .dataTaskPublisher(for: request)
      .mapError(Error.networkError(_:))
      .map(\.data)
      .handleEvents(receiveOutput: { data in
        print(endPoint.path)
        print(String(data: data, encoding: .utf8) ?? "")
      }, receiveCompletion: { completion in
        switch completion {
        case .finished: return
        case let .failure(error):
          print(endPoint.path)
          print("ERROR:\(error.localizedDescription)")
        }
      })
      .decode(type: Either<SomeDecodable, ErrorMessage>.self, decoder: Self.jsonDecoder)
      .mapError(Error.decodingError(_:))
      .map { either -> AnyPublisher<SomeDecodable, Error> in
        switch either {
        case let .left(someDecodable): return Just(someDecodable).setFailureType(to: Error.self).eraseToAnyPublisher()
        case let .right(errorMessage): return Fail(error: Error.server(message: errorMessage.message)).eraseToAnyPublisher()
        }
      }
      .switchToLatest()
      .map(transform)
      .eraseToAnyPublisher()
  }
```

We discussed :
* how side effects should be handled by `handleEvents` 
* errors can be made strongly typed with `mapError`.  
* using a generic `Either` enum to decode heterogenous types from our response (either the decodable type we are looking for or a server error):

```swift
enum Either<Left, Right> {
  case left(Left), right(Right)
}

extension Either: Decodable where Left: Decodable, Right: Decodable {
  init(from decoder: Decoder) throws {
    let container = try decoder.singleValueContainer()
    if let value = try? container.decode(Left.self) {
      self = .left(value)
    } else if let value = try? container.decode(Right.self) {
      self = .right(value)
    } else {
      throw DecodingError.typeMismatch(Self.self, DecodingError.Context(codingPath: decoder.codingPath, debugDescription: "Wrong type for \(String(describing:Self.self))"))
    }
  }
}
```
---

## 2021.01.23

### Proxy 

Discussed network security and _SSL pinning_. Potential topic for future meetup.  You can try it out:

https://www.charlesproxy.com

https://proxyman.io

### Swift Fiddle

It let's you play with the Swift compiler (and different versions) online.

https://swiftfiddle.com

### Enums

We talked about how equality checking for enums do not consider argument labels.  The same thing goes for comparison and hash values coming in a future
version of Swift when [tuples will become Equatable, Comparable and Hashable[(https://github.com/apple/swift-evolution/blob/main/proposals/0283-tuples-are-equatable-comparable-hashable.md) if all of the element types are Equatable, Comparable and Hashable respectively.


Regarding comparison of floating point, question about zero was raised.  IEEE-754 specifies a sign bit so there are multiple representations of zero.

https://developer.apple.com/documentation/swift/double/1538731-iszero

### Your Demo Here

If you have a trick or tip and want to show the group, remember to write it down.

https://www.dunebook.com/best-xcode-themes/ - 
https://github.com/tonsky/FiraCode - font for terminal and Xcode that includes ligatures for common two-char symbols
[How to draw bounding boxes with SwiftUI (Medium)](https://medium.com/swlh/how-to-draw-bounding-boxes-with-swiftui-d93d1414eb00) - useful for scanning-related project ideas, ex: draw a box around a QR code in a video capture. 

### Demo SwiftUI Picker

We explored Picker with a simple example. 

https://gist.github.com/rayfix/ed02927bce0d645911b578edf5379baf

### Names in the app store

Needs to be a real name or company name (LLC, Corporation, etc).  Apple doesn't allow DBAs.

https://developer.apple.com/support/enrollment/

### Demo Exquisite Corpse

Got a quick demo of a game that Jo is building. And talked about debugging Firebase cloud functions.  It is taking minutes to spin up an instance and something seems wrong.

---

## 2021.01.18

### Discussion of Corporate Dev Account vs Personal Account

Be careful of LLC (with a single person) or even a corporation. If you don't do everything to the letter, chances are the corporate veil can be pierced.  When you are just starting out, it is probably easiest to use a personal account.  While there was agreement that it can be changed later there was some disagreement about how hard it is to do.

### Emil's TikTok App Tutorial Recommendation
https://www.youtube.com/watch?v=71-l3Ndf6Ug

### iCloud sync

What folder should you use to sync with?

- Library - saved, not directly accessible
- Document - save, user access
- Cache - purgeable not directly accessible

Sync is surprisingly hard so it makes sense to use a third party library.  Several exist:

- iCloud https://developer.apple.com/icloud/cloudkit/
  - [Apple - Mirroring a Core Data Store with CloudKit](https://developer.apple.com/documentation/coredata/mirroring_a_core_data_store_with_cloudkit)
- Realm  https://realm.io
- Apollo for GraphQL https://www.apollographql.com/docs/ios/
- Google Firebase https://firebase.google.com
- Parse 

### Refactoring to Combine

Emily gave us a presentation on Caleb and her experience refactoring to Combine.

- The code is nicer than nested callbacks.
- Discussion on weak captures to prevent extension of lifetime (capture self, or just capture exactly what is needed in the callback closure).
- How can the number of error states be reduced?

Josh reminded us of a previous project that abstracts loading state and error / empty response handling.

https://github.com/joshuajhomann/ShimmeringLoadingState

Josh also recommends a single access point for doing requests.  Link TBD. (Next week?)


### Proposal for Visualization Toolkit

The idea is to have a library to allow you to read in a CSV file and then render as a plot.

Can we make something comparable to D3 https://d3js.org

### Tesla Watch App: Modules

Josh showed an in-progress watch app that uses the Tesla API to unlock the car. We will look at it in greater detail in a future meetup.

This week he showed how to factor out watch and iOS code into a common Swift Package Manager module.


---

## 2021.01.09
We discussed the new [asynchronous sequence proposal](https://github.com/apple/swift-evolution/blob/main/proposals/0298-asyncsequence.md)

We discussed `reduce` (fold) and its inverse (unfold) `sequence` https://developer.apple.com/documentation/swift/2011998-sequence
```swift
let a = (0..<20).reduce(0, +)
print(a)

let b = sequence(state: (total: a, counter: 0)) { state -> Int? in
  guard state.total > 0 else { return nil }
  state.total -= state.counter
  defer { state.counter += 1}
  return state.counter
}

print(Array(b))
```
We then explored the limitations of `sequence` ie (its inability to remove a element once its been produced) and derived a new unfold operator:
```swift
@discardableResult func unfold<State>(into value: State, next: @escaping (inout State) -> State?) -> State {
  var localState = value
  var unfolded = sequence(state: localState) { _ -> State? in
    next(&localState)
  }
  while unfolded.next() != nil { }
  return localState
}
```
and we used it to replace an imperative version of reversi:
```swift
  private func flipsForAdding(_ targetColor: Piece.Color, at coordinate: Coordinate) -> [Coordinate] {
    guard coordinate.isValidForBoard && board[coordinate].color == nil else { return [] }
    var total = [Coordinate]()
    for offset in Constant.adjacentOffsets {
      var subtotal = [Coordinate]()
      var next = coordinate + offset
      while next.isValidForBoard {
        guard let color = board[next].color else {
          subtotal.removeAll()
          break
        }
        if color == targetColor {
          break
        }
        subtotal.append(next)
        next = next + offset
      }
      total.append(contentsOf: subtotal)
    }
    return total
  }
```
with a functional version:
```swift
 private func flipsForAdding(_ targetColor: Piece.Color, at coordinate: Coordinate) -> [Coordinate] {
    guard coordinate.isValidForBoard && board[coordinate].color == nil else { return [] }
    return Constant.adjacentOffsets.flatMap { [board] offset -> [Coordinate]  in
      unfold(into: (coordinate: coordinate, accumulated: [Coordinate]())) { [board] state in
        state.coordinate = state.coordinate + offset
        guard state.coordinate.isValidForBoard, let color = board[state.coordinate].color else {
          state.accumulated.removeAll()
          return nil
        }
        if color == targetColor {
          return nil
        }
        state.accumulated.append(state.coordinate)
        return state
      }
      .accumulated
    }
  }
```

Full project: https://github.com/joshuajhomann/Reversi-SwiftUI-Animation
![Reversi](https://github.com/joshuajhomann/Reversi-SwiftUI-Animation/blob/master/preview.gif)
---

## 2021.01.02

Happy New Year!

Josh created an animated SwiftUI `RingChart` view that he plans to integrate into the **Tides** app.  

https://github.com/joshuajhomann/RingChart

![RingChart](resources/ringchart.gif)

## Archives

- [2020 Meetings](2020/README.md)
