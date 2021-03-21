# A Flock of Swifts 

We are a group of people excited by the Swift language. We meet each Saturday morning to share and discuss Swift-related topics. 

All people and all skill levels are welcome to join.  


---
## 2021.03.27

- **RSVP**: https://www.meetup.com/A-Flock-of-Swifts/

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
