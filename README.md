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

---

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
