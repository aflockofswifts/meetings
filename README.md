# A Flock of Swifts

We are a group of people excited by the Swift language. We meet each Saturday morning to share and discuss Swift-related topics. 

All people and all skill levels are welcome to join. 

## Archives

- [2020 Meetings](2020/README.md)
- [2021 Meetings](2021/README.md)
- [2022 Meetings](2022/README.md)

## 2023.01.15

- **RSVP**: https://www.meetup.com/A-Flock-of-Swifts/

---

## 2023.01.14

### PointFree Dependency Injection

A new library for dependency injection was announced this week by the folks at pointfree.co.  Josh gave us a quick tour of the library and an additions library:

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
