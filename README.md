# A Flock of Swifts 

A Flock of Swifts is a physical space meeting of like-minded people excited about the Swift language.  We normally meet each Saturday morning.  Here is our meetup page.  All people and all skill levels are welcome to join.  

https://www.meetup.com/A-Flock-of-Swifts/

## 2019.12.28 [One two three four]

Swift for TensorFlow models?


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

