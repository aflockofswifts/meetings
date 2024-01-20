# A Flock of Swifts
![Flock](materials/flock.jpg)
We are a group of people excited by the Swift language. We meet each Saturday morning to share and discuss Swift-related topics. 

All people and all skill levels are welcome to join. **RSVP**: https://www.meetup.com/A-Flock-of-Swifts/

## Archives

- [2020 Meetings](2020/README.md)
- [2021 Meetings](2021/README.md)
- [2022 Meetings](2022/README.md)
- [2023 Meetings](2023/README.md)

---

## Notes

## 2024.01.20

### Presentation: Plugin Explorer

Carlyn presented findings about how to implement plugin commands.

The repo for the PluginExplorer is found here:

https://github.com/carlynorama/PluginExplorer

WWDC references:

- https://developer.apple.com/wwdc22/110359
- https://developer.apple.com/wwdc22/110401

Swift Package Manager:

- https://github.com/apple/swift-package-manager/

The Original Pitch and Proposal:

- https://forums.swift.org/t/pitch-package-manager-command-plugins/53172

- https://github.com/apple/swift-evolution/blob/main/proposals/0332-swiftpm-command-plugins.md

Other resources:

- https://www.youtube.com/watch?v=1GcU70xZ-P8

### Questions and Discusssion


#### Apple Vision Pro Pre-orders

The process was a little bumpy but it sounded like everyone that wanted to get one was able to. It seems like the backlog now is only about a month.

#### Device Disposal

Apple has special equipment to disassemble devices so the materials can be properly recycled.

https://www.apple.com/environment/

#### Perception and Observation:

Josh showed us a new framework from pointfree.co that backports Observable by taking inspiration from the Swift open source library which uses system private interfaces (aka `_spi(SwiftUI)`) to implement observation. 

https://www.pointfree.co/blog/posts/129-perception-a-back-port-of-observable


Josh also gave us a link to an article that goes into depth about Observation:

- https://fatbobman.com/en/posts/mastering-observation/


## 2024.01.13

### Questions and Discusssion

#### VisonOS
Paul Hudson is running a [VisionOS course](https://ti.to/hacking-with-swift/unwrap-live-2024).  
Apple's [VisonOS news release](https://developer.apple.com/news/?id=8fppguuh).  

#### OS Log
We discussed OSLog and how to use the console app using this [example](https://github.com/joshuajhomann/Logging).   
![preview](https://github.com/joshuajhomann/Logging/raw/master/preview.png). 

#### MVVM
We discussed MVVM using this [example](https://github.com/joshuajhomann/Magic-Browser-SwiftUI).  
![MVVM](materials/MVVM.png)

---

## 2024.01.06

### Feature Presentation: VisionOS

Josh continued his VisionOS example from last year building a 3D style shooting game were you can knock down blocks by firing balls from a cannon. Some of the topics discussed included:

- Taking in game controller events
- Mapping these events to transforms that move the cannon
- Creating new entities with initial velocity and physics
- Dynamic and static entities. Dynamic entities were the blocks and the balls. The floor was static entity.
- Composing new components into the system. The example was to control the lifetime of fired balls so they disappear after a few seconds.

[Code](https://github.com/joshuajhomann/Cannon)
![Preview](https://github.com/joshuajhomann/Cannon/blob/main/preview.gif)

### Questions and Discusssion

#### Logging

Bob D looking into logging code from previous meetings and updating the SwiftUI navigation to the latest version (NavigationStack).

Some of the videos he found useful:

- WWDC 23 Video on Structured Logging https://developer.apple.com/wwdc23/10226
- Stewart Lynch video on Logging https://www.youtube.com/watch?v=Zi6JRczGoME

Ray mentioned testing logging using a DI framework.

- https://github.com/tgrapperon/swift-dependencies-additions/blob/main/Sources/LoggerDependency/Logger.swift

Josh mentioned that with recent improvements to OSLog even without dependency injection or mocking you can write out the log to an array and check it in a test if you are interested in.


#### Buying a New Mac

Be careful of using old machines that are connected to the Internet that aren't getting security updates.  Go to Apple Silicon if possible but recent Intel machines are still viable for a few more years. The important thing is getting security updates.

Some places to look from deals:

- https://www.apple.com/shop/refurbished/mac
- https://smalldog.com/


For those missing the touch pad, consider stream deck.

- https://www.elgato.com/us/en/s/welcome-to-stream-deck

#### Swift Package Preview

The Swift blog showcases some interesting packages.

- 	https://www.swift.org/packages/showcase.html

One that we took note of was a macro system to cut down on initializer boilerplate.  1000 line code reductions in real projects.

- https://swiftpackageindex.com/gohanlon/swift-memberwise-init-macro


#### Dimissing Windows in VisionOS

The key is doing this through the environment:

```swift
@Environment(\.dismissWindow) private var dismissWindow
```

Ed was having trouble doing this probably because he was calling it at the wrong time.

John B gave us a quick working example:

```swift
.onChange(of: showImmersiveSpace) { _, newValue in
    Task {
        if newValue {
            switch await openImmersiveSpace(id: "ImmersiveSpace") {
            case .opened:
                immersiveSpaceIsShown = true
                dismissWindow(id: "MainWindow")
            case .error, .userCancelled:
                fallthrough
            @unknown default:
                immersiveSpaceIsShown = false
                showImmersiveSpace = false
            }
        } else if immersiveSpaceIsShown {
            await dismissImmersiveSpace()
            immersiveSpaceIsShown = false
        }
    }
}
```

For completeness, this is how he shows the window though he notes that it should be factored out from the collision handler where it currently lives.  Hopefully, Ed can use this working example to get his own project working.

```swift
collisionSubscription = content.subscribe(to: CollisionEvents.Began.self) { [self]
    event in
    if event.entityA == lander {
        handleCollision()
        DispatchQueue.main.asyncAfter(deadline: DispatchTime.now() + 5) {
            Task {
                await dismissImmersiveSpace()
                openWindow(id: "MainWindow")
            }
        }
    }
}
```

---
