# A Flock of Swifts

We are a group of people excited by the Swift language. We meet each Saturday morning to share and discuss Swift-related topics. 

All people and all skill levels are welcome to join. 

## Archives

- [2020 Meetings](2020/README.md)
- [2021 Meetings](2021/README.md)
- [2022 Meetings](2022/README.md)


## 2023.01.28

- **RSVP**: https://www.meetup.com/A-Flock-of-Swifts/

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
