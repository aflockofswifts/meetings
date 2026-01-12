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
