# A Flock of Swifts 

A Flock of Swifts is a physical space meeting of like-minded people excited about the Swift language.  We normally meet each Saturday morning.  Here is our meetup page.  All people and all skill levels are welcome to join.  

https://www.meetup.com/A-Flock-of-Swifts/

## 2020.05.02

We met today on Zoom.  There were four presentations.

### A demonstration of scale and rotation effect anchor with `UnitPoint`
by Ray Fix

We created a simple project and explored animation modifiers.
https://gist.github.com/rayfix/6cdfcbffc9294456729d46aab8184ef8

### Charting in SwiftUI
by John James

First load in the package using the package manager:
https://github.com/AppPear/ChartView

It is very easy to add and remove packages.

Show off the code using this sample code:
https://gist.github.com/rayfix/89e6d6167e7c1881e222413e1d3cee03

### John Conway's Life in SwiftUI
https://github.com/joshuajhomann/Conway-Life-SwiftUI

### Concentration in SwiftUI
by Josh Homann

## 2020.04.25

We met on Zoom.

Talked about Dave Abrahams' apperance on the Swift by Sundell podcast.

https://www.swiftbysundell.com/podcast/71/

Start with a value type, you will discover (not invent) the protocols by exploring the problem domain.

John was running into a problem with creating fancy buttons:

https://www.appcoda.com/swiftui-button-style-animation/

Discovered the problem was that the gradient code using colors from the asset catalog not registered.  They can be registered.

Josh: Why can't Xcode auto generate code for the assets?

Presentation on Swift on the Server using Vapor

https://iosdevsurvey.com/2019/08-swift-on-the-server/

Ray will be giving a presentation on this on Monday night.

https://www.meetup.com/sdiosdevelopers/events/270119290/

Josh working on a Combine / SwiftUI version of John Conway's Life. Having trouble with timer events.

Next week we will look more at SwiftUI animation and app architecture. If you have DispatchQueue in your View code you are doing it wrong.

## 2020.04.11

We met on Zoom.

Josh presented how to make a type eraser, and when to use type erasure in SwiftUI and Combine: https://github.com/joshuajhomann/TypeErasure

Ray talked about type erasure with opaque return types using the `some` keyword.

John presented a flip animationf or his card game and we discussed various ideas for how to animate cards moving from one section of the game board to another.

## 2020.04.04

We met on Zoom.

There have been many small improvements to Swift from Swift 4 to the current 5.2.  We are noticing how many of these changes are being utilized in interesting and even unexpected ways in libraries like SwiftUI.

Ray presented a playground on `keyPaths`
* More on keypaths: https://github.com/apple/swift-evolution/blob/master/proposals/0161-key-paths.md
* The sample code that we played with: https://gist.github.com/rayfix/4ca37c321fb64fc376b100b2f6b08ef5

There are many `KeyPath` types that the compiler uses in various situations:

* `KeyPath<Root, Value>`
* `WriteableKeyPath<Root, Value>`
* `ReferenceWritableKeyPath<Root, Value>`
* `PartialKeyPath<Root>`
* `AnyKeyPath`

Josh presented a playground on `propertyWappers`, their `wrappedValues` and their `projectedValues` and then demostrated a project to show the `projectedValues` for the `propertyWrappers` in SwiftUI and Combine: https://github.com/aflockofswifts/2020-4-5-Property-Wrappers

* More on property wrappers: https://github.com/apple/swift-evolution/blob/master/proposals/0258-property-wrappers.md
* More on key apth dynamic member lookup: https://github.com/apple/swift-evolution/blob/master/proposals/0252-keypath-dynamic-member-lookup.md

John showed his card game in SwiftUI, using image slicing.  We discussed some possible solutions for animations.

## 2020.03.28

We met on Zoom due to California's current "Safer at home" restrictions.

Ray presented a measure utility to explore sizing of SwiftUI.Views.
Ray discussed new features in Swift 5.2:
  * Key Path Expressions as Functions https://github.com/apple/swift-evolution/blob/master/proposals/0249-key-path-literal-function-expressions.md
  * Callable values of user-defined nominal types https://github.com/apple/swift-evolution/blob/master/proposals/0253-callable.md
and new in Swift 5.3:
  * Enum cases as protocol witnesses https://github.com/apple/swift-evolution/blob/master/proposals/0280-enum-cases-as-protocol-witnesses.md

Josh presented debouncing expensive operations in combine with an Ascii filter example available here: https://github.com/joshuajhomann/AsciiFilter

Jo fixed her launch image by purging the similator & fixed an opacity animation.  Note that that requirement to use a storybaord for your launch screen has been delayed: https://developer.apple.com/news/

## 2020.03.07

We met at Daden LLC where Ray gave a presentation on layout in SwiftUI and how to communicate information up the View tree by using `PreferenceKey`.

We broke into groups and tried to apply `PreferenceKey` to the problem of making a grid where you can select a number of squares by dragging.

Josh's solution to this problem is here: https://github.com/joshuajhomann/Preferences

A similar problem solved without preferences by manually calcaluating everything is here: https://github.com/joshuajhomann/Boggle-SwiftUI

## 2020.02.15

Josh is working on AWS amplify: https://aws-amplify.github.io/docs/ios/start?ref=amplify-iOS-btn

Decoding JSON from firebase dictionaries:
```
protocol JSONRepresentable {
  init?(json: [String: Any])
  func json() -> [String: Any]?
}

extension JSONRepresentable where Self: Codable {
  init?(json: [String:Any]) {
    guard let value = (try? JSONSerialization.data(withJSONObject: json, options: []))
      .flatMap ({ try? JSONDecoder().decode(Self.self, from: $0) }) else {
        return nil
    }
    self = value
  }
  func json() -> [String:Any]? {
    return (try? JSONEncoder().encode(self))
      .flatMap { try? JSONSerialization.jsonObject(with: $0, options: []) } as? [String: Any]

  }
}


struct User: Codable, JSONRepresentable {
  var name: String
}

let dictionary: [[String: Any]] = [
  ["name" : "John"],
  ["name" : "Bill"],
  ["invalid": "test"]
]

let users = dictionary.compactMap(User.init(json:))
print(users)
```

## 2020.02.08
* Josh made 2D water in spriteKit: https://github.com/joshuajhomann/Waves
* John worked on bar charts in SwiftUI

## 2020.02.01
* We met at Daden LLC for some presentations
* Ray covered github & swift package manger https://gitup.co
* Josh covered SwiftUIAnimations: https://github.com/joshuajhomann/SwiftUI-Animations

## 2020.01.25

* John is exploring swift package manager: https://swift.org/package-manager/
* Josh worked on displaying a chain of CFilters in a MTKView: https://github.com/joshuajhomann/Core-Image-Metal-View
* Feathering: https://stackoverflow.com/questions/40593884/how-to-achieve-real-feather-fade-effect-on-a-uiimage-which-is-cropped-by-a-uibez/40667463#40667463

## 2020.01.18

Coding challenges for all levels if anyone is interested in trying: https://www.reddit.com/r/dailyprogrammer/

The deadline is fast approaching.  Update your apps with a launch storyboard and support for arbitrary screen sizes.
```As announced at WWDC19, starting April 2020, apps submitted to the App Store must use an Xcode storyboard to provide the app’s launch screen and must have an interface that supports any display size.```
https://developer.apple.com/news/?id=01132020b

CIFilter example:
```
import PlaygroundSupport
import UIKit

let ciImage = Bundle.main.url(forResource: "dog", withExtension: "jpg")
  .flatMap { try! Data(contentsOf:$0) }
  .flatMap(UIImage.init(data:))?
  .cgImage
  .flatMap(CIImage.init(cgImage:))!

let blur = CIFilter(name: "CIGaussianBlur")
blur?.setValue(ciImage, forKey: kCIInputImageKey)
blur?.setValue(16, forKey: "inputRadius")
let uncroppedImage = (blur?.value(forKey: kCIOutputImageKey) as? CIImage)
  .flatMap(UIImage.init(ciImage:))!
let croppedImage = UIGraphicsImageRenderer(size: ciImage!.extent.size).image { _ in
  uncroppedImage.draw(at: .init(
    x: (ciImage!.extent.size.width - uncroppedImage.size.width) / 2,
    y: (ciImage!.extent.size.height - uncroppedImage.size.height) / 2
  ))
}
```


## 2020.01.11

John working on button customization using a view modifier.  I suggested creating a `ButtonModifier` because you can get at the button.

```swift
struct RectangularButtonStyle: ButtonStyle {

  func makeBody(configuration: Configuration) -> some View {
    configuration.label.frame(width: 150, height: 50)
      .background(Color.blue)
      .foregroundColor(.white)
      .font(.subheadline)
      .cornerRadius(10)
    
  } 
}

// Use it like this:

Button("Press Me!") {
  print("Hello")
}.buttonStyle(RectangularButtonStyle())

```


Josh and Ray working on SwiftUI navigation.

Some background links:

### Basic SwiftUI Navigation
https://www.raywenderlich.com/5824937-swiftui-tutorial-navigation

### Deep Linking (Uses AppState to control navigation)
https://nalexn.github.io/swiftui-deep-linking/
This uses `AppState` to figure out how views set themselves up.

### Combine Tutorial Navigation
https://www.raywenderlich.com/4161005-mvvm-with-combine-tutorial-for-ios
Combine tutorial which contains some info on "pragmatic navigation" using a view builder function.

### Starter Project from Josh
This uses the TVMaze API that creates a simple navigation.
https://github.com/joshuajhomann/TVMaze-SwiftUI-Navigation

Adding a coordinator turns out to be a little less straightforward than originally thought.


### Looking for a Job

Some ideas in no particular order.

- Hired
- Vettery
- TrippleByte
- Karat
- Mainz Brady Group
- StackOverflow
- Zip Recruiter
- AngelList

Project a professional appearance online.

## 2020.01.04 

- Simon Simon worked on SwiftUI navigation.  We hit a bug where you can't push a view after it has been dismissed.  This is really weird.

```swift
struct DetailView: View {

    @Environment(\.presentationMode) var presentation

    var body: some View {
        Button("Done") {
            self.presentation.wrappedValue.dismiss()
        }
    }
}

struct ContentView: View {
    var body: some View {
        NavigationView {
            NavigationLink(destination: DetailView()) {
                Text("Hello")
            }
        }
    }
}
```

Any ideas?

--EDIT: Josh--

John and I worked on the same issue a few weeks ago.  The solution is to use a binding for the navigationLink.  If you think about it its wierd to be manipulating the global presentation state since whether or not a view is presented is a piece of local state that someone should own (in this case that someone is the parent).

```swift
struct DetailView: View {
  @Binding var isShown: Bool
  var body: some View {
    Button("done") {
      self.isShown = false
    }
  }
}

struct ContentView: View {
  @State private var isDetailShown = false
  var body: some View {
    NavigationView {
      NavigationLink("hello", destination: DetailView(isShown: $isDetailShown), isActive: $isDetailShown)
    }
  }
}
```
--END EDIT--

Ray:  Actually this also does not work. If you go back using the back button, you can no longer push onto the navigation stack.  (At least in the 13.3 sim).  Ray Posted feedback to Apple FB7522002


- Victoria worked on SpriteKit and attempted to commit her code with Gitup.  She understands the importance of version control but isn't a fan of the current product offerings.  

https://gitup.co

- Other topics included working with Firebase (cascading multiple requests)


## 2019.12.21 [A Geeky Swiftmas Party]

Making Ornaments, snacks, drinks (moldly drinks!), iPad Pictionary, a presentation, discussion. 

Five Swift things to be excited about in 2020.

- SwiftUI and Combine
- Swift on the Server
- Swift for Machine Learning (TensorFlow)
- The vibrant Swift community
- Our community

Brainstorm ideas for 2020.

- Analyze buoy data in relation to tsunamis
- Build a game for Apple Arcade (or find out what it takes)
- Build a self driving car (Use Swift for TensorFlow)
- Build a Draw and Guess Game

### Links:
- https://www.donkeycar.com
- https://www.robolink.com/codrone/


## 2019.12.14 [New Beginnings]

- Discussion  of Markov Chains, Markov Chain Monte Carlo (MCMC)

- Ray starting aflockofswifts github organization.  See me (ray) IRL if you want to join the organization.  

- Josh and John are working on a SwiftUI version of Boggle.  https://github.com/joshuajhomann/Boggle-SwiftUI

- John and Josh used `UITextChecker` to validate the dictionary which contained 250k invalid words.  Seems to be slow, it takes 5 minutes to process the 300k dictionary.  Cleaned up dictionary opens fast in iOS but crashes in catalyst (???)

- Xcode 11.3 seems to have trouble opening a large json array. Hangs. (Reported to Apple as FB7493904)

- Bill wants to know how to use hash tags in his instagram profile (Not Swift related but hey...)

- Simon is working of SwiftUI layout with video player.  Also used `Bundle.main` to fetch a local video rather than streaming from the web.

- Victoria is going through a SpriteKit tutorial  

- Swiftforgood.com Book is on pre-order.

### Some Code

`PrefixTree` is a trie that provides fast lookup in the English dictionary for a valid word.  Here is the key method:

```swift
     func contains(_ collection: SomeCollection) -> Bool {
        collection.reduce(into: self, { $0 = $0?.children[$1]})?.isTerminal == true
     }
```

### Required init issue

A short coming in the current version of Swift is that even if you have a `final class` if you reference and init a `Self` you *MUST* have a `required` initializer.  It seems like it should not be `required` if the class is `final`.

#### Screenshot of Boogle App

![Boogle Screen shot](resources/boggle_screenshot.png)

