# A Flock of Swifts

We are a group of people excited by the Swift language. We meet each Saturday morning to share and discuss Swift-related topics. 

All people and all skill levels are welcome to join. 

## Archives

- [2020 Meetings](2020/README.md)
- [2021 Meetings](2021/README.md)
- [2022 Meetings](2022/README.md)


## 2023.03.18

- **RSVP**: https://www.meetup.com/A-Flock-of-Swifts/

---

## 2023.03.11
### Whats new in Swift

Swift 5.8 has been released to beta:
- https://www.hackingwithswift.com/articles/256/whats-new-in-swift-5-8

Also Swift 9 is on the way
- https://forums.swift.org/t/swift-5-9-release-process/63557

New actor proposal

Frank's code for his talk about distributed actors:
h-ttps://github.com/franklefebvre/DistributedActors-FrenchKit

Question from Allen: how to we sync state between SwiftUI and Scenekit
- Answer: have a single source of truth:
```swift
    final class ViewModel: ObsevableObject {
        @Published var truth
    ...
    }
```
- share with SwiftUI with binding via the projected value of the `StateObject`:
```
   childview($viewmodel.binding)
```
- share with SceneKit with a publisher projected fromt he `@Published` property
```
   scene(viewmodel.$truth)
```

### Demo: ImageIO

Josh went over the ImageIO library and using it to read files, and image meta data.  The full project is below:
- https://github.com/joshuajhomann/ImageIOExample
![preview](https://github.com/joshuajhomann/ImageIOExample/raw/main/preview.gif "ImageIOExample")

---

## 2023.03.04

### Conferences

- Deep Dish Swift https://deepdishswift.com
- Try Swift https://www.tryswift.co/events/2023/nyc/

### Escaping Closures

@escaping means they can be stored in a property and used as a callback later.

- http://www.goshdarnclosuresyntax.com

Also recommended by Carlyn:

- https://www.hackingwithswift.com/quick-start/beginners/how-to-accept-functions-as-parameters


### Generative AI for Game Assets

- https://aiva.ai
- https://www.scenario.com


### Metal

Josh created an Apple cross-platform app to show how to get Metal going in SwiftUI and created a `MetalView`. (Watch does not support metal yet.)

Roughly based on:

- https://medium.com/@warrenm/thirty-days-of-metal-day-1-devices-e371729d05ca

Also see:

- https://developer.apple.com/metal/Metal-Shading-Language-Specification.pdf


You can see some amazing WebGL based demos at:

 - https://www.shadertoy.com

Project:
- https://github.com/joshuajhomann/MetalExample

![preview](https://github.com/joshuajhomann/MetalExample/blob/main/preview.png "MetalExample")

---

## 2023.02.25

### WeightedStackView


Josh put together a new type of stack layout that lets each view communicate what weight it wants to the layout system. He wrote the logic for placing views in a functional style and utilized lazy sequences to avoid creation of temporary copies.

See https://developer.apple.com/documentation/swift/lazysequenceprotocol


```swift
import PlaygroundSupport
import SwiftUI

struct V: View {
    var body: some View {
        WeightedStackLayout(axis: .vertical, spacing: 0) {
            Color.red.stack(weight: 7)
            Color.green.stack(weight: 5)
            Text("hi").background(Color.yellow)
            Color.blue.stack(weight: 3)
            Color.orange.stack(weight: 2)
            Color.brown.stack(weight: 4)
            Color.cyan.stack(weight: 3)
        }
            .frame(width: 400, height: 400)
    }
}

PlaygroundPage.current.setLiveView(V())

struct WeightedStackLayoutKey: LayoutValueKey {
    static var defaultValue = 1.0
}

extension View {
    func stack(weight: Double) -> some View {
        layoutValue(key: WeightedStackLayoutKey.self, value: weight)
    }
}

extension Layout.Subviews.Element {
    var stackWeight: Double {
        max(self[WeightedStackLayoutKey.self], 1e-6)
    }
}

struct WeightedStackLayout: Layout {
    var axis: Axis = .vertical
    var spacing: CGFloat = 10

    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        proposal.replacingUnspecifiedDimensions(by: .zero)
    }

    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        let totalSpace = CGFloat(subviews.count - 1) * spacing
        let dimension = (axis == .vertical ? bounds.height : bounds.width) - totalSpace
        let pointsPerWeight = dimension / subviews.lazy.map(\.stackWeight).reduce(0, +)
        let weights = subviews.lazy.map(\.stackWeight).accumulated(0, +)
        let points = zip(
            weights.dropLast(),
            weights.dropFirst()
        ).enumerated().lazy.map { offset, element in
            let (startWeight, endWeight) = element
            let spaceBefore = spacing * CGFloat(offset)
            let offset = axis == .vertical ? bounds.origin.y : bounds.origin.x
            return (
                start: startWeight * pointsPerWeight + spaceBefore + offset,
                end: endWeight * pointsPerWeight + spaceBefore + offset
            )
        }
        zip(subviews, points).forEach { view, point in
            let distance = point.end - point.start
            switch axis {
            case .vertical:
                view.place(
                    at: .init(x: bounds.midX, y: point.start + distance / 2),
                    anchor: .center,
                    proposal: .init(width: bounds.width, height: distance)
                )
            case .horizontal:
                view.place(
                    at: .init(x: point.start + distance / 2, y: bounds.midY),
                    anchor: .center,
                    proposal: .init(width: distance, height: bounds.height)
                )
            }
        }
    }

}

struct LazyAccumulatedSequence<Accumulated>: LazySequenceProtocol {
    private let _makeIterator: () -> Iterator
    init<Element>(
        underlying: some Sequence<Element>,
        initial: Accumulated,
        accumulate: @escaping (Accumulated, Element) -> Accumulated
    ) {
        _makeIterator = {
            var iterator = underlying.makeIterator()
            var nextAccumulated: Accumulated? = initial
            return Iterator {
                nextAccumulated.map { accumulated in
                    nextAccumulated = iterator.next().map { next in
                        accumulate(accumulated, next)
                    }
                    return accumulated
                }
            }
        }
    }
    func makeIterator() -> Iterator { _makeIterator() }
    struct Iterator: IteratorProtocol {
        let _next: () -> Accumulated?
        mutating func next() -> Accumulated? { _next() }
    }
}

extension LazySequenceProtocol {
    func accumulated<Accumulated>(
        _ initial: Accumulated,
        _ accumulate: @escaping (Accumulated, Element) -> Accumulated
    ) -> LazyAccumulatedSequence<Accumulated> {
        LazyAccumulatedSequence(underlying: self, initial: initial, accumulate: accumulate)
    }
}

extension Sequence {
    func accumulated<Accumulated>(
        _ initial: Accumulated,
        _ accumulate: (Accumulated, Element) throws -> Accumulated
    ) rethrows -> [Accumulated] {
        var current = initial
        var accumulated = [Accumulated]()
        accumulated.reserveCapacity(underestimatedCount + 1)
        accumulated.append(current)
        for element in self {
            current = try accumulate(current, element)
            accumulated.append(current)
        }
        return accumulated
    }
}

print([1,2,3].accumulated(0, +))

```

### Deep linking in Apps

Josh had an example:

- https://github.com/joshuajhomann/PokemonNavigation

### Learning AI

General Neural Networks

- https://www.youtube.com/watch?v=aircAruvnKk

Running on you own computer

- https://github.com/karpathy/nanoGPT


Facebook's Large Language Model

- https://ai.facebook.com/blog/large-language-model-llama-meta-ai/
- https://github.com/facebookresearch/llama


ChatGPT Client for iOS

- https://github.com/adamrushy/OpenAISwift.git


---

## 2023.02.18


### Upcoming Conferences

- https://www.tryswift.co/events/2023/nyc/


### Edit Kit Pro

From iOSDev weekly, Ed told us about https://digitalbunker.dev/editkit-pro/

### URLSessionTaskDelegate

Carlyn is doing some work on the 

- https://developer.apple.com/documentation/foundation/urlsessiontaskdelegate
- https://github.com/MastodonKit/MastodonKit
- https://github.com/TootSDK/TootSDK
- https://github.com/carlynorama/TrunkLine/blob/dev/Sources/TrunkLine/Mastodon/ServerSentEventListener.swift


### Models 

You can do a lot of work to cleanup models by declaring custom initializers.  (You don't have to expose ViewModels but can construct those internally.)  You can also use custom Codable to cleanup your code.

- https://developer.apple.com/documentation/foundation/archives_and_serialization/encoding_and_decoding_custom_types
- https://quicktype.io/


### Tagged

Ray revisited the `Identifier<Tag>` type that we looked at in November. The folks over at point free have a library that makes it easy to make unique little types.

- https://github.com/pointfreeco/swift-tagged

```swift
import Tagged

struct User {
    var id: Tagged<Self, UUID>
}
```

The point free guys have a whole series on modern SwiftUI development that you can check out on their blog.
https://www.pointfree.co/blog


### Swift Evolution Proposals

- Attached Macros (https://forums.swift.org/t/se-0389-attached-macros/63165)
- Expression Macros (https://forums.swift.org/t/se-0382-second-review-expression-macros/63064)
- Convenience Async makeStream methods (https://forums.swift.org/t/se-0388-convenience-async-throwing-stream-makestream-methods/63139)

### Unicode

Swift Strings are unique in the way that they handle Unicode. Several examples from Josh about how mutation is handled with both `String` and bridged `NSString` and `NSMutableString`. Swift makes a defensive copy for you when assigning.

```swift
var a: String = "a"
var b: UnsafeMutablePointer<String> = .init(&a)
a = "b"
print(a,b.pointee)

var c: NSMutableString = "c"
var d: NSString = c
c = "d"
print(c,d)

@propertyWrapper
struct Reference<Value> {
    final class Wrapper<Value> {
        var value: Value
        init(value: Value) {
            self.value = value
        }
    }
    private var wrapper: Wrapper<Value>
    var wrappedValue: Value {
        get { wrapper.value }
        set { wrapper.value = newValue }
    }
    init(wrappedValue: Value) {
        wrapper = .init(value: wrappedValue)
    }
}

var e = Reference(wrappedValue: "e")
var f = e
e.wrappedValue = "f"
print(e.wrappedValue, f.wrappedValue)

["âa", "áb", "àc", "ad", "äe"].lazy.map { string in
    string.contains("a")
}.forEach { print($0) }

["âa", "z", "áb", "àc", "ad", "äe"].sorted { lhs, rhs in
    lhs.lexicographicallyPrecedes(rhs)
}.forEach { print($0) }

["âa", "áb", "àc", "ad", "äe"].lazy.map { string in
    string.localizedStandardContains("a")
}.forEach { print($0) }

["âa", "z", "áb", "àc", "ad", "äe"].sorted { lhs, rhs in
    lhs.localizedCaseInsensitiveCompare(rhs) == .orderedAscending
}.forEach { print($0) }
```

---

## 2023.02.11

### Virtual Buddy

A useful tool for creating clean installs. Frank will soon be making a pull request for linux VMs.

- https://github.com/insidegui/VirtualBuddy
- https://developer.apple.com/documentation/virtualization/installing_macos_on_a_virtual_machine

### Smooth Data

Common methods include moving averages, exponential smoothing, kernel smoothing, and splines. 

We discussed a moving average which is probably the simplest.  You can do this with a queue.

- https://github.com/apple/swift-collections/blob/main/Documentation/Deque.md


### Passing Data

Although not discussed on video, this was a side discussion in the chat.

- https://www.bigmountainstudio.com/data
- https://developer.apple.com/wwdc20/10040 

### Facebook Engineering

Discussion of the technology Facebook uses (C++, Obj-C++)   

  - https://engineering.fb.com/2023/02/06/ios/facebook-ios-app-architecture/

If you want to do hardcore Swift, Facebook might not be your first choice.

### Cross Platform SwiftUI

- https://www.scade.io

Although they might only have a small subset of things done.

### Swift on the Command Line (Scripting)

Carlyn talked about work she is doing in VS Code and Swift

- https://github.com/carlynorama/swift-scripting
- https://github.com/carlynorama/tipsy-robot-swift


Link mentioned in chat:

- https://rderik.com


A side topic to this was Swift on the Server:

- https://vapor.codes
- https://www.swift.org/sswg/
- https://www.areweserveryet.org

Frank mentioned that the biggest gotcha is differences between implementations on Linux and macOS. Several (Josh and Franklin) noting that this will eventually be solved when Foundation becomes pure Swift:

- https://www.swift.org/blog/future-of-foundation/


### Wordle Animation!

Josh shows how animation can be brought into the wordle app with a little restructuring.  Shows the difference between implicit and explicit animation.

https://github.com/joshuajhomann/Wordle



---

## 2023.02.04

### Parsing RSS Feeds

RSS is simple XML, so the the old XML Parser API should work.
    
- https://developer.apple.com/documentation/foundation/xmlparser

Frank did some work on this previously. This project might help.

- https://github.com/franklefebvre/XMLCoder

Josh implemented a partial SVG reader where he didn't implement all of the callbacks but got the information that he was interested in.  See: https://github.com/joshuajhomann/SVGPasteBoard/blob/master/SVGPasteBoard/ContentView.swift


### Using Custom Fonts

Ed wants his custom fonts to play nicely with the OS (and respect dynamic type).

Franklin mentioned:

```swift
@ScaledMetric(relativeTo: .largeTitle) var dynamicHeader1Size: CGFloat = 24
```

### iOS Podcast GPT

- https://www.buzzsprout.com/1414396


### Writing Apps with ChatGPT

Emil reports that ChatGPT is helping him to get going with SwiftUI.  He has reproduced a major portion of his previous app in SwiftUI in a few days where the original took him months (as he was learning).

Noting that some of the code is old (because ChatGPT was trained before 2021).  

The licensing of the code is ambiguous.


### Space, the final Frontier

Carlyn mentioned that many of her space friends are excited about this new release:

https://www.penguinrandomhouse.com/books/651844/critical-mass-by-daniel-suarez/


### The Nature of Code 

Carlyn has been working through these (knows the author) in the last couple of months:

 - https://natureofcode.com/ 
 - https://thecodingtrain.com/


### Wordle Clone!

Josh implemented all of the game logic for his wordle clone. He used a reducer that took inputs through a tap gesture recognizer and reduced the state, modifying two properties that drive the UI updates.

https://github.com/joshuajhomann/Wordle

---


## 2023.01.28

### AsyncImage Fix

Jake had an update to how he was able to fix the animation problem with `AsyncImage`. Here is the code:

```swift
AsyncImage(url: user.profileURL,
           transaction: Transaction(animation: .default)) { phase in
  switch phase {
    case .success(let image):
             image.resizable()
                  .clipShape(Circle())
                  .aspectRatio(contentMode: .fit)
    default:
            ZStack {
              Circle().stroke(.black)
                      .frame(width: 90, height: 90)
              Image(systemName: "person")
                      .font(.title.bold())
                      .scaledToFill()
            }
    }                                  
}.frame(width: 90, height: 90)
```

### Non-uniform shuffling

Carlyn asked about the most Swifty way to enable non-uniform probability picking.

Some suggestions from the group:

- Look around in GameKit? (Perhaps look at this: https://www.youtube.com/watch?v=gXnuMk7AVwc)
- Create an array with duplicates of the number of elements in the probablilty you want.
- Create a special collection that vends the duplicates without actually hosting them in memory.

A related topic:  https://en.wikipedia.org/wiki/Rejection_sampling


### Speeding up Conformance Checking

We reviewed this blog post about how you can re-order conformance records to get a 20% performance boost.

-  https://www.emergetools.com/blog/posts/how-order-files-speed-up-protocols


### Wurdle (Wordle Clone)

Josh continued his epic presentation on a Wordle clone.  Attempted to make it work pretty. Namely, `GeometryReader` is not greedy and anchors things to the upper-left. You can work around it by adding a ZStack that contains a greedy view like Color.clear or Rectangle().hidden() to the ZStack.

We used the `Layout` protocol which is a type of view that can explicitly control the layout of a view and its subviews. Josh created a AnchorInParentLayout that lets you align an arbitrary position (`UnitPoint`) with an arbitrary position of the subview(s). A view modifier makes it easy to use.

---

## 2023.01.21


### Layout with AsyncImage

Jake was seeing a problem with `AsyncImage` where the transition animation would be cancelled when the async image loaded.  The image would appear at the destination without loading. Josh theorized that the problem was happening because its identity was changing. However, we could not seem to fix the problem by explicitly setting `id` on the views.

One recommendation is to use a much more capable third party library like Nuke.

- https://github.com/kean/Nuke


### Dates

Using Core Data to sort by date. Ed says, "`CalendarComponents` is your friend."  Trevor recommended this resource:  https://nsdateformatter.com/

### Inspiration for UI

- https://dribbble.com
- https://twitter.com/_kavsoft?lang=en
- Edward Tufte

Jacey noted that SnapKit is also good (easy) way to layout views.

- https://github.com/SnapKit/SnapKit


### Sendable

Sendable conformance will be one of the important areas to be aware of as come into Swift 6. You can enable strict concurrency warnings in your build settings. The default is minimal but you can use "targetted" to check your own code.

When you enabled this checking, you will see warnings where an instance is passed across a concurrency domain and is not `Sendable`. For example:

```swift
func findInBackground(quadTree: QuadTree,
                      region: CGRect) async -> Task<[CGPoint], Never> {
  Task.detached {
    quadTree.find(in: region) // WARNING: QuadTree is not Sendable
  }
}
```

You can mark `QuadTree` as `Sendable` to fix this warning. This will, in turn, lead to a warning that `Node`, the reference type, is not sendable. If you mark `Node` sendable you get more warnings. This is because the class contains multiple immutable stored properties that could get modified from another concurrency domain. In this case you can mark `Node` with `@unchecked Sendable` since you know that all mutation is protected by `isKnownUniquelyReferenced` and makes a deep copy if it is not unique. (Aka COW.) 


### Benchmarks

The collection-benchmark project allows you to create benchmarks where the time might be dependent on the size of the input.  We created a command-line target and included the benchmark package.

- https://github.com/apple/swift-collections-benchmark


We wrote the following benchmarks:

```swift
import CollectionsBenchmark
import CoreGraphics.CGBase

struct TestPoints {
  let region: CGRect
  let points: [CGPoint]
  
  init(size: Int) {
    region = CGRect(origin: .zero, size: CGSize(width: size, height: size))
    points = zip((0..<size).shuffled(), (0..<size).shuffled())
      .map { CGPoint(x: $0.0, y: $0.1) }
  }
}


var benchmark = Benchmark(title: "QuadTree Benchmarks")

benchmark.registerInputGenerator(for: TestPoints.self) { size in
  TestPoints(size: size)
}


benchmark.add(title: "QuadTree find",
              input: TestPoints.self) { testPoints in
  
  let tree = QuadTree(region: testPoints.region, points: testPoints.points)
  return { timer in
    testPoints.points.forEach { point in
          let searchRegion = CGRect(origin: point, size: .zero).insetBy(dx: -1, dy: -1)
          blackHole(tree.find(in: searchRegion))
        }
  }
}

benchmark.addSimple(title: "Array<CGPoint> filter",
                    input: TestPoints.self) { testPoints in
  testPoints.points.forEach { point in
    let searchRegion =  CGRect(origin: point, size: .zero).insetBy(dx: -1, dy: -1)
    blackHole(testPoints.points.filter { candidate in
      searchRegion.contains(candidate)
    })
  }
}

benchmark.main()
```

Then we ran the following commands arguments:

```
run QuadFindResult.json --cycles 1
render QuadFindResults.json QuadFindResults.png
```

This produced the following results:

![Benchmark Results for Find](materials/QuadFindResults.png)

This is a log-log chart and you can see that the growth of the array implementation is linear.

You can see the jump at 4 items which is where the QuadTree logic is kicking in.  I found that on my machine, I can boost this constant to 512 to make it always perform better than array.

You can also use a special group file to automatically produce sets of benchmarks and multiple graphs.

### Wurdle

Josh continued working on the Wordle game example getting through a lot of the layout issues of the words and keyboard (adding return and backspace). 
```swift
import SwiftUI

extension Color {
    static let darkGray = Color(#colorLiteral(red: 0.4784313725, green: 0.4823529412, blue: 0.4980392157, alpha: 1))
    static let lightGray = Color(#colorLiteral(red: 0.8274509804, green: 0.8431372549, blue: 0.8549019608, alpha: 1))
    static let darkGreen = Color(#colorLiteral(red: 0.4117647059, green: 0.6705882353, blue: 0.3803921569, alpha: 1))
    static let darkYellow = Color(#colorLiteral(red: 0.7960784314, green: 0.7098039216, blue: 0.3137254902, alpha: 1))
}

struct Row: Hashable, Identifiable {
    var id: Int
    var letters: [Letter]
}

struct Letter: Hashable, Identifiable {
    var id: Int
    var character: Character
    var status: Status
    enum Status: Int, Comparable {
        static func < (lhs: Letter.Status, rhs: Letter.Status) -> Bool { lhs.rawValue < rhs.rawValue }
        case unguessed, wrong, wrongPosition, correct
    }
}

@MainActor
final class GameViewModel: ObservableObject {
    @Published private(set) var words: [Row] = []
    @Published private(set) var keys: [Row] = []
    init() {
        words = ["SWIFT", "CODER", "PLAYA", "     ", "     ", "     "]
            .enumerated()
            .map { word in
                Row(
                    id: word.offset,
                    letters: word.element.enumerated().map { character in
                        Letter(
                            id: word.offset * 10 + character.offset,
                            character: character.element,
                            status: {
                                switch character.element {
                                case " ": return Letter.Status.unguessed
                                case "O", "A": return .correct
                                case "L": return .wrongPosition
                                default: return .wrong
                                }
                            }()
                        )
                    }
                )
            }
        $words
            .map { rows in
                let keys = rows
                    .lazy
                    .flatMap(\.letters)
                    .reduce(into: [Character: Letter.Status]()) { accumulated, next in
                        accumulated[next.character] = accumulated[next.character].map { max($0, next.status) } ?? next.status
                    }
                return ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
                    .enumerated()
                    .map { string in
                        Row(
                            id: string.offset,
                            letters: string.element.enumerated().map { character in
                                Letter(
                                    id: string.offset * 100 + character.offset,
                                    character: character.element,
                                    status: keys[character.element] ?? .unguessed
                                )
                            }
                        )
                    }
            }
            .assign(to: &$keys)
    }
}

struct ContentView: View {
    @StateObject var viewModel = GameViewModel()
    var body: some View {
        GeometryReader { reader in
            VStack(spacing: 36) {
                Grid(alignment: .topLeading, horizontalSpacing: 12, verticalSpacing: 12) {
                    ForEach(viewModel.words) { row in
                        GridRow {
                            ForEach(row.letters) { letter in
                                LetterView(style: .word(letter))
                            }
                        }
                    }
                }
                .frame(maxWidth: 600)
                VStack (spacing: 12) {
                    ForEach(viewModel.keys) { row in
                        HStack(spacing: 8) {
                            if viewModel.keys.last == row {
                                LetterView(style: .keyImage("return"))

                                keys(for: row)
                                LetterView(style: .keyImage("delete.backward"))

                            } else {
                                keys(for: row)
                            }
                        }
                    }
                }
            }
            .padding()
        }
    }

    private func keys(for row: Row) -> some View {
        ForEach(row.letters) { letter in
            LetterView(style: .key(letter))
        }
    }
}

struct LetterView: View {
    var style: Style
    enum Style {
        case key(Letter), word(Letter), keyImage(String)
    }
    private let fontSize: CGFloat
    private let aspectRatio: CGFloat
    private let textColor: Color
    private let backgroundColor: Color
    private let outlineColor: Color

    init(style: Style) {
        self.style = style
        switch style {
        case .keyImage:
            aspectRatio = 0.66 * 1.5
            fontSize = 48
            textColor = .black
            backgroundColor = .lightGray
            outlineColor = .clear
        case let .key(letter):
            aspectRatio = 0.66
            fontSize = 48
            (textColor, backgroundColor, outlineColor) = colors(for: letter, isKey: true)
        case let .word(letter):
            aspectRatio = 1
            fontSize = 100
            (textColor, backgroundColor, outlineColor) = colors(for: letter, isKey: false)
        }
        func colors(for letter: Letter, isKey: Bool) -> (Color, Color, Color) {
            switch (letter.status, isKey) {
            case (.unguessed, true): return (.black, .lightGray, .clear)
            case (.unguessed, false): return (.black, .white, .black)
            case (.correct, _): return (.white, .darkGreen, .clear)
            case (.wrongPosition, _): return (.white, .darkYellow, .clear)
            case (.wrong, _): return (.white, .darkGray, .clear)
            }
        }
    }

    var body: some View {
        GeometryReader { proxy in
            RoundedRectangle(cornerRadius: 8)
                .strokeBorder(outlineColor, lineWidth: 4)
                .background(RoundedRectangle(cornerRadius: 8).fill(backgroundColor))
                .overlay {
                    switch style {
                    case let .keyImage(name):
                        Image(systemName: name)
                    case let .key(letter), let .word(letter):
                        Text(String(describing: letter.character))
                    }
                }
                .foregroundColor(textColor)
                .font(.system(size: fontSize, weight: .bold))
        }
        .aspectRatio(aspectRatio, contentMode: .fit)
    }
}

```
---

## 2023.01.14

### PointFree Dependency Injection

A new library for dependency injection was announced this week by the folks at pointfree.co. Josh gave us a quick tour of the library and an additions library:

https://github.com/pointfreeco/swift-dependencies

Peter posted this example of using the additions library:

https://twitter.com/tgrapperon/status/1612698675356250114

### Ed Launches Testflight

Ed launched a private testfligt build for his new app. During the coarse of the meeting was able to find and fix an out of bounds crasher when there is no data. The power of testing in action.

### Learning Swift

Some of the tried and true:

- https://cs193p.sites.stanford.edu
- https://twostraws.gumroad.com/l/pro-swiftui

### Async Result

You can create an async init for result types to get clean monadic chaining instead of nested `do {} catch {}` blocks. Daniel and Josh showed us how!


### CoreData

Core Data is a deep subject. A good place to start:

- https://developer.apple.com/documentation/coredata/setting_up_a_core_data_stack



### Noise Generation

GameKit although old and written in ObjectiveC, has API for creating "natural" noise often used for procedural terrain generation in games. 

- https://developer.apple.com/documentation/gameplaykit/gknoisemap


### Wurdle

As part of another epic, multipart demo, Josh is implementing a version of the popular game in SwiftUI.  Today he created the basic model for Rows and Letters and Keys as well as the Status for each.


---

## 2023.01.07

### Using contraMap Example

You can write a contramap function on `CurrentValueSubject<Int>` to make functions
that can send other types into the current value.

```swift
import Foundation
import Combine

extension CurrentValueSubject {
    func contraMap<Value>(transform: @escaping (Value) -> Output) -> (Value) -> Void {
      { [weak self] input in
          self?.send(transform(input))
      }
    }
}

let subject = CurrentValueSubject<Int, Never>(0)
let sendBool = subject.contraMap { (bool: Bool) in bool ? 1 : 0 }
sendBool(true)
print(subject.value)
```

### Learning SwiftUI

- https://swiftui-lab.com
- https://swiftui-lab.com/companion/


### Core Data Debugging

Suggestions for Dan's app that has a crashing problem:

- Log non-fatal errors
- Think about all of the validations done by the Core Data model
- It reliably crashes on start
- Take note of the OS / devices it is happening on in the crash logs
- Debugging concurrency issues with -com.apple.CoreData.ConcurrencyDebug 1

### Returning Swift Conferences

- https://deepdishswift.com
- https://www.swiftconf.to
- https://tryswift.jp (meetup style on 1/21)

### Swift Charts Performance

Ed wrote his own charts with `GeometryReader` instead of SwiftUI Charts because of
performance problems on rotation and scrolling.

### Photo Picker iOS16

- Jake reports it is awesome.
- Requires user iteraction so no permission is required.
- https://developer.apple.com/documentation/photokit/photospicker


### New Swift Proposals

https://www.swift.org/swift-evolution/

- SE-0383 Deprecate @UIApplicationMain and @NSApplicationMain
- SE-0384 Importing Forward Declared Objective-C Interfaces and Protocols
- SE-0382 Expression Macros

### Compression
The new multicore APFS aware Apple Archive framework: https://developer.apple.com/documentation/applearchive

### Swift Collections

Josh took us on a guided tour of the Swift Collections package.

- https://github.com/apple/swift-collections

Exploration of CHAMP:
- https://blog.acolyer.org/2015/11/27/hamt/
- https://www.youtube.com/watch?v=imrSQ82dYns


Aside: A Benchmarking Tool
- https://github.com/apple/swift-collections-benchmark


### JSON with decode indirect enum


You can represent JSON with swift with this:

```swift
enum JSON {
	indirect case array([JSON])
	indirect case dictionary([String: JSON])
	case boolean(Bool)
	case number(Double)
	case string(String)
	case null
}
```

You can implement `Decodable` using a single value container. Naively it is a bunch of nested `do {} catch {}` blocks but it can be done quite succinctly by using a `Result` type and `flatMapError` to implement successive retries.

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
