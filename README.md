# A Flock of Swifts 

We are a group of people excited by the Swift language. We meet each Saturday morning to share and discuss Swift-related topics. 

All people and all skill levels are welcome to join.  

---
### 2021.02.27
- **RSVP**: https://www.meetup.com/A-Flock-of-Swifts/

---

### 2021.02.20

#### Discussion

This is a good system to produce animations made by designers.
https://github.com/airbnb/lottie-ios

#### What are some good SwiftUI starter resources?

- https://www.raywenderlich.com
- Stanford course https://cs193p.sites.stanford.edu
- The landmarks tutorial from Apple https://developer.apple.com/tutorials/swiftui/
- Paul Hudson's 100 days of Swift / SwiftUI 
- A new tutorial from Apple https://developer.apple.com/tutorials/app-dev-training
- Newsletter by Matteo Manferdini https://matteomanferdini.com
- Another list of resources: http://bit.ly/get-started-with-swift

#### Debug session: problem with gestures in a collection view

We did a group debug of Clarissa's code. The tap selector for the tap selector wasn't being called.  Josh spoted the problem: the gesture was being added to the cell's root view instead of the `contentView`.  Remember that table view cells and collection view cells have a `contentView` that you need to add your custom views and gestures to.

#### Problem with Collection Views in iOS 14.4

Jumping to a particular cell seems to be broken. Mira provided a discussion link:

https://developer.apple.com/forums/thread/663156?answerId=642133022#642133022

#### How do you make an app that uses landscape but only in one view

One way is to make a class derived from UIViewController that is a NonRotatingView and overrides supported orientations.  All the views
that don't rotate derive from that.

https://developer.apple.com/documentation/uikit/uiviewcontroller/1621435-supportedinterfaceorientations

#### How do you make an enable button and a slider

https://gist.github.com/rayfix/11827eaf8acae38a08b2190c0db72cee

We used `onAppear` and `onChange` to sync state and a binding.

We hit a disable styling problem.  Jo mentioned this:

https://stackoverflow.com/questions/64756306/using-a-toggle-to-disable-a-slider-in-swiftui-results-in-styling-problems


---
### 2021.02.13

#### Tricks and tips

John shared Xcode tips from [24 Quick Xcode Tipes article by Paul Hudson](https://www.hackingwithswift.com/articles/229/24-quick-xcode-tips)

Notable shortcuts:
  - **Command-option-control g**  - Run the last unit test.
  - **Command-option /**  - Automatic doc comment template.
  - **Command-control-shift A**  - Author's view (git blame) 

#### M1 Rumors 

Bill is interested in M1 rumors, especially this one about a [Mac Mini _Pro version_ in space grey](https://www.macworld.co.uk/news/mac-trends-2021-3800044/#toc-3800044-4)!

#### SwiftUI Composition

Tim Colson presented strategies for SwiftUI Composition, i.e. breaking views down into components. SwiftUI composition exercises were inspired by strategies from articles/code/videos by Joseph Pacheco and Paul Hudson. 

The code-along session style was inspired by Tim's year teaching and David Laing's [Grand Unified Theory of Documentation (Divio)](documentation.divio.com) which itself decomposes documentation into four types. Intent was a hands-on learning oriented tutorial, applying composition techniques to a task reminders view. (Unfortunately, Zoom sharing + Xcode + (2 x 4K monitors) crippled Tim's 2015 MBP 13" i7/16GB. He needs an M1x MBP 14"! 

See Tim's GitHub repo has for links and sample code:
https://github.com/timcolson/tut-swiftui-comp -- start with tag v1  `git co tags/v1`

If interested in working thru the code together, reach out to Tim. 

#### Breakout rooms

We will try this next week.

---


### 2021.02.06

#### Xcode Tricks and Tips

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

#### Other tricks:

* [Emacs keybindings](https://caiorss.github.io/Emacs-Elisp-Programming/Keybindings.html)
* [Custom Code Snippets in Xcode](https://medium.com/@hassanahmedkhan/writing-custom-code-snippets-in-xcode-9e91f8ed4207)

#### xcconfig

Frank introduced us to the world of xcconfig files. You can specify these files to use in your build.  They handle comments, key values such as:

MY_SETTING = "this is debug mode"

- You can cut and past from the build configuration of Xcode.
- It understands include files to support common settings.
- You can use `include?` for optional includes used for local configuration not checked into version control.

* [Xcode Build Configuration Files article by Mattt @ NSHipster](https://nshipster.com/xcconfig/) - reference article with info similar to what Frank shared 

#### SHA256

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

#### URL Publishing Chain Revisited

By request, Josh walked us step-by-step thru the Combine URL publishing chain in his [TeslaOwnerAPI.swift](https://github.com/joshuajhomann/tesla/blob/main/TeslaOwnerAPI/Sources/TeslaOwnerAPI/TeslaOwnerAPI.swift)

---

### 2021.01.30
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

### 2021.01.23

#### Proxy 

Discussed network security and _SSL pinning_. Potential topic for future meetup.  You can try it out:

https://www.charlesproxy.com

https://proxyman.io

#### Swift Fiddle

It let's you play with the Swift compiler (and different versions) online.

https://swiftfiddle.com

#### Enums

We talked about how equality checking for enums do not consider argument labels.  The same thing goes for comparison and hash values coming in a future
version of Swift when [tuples will become Equatable, Comparable and Hashable[(https://github.com/apple/swift-evolution/blob/main/proposals/0283-tuples-are-equatable-comparable-hashable.md) if all of the element types are Equatable, Comparable and Hashable respectively.


Regarding comparison of floating point, question about zero was raised.  IEEE-754 specifies a sign bit so there are multiple representations of zero.

https://developer.apple.com/documentation/swift/double/1538731-iszero

#### Your Demo Here

If you have a trick or tip and want to show the group, remember to write it down.

https://www.dunebook.com/best-xcode-themes/ - 
https://github.com/tonsky/FiraCode - font for terminal and Xcode that includes ligatures for common two-char symbols
[How to draw bounding boxes with SwiftUI (Medium)](https://medium.com/swlh/how-to-draw-bounding-boxes-with-swiftui-d93d1414eb00) - useful for scanning-related project ideas, ex: draw a box around a QR code in a video capture. 

#### Demo SwiftUI Picker

We explored Picker with a simple example. 

https://gist.github.com/rayfix/ed02927bce0d645911b578edf5379baf

#### Names in the app store

Needs to be a real name or company name (LLC, Corporation, etc).  Apple doesn't allow DBAs.

https://developer.apple.com/support/enrollment/

#### Demo Exquisite Corpse

Got a quick demo of a game that Jo is building. And talked about debugging Firebase cloud functions.  It is taking minutes to spin up an instance and something seems wrong.

---

### 2021.01.18

#### Discussion of Corporate Dev Account vs Personal Account

Be careful of LLC (with a single person) or even a corporation. If you don't do everything to the letter, chances are the corporate veil can be pierced.  When you are just starting out, it is probably easiest to use a personal account.  While there was agreement that it can be changed later there was some disagreement about how hard it is to do.

#### Emil's TikTok App Tutorial Recommendation
https://www.youtube.com/watch?v=71-l3Ndf6Ug

#### iCloud sync

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

#### Refactoring to Combine

Emily gave us a presentation on Caleb and her experience refactoring to Combine.

- The code is nicer than nested callbacks.
- Discussion on weak captures to prevent extension of lifetime (capture self, or just capture exactly what is needed in the callback closure).
- How can the number of error states be reduced?

Josh reminded us of a previous project that abstracts loading state and error / empty response handling.

https://github.com/joshuajhomann/ShimmeringLoadingState

Josh also recommends a single access point for doing requests.  Link TBD. (Next week?)


#### Proposal for Visualization Toolkit

The idea is to have a library to allow you to read in a CSV file and then render as a plot.

Can we make something comparable to D3 https://d3js.org

#### Tesla Watch App: Modules

Josh showed an in-progress watch app that uses the Tesla API to unlock the car. We will look at it in greater detail in a future meetup.

This week he showed how to factor out watch and iOS code into a common Swift Package Manager module.


---

### 2021.01.09
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

### 2021.01.02

Happy New Year!

Josh created an animated SwiftUI `RingChart` view that he plans to integrate into the **Tides** app.  

https://github.com/joshuajhomann/RingChart

![RingChart](resources/ringchart.gif)

## Archives

- [2020 Meetings](2020/README.md)
