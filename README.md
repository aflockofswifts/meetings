# A Flock of Swifts

We are a group of people excited by the Swift language. We meet each Saturday morning to share and discuss Swift-related topics. 

All people and all skill levels are welcome to join. 

## 2022.07.09

- **RSVP**: https://www.meetup.com/A-Flock-of-Swifts/

---

## 2022.07.09

Sample project for navigation:
https://github.com/joshuajhomann/PokemonNavigation
![preview](https://github.com/joshuajhomann/PokemonNavigation/raw/main/preview.gif)
---

## 2022.07.02


### Useful Links

Experiment with Swift Regex online.  Brought to you by Kishikawa Katsumi and the Swift Fiddle.

- https://swiftregex.com

New static methods in iOS 16 for getting to common file directories:

- https://nilcoalescing.com/blog/GetURLsForSystemFolders

Format your Swift code

- https://github.com/ruiaureliano/X-SwiftFormat

Quick formatting longer lines:

- https://github.com/aheze/Multiliner


### Pokemon Navigation

Josh builds a sample project using the new navigation types in iOS 16.  The new navigation gives you full programmatic control of navigation including state restoration and deep linking.

- `NavigationSplitView` - The overload that you want is the one that gives you a binding to column visibility.
- `NavigationStack` - Use path as a data tree that controls the views that get pushed on the nav stack.
- `NavigationLink` - New overload lets you specify a value that gets propogated to the parent navigation (not a view).


#### Miscellaneous

- **JSON Tip**: Build your JSON type with: https://app.quicktype.io
- **Xcode Tip**: Use control-shift click to create multiple cursors.
- Make sequences lazy to prevent allocation of temporary arrays.  `zip(pokemon.lazy.map(\.id), pokemon)`
- Be careful creating dictionary with uniqueKeysAndValues init, it will trap if that assumption is violated. Instead, use the init that specifies a collision rule. You can log an error or even throw a recoverable error if you use that version.
- Use `@MainActor` to prevent purple errors when assigning back to published properties in your view model.
- iPadOS 16 supports virtual memory on M1 iPads
- Use `for await item in asyncSequence { }` to access a stream of changing values from `.task()` modifier.
- Compiler reasons about lifetime inside `for await` so you don't have to weak capture self. (It is okay even when you put it in a Task, but can't reason about `Task.detached`)

https://github.com/joshuajhomann/PokemonNavigation
![preview](https://github.com/joshuajhomann/PokemonNavigation/raw/main/preview.gif)
---

## 2022.06.25

### Weather App Demo

Carlyn gave a demo of the new WeatherKit API. You can find her repo at:

https://github.com/carlynorama/BlueSky


### HaveNWant Demo

HaveNWant is a biologically inspired cognitive architecture by Allen King.  Walked us through a few different demos shown on his website.

http://brain-gears.blogspot.com/p/bica16-simulations.html

More recently he is implementing his Factal Workbench in SwiftUI and SceneKit.


### Algorithms and Data Structures

We discussed differences about the heap and stack.  A heap allocator is complicated because it has to worry about threads, fragmentation and performance.  Allocation is non-deterministic had needs to be avoided in hard realtime systems.

We talked very briefly about dictionaries and hashing algorithms. When there is a key collision in a hash table, usually it falls back to a linear search.  If you have a hashing algorithms with too many collisions you will end up with linear performance.  If you have a hash algorithm with no collisions, your hash table is probably too big.

Some links:

A picture is worth 1000 words:

https://github.com/girliemac/a-picture-is-worth-a-1000-words


A introductory computer science course:

- https://www.edx.org/course/introduction-computer-science-harvardx-cs50x


### Swift, SwiftUI 

Josh presented some links.

What's new in SwiftUI:
- https://mackuba.eu/swiftui/changelog
- https://bigmountainstudio.github.io/What-is-new-in-SwiftUI/

The code gets written for you:
- https://github.com/features/copilot/

Discussions caught from the WWDC SwiftUI lab:
- https://midnight-beanie-ccb.notion.site/swiftui-lounge-wwdc22-e20094b91f074398ba395c3fa245e63d


### Music written for your game

Free to use but costs a subscription if you want to own the copyright.
- www.aiva.ai


### SwiftUI Layout protocol

Josh went though an example by the objc.io guys. Here is the free presentation with more details:

https://talk.objc.io/episodes/S01E308-the-layout-protocol

```Swift
import SwiftUI

enum Layouts: String, Identifiable, CaseIterable {
    case vStack
    case hStack
    case zStack
    case grid
    case circle
    var id: Self { self }
    var layout: any Layout {
        switch self {
        case .vStack: return VStack()
        case .hStack: return HStack()
        case .zStack: return _ZStackLayout()
        case .grid: return Grid()
        case .circle: return _CircleLayout(radius: 100)
        }
    }
    func eraseToAnyLayout() -> AnyLayout {
        .init(layout)
    }
}

struct ContentView: View {

    @State private var selectedLayout = Layouts.hStack
    static let colors = [#colorLiteral(red: 0.2588235438, green: 0.7568627596, blue: 0.9686274529, alpha: 1), #colorLiteral(red: 0.8078431487, green: 0.02745098062, blue: 0.3333333433, alpha: 1), #colorLiteral(red: 0.5568627715, green: 0.3529411852, blue: 0.9686274529, alpha: 1), #colorLiteral(red: 0.9411764741, green: 0.4980392158, blue: 0.3529411852, alpha: 1), #colorLiteral(red: 0.9686274529, green: 0.78039217, blue: 0.3450980484, alpha: 1), #colorLiteral(red: 0.5843137503, green: 0.8235294223, blue: 0.4196078479, alpha: 1),].map(Color.init(nsColor:))
    var body: some View {
        VStack {
            Picker("Layout", selection: $selectedLayout) {
                ForEach(Layouts.allCases) { layout in
                    Text(layout.rawValue).tag(layout)
                }
            }.pickerStyle(.segmented)
            Spacer()
            selectedLayout.eraseToAnyLayout()() {
                ForEach(Self.colors.indices, id: \.self) { index in
                    Capsule()
                        .foregroundStyle(Self.colors[index].gradient)
                        .frame(width: 60, height: 30)
                }
            }
            Spacer()
        }
        .animation(.linear, value: selectedLayout)
        .padding()
    }
}
```
### Bust-a-move development continued

Josh covered the recursive adjacency algorithms to compute the game pieces that can be removed and the ones not connected to the top.  SwiftUI handles all of the animation for you.


### SuperHappyDevHouse: 

In person meetup if you are in the bay area:

http://superhappydevhouse.org/w/page/16345504/FrontPage

---

## 2022.06.18

### New APIs

- `UIHostingControllerSizingOptions`
- `UIHostingConfiguration`

These help with the interop story.  `UIHostingConfiguration` is for putting SwiftUI views into UICollectionView cells, etc.

- `TextField` now has a lineLimit property that takes a range.
- OSAllocatedUnfairLock A better, safer lock.

Formatting styles are not documented very well. This website helps with that:

- https://goshdarnformatstyle.com

Grab live text and qr codes, etc:

- DataScannerViewController 


### Evolution to Study

Here are a couple of proposals to learn about:

- https://github.com/apple/swift-evolution/blob/main/proposals/0352-implicit-open-existentials.md
- https://github.com/apple/swift-evolution/blob/main/proposals/0351-regex-builder.md

### Layout with Bust-a-move

Josh has a new example to implement with custom layout.  He is implementing the CirclePacked layout from bust-a-move using the API that we discussed last time.  This time he can use the cache to speed the calculations up.

Code TBD.


---

## 2022.06.11

Today was the WWDC roundup.  Apple produced a LOT of new stuff this year.  We will be spending the next many weeks covering it.  Each attendee (more than 20 this week) told us what feature that impressed them the most. 

- Watch as many of the 175 sessions that you can!
- MAKE SURE to watch  https://developer.apple.com/wwdc22/110335
- Take notes!

Speaking of notes: https://www.wwdcnotes.com/

Roundups:

### Congratulations

- Explore Apple Business Essentials - https://developer.apple.com/wwdc22/110335

- Josh Tint (Tim Colson's former student) https://www.apple.com/ma/newsroom/2022/06/apples-wwdc22-swift-student-challenge-winners-help-communities-through-coding/ 


### Combine Leak 

No direct news about the future of combine. Navigation Recipes talk mentioned `objectWillChangeSequence`. Another in the lounge overheard an Apple engineer say the future of combine is AsyncSequence.

### Career Thinking 

Anonymous postings that are useful but sometimes "toxic" so beware:

- https://www.teamblind.com/post/4-onsite-4-offers-3-FAANG-Strategy-AMA-L4SDE2-uQUPj5Sm


### Animated Radial Layout Demo

Josh showed of how easy it is to create a custom layout in SwiftUI with the `Layout` protocol.  You only need to implement two methods (though you can override more if you want fancy things like caching).  The first method is what your prefered size given subviews and the parents proposal.  The second is to position the subviews.

Josh also used some new modifiers for getting color gradients and drop shadows to make things look really good.

https://github.com/joshuajhomann/Radial


![preview](https://github.com/joshuajhomann/Radial/raw/master/preview.gif)
---

## 2022.06.04


### Get ready for WWDC

WWDC starts on Monday.  I will be watching from the developer app.  Make sure you download it.  Take notes for next week as we will be talking about it.

- https://developer.apple.com/wwdc22/beyond-wwdc/
- https://wwdc.community
- https://wwdc.community/events
- https://www.eventbrite.com/o/ios-dev-happy-hour-admins-31205108337


### Developer Setup


Some cool products to make your setup more sleek:

- https://www.twelvesouth.com/products/hoverbar-duo
- https://www.twelvesouth.com/products/bookarc-macbook
- https://www.twelvesouth.com/products/staygo-usb-c-hub


### Better code

Seven attributes of good software: simple, consistent, composable, scalable, obvious, communicative, and accommodating. Some old and new ideas mixed together in one place. --Ken Kocienda (@kocienda)

https://twitter.com/kocienda/status/1531423290316558337?cxt=HHwWgsCgwczX2sAqAAAA


"Easy to change"

https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/

### Showing images

There are some great async APIs if you are dealing with lists of images.

- https://developer.apple.com/documentation/uikit/uiimage


### Property wrappers

An interesting article about property wrappers:

https://www.swiftbysundell.com/articles/accessing-a-swift-property-wrappers-enclosing-instance/


The original property-wrapper proposal:

https://github.com/apple/swift-evolution/blob/main/proposals/0258-property-wrappers.md


### Bridging between different asynchronous programming models

- Imperative: completion handlers, callbacks, delegates, KVO, notifications, target-action, etc  
- Combine: publishers, futures
- Async/Await: AsyncSequence, Task

(aside: Think you understand Sequence? See if you can write a "prefix".)

`lazy` allows you to evalate sequences on the fly instead of materializing the entire sequence in an array.  This is useful and necessary for infinite / expensive to compute when you are only looking for the first element sequences.

Most of this weeks discussion focused around Sequence/Iterator and how similar it is to AsyncSequence/AsyncIterator looking at creating Fibonacci with `sequence(state:next:)` and `AsyncStream.init()`.  Future weeks will look at actual bridging techniques. (You can also find information in the history.)

```swift
let fib = sequence(state: (0,1)) { state -> Int? in
    let (antepenultimate, penultimate) = state
    let value = antepenultimate + penultimate
    state = (penultimate, value)
    return value
}

var iterator = fib.prefix(10).makeIterator()
while let value = iterator.next() {
    print(value)
}

var state = (0, 1)
let asyncFib = AsyncStream<Int> {
    let (antepenultimate, penultimate) = state
    let value = antepenultimate + penultimate
    state = (penultimate, value)
    try? await Task.sleep(nanoseconds: UInt64(0.25e9))
    return value
}

Task {
    var iterator = asyncFib.prefix(10).makeAsyncIterator()
    while let value = await iterator.next() {
        print(value)
    }
}

```

---

## 2022.05.28

“If you hire smart people, you can't tell them what to do more than once a year." ––Steve Jobs

### Preliminary Banter

#### VR Headsets

- https://arstechnica.com/gadgets/2022/05/the-full-saga-of-apples-troubled-mixed-reality-headset-has-been-revealed/

#### Autocompletion

Add to your .zshrc:

```sh
autoload -Uz compinit && compinit
```

It will make autocomplete for git subcommands work, for example.

The full story:

https://zsh.sourceforge.io/Doc/Release/Completion-System.html

A nice book:

https://scriptingosx.com/2019/06/moving-to-zsh/


#### Allen King's Website

https://brain-gears.blogspot.com


### Interesting Swift Links

Josh showed us a set of interesting links.


#### Transition by switching identity

https://sakunlabs.com/blog/swiftui-identity-transitions/

#### SwiftUI Series

A hackathon type event that is now over.

https://www.swiftuiseries.com/


#### Making Simple Swift Games in the Browser with WASM

https://pyrus.io/2021/05/15/gaming-with-swiftwasm.html


#### Quick Look Hero Transition made easy

https://twitter.com/JordanMorgan10/status/1526999338928439296

#### Everyone loves spirals

https://swiftpackageindex.com/buh/Spiral


#### 100 Cool SwiftUI Recipes

Catch up on all of these cool tips and tricks before WWDC 2022

https://medium.com/devtechie/100-swiftui-recipes-by-devtechie-com-26a4bea15e95


#### Hover Effect for iPad

https://medium.com/devtechie/hovereffect-in-swiftui-e756b92747d2


Works great with Universal Control

https://support.apple.com/en-us/HT212757

#### Git Worktrees

Have multiple working copies set to different branches. (John points out that Xcode might get confused.)

https://git-scm.com/docs/git-worktree

#### How Apple is Organized for Innovation

Before Steve left, he thought a lot about the roadmap that Apple should follow to maximize innovation.

https://hbr.org/2020/11/how-apple-is-organized-for-innovation


### SVG import
Josh showed the beginning of how to import SVG files from Illustrator via the paste board: https://github.com/joshuajhomann?tab=repositories

* We looked at how using `UIPasteboard` and enumerating the types in the pasteboard as well as getting the data
* We used `XMLParser` to grab the polugon tag from SVG file
* We used `Scanner` to extract the points into a `sequence` that could then be converted into a `CGPath`
<img src="https://github.com/joshuajhomann/SVGPasteBoard/blob/master/preview.png" width="640" alt="Preview">

---

## 2022.05.21

This week featured a lot of developer banter.  Here are some of the takeaways:


### iOS 16

Bill wanted to know about about iOS 16. We won't know anything concrete until WWDC in a couple weeks.

### Upgrading Legacy Code

John Brewer recommended this classic:

https://www.amazon.com/Working-Effectively-Legacy-Michael-Feathers/dp/0131177052

Daniel Young mentioned this tool that converts from Obj-C to Swift:

https://swiftify.com/converter/code/

### Debugging SwiftUI

Daniel Young mentioned that `_printChanges()` is a static method on view that dumps the things that changed causing a re-render.

```swift
:
var body: some View {
  let _ = Self._printChanges()
  :
}
:
```

### Pointer Authentication

Pointers can be cryptographically signed?  Coming soon perhaps.  John Brewer:

https://developer.apple.com/documentation/security/preparing_your_app_to_work_with_pointer_authentication

### Git Work Trees

Have multiple working copies in the same repo.

https://levelup.gitconnected.com/git-worktrees-the-best-git-feature-youve-never-heard-of-9cd21df67baf


### App Architecture

Talked about app architecture some.  One of Josh's many sample projects:

https://github.com/joshuajhomann/ImperativeCoordinator


### Evolution Proposals

We will talk more about some of them next week.  There is a nice new blog about evolution:

https://jeehut.medium.com/swift-evolution-monthly-april-22-issue-f7df19377b0b


---

## 2022.05.14

### Classifying Sounds

Rainer is working on using CoreML models for classifying. One suggestion (Ed A.) to split out different songs was to use ShazamKit:  https://wwdcbysundell.com/2021/roll-your-own-shazam-with-shazamkit/

### Searchable

Mark asked about optimizing a list view with a search text field.  The recommendation from Josh was to check out the `.searchable(text: Binding<String>)`.

### Caching

Ray presented improvements from last week to caching.  Some things discussed:

- Making generic keys
- Implementing low memory warning
- Updating the fetch method to include a closure to compute the real value
- Making errors explicit

Regarding the last point, Josh pointed out that it is probably not a good idea to cache errors.  We came up with a solution during the meeting but after the meeting I realized that it is actually better not to cache tasks if errors aren't being cached.  The final code came out like this:

```swift
import Foundation
import UIKit.UIApplication

actor LRUCache<Key: Hashable, Value> {
  let maxCount: Int
  private var values: [Key: Value] = [:]
  internal var lru: [Key] = []
  private var isMonitoringMemory = false
  
  init(maxCount: Int) {
    self.maxCount = maxCount
  }
      
  func evictAll() {
    values = [:]
    lru = []
  }
  
  func evict(key: Key) {
    values.removeValue(forKey: key)
    lru.removeAll(where: {$0 == key})
  }
  
  @discardableResult
  func fetch(key: Key,
             fallback: @escaping () async throws -> Value) async throws -> Value {
    startMonitoringMemory()
    updateLRU(for: key)
    
    // Get it and go.
    if let value = values[key] { return value }
    let value = try await fallback()
    values[key] = value
    return value
  }
  
  private func trim(count: Int) {
    if count > 0 {
      lru.reversed()[0..<count].forEach { key in
        values.removeValue(forKey: key)
      }
      lru = lru.dropLast(count)
    }
  }
  
  private func updateLRU(for key: Key) {
    lru.removeAll(where: { $0 == key})
    lru.insert(key, at: 0)
    let extra = max(lru.count - maxCount, 0)
    trim(count: extra)
  }
  
  private func lowMemoryAction() {
    evictAll()
  }
  
  private func startMonitoringMemory() {
    if !isMonitoringMemory {
      Task { @MainActor in
        NotificationCenter.default
          .addObserver(forName: UIApplication.didReceiveMemoryWarningNotification,
                       object: nil, queue: nil) { [weak self] _ in
            Task { [weak self] in
              await self?.lowMemoryAction()
            }
          }
      }
      isMonitoringMemory = true
    }
  }
}
```

Josh was wondering if memory warnings could be done in the initializer using a Combine publisher.

```swift
fileprivate let outOfMemory = NSNotification.Name(rawValue: UIApplication.didReceiveMemoryWarningNotification.rawValue)

actor LRUCache<Key: Hashable, Value> {
    let maxCount: Int
    @Published private var tasks: [Key: Task<Value?, Never>] = [:]
    @Published internal var lru: [Key] = []
    var monitoringMemory = false

    init(maxCount: Int) {
        self.maxCount = maxCount
        NotificationCenter.default.publisher(for: outOfMemory).map { _ in [:] }.assign(to: &$tasks)
        NotificationCenter.default.publisher(for: outOfMemory).map { _ in [] }.assign(to: &$lru)
    }
```

This works but he notes that you get the following warning: `This use of actor 'self' can only appear in an async initializer; this is an error in Swift 6`


### Animation in Core Animation, UIKit and SwiftUI

This presentation by Josh H. covered the ins and outs of implicit and explicit animations. As background reading, he recommends reading this: http://rensbr.eu/blog/swiftui-render-loop/

Here are some points he made with his code:

- Core Animations are implicit.
- UIView animations are implicit.
- The new SwiftUI implicit animation API specifies the property to trigger the animation off of. 
- When this specified property triggers, all implicit animations fire.  
- The inner-most animation wins.  
- Explicit animations (`withAnimation`) override implicit ones.

```swift
import UIKit

final class V: UIView {

    let shapeLayer = CAShapeLayer()

    override func didMoveToWindow() {
        super.didMoveToWindow()
        if shapeLayer.superlayer == nil {
            layer.addSublayer(shapeLayer)
        }
    }
    override func layoutSubviews() {
        super.layoutSubviews()
        let inset = bounds.insetBy(dx: 20, dy: 20)
        let center = CGPoint(x: inset.midX, y: inset.midY)
        let radius = 0.5 * min(inset.width, inset.height)
        shapeLayer.path = UIBezierPath(
            arcCenter: center,
            radius: radius,
            startAngle: 0,
            endAngle: 2 * .pi,
            clockwise: true
        ).cgPath
        shapeLayer.fillColor = UIColor.clear.cgColor
        shapeLayer.strokeColor = UIColor.red.cgColor
        shapeLayer.lineCap = .round
        shapeLayer.lineWidth = 20
        shapeLayer.strokeEnd = 0
        //backgroundColor = .clear
        Task { @MainActor in
            try? await Task.sleep(nanoseconds: UInt64(1e9))
            shapeLayer.strokeEnd = 0.75
        }
        UIView.animate(withDuration: 4, delay: 2, usingSpringWithDamping: 0.5, initialSpringVelocity: 1) {
            self.transform = .init(rotationAngle: .pi)
        }
    }
}
```

```swift
import SwiftUI
import UIKit

struct ContentView: View {
    @State private var isLeading = true
    @State private var isBlue = true
    var body: some View {
        VStack {
            VStack(alignment: isLeading ? .leading : .trailing) {
                Color.white
                Circle()
                    .foregroundColor(isBlue ? Color.blue : Color.red)
                    .frame(width: 300, height: 300)
                Color.white
            }
            HStack {
                Button("Toggle Alignment") { isLeading.toggle() }
                    .padding()
                Button("Toggle Color") { isBlue.toggle() }
                    .padding()
                Button("Toggle All") {
                    isBlue.toggle()
                    isLeading.toggle()
                }
                    .padding()
            }
        }
            .animation(Animation.linear(duration: 0.5), value: isBlue)
            .animation(Animation.linear(duration: 3), value: isLeading)
    }
}
```
## 2022.05.07

### Bridging async/await and callbacks

Peter discussed the design of a system he was building. Continuations provide a bridge between the worlds.

https://developer.apple.com/documentation/swift/3814988-withcheckedcontinuation


### Building an LRU cache

We walked through making an LRU cache example. The original design that I proposed had a way to get a value from the cache and another to update it.  After we finished the example, Josh suggested that a better API would be to provide a closure to do resource creation.  Since `Task` is effecively a future, we can make the cache hold these tasks.  That way multiple clients asking for the same resource will grab the same task rather than needlessly spawn multiple versions of the same work.  Also missing was some low memory handling.  After the meeting I (Ray) refactored the interface and cleaned up some of the shortcomings.  The solution looks like this:

```swift
//
//  LRUCache.swift
//  Practice
//
//  Created by Ray Fix on 5/7/22.
//

import Foundation
import UIKit.UIImage
typealias ImageCache = LRUCache<UUID, UIImage>

actor LRUCache<Key: Hashable, Value> {
  let maxCount: Int
  private var tasks: [Key: Task<Value?, Never>] = [:]
  internal var lru: [Key] = []
  var monitoringMemory = false
  
  init(maxCount: Int) {
    self.maxCount = maxCount
    // Memory monitoring is deferred until first point of use
    // so that we don't need an async initializer for the actor.
  }
      
  func evictAll() {
    tasks.values.forEach { $0.cancel() }
    tasks = [:]
    lru = []
  }
  
  func evict(key: Key) {
    if let task = tasks[key] { task.cancel() }
    tasks.removeValue(forKey: key)
    lru.removeAll(where: {$0 == key})
  }
  
  @discardableResult
  func fetch(key: Key,
             priority: TaskPriority? = nil,
             fallback: @escaping (Key) async -> Value?) async -> Value? {
    startMonitorMemory()
    updateLRU(for: key)
    
    // Get it and go.
    if let task = tasks[key] { return await task.value }
    // Spin up a new task, and get the value.
    let task = Task(priority: priority) { await fallback(key) }
    tasks[key] = task
    return await task.value
  }
  
  private func trim(count: Int) {
    if count > 0 {
      lru.reversed()[0..<count].forEach { key in
        tasks[key]?.cancel()
        tasks.removeValue(forKey: key)
      }
      lru = lru.dropLast(count)
    }
  }
  
  private func updateLRU(for key: Key) {
    lru.removeAll(where: { $0 == key})
    lru.insert(key, at: 0)
    let extra = max(lru.count - maxCount, 0)
    trim(count: extra)
  }
  
  private func lowMemoryAction() {
    evictAll()
  }
  
  private func startMonitorMemory() {
    if !monitoringMemory {
      Task { @MainActor in
        NotificationCenter.default
          .addObserver(forName: UIApplication.didReceiveMemoryWarningNotification,
                       object: nil, queue: nil) { [weak self] _ in
            Task { [weak self] in
              await self?.lowMemoryAction()
            }
        }
      }
      monitoringMemory = true
    }
  }
}
``` 

Some tests:

```swift
//
//  PracticeTests.swift
//  PracticeTests
//
//  Created by Ray Fix on 5/7/22.
//

import XCTest
@testable import Practice

class PracticeTests: XCTestCase {

  func testLRUCacheBasic() async throws {
    let cache = LRUCache<String, Int>(maxCount: 3)
    
    // Test getting value from the fallback
    do {
      let value = await cache.fetch(key: "magic", fallback: { _ in 42 })
      XCTAssertEqual(value, 42)
    }
    
    // Test getting value from cache
    do {
      let value = await cache.fetch(key: "magic", fallback: { _ in nil })
      XCTAssertEqual(value, 42)
    }
   
    // Test getting value from the fallback
    do {
      await cache.evict(key: "magic")
      let value = await cache.fetch(key: "magic", fallback: { _ in 16 })
      XCTAssertEqual(value, 16)
    }
    
  }
  
  func testReset() async throws {
    let cache = LRUCache<String, Int>(maxCount: 3)

    do {
      await cache.fetch(key: "magic0", fallback: { _ in 0 })
      await cache.fetch(key: "magic1", fallback: { _ in 1 })
      await cache.fetch(key: "magic2", fallback: { _ in 2 })
    }
    
    do {
      let value = await cache.fetch(key: "magic0", fallback: { _ in 16 })
      XCTAssertEqual(value, 0)
    }
    
    do {
      let value = await cache.fetch(key: "magic1", fallback: { _ in 16 })
      XCTAssertEqual(value, 1)
    }
    
    do {
      let value = await cache.fetch(key: "magic2", fallback: { _ in 16 })
      XCTAssertEqual(value, 2)
    }
    // 210
    
    
    // Insert magic4 which will evict magic0
    do {
      let value = await cache.fetch(key: "magic3", fallback: { _ in 16 })
      XCTAssertEqual(value, 16)
    }
    // 321
    
    do {
      let value = await cache.fetch(key: "magic1", fallback: { _ in 16 })
      XCTAssertEqual(value, 1)
    }
    // 132
    
    
    do {
      let value = await cache.fetch(key: "magic2", fallback: { _ in 16 })
      XCTAssertEqual(value, 2)
    }
    //213
    
    do {
      let value = await cache.fetch(key: "magic0", fallback: { _ in 16 })
      XCTAssertEqual(value, 16)
    }
    // 021
    
    do {
      let value = await cache.fetch(key: "magic3", fallback: { _ in 17 })
      XCTAssertEqual(value, 17)
    }
    // 302
    
    do {
      await cache.evict(key: "magic3")
      let value = await cache.fetch(key: "magic3", fallback: { _ in 17 })
      XCTAssertEqual(value, 17)
    }
    // 302
    
    do {
      let lru = await cache.lru
      XCTAssertEqual(lru, ["magic3", "magic0", "magic2"])
    }
    
    do {
      await cache.evict(key: "magic0")
      let lru = await cache.lru
      XCTAssertEqual(lru, ["magic3", "magic2"])
    }
  }

}
```

---

## 2022.04.30

### Server Side Solutions

Tim Condon of the Swift Server Work Group (SSWG) gave their annual update on the Swift blog https://www.swift.org/blog/sswg-update/

Of interest to the group were the different frameworks:

* Vapor (https://github.com/vapor/vapor)
* Smoke (https://github.com/amzn/smoke-framework)
* Hummingbird (https://github.com/amzn/smoke-framework)

All of these have made progress to async/await.

For the problem being asked about something as simple as a WebDAV server where you can get and put files might be enough.

### Localization in SwiftUI



We talked about how to do Swift localization.  Creating a Swift strings file (dictstring for pluralization).  The strings file can contain stuff like this:


```
// The welcome string that appears at launch.
"CONTENT_VIEW_TITLE %@" = "Hello, world! %@";
```

```
/* The welcome string that appears at launch. */
"CONTENT_VIEW_TITLE %@" = "%@ こんにちは、元気？";
```

This can be used in the code like so:

```swift
struct ContentView: View {
    var body: some View {
      let thing = "Ray"
      Text("CONTENT_VIEW_TITLE \(thing)")
    }
}
```

It is probably good to use names like CONTENT_VIEW_TITLE so it is obvious when they are wrong and just in case the same word in English maps to different translations in the target languages.


Translations can be imported and exported through the products menu .xcloc files that have an editor that translators can use.

Schemes let you change the language of the app to test.  There are special language for simulating text, having lots of diacritics, etc.


The main type is `LocalizedStringKey` which does the lookup.



---

## 2022.04.23


### Build problems

- Discussed the plight of large projects with lots of pods having build problems

Adding Build configurations: 

https://developer.apple.com/documentation/xcode/adding-a-build-configuration-file-to-your-project?changes=__6

### Thunderbolt Hubs

- You want thunderbolt ports? Be prepared to spend the money.
- Search the usual suspects, amazon, ebay, macsales, newegg, etc

### Making Diagrams

You can make diagrams using Omnigraffle from https://Omnigroup.com

### Local Swift Packages

Ray demo'ed making a local package using Josh's project from last week.  Created JoshKit and did various other experiments.  The documentation is here: https://developer.apple.com/documentation/swift_packages/

Looked at the Swift Package Index project:

https://swiftpackageindex.com

Ray will do a presentation on Tuesday for the SDiOS group.

https://www.meetup.com/sdiosdevelopers/events/284812539/

### Extensible build tools in SwiftPM

https://github.com/apple/swift-evolution/blob/main/proposals/0303-swiftpm-extensible-build-tools.md


---

## 2022.04.16

### Linting

Talked about introducing linting to a group.

- Make a separate target for linting
- Run lint only on the diffs
- RW has a style guide that uses lint for checking

https://github.com/raywenderlich/swift-style-guide/blob/main/SWIFTLINT.markdown


### New Proposals

Several new proposals are landing including many around RegEx.

Here are some links to the proposals.  Will be covering in future meetings.

- https://github.com/apple/swift-evolution/blob/main/proposals/0350-regex-type-overview.md
- https://github.com/apple/swift-evolution/blob/main/proposals/0351-regex-builder.md


### Hex Grids

Need to implement a hex grid?  You can use arrays with special offsets.

https://www.redblobgames.com/grids/hexagons/


### Match Three Continued

Josh completed his epic presentation on using SwiftUI to implement a match three style game. You can leverage the SwiftUI system to do all of the layout and animation for you. Some cool subtopics included:

- A `with` function for mutation
- User defined coordinate spaces
- Using async system to trigger animations
- Static member lookup for code clarity at the call site
- Functional board manipulations and 2d algorithms
- Types of animations (transitions vs property changes)

code: https://github.com/joshuajhomann/Bejeweled

![preview](https://github.com/joshuajhomann/Bejeweled/blob/master/preview.gif "Bejeweled")

---

## 2022.04.09

### WWDC Announced

Apple announced an all online meeting from June 6-10 along with an limited Apple Park June 6th event for developers and students.

### Transitions and Forms

Joe is working on a SwiftUI app that has a bunch of form views that want to slide back and forth. His initial version used the `AnyTransition` view to accomplish transitions. The `.move` transition only moves about halfway and using combined lets you get something that looks like a full transition.

```swift
enum MoveDirection {
  case normal
  case undo
  
  var intent: AnyTransition {
    switch self {
    case .normal:
      return AnyTransition.asymmetric(
        insertion: AnyTransition.move(edge: .trailing)
          .combined(with: .move(edge: .trailing)),
        removal: AnyTransition.move(edge: .leading)
          .combined(with: .move(edge: .leading)))
      
    case .undo:
      return AnyTransition.asymmetric(
        insertion: AnyTransition.move(edge: .leading)
          .combined(with: .move(edge: .leading)),
        removal: AnyTransition.move(edge: .trailing)
          .combined(with: .move(edge: .trailing)))
    }
  }
}
```

These transition can be used with the `.transition()` modifier.

Josh noted that SwiftUI's `TabView` can be used with a style to make something very analogous to a page controller.  We worked through the example and it looks like this:

```swift
//
//  ContentView.swift
//
//  Created by Joe Mestrovich on 3/6/22.
//

import SwiftUI

struct ContentView: View {
  @State var selectedForm = 0
  
  var body: some View {
    VStack {
      ZStack {
        Rectangle()
          .frame(maxWidth: .infinity, maxHeight: 200, alignment: .top)
        
        Text("This space intentionally left blank.")
          .fontWeight(.bold)
          .foregroundColor(.white)
      }
      
      TabView(selection: $selectedForm) {
        AnyForm(name: "A",
                next: { selectedForm = 1 },
                prev: nil ).tag(1)
        AnyForm(name: "B",
                next: { selectedForm = 2 },
                prev: { selectedForm = 0 }).tag(1)
        AnyForm(name: "C",
                next: { selectedForm = 3 },
                prev: { selectedForm = 1 }).tag(2)
        AnyForm(name: "D",
                next: nil,
                prev: { selectedForm = 2 }).tag(3)
      }
      .tabViewStyle(.page(indexDisplayMode: .never))
    }
  }
}

struct AnyForm: View {
  var name: String
  var next: (() -> Void)?
  var prev: (() -> Void)?

  var body: some View {
    ZStack {
      Rectangle()
        .cornerRadius(24)
        .padding()      
      VStack {
        Spacer()        
        Text(name)
          .font(.largeTitle)
          .fontWeight(.heavy)
          .foregroundColor(.white)        
        Spacer()        
        Button {
          withAnimation {
            next?()
          }
        } label: {
          Text("normal move")
            .fontWeight(.bold)
        }
        .disabled(next == nil)
        
        Spacer()
        
        Button {
          withAnimation {
            prev?()
          }
        } label: {
          Text("undo move")
            .fontWeight(.bold)
        }
        .disabled(prev == nil)
        Spacer()
      }
    }
  }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
```

### Match Three Game 

Josh began building a match three game that he will continue on next week. Some points that he touched on:

- View models should be @MainActor
- You can use `typealias ViewModel = GameViewModel` to make a local `var viewModel: ViewModel` in your views.
- Special care must be taken to initialize main actor view models that are declared with `@StateModel`
- Preference keys can be used to propogate layout information up the view hierarchy
- It is easy to create custom coordinate spaces that you can use with a geometry reader to compute frames with.

```swift
import SwiftUI

@MainActor
final class GameViewModel: ObservableObject {
    @Published private(set) var cells: [Cell] = []
    struct Cell: Identifiable, Hashable {
        let id: UUID = .init()
        var position: Int
        var x: Int { position % Constant.boardWidth }
        var y: Int { position / Constant.boardWidth }
        var content: Int = Constant.cellContents.indices.randomElement() ?? 0
        var isMatched = false
    }
    enum Constant {
        static let boardWidth = 8
        static let boardHeight = 8
        static var cellCount: Int { boardWidth * boardHeight }
        static let adjacentOffsets: [[(Int, Int)]] = [
            [(0, 1), (0, 0), (0, -1)],
            [(1, 0), (0, 0), (-1, 0)],
            [(-1, -1), (0, 0), (1, 1)],
            [(-1, 1), (0, 0), (1, -1)]
        ]
        static let cellContents = ["suit.spade.fill", "circlebadge.fill", "flame.fill", "tag.circle.fill", "ladybug.fill", "face.dashed.fill"]
        static let colors = [#colorLiteral(red: 0.1764705926, green: 0.4980392158, blue: 0.7568627596, alpha: 1), #colorLiteral(red: 0.8078431487, green: 0.02745098062, blue: 0.3333333433, alpha: 1), #colorLiteral(red: 0.9372549057, green: 0.3490196168, blue: 0.1921568662, alpha: 1), #colorLiteral(red: 0.8623957038, green: 0.2169953585, blue: 1, alpha: 1), #colorLiteral(red: 0.4666666687, green: 0.7647058964, blue: 0.2666666806, alpha: 1), #colorLiteral(red: 1, green: 0.8398167491, blue: 0, alpha: 1)]
    }
    init() {
        cells = Self.newBoard()
    }

    private static func newBoard() -> [Cell] {
        .init(
            (0..<Constant.cellCount).map { index in
                Cell(position: index)
            }
        )
    }
}

struct SquaresPreferenceKey: PreferenceKey {
    typealias Value = [Int: CGRect]
    static var defaultValue: Value { [:] }
    static func reduce(value: inout [Int : CGRect], nextValue: () -> [Int : CGRect]) {
        nextValue().forEach { value[$0] = $1 }
    }
}

struct ContentView: View {
    typealias ViewModel = GameViewModel
    @StateObject private var viewModel: ViewModel
    @State private var squares = SquaresPreferenceKey.defaultValue
    private enum Space: Hashable {
        case board
    }
    init(viewModel: ViewModel) {
        _viewModel = StateObject(wrappedValue: viewModel)
    }
    var body: some View {
        ZStack(alignment: .topLeading) {
            VStack(spacing: 2)  {
                ForEach(0..<GameViewModel.Constant.boardHeight, id: \.self) { y in
                    HStack(spacing: 2) {
                        ForEach(0..<GameViewModel.Constant.boardWidth, id: \.self) { x in
                            let index = x + y * GameViewModel.Constant.boardWidth
                            GeometryReader { proxy in
                                RoundedRectangle(cornerRadius: 4)
                                    .aspectRatio(1, contentMode: .fit)
                                    .preference(
                                        key: SquaresPreferenceKey.self,
                                        value: [index: proxy.frame(in: .named(Space.board))]
                                    )
                            }
                        }
                    }
                }
            }
        }
        .coordinateSpace(name: Space.board)
        .onPreferenceChange(SquaresPreferenceKey.self) { squares = $0 }
    }
}
```
---

## 2022.04.02

### Update

Bill suggests to update to 15.4.1 ASAP.

https://www.engadget.com/apples-ios-mac-os-update-patches-two-zero-day-vulnerabilities-094010389.html


### Practicing for Interviews

Don't panic, reason through the problem and pay attention to 

John Brewer recommends "Cracking the Code Interview"

- https://leetcode.com

- https://www.hackerrank.com

### Accessiblity

Lots of insights and discussion about Bluetooth and Telephony from Carlyn.

Also:

https://www.ablenetinc.com/switches/all-switches/

### Learn about Modern Collection Views

This app shows a bunch of different layouts (including table-like) layouts.

- https://developer.apple.com/documentation/uikit/views_and_controls/collection_views/implementing_modern_collection_views


### Ed Arenberg's app is in public beta

- https://testflight.apple.com/join/siw7LAin

There is a large wordset community. After getting a good dataset he wrote a bunch of quick lookup functions.

Franklin suggested using the airport community if he is looking for a wider audience.

### Tries

```swift
//
//  PrefixTree.swift
//  Boggle-SwiftUI
//
//  Created by Joshua Homann on 12/13/19.
//  Copyright © 2019 Joshua Homann. All rights reserved.
//
import Foundation

final class PrefixTree<SomeCollection: RangeReplaceableCollection> where SomeCollection.Element: Hashable  {
  typealias Element = SomeCollection.Element

  private var children: [Element: Self]
  private var isTerminal: Bool = false

  required init() {
    self.children = [:]
  }

  init(elements: [SomeCollection]) {
    self.children = [:]
    elements.forEach { self.insert($0) }
  }

  func insert(_ collection: SomeCollection) {
    let terminalNode = collection.reduce(into: self) { node, element in
      let child = node.children[element, default: Self()]
      node.children[element] = child
      node = child
    }
    terminalNode.isTerminal = true
  }

  func contains(_ collection: SomeCollection) -> Bool {
    collection.reduce(into: self, { $0 = $0?.children[$1]})?.isTerminal == true
  }

  func contains(prefix: SomeCollection) -> Bool {
    return prefix.reduce(into: self, { $0 = $0?.children[$1]}) != nil
  }
}
```

---

## 2022.03.26

### CI Servers and Security

We began today talking about CI servers and automatically publishing to test flight.  If you are in a large organization you have to be careful about sharing keys to the app store API because it could allow anyone (including former employees) to publish or remove apps from the app store.  Carl suggested that you might want to do CI as an automated process but leave app publishing up to a human who has special access to the keys.

### Group Activity Sharing

Ed gave a demo of an app he is making that uses group activity sharing.  He found out about it with this tweet:

https://mobile.twitter.com/imryanw/status/1486815964251320321


There is some documentation here:

https://developer.apple.com/documentation/groupactivities/groupactivitysharingcontroller

We talked about message passing to keep shared apps in sync.  Josh pointed out that this is a real strength of a unidirectional redux architecture where state can be be derived by an initial value and a list of every subsequent change.

### Async Sequence Library

Peter alerted us to a new Apple Swift library for Async Sequences that provides much of the Combine functionality:

https://www.swift.org/blog/swift-async-algorithms/


Josh notes that sharing a sequence (like combine does) still seems to be an issue that is not addressed.

### Build Partial Block Proposal 0348

Josh took us on a tour of a new proposal:

https://github.com/apple/swift-evolution/blob/main/proposals/0348-buildpartialblock.md

Accepting this proposal would solve the "you can only have 10 subviews in a container view" in SwiftUI problem. It could also be used for other domain specific languages (DSLs) such as RegEx or HTML or specifying neural network architectures.

This talk at WWDC21 about making DSLs with result builders:

https://developer.apple.com/videos/play/wwdc2021/10253/


The thing that I really like about Becca's talk is how she uses compiler generated messages as a todo list for adding new functionality.  Brilliant.

Josh has demo'ed making result builders in the past:

https://github.com/joshuajhomann/AttributedStringBuilder
<img src="https://github.com/joshuajhomann/AttributedStringBuilder/blob/master/preview.png?raw=true" width="140" alt="Preview">


### Result Builder Snippet

```swift
@resultBuilder
struct <#Name#>Builder {
    typealias Expression = <#Expression#>
    typealias Component = <#Component#>
    typealias FinalResult = <#FinalResult#>

    static func buildBlock(_ components: Component...) -> Component {
        buildArray(components)
    }
    static func buildExpression(_ expression: Expression) -> Component {

    }
    static func buildOptional(_ component: Component?) -> Component {
        component ?? <#empty#>
    }
    static func buildEither(first component: Component) -> Component {
        component
    }
    static func buildEither(second component: Component) -> Component {
        component
    }
    static func buildArray(_ components: [Component]) -> Component {

    }
    static func buildLimitedAvailability(_ component: Component) -> Component {
        component
    }
    static func buildFinalResult(_ component: Component) -> FinalResult {

    }
}
```

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

Several suggestions:

  - Put the work on a background task
  - Do transformation of the data model early and cache it
  - Reverse the order of the loop
  - Look into other approaches such as RegEx, computing Levenshtein distance, etc

Here is a FRP example of solving the problem.

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

   - https://okaleniuk.medium.com/premature-optimization-is-the-root-of-all-evil-is-the-root-of-evil-a8ab8056c6b


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
