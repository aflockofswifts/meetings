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

---

## Notes
## 2024.06.01

### Making a quartiles generator:
![image](materials/quartiles.png)
```swift
import SwiftUI

@Observable
@MainActor
final class WordViewModel: ObservableObject {
    var searchTerm: String = "" {
        didSet { update() }
    }
    private(set) var words: [Word] = []
    private(set) var selectedWords: [Word] = []
    private(set) var solutions: [Word] = []
    private var allWords: [Word] = []
    private var fourSyllableWords: [Word] = []
    func load() async {
        async let makeWords = Word.makeFromFewestSyllables()
        allWords = await makeWords
        async let makeFourSyllableWords = {
            await allWords.filter { $0.syllables.count == 4 }
        }()
        fourSyllableWords = await makeFourSyllableWords
        await updateWords()
    }
    func select(_ word: Word) {
        selectedWords.append(word)
        update()
    }
    func delete(at offsets: IndexSet) {
        selectedWords.remove(atOffsets: offsets)
        update()
    }
    private func update() {
        Task { await updateWords() }
    }
    private func updateWords() async {
        let term = searchTerm
            .trimmingCharacters(in: .whitespacesAndNewlines)
            .folding(options: [.caseInsensitive, .diacriticInsensitive], locale: nil)
        let usedSyllables = selectedWords.reduce(into: Set<String>()) { accumulated, word in
            word.syllables.forEach { accumulated.insert($0) }
        }
        async let availableWords = {
            let fourSyllableWordsWithUnusedSyllables = await self.fourSyllableWords.filter {
                $0.syllables.intersection(usedSyllables).isEmpty
            }
            return fourSyllableWordsWithUnusedSyllables
        }()
        let fourSyllableWordsWithUnusedSyllables = await availableWords
        if term.isEmpty {
            words = fourSyllableWordsWithUnusedSyllables
        } else {
            async let filteredWords = {
                fourSyllableWordsWithUnusedSyllables.filter { $0.description.hasPrefix(term) }
            }()
            words = await filteredWords
        }
        async let makeSolutions = {
            let allWords = await self.allWords
            return allWords.filter { $0.syllables.isSubset(of: usedSyllables) && $0.syllables.count > 1}
        }()
        solutions = await makeSolutions
    }
}

@MainActor
struct ContentView: View {
    var viewModel = WordViewModel()
    var body: some View {
        NavigationSplitView(columnVisibility: .constant(.all)) {
            NavigationStack {
                @Bindable var vm = viewModel
                List(viewModel.words) { word in
                    HStack {
                        Text(word.description)
                        Text(word.syllableDescription).foregroundStyle(.secondary)
                    }
                    .contentShape(Rectangle())
                    .onTapGesture { viewModel.select(word) }
                }
                .navigationTitle("Available Words")
                .searchable(text: $vm.searchTerm)
            }
        } content: {
            List {
                ForEach(viewModel.selectedWords) { word in
                    HStack {
                        Text(word.description)
                        Text(word.syllableDescription).foregroundStyle(.secondary)
                    }
                }
                .onDelete(perform: viewModel.delete(at:))
            }
            .navigationTitle("Selected Words")
        } detail: {
            List(viewModel.solutions) { word in
                HStack {
                    Text(word.description)
                    Text(word.syllableDescription).foregroundStyle(.secondary)
                }
            }
            .navigationTitle("Solutions")
        }
        .task { await viewModel.load() }
    }
}

import OSLog

let signposter = OSSignposter(subsystem: "com.josh.quartilesolver", category: "signposts")

struct Word: CustomStringConvertible, Identifiable, Hashable, Sendable {
    var id: String { description }
    var description: String
    var syllableDescription: String
    var syllables: Set<String>
}

extension Word {
    static func makeFromFewestSyllables() -> [Word] {
        func stringsFromFile(name: String) -> [String] {
            Bundle.main.url(forResource: name, withExtension: "json")
                .flatMap { try? Data(contentsOf: $0) }
                .flatMap { try? JSONDecoder().decode([String].self, from: $0) } ?? []
        }
        let words = stringsFromFile(name: "words")
        let syllables = Set(stringsFromFile(name: "syllables"))
        let longest = syllables.lazy.map(\.count).max()
        let start = Date()
        let wordSignpostID = signposter.makeSignpostID()
        let signpostWordState = signposter.beginInterval("Words", id: wordSignpostID)
        let validWords = words.reduce(into: [Word]()) { validWords, candidate in
            var suffix = candidate
            var foundSyllables: [String] = []
            while !suffix.isEmpty {
                let found = stride(from: min(5, candidate.count), to: 0, by: -1)
                    .lazy
                    .compactMap { window in
                        let prefixCandidate = String(suffix.prefix(window))
                        return syllables.contains(prefixCandidate) ? prefixCandidate : nil
                    }
                    .first
                guard let found else { return }
                foundSyllables.append(found)
                suffix = String(suffix.dropFirst(found.count))
                let foundSyllablesSet = Set(foundSyllables)
                if suffix.isEmpty, foundSyllablesSet.count == foundSyllables.count {
                    validWords.append(.init(description: candidate, syllableDescription: foundSyllables.joined(separator: "•"), syllables: foundSyllablesSet))
                }
            }
        }
        signposter.endInterval("Words", signpostWordState)
        return validWords
    }
}
```
## 2024.05.25

### Dates and Times
* We discussed using Calendar to determine when a given date is the same day as another date: 
https://developer.apple.com/documentation/foundation/nscalendar/1417649-isdate 
https://yourcalendricalfallacyis.com 
https://vimeo.com/865876497 

### Modernizing code
We took a look at modernizing this project: https://github.com/joshuajhomann/AsciiFilter
![image](https://github.com/joshuajhomann/AsciiFilter/blob/master/preview.gif)

## 2024.05.18

### Accessibility
https://developer.apple.com/documentation/accessibility/performing-accessibility-audits-for-your-app  
https://nfb.org/programs-services/center-excellence-nonvisual-access/blind-users-innovating-and-leading-design  
https://a11y-guidelines.orange.com/en/mobile/ios/wwdc/nota11y/2023/2310035/  

Swift replica of the [Manim](https://docs.manim.community/en/stable/reference/manim.animation.transform_matching_parts.TransformMatchingShapes.html) transform matching parts animation.  

[Core Text Programming Guide](https://developer.apple.com/library/archive/documentation/StringsTextFonts/Conceptual/CoreText_Programming/Introduction/Introduction.html)  
[iOS Text](https://developer.apple.com/library/archive/documentation/StringsTextFonts/Conceptual/TextAndWebiPhoneOS/Introduction/Introduction.html) 

![Flock](materials/anagram.gif)

```swift
import SwiftUI
import simd

@Observable
final class AnagramViewModel {
    let sourcePathsAndRects: [(CGPath, CGRect)]
    let destinationPathAndRects: [(CGPath, CGRect)]
    var sourceWidth: CGFloat {
        sourcePathsAndRects.last?.1.maxX ?? .zero
    }
    let source = "I am Lord Voldemort"
    let destination = "Tom Marvolo Riddle"
    let sourceIndexToDestinationIndex: [Int : Int]
    let lineHeight: Double
    init() {
        let normalizedSource = source.folding(options: [.caseInsensitive, .diacriticInsensitive], locale: nil).replacingOccurrences(of: " ", with: "")
        let normalizedDestination = destination
            .folding(options: [.caseInsensitive, .diacriticInsensitive], locale: nil).replacingOccurrences(of: " ", with: "")
        var destinationIndices = normalizedDestination.enumerated().reversed().reduce(into: [Character: [Int]]()) { accumulated, next in
            accumulated[next.element, default: []].append(next.offset)
        }
        sourceIndexToDestinationIndex = normalizedSource.enumerated().reduce(into: [Int: Int]()) { accumulated, next in
            let target = destinationIndices[next.element]?.popLast()
            accumulated[next.offset] = target
        }
        let font = UIFont.preferredFont(forTextStyle: .largeTitle)
        lineHeight = font.lineHeight
        sourcePathsAndRects = source.glyphs(applying: font)
        destinationPathAndRects = destination.glyphs(applying: font)
    }
}

struct ContentView: View {
    @State private var t = 0.0
    @State var viewModel = AnagramViewModel()
    var body: some View {
        Slider(value: $t)
        TimelineView(.animation) { context in
            let curve = UnitCurve.easeInOut
            let t = curve.value(at: abs(fmod(context.date.timeIntervalSince1970, 4) / 2 - 1))
            Canvas {
                context,
                size in
                context.transform = .init(scaleX: 1, y: -1)
                    .translatedBy(x: size.width/2, y: -size.height/2)
                let xOffset = viewModel.sourceWidth / 2
                for (index, (path, rect)) in viewModel.sourcePathsAndRects.enumerated() {
                    let (destinationPath, destinationRect) = viewModel.sourceIndexToDestinationIndex[index].map { index in
                        viewModel.destinationPathAndRects[index]
                    } ?? (nil, nil)
                    var point: SIMD2<Double>
                    if let destinationRect {
                        let height = (rect.minX - destinationRect.minX) / 2.5
                        let curve = CubicBezierCurve(
                            start: .init(rect.minX, rect.minY),
                            control1: .init(rect.minX, rect.minY + height),
                            control2: .init(destinationRect.minX, destinationRect.minY  + height),
                            end: .init(destinationRect.minX, destinationRect.minY)
                        )
                        point = curve(t)
                    } else {
                        point = .init(rect.minX, rect.minY)
                    }
                    point.x -= xOffset
                    var pathContext = context
                    pathContext.transform = pathContext.transform
                        .translatedBy(x: point.x, y: point.y)
                    pathContext.stroke(Path(path), with: .color(Color.red.opacity(1-t)))
                    guard let destinationPath else { continue }
                    var destinationPathContext = context
                    destinationPathContext.transform = destinationPathContext.transform
                        .translatedBy(x: point.x, y: point.y)
                    destinationPathContext.fill(Path(destinationPath), with: .color(Color.black.opacity(t)))
                }
            }
            Canvas { context, size in
                context.transform = .init(scaleX: 1, y: -1)
                    .translatedBy(x: size.width/2, y: -size.height/2)
                let xOffset = viewModel.sourceWidth / 2
                for (index, (path, rect)) in viewModel.sourcePathsAndRects.enumerated() {
                    let (destinationPath, destinationRect) = viewModel.sourceIndexToDestinationIndex[index].map { index in
                        viewModel.destinationPathAndRects[index]
                    } ?? (nil, nil)
                    let rectMin = (destinationRect.map { destinationRect in
                        simd_mix(rect.minX, destinationRect.minX, t)
                    } ?? rect.minX) - xOffset

                    var pathContext = context
                    pathContext.transform = pathContext.transform
                        .translatedBy(x: rectMin, y: 0)
                    pathContext.fill(Path(path), with: .color(Color.black.opacity(1 - t)))
                    guard let destinationPath else { return }
                    var desintationPathContext = context
                    desintationPathContext.transform = desintationPathContext.transform
                        .translatedBy(x: rectMin, y: 0)
                    desintationPathContext.fill(Path(destinationPath), with: .color(Color.black.opacity(t)))
                }
            }
        }
        Canvas { context, size in
            context.transform = .init(scaleX: 1, y: -1)
                .translatedBy(x: size.width/2, y: -size.height/2)
            let xOffset = viewModel.sourceWidth / 2
            for (path, rect) in viewModel.sourcePathsAndRects {
                var pathContext = context
                pathContext.transform = pathContext.transform
                    .translatedBy(x: rect.minX - xOffset, y: 0)
                pathContext.fill(Path(path), with: .color(Color.black))
                var squareContext = context
                squareContext.transform = squareContext.transform
                    .translatedBy(x: -xOffset, y: 0)
                squareContext.stroke(Path(roundedRect: rect, cornerSize: .zero), with: .color(Color.red))
            }
        }
    }
}

extension String {
    func glyphs(applying font: UIFont) -> [(CGPath, CGRect)] {
        let attributedString = NSAttributedString(string: self, attributes: [.font: font])
        let line = CTLineCreateWithAttributedString(attributedString)
        return (CTLineGetGlyphRuns(line) as? [CTRun]).map { runs in
            runs.flatMap { run in
                let count = CTRunGetGlyphCount(run)
                var advances = [CGSize](repeating: .zero, count: count)
                CTRunGetAdvances(run, CFRangeMake(0, count), &advances)
                var transform = CGAffineTransform.identity
                let paths = [CGGlyph](unsafeUninitializedCapacity: count) { buffer, allocatedCount in
                    CTRunGetGlyphs(run, CFRange(), buffer.baseAddress!)
                    allocatedCount = count
                }.lazy.map { glyph in
                    CTFontCreatePathForGlyph(font as CTFont, glyph, &transform)
                }
                return zip(
                    paths,
                    advances.map(\.width).scanMap(initial: 0.0) { x, width in
                        defer { x += width }
                        return CGRect(x: x, y:font.descender + font.leading, width: width, height: font.lineHeight)
                    }
                )
                .compactMap { paths, rect in paths.map { ($0, rect) } }
            }
        } ?? []
    }
}

extension Sequence {
    func scanMap<State, Transformed>(
        initial: consuming State,
        transform: @escaping (inout State, Element) -> Transformed
    ) -> some Sequence<Transformed> {
        sequence(state: (accumulated: initial, iterator: self.makeIterator())) { state in
            state.iterator.next().map { element in
                transform(&state.accumulated, element)
            }
        }
    }
}

struct QuadraticBezierCurve {
    typealias Point = SIMD2<Double>
    typealias Vector = SIMD3<Double>
    typealias Matrix = matrix_double3x3
    private let x: Vector
    private let y: Vector
    static let matrix = Matrix([
        .init(1, -2,  1),
        .init(0,  2, -2),
        .init(0,  0,  1)
    ])
    init(start: Point, control: Point, end: Point) {
        x = Vector(start.x, control.x, end.x)
        y = Vector(start.y, control.y, end.y)
    }
    init(start: CGPoint, control: CGPoint, end: CGPoint) {
        x = Vector(start.x, control.x, end.x)
        y = Vector(start.y, control.y, end.y)
    }
    func callAsFunction(_ t: Double) -> Point {
        let powerSeries = Vector(1, t, t*t)
        let scaleVector = powerSeries * Self.matrix
        let xProduct = scaleVector * x
        let yProduct = scaleVector * y
        return Point(xProduct.sum(), yProduct.sum())
    }
    func cgPoint(at t: Double) -> CGPoint {
        let point = self(t)
        return .init(x: point.x, y: point.y)
    }
}

struct CubicBezierCurve {
    typealias Point = SIMD2<Double>
    typealias Vector = SIMD4<Double>
    typealias Matrix = matrix_double4x4
    private let x: Vector
    private let y: Vector
    static let matrix = Matrix([
        .init(1, -3,  3, -1),
        .init(0,  3, -6,  3),
        .init(0,  0,  3, -3),
        .init(0,  0,  0,  1)
    ])
    init(start: Point, control1: Point, control2: Point, end: Point) {
        x = Vector(start.x, control1.x, control2.x, end.x)
        y = Vector(start.y, control1.y, control2.y, end.y)
    }
    init(start: CGPoint, control1: CGPoint, control2: CGPoint, end: CGPoint) {
        x = Vector(start.x, control1.x, control2.x, end.x)
        y = Vector(start.y, control1.y, control2.y, end.y)
    }
    func callAsFunction(_ t: Double) -> Point {
        let powerSeries = Vector(1, t, t*t, t*t*t)
        let scaleVector = powerSeries * Self.matrix
        let xProduct = scaleVector * x
        let yProduct = scaleVector * y
        return Point(xProduct.sum(), yProduct.sum())
    }
    func cgPoint(at t: Double) -> CGPoint {
        let point = self(t)
        return .init(x: point.x, y: point.y)
    }
}
```


## 2024.05.11

We looked at the transform matching parts animation in [Manim](https://docs.manim.community/en/stable/reference/manim.animation.transform_matching_parts.TransformMatchingShapes.html)  
We started recreating this by making a Bezier Curve.  First a [quadratic](https://www.desmos.com/calculator/mbgwndpeeh):
```swift
struct QuadraticBezierCurve {
    typealias Point = SIMD2<Double>
    typealias Vector = SIMD3<Double>
    typealias Matrix = matrix_double3x3
    private let x: Vector
    private let y: Vector
    static let matrix = Matrix(rows: [
        .init(1, -2,  1),
        .init(0,  2, -2),
        .init(0,  0,  1)
    ])
    init(start: Point, control: Point, end: Point) {
        x = Vector(start.x, control.x, end.x)
        y = Vector(start.y, control.y, end.y)
    }
    init(start: CGPoint, control: CGPoint, end: CGPoint) {
        x = Vector(start.x, control.x, end.x)
        y = Vector(start.y, control.y, end.y)
    }
    func callAsFunction(_ t: Double) -> Point {
        let powerSeries = Vector(1, t, t*t)
        let scaleVector = Self.matrix * powerSeries
        let xProduct = scaleVector * x
        let yProduct = scaleVector * y
        return Point(xProduct.sum(), yProduct.sum())
    }
    func cgPoint(at t: Double) -> CGPoint {
        let point = self(t)
        return .init(x: point.x, y: point.y)
    }
}
```

and then a [Cubic](https://www.desmos.com/calculator/ebdtbxgbq0):
```swift
struct CubicBezierCurve {
    typealias Point = SIMD2<Double>
    typealias Vector = SIMD4<Double>
    typealias Matrix = matrix_double4x4
    private let x: Vector
    private let y: Vector
    static let matrix = Matrix([
        .init(1, -3,  3, -1),
        .init(0,  3, -6,  3),
        .init(0,  0,  3, -3),
        .init(0,  0,  0,  1)
    ])
    init(start: Point, control1: Point, control2: Point, end: Point) {
        x = Vector(start.x, control1.x, control2.x, end.x)
        y = Vector(start.y, control1.y, control2.y, end.y)
    }
    init(start: CGPoint, control1: CGPoint, control2: CGPoint, end: CGPoint) {
        x = Vector(start.x, control1.x, control2.x, end.x)
        y = Vector(start.y, control1.y, control2.y, end.y)
    }
    func callAsFunction(_ t: Double) -> Point {
        let powerSeries = Vector(1, t, t*t, t*t*t)
        let scaleVector =  powerSeries * Self.matrix
        let xProduct = scaleVector * x
        let yProduct = scaleVector * y
        return Point(xProduct.sum(), yProduct.sum())
    }
    func cgPoint(at t: Double) -> CGPoint {
        let point = self(t)
        return .init(x: point.x, y: point.y)
    }
}
```

then demonstrating that we can trace the same path as SwiftUI and use that path to drive an animation position:
```swift
struct ContentView: View {
    var body: some View {
        GeometryReader { proxy in
            let size = proxy.size
            let points: [CGPoint] = [
                .init(x: 0, y: size.height),
                .init(x: 0, y: size.height * 0.33),
                .init(x: size.width, y: size.height * 0.33),
                .init(x: size.width, y: size.height),
            ]
            let cubic = CubicBezierCurve(start: points[0], control1: points[1], control2: points[2], end: points[3])
            Canvas { context, size in
                let path = Path { path in
                    path.move(to: points[0])
                    path.addCurve(to: points[3], control1: points[1], control2: points[2])
                }
                context.stroke(path, with: .foreground, style: .init(lineWidth: 2))
                stride(from: 0.0, through: 1.0, by: 0.1).forEach { t in
                    let center = cubic.cgPoint(at: t)
                    context.fill(Path { path in
                        path.addArc(center: center, radius: 10, startAngle: .zero, endAngle: .radians(.pi * 2), clockwise: true)
                    }, with: .color(.red))
                }
            }
            TimelineView(.animation) { timeline in
                Canvas { context, size in
                    let t = fmod(timeline.date.timeIntervalSince(.distantPast), 5) / 5
                    let center = cubic.cgPoint(at: t)
                    context.fill(Path { path in
                        path.addArc(center: center, radius: 10, startAngle: .zero, endAngle: .radians(.pi * 2), clockwise: true)
                    }, with: .color(.green))
                }
            }
        }
    }
}
```
![Flock](materials/bezier.gif)

[Matrix form of a quadratic bezier](https://blog.demofox.org/2016/03/05/matrix-form-of-bezier-curves/)  
[Matrix form of a cubic bezier](https://pomax.github.io/bezierinfo/#matrix)
## 2024.05.04

### Topics Discussed

- Dependency injection how and why.  
Monty asked about making his dates and times testable:
```swift
import Foundation

protocol SystemServiceProtocol {
    var now: Date { get }
}

final class SystemService: SystemServiceProtocol {
    var now: Date {
        .now
    }
}

final class MockSystemService: SystemServiceProtocol {
    var now: Date = .distantPast
}
```
We also discussed remote configuration and making a debug menu and debugService

- Swift Evolution: Synchronous Mutex Exclusion Lock

    - https://github.com/apple/swift-evolution/blob/main/proposals/0433-mutex.md
Mark asked about making the lock checkable.  We discussed adding a wrapper to to this:
```swift
@dynamicMemberLookup
struct Flagged<Wrapped> {
    var isLocked: Bool
    var wrapped: Wrapped
    subscript<Value>(dynamicMember dynamicMember: WritableKeyPath<Self, Value>) -> Value {
        self[dynamicMember: dynamicMember]
    }
}
```

- Solving coding challenges with idiomatic Swift
    - https://leetcode.com/discuss/general-discussion/460599/blind-75-leetcode-questions
    - https://github.com/apple/swift-collections
    - https://github.com/apple/swift-algorithms

```swift
func two(sum target: Int, from values: [Int]) -> (Int, Int)? {
    let lookup = values.enumerated().reduce(into: [Int: [Int]]()) { accumulated, next in
        accumulated[next.element, default: []].append(next.element)
    }
    return values.print().enumerated().lazy.compactMap { (index, value) -> (Int, Int)? in
        guard let other = lookup[target - value], let otherIndex = other.last, otherIndex != index else { return nil }
        return (index, otherIndex)
    }
    .first
}
```

Peter asked about a print for Sequence mirroring Combine's print operator.  We looked at the general form:
```swift
extension Sequence {
    func sideEffect(_ effect: (Element) -> Void) -> some Sequence<Element> {
        map { value in
            effect(value)
            return value
        }
    }
}
```
and the specific solution:
```swift
extension Sequence where Element: CustomStringConvertible {
    func print() -> some Sequence<Element> {
        sideEffect { Swift.print(String(describing: $0)) }
    }
}
```

Carlyn shared two free computer science courses:
  - https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/
  - https://www.cs.cornell.edu/courses/cs6120/2020fa/self-guided/
---

## 2024.04.27

### Questions and Discussion

#### LLDB Debugging

You can use the LLDB prompt in Xcode that comes up when you hit a breakpoint in the console window.

- https://stackoverflow.com/questions/19748866/how-to-print-the-contents-of-a-memory-address-using-lldb

As an example:

```
memory read -s1 -fu -c10000 0xb0987654 --force
```

- https://lldb.llvm.org/use/tutorial.html


LLDB Basics in 11 Minutes

- https://www.youtube.com/watch?v=v_C1cvo1biI


#### Computers

Some shows about how computers are awesome

-   https://www.pbs.org/show/crash-course-computer-science/
- https://www.bbc.co.uk/programmes/p00kjq6d/episodes/guide


#### Swift 6 

In this SPI podcast, Holly Borla notes that the transition to Swift 6 shouldn't be as bad as many people are fearing.

- https://swiftpackageindexing.transistor.fm/episodes/43-now-i-m-worried-our-metrics-aren-t-correct-with-special-guest-holly-borla


#### Glow Shine Effect

- https://uvolchyk.medium.com/making-things-glow-and-shine-with-swiftui-80448c560f88

#### AI

A ton of research materials from Georgi with regard many advanced attribution topics (including Revtrival Augmented Generation [RAG]):

- https://arxiv.org/abs/2404.07143
- https://arxiv.org/pdf/2211.00593
- https://arxiv.org/pdf/2403.13187
- https://huggingface.co/blog/mlabonne/merge-models

- Understanding GPT https://www.youtube.com/watch?v=wjZofJX0v4M

Ed noting that Apple released some on-device models.

- Ed on Microsoft's VASA-1 https://www.microsoft.com/en-us/research/project/vasa-1/

---

## 2024.04.20

### Presentation: Swift Package Manager

Carlyn showed us a new command line tool she is working on for managing her many Swift Packages.

```
  - https://github.com/carlynorama/TemplatePackageToolLibrary
```

### Presentation: Maps and SwiftUI

Frank showed us how to implement a map today in SwiftUI. His implementation let us put down points of interest with a long tap in pure SwiftUI.

```swift
import SwiftUI
import MapKit
  
struct POI: Identifiable {
  let id = UUID().uuidString
  var location: CLLocationCoordinate2D
      
  init(coordinate: CLLocationCoordinate2D) {
    location = coordinate
  }
      
  init(latitude: CLLocationDegrees, longitude: CLLocationDegrees) {
    location = .init(latitude: latitude, longitude: longitude)
  }
}

struct ContentView: View {
  @State private var points: [POI] = [
          .init(latitude: 48.85, longitude: 2.33),
          .init(latitude: 48.87, longitude: 2.38)
      ]
      
  var body: some View {
      MapReader { mapProxy in
          Map {
            ForEach(points) { point in
                Marker(coordinate: point.location) {
                    Image(systemName: "globe")
                }
            }
          }.onLongPressGestureWithLocation { point in
            if let coordinate = mapProxy.convert(point, from: .local) {
                  points.append(.init(coordinate: coordinate))
            }
        }
    }
  }
}

struct LongPressGestureWithLocation: ViewModifier {
  private var perform: (CGPoint) -> Void
  @State private var location: CGPoint?
      
  init(perform: @escaping (CGPoint) -> Void) {
    self.perform = perform
  }
      
  @ViewBuilder
  func body(content: Content) -> some View {
    content
      .gesture(DragGesture(minimumDistance: 0)
      .onChanged { value in
          location = value.location
      }
      .simultaneously(with: LongPressGesture()
      .onEnded { done in
          if done, let location {
            perform(location)
          }
        })
      )
    }
  }
  
extension View {
  func onLongPressGestureWithLocation(perform: @escaping (CGPoint) -> Void) -> some View {
    modifier(LongPressGestureWithLocation(perform: perform))
  }
}
```

Related resources:

- https://developer.apple.com/documentation/mapkit/mapreader
- https://developer.apple.com/documentation/swiftui/coordinatespace

We came to the consensus that you need UIKit to implement full gesture capabilities:

- https://developer.apple.com/documentation/uikit/uigesturerecognizer

### Presentation: SwiftUI Layout

Josh continued to review the details of SwiftUI layout. Most of the code was presented in the previous week with special attention this week put on `fixedSize`.

Related resource:

- https://www.neilmacy.co.uk/blog/swiftui-button-equal-sizing


### Discussion and Questions

#### Swift for C++ Practitioners

- https://www.douggregor.net

---

## 2024.04.13

### Presentation: SwiftUI Layout

Josh showed the details of how SwiftUI layout works
by creating a custom layout that inspects the calls
of the layout system. 

Also see:

- https://developer.apple.com/documentation/swiftui/layoutvaluekey

#### Fixing up Geometry Reader

As a bonus side-topic, Josh showed how to "fix" how layout of a geometry reader works.

```swift
var body some View {
  let _ = Self._printChanges()
  GeometryReader { geometry in
    VStack {
      Image (systemName: "globe")
        .imageScale(.large)
      Text ("Hello, world!")
        .padding()
    }
    .frame(
        width: geometry.size.width, 
        height: geometry.size.height, 
        alignment: .center)
    }
}
```

Here is the code for the inspector:


```swift
struct InspectorLayout: Layout {
    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        let size = subviews.first?.sizeThatFits(proposal) ?? .zero
        print(
        """
        \(subviews.first?[LayoutNameKey.self] ?? ""):
        Received proposal: width \(proposal.width.proposalDescription) height: \(proposal.height.proposalDescription)
        Returning \(size)
        """
        )
        return size
    }

    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        subviews.forEach {
            print("placing \(subviews.first?[LayoutNameKey.self] ?? ""): width: \(proposal.width.proposalDescription) height: \(proposal.height.proposalDescription)")
            $0.place(at: .init(x: bounds.midX, y: bounds.midY), anchor: .center, proposal: proposal)
        }
    }
}


private struct LayoutNameKey: LayoutValueKey {
    static let defaultValue = "[unnamed view]"
}

extension View {
    func inspectLayout(name: some CustomStringConvertible) -> some View {
        InspectorLayout() {
            layoutValue(key: LayoutNameKey.self, value: String(describing: name))
        }
    }
}

private extension Optional where Wrapped == CGFloat {
    var proposalDescription: String {
        map {
            switch $0 {
            case .infinity: "max"
            case .zero: "min"
            default: "custom \(self!)"
            }
        } ?? "ideal"
    }
}
```
#### Format

Bonus topic about how to format numbers.

https://goshdarnformatstyle.com


#### Swift Talk Reimplements SwiftUI

- https://talk.objc.io/collections/swiftui-layout-explained

### Questions and Discussion

#### One More Thing

A new AltWWDC/Alt-Conf/Layers Inspired Conference happening WWDC week.

- https://omt-conf.com

#### Scheduling Background Work

Mark asking about how to schedule background work.

- https://developer.apple.com/documentation/swiftui/scene/backgroundtask(_:action:)


#### Assembly Language

Carlyn posting three links on assembly:

* https://www.youtube.com/watch?v=in-UY_EyI14&list=PL2EF13wm-hWAlQe87UB2HV0SVhBXFpXbn
  
* https://cpulator.01xz.net
  
* Assembly Language & Computer Architecture from MIT 6.172 Performance Engineering of Software Systems, Fall 2018 https://www.youtube.com/watch?v=L1ung0wil9Y

Also,

- https://www.youtube.com/watch?v=in-UY_EyI14&list=PL2EF13wm-hWAlQe87UB2HV0SVhBXFpXbn


#### Async From a Low Level

- https://www.youtube.com/watch?v=H_K-us4-K7s

## 2024.04.06

### Presentation: Ordering Async Work

Josh showed us an outline for a solution to order async work. It uses an actor to organize (and protect) a list of prioritized sendable closures that it can execute using a discardable task group. It uses the `Heap` structure from Swift Collection to establish the work order and an async stream to feed in and process work.

- https://github.com/apple/swift-collections/blob/main/Documentation/Heap.md

```swift
import Foundation
import HeapModule

actor AsyncPriorityWorkQueue<Priority: Comparable & Sendable, Output> {
    private let maxConcurrentElements: Int
    private let postWorkNotification: AsyncStream<Void>.Continuation
    private var concurrentItems = 0
    private var subscriptions = Subscriptions()
    private var priorityQueue = Heap<Work>()
    init(of output: Output.Type, priorityOfType: Priority.Type = Int.self, maxConcurrentElements: Int) {
        self.maxConcurrentElements = maxConcurrentElements
        let (workNotifications, postWorkNotification) = AsyncStream.makeStream(of: Void.self, bufferingPolicy: .unbounded)
        self.postWorkNotification = postWorkNotification
        subscriptions += Task {
            await withDiscardingTaskGroup { [weak self] group in
                for await _ in workNotifications {
                    while let work = await self?.dequeueWork() {
                        group.addTask {
                            await work.operation()
                            postWorkNotification.yield()
                        }
                    }
                }
            }
        }
    }
    private func dequeueWork() -> Work? {
        concurrentItems < maxConcurrentElements
            ? priorityQueue.popMax()
            : nil
    }
    private func enqueue(priority: Priority, operation: @escaping @Sendable () async -> Void) {
        priorityQueue.insert(.init(priority: priority, operation: operation))
        postWorkNotification.yield()
    }
    func perform(priority: Priority, operation: @escaping @Sendable () async throws -> Output) async throws -> Output {
        try await withCheckedThrowingContinuation { [weak self] continuation in
            Task { [weak self] in
                await self?.enqueue(priority: priority) {
                    continuation.resume(with: await Result {
                        async let value = operation()
                        return try await value
                    })
                }
            }
        }
    }
}

extension AsyncPriorityWorkQueue {
    struct Work: Comparable, Sendable  {
        let id = UUID()
        var priority: Priority
        var operation: @Sendable () async -> Void
        static func < (lhs: Self, rhs: Self) -> Bool { lhs.priority < rhs.priority }
        static func == (lhs: Self, rhs: Self) -> Bool { lhs.id == rhs.id }
    }
}

extension Result where Failure == Error {
    init(_ operation: () async throws -> Success) async {
        do { self = .success(try await operation()) } catch { self = .failure(error) }
    }
}

final class Subscriptions {
    private var cancellations: [() -> Void] = []
    deinit { cancellations.forEach { $0() } }
    static func += <Value, Failure>(lhs: Subscriptions, rhs: Task<Value, Failure>) { lhs.cancellations.append(rhs.cancel) }
}
```
### Discussions and Questions

#### Conferences

Upcoming conferences in Europe.

- https://swiftconnection.io
- https://2023.nsspain.com
- https://www.iosdevuk.com

Frank L. (just back from try! Swift Tokyo) notes:

Tickets are not on sale for NSSpain yet, but the dates are known. September 18-20th. Swift Connection is September 23-24, and there's Server-Side Swift in London on September 26-27.

#### Privacy Manifest

Peter was noting problems showing up on the app store complaining about privacy manifest files. The consensus seemed to be that there was an error in one of the third party packages being used.

- https://developer.apple.com/support/third-party-SDK-requirements/
- https://developer.apple.com/documentation/bundleresources/privacy_manifest_files

#### Inlinable vs inline(\_\_always) vs \_transparent

- https://github.com/apple/swift/blob/main/docs/ReferenceGuides/UnderscoredAttributes.md


#### Breaking out of nested loops

- https://www.hackingwithswift.com/example-code/language/how-to-break-out-of-multiple-loop-levels-using-labeled-statements

In the end, the code didn't need the label.


#### Testing Framework

Might be an interesting topic for future discussion.

- https://github.com/apple/swift-testing

#### ~Copyable

This is an interesting beast. Carlyn notes:

- https://github.com/apple/swift-evolution/blob/main/proposals/0427-noncopyable-generics.md

```
                 any ~Copyable
                 /         \
                /           \
     Any == any Copyable   <all purely noncopyable types>
          |
  <all copyable types>
```

---

## 2024.03.30

### Presentation: ViewModel as a Function

Josh presented how to write a view model as a single function. Writing code in this style enhances local reasoning and testability. Thinking of the logic in this way (even if you use a different framework) can help influence how you write code in a positive way.

```swift

import Combine
import UIKit

import PlaygroundSupport

typealias Input = (
    increaseFirst: AnyPublisher<Void, Never>,
    increaseSecond: AnyPublisher<Void, Never>
)
typealias Output = (
    firstValue: AnyPublisher<String, Never>,
    secondValue: AnyPublisher<String, Never>,
    total: AnyPublisher<String, Never>
)
typealias AddViewModel = (Input) -> Output

final class AddViewController: UIViewController {
    private var subscriptions: Set<AnyCancellable> = []
    init(viewModel: AddViewModel) {
        super.init(nibName: nil, bundle: nil)
        let firstInputSubject = PassthroughSubject<Void, Never>()
        let secondInputSubject = PassthroughSubject<Void, Never>()
        let outputs = viewModel((
            increaseFirst: firstInputSubject.eraseToAnyPublisher(),
            increaseSecond: secondInputSubject.eraseToAnyPublisher()
        ))
        with(UIStackView(arrangedSubviews: [
            UIButton(type: .roundedRect, primaryAction: .init(title: "Increase First") { _ in firstInputSubject.send() }),
            UIButton(type: .roundedRect, primaryAction: .init(title: "Increase Second") { _ in secondInputSubject.send() }),
            with(UILabel()) { label in
                outputs.firstValue.sink { [label] value in label.text = value }.store(in: &subscriptions)
            },
            with(UILabel()) { label in
                 outputs.secondValue.sink { [label] value in label.text = value }.store(in: &subscriptions)
            },
            with(UILabel()) { label in
                outputs.total.sink { [label] value in label.text = value }.store(in: &subscriptions)
            }
        ])) { stack in
            stack.translatesAutoresizingMaskIntoConstraints = false
            stack.axis = .vertical
            stack.alignment = .leading
            view.addSubview(stack)
            NSLayoutConstraint.activate([
                view.centerXAnchor.constraint(equalTo: stack.centerXAnchor),
                view.centerYAnchor.constraint(equalTo: stack.centerYAnchor)
            ])
        }
    }
    @available(*, unavailable)
    required init?(coder: NSCoder) { fatalError("")}
}


func addViewModel(_ input: Input)-> Output {
    let firstValue = input.increaseFirst.map { _ in 1 }.scan(0, +).prepend(0)
    let secondValue = input.increaseSecond.map { _ in 1 }.scan(0, +).prepend(0)
    return (
        firstValue: firstValue.map(String.init(describing:)).eraseToAnyPublisher(),
        secondValue: secondValue.map(String.init(describing:)).eraseToAnyPublisher(),
        total: Publishers.CombineLatest(firstValue, secondValue)
            .map(+)
            .map(String.init(describing:))
            .eraseToAnyPublisher()
    )
}

PlaygroundPage.current.setLiveView(AddViewController(viewModel: addViewModel))

```

To code efficiently in this style, you'll need to build some infrastructure (e.g. `with` and `bind`) or bring it into your code with a Swift Package.

### Presentation: Date Parsing

Carlyn presented about dates and scanning text which she has written extensively about during the last week!

- https://www.whynotestflight.com/excuses/date-parsing.-nose-wrinkle./

- https://www.whynotestflight.com/excuses/wait-how-do-i-scan-text-again/

Some other resources that were mentioned:

Formatting in general:

- https://goshdarnformatstyle.com

Dave Delong on points in space and time:

- https://vimeo.com/865876497

### Questions and Discussion

### Apple Vision Pro Conference

Ed was speaking to us live from an Apple Vision Pro hackathon. He had some questions about Multipeer connectivity and 3D.

- https://github.com/carlynorama/SketchPad

### SwiftData

Monty is learning how to use SwiftData and had some questions about making relationships. I debugging, Josh suggested making his view @MainActor and changing one of his optional arrays to be just an empty array.

Resource:

- https://www.hackingwithswift.com/quick-start/swiftdata/how-to-create-one-to-many-relationships


### SwiftIO Embedded Playground

Ray mentioned that he bought a SwiftIO kit.

https://madmachine.io

---

## 2024.03.23

### Presentation: Actor reentrancy

We looked at the issue of actor reentrancy which is discussed at length in the original Actor proposal: https://github.com/apple/swift-evolution/blob/main/proposals/0306-actors.md#actor-reentrancy

We did this by creating the original code example and then running as a unit test repeatedly.

Once we got to a failing state we implemented a Swift concurrency friendly Semaphore based on the open source library: https://github.com/groue/Semaphore/blob/main/Sources/Semaphore/AsyncSemaphore.swift 

Then we changed the test code so that it generated deadlocks. The complete example:

```swift
import XCTest

enum Judgement {
  case noIdea, goodIdea, badIdea
}

typealias Decision = Judgement


public final class AsyncSemaphore: @unchecked Sendable {
  
  private var count: Int
  
  init(count: Int) {
    precondition(count >= 0)
    self.count = count
  }
  
  private let _lock = NSRecursiveLock()
  private func lock() {
    _lock.lock()
  }
  private func unlock() {
    _lock.unlock()
  }
  private class Suspension: @unchecked Sendable {
    enum State {
      case suspended(CheckedContinuation<Void, Never>)
    }
    var state: State
    init(state: State) {
      self.state = state
    }
  }
  private var suspensions: [Suspension] = []
  
  deinit {
    precondition(suspensions.isEmpty)
  }
  
  public func wait() async {
    lock()
    count -= 1
    if count >= 0 {
      unlock()
      return
    }
    await withCheckedContinuation { continuation in
      let s = Suspension(state: .suspended(continuation))
      suspensions.insert(s, at: 0)
      unlock()
    }
  }
  
  @discardableResult
  public func signal() -> Bool {
    lock()
    count += 1
    switch suspensions.popLast()?.state {
    case .suspended(let continuation):
      unlock()
      continuation.resume()
      return true
    default:
      unlock()
      return false
    }
  }
}

actor Person {
  var friend: Person?
  var opinion: Decision = .noIdea
  let semaphore = AsyncSemaphore(count: 1)
  
  func tell(_ opinion: Judgement, heldBy person: Person) async {
    
    if .random() {
      if opinion == .goodIdea {
        _ = await person.thinkOfABadIdea()
      } else {
        _ = await person.thinkOfAGoodIdea()
      }
    }
    
  }
  
  init(friend: Person? = nil, opinion: Decision) {
    self.friend = friend
    self.opinion = opinion
  }
  
  func thinkOfAGoodIdea() async -> Decision {
    await semaphore.wait()    
    defer {
      semaphore.signal()
    }
    opinion = .goodIdea
    await friend?.tell(opinion, heldBy: self)
    return opinion
  }
  
  func thinkOfABadIdea() async -> Decision {
    await semaphore.wait()
    defer {
      semaphore.signal()
    }
    opinion = .badIdea
    await friend?.tell(opinion, heldBy: self)
    return opinion
  }
}

final class Reent2Tests: XCTestCase {
  func testRace() async {
    let friend = Person(friend: nil, opinion: .noIdea)
    let person = Person(friend: friend, opinion: .noIdea)

    // deadlock!

    let a = await person.thinkOfAGoodIdea()
    XCTAssertEqual(Judgement.goodIdea, a)
      
    let idea = await person.thinkOfABadIdea()
    XCTAssertEqual(Judgement.badIdea, idea)
  }

}
```

A followup would be to see how to find the deadlock introduced with the locks in this way.

### Questions and Discussion

#### Interfacing to C and C++

Ed is working on protein folding visualization for Apple Vision Pro and wants to interface with some existing libraries that load pdb files. Carlyn gave him some advice about that:

https://www.whynotestflight.com/excuses/but-some-of-my-best-friends-are-c/

Also, these two repos:

- https://github.com/carlynorama/UnsafeExplorer/tree/471f563afe223e41c0a29e4dc5e4253508fa46ce

- https://github.com/carlynorama/UnsafeWrapCSampler

Another particular is working with fixed size C arrays that come back as tuples:

- https://github.com/carlynorama/FixedSizeCollection/blob/main/Sources/FixedSizeCollection/TupleLove.swift

Another treat was learning about Monty other endeavors.

- https://montyharper.com/track/2216372/what-is-the-shape-of-the-molecule


#### App Architecture

Allen had a question about how to take his App model object and use it with SwiftUI.

We talked about the new Observable macro and how you can use it to target older versions of iOS.

https://www.pointfree.co/blog/posts/129-perception-a-back-port-of-observable

#### Vision Dev Camp

Coming up next week. Ed and John will both be there.

- https://www.eventbrite.com/e/visiondevcamp-tickets-849184312137


#### Date and Time

There was a lot of chat discussion about date and time.

- https://www.donnywals.com/formatting-dates-in-swift-using-date-formatstyle-on-ios-15/

- https://swiftpackageindex.com/davedelong/time/1.0.1/documentation/time

- https://developer.apple.com/documentation/foundation/date/iso8601formatstyle

#### Fixing SwiftData Initialization Error

Monty was having trouble with his SwiftData app.

The hypothesis is that he needed to add a config. i.e.

```swift
let schema = Schema([
                Item.self,
            ])
            let modelConfiguration = ModelConfiguration(schema: schema, isStoredInMemoryOnly: false)
```

---

## 2024.03.16

### Presentation: Custom Encoders

Carlyn took us on a guided tour of writing a custom encoder.

- https://www.whynotestflight.com/excuses/how-do-custom-encoders-work/
- https://www.whynotestflight.com/excuses/and-what-can-i-make-a-custom-encoder-do/

Frank also previously presented about this topic:

- https://github.com/franklefebvre/slides/blob/master/2018-10-11-CocoaHeadsParis-codable-xml.pdf

### Questions and Discussion

#### Apple Vision Pro

John B showed us a demo of one of his Apple Vision Pro app. He also gave us a link to an app that he is currently working on.

- https://jera.com/bluebird

There is an upcoming Apple Vision Pro in-person conference:

- https://www.eventbrite.com/e/visiondevcamp-tickets-849184312137

#### Swift News

Playdate

- https://www.swift.org/blog/byte-sized-swift-tiny-games-playdate/

Parameter packs

- https://www.swift.org/blog/pack-iteration/


#### Swift Hardware

- https://madmachine.io


## 2024.03.09

### Questions and Discussion

There were other other discussions about working remotely in teams, getting experience at hackathons and working on open source PRs.

#### Performance

We looked at a performance problem in an app.  First we looked at it with insturments and found that the main loop was running with 98% CPU, a battery destroyer. It was hard to figure out in insturments exactly why this was happening but it did eventually lead us to the SwiftUI `View` that was re-rendering.

Then we insturmented this view with:

```swift
    let _ = Self._printChanges()
```

After closer inspection, we found that the view was using a geometry reader and then putting that into the view as an environment object. That would cause the view to re-render causing the whole cycle to repeat in a tight loop.

Josh's suggestion was to use a environment value instead:

Create a windowSize value that can be inserted into the environment.:

```swift
    extension EnvironmentValues {
        var windowSize: CGSize {
            get { self[SizeEnvironmentKey.self] }
            set { self[SizeEnvironmentKey.self] = newValue }
        }
    }
```

Create a method that you can set the size with (from something like a geometry reader).

```swift    
    extension View {
        func insertSizeIntoEnvironment(_ size: CGSize) -> some View {
            environment(\.windowSize, size)
        }
    }
```

Any view can get access to the size with this:

```swift
@Environment(\.windowSize) private var size
```

This would prevent the rapid invalidation of views caused by constantly updating the environment object.


## 2024.03.02

### Questions and Discussion

#### Apple AirPods and Vision Pro

Rainer notes that AirPod Pros give amazing sound for the small package they are in. He was wondering how they compare to Vision Pro. The consensus seemed to be that Vision Pro audio is better than AirPod Pro audio but not as good as AirPod Max audio.

#### Concurrency Isolation

We went through the points in https://www.massicotte.org/intro-to-isolation 

These include:

  - You can determine isolation from a types declaration
  - Sometimes you have to look at base types to get the answer
  - When you await you can change isolation
  - Closures can inherit isolation
  - You can opt out of isolation
  - Protocols can specify isolation and it has tricky consequences
  - SwiftUI only specifies the body property as `@MainActor` which can be confusing
  - Turn on complete checking to find out where your data races might be.

Josh showed several additional examples including several examples of how you can run into problems with view model isolation. The conversation then turned to state management more generally comparing different approaches.  We also talked about task inheritance and structured concurrency more generally.  Memorize this:

![Task Inheritence](https://github.com/aflockofswifts/meetings/blob/main/2022/materials/task-inheritance.png?raw=true)

---

## 2024.02.24

### Presentation: Generalized Pagination

Josh started project for handling pagination in a generalized way.

- Use an enumeration to handle loading, loaded(Content), error, empty states.
- Use https://pointfree.co `@CasePathable` to ergonomically handle the enum states.
- Make a generic type to handle the content and getting the next set of data.
- Make the pagination type conform to `RandomAccessCollection` and friends by projecting the underlying content array.
- Make a pagination manager using an actor that accepts closures for fetching data and synchronizing fetching calls and publishing result via an async stream. 

Source code TBD.

### Questions and Discussion

#### Swift 6 and Swift Evolution

Swift 6 branch was announced meaning 5.10 and Swift 6 are being developed together.

- https://github.com/apple/swift-evolution


An alternative view of evolution sorted by status:

- https://www.swift.org/swift-evolution/

Some recent proposals highlighted by Josh:

- https://github.com/apple/swift-evolution/blob/main/proposals/0421-generalize-async-sequence.md


#### Implementing a `with` method

Allows mutation of a builder type were the final built type may be declared with a let.


#### Mojo

Performance analysis of Mojo looking specifically at TCO (tail call optimization) in recursive functions.

- https://www.modular.com/blog/mojo-vs-rust-is-mojo-faster-than-rust


With regard to optimization and debugging we discussed looking at output from godbolt.com.

- https://github.com/apple/swift/blob/main/docs/DebuggingTheCompiler.md

```sh
(lldb) p getFunction()->dump()
```

Georgi shared this link:

- https://trinhngocthuyen.com/posts/tech/how-a-swift-file-is-compiled/

#### PKL 

A configuration language that plays nicely with Swift types and others.

https://pkl-lang.org/


---

## 2024.02.17

### Presentation: Transforms and SwiftUI

Josh took us through an example of using transforms, matrix multiplication and
how homogeneous coordinates work to produce affine transforms. Discussion of 
column-based vs row-based transforms.

Carlyn notes this tutorial series:

- https://www.3blue1brown.com/lessons/linear-transformations

Peter notes this Tech note from Apple about transforming images:

- https://developer.apple.com/documentation/accelerate/applying_geometric_transforms_to_images

### Questions and Discussion

#### New SwiftUI Field Guide

- https://www.swiftuifieldguide.com

#### Swift System

Cross platform abstractions for file access, etc.

- https://github.com/apple/swift-system


For example, Swift NIO uses System as a dependency.

#### Underscored attributes

What do they all mean? Find out here:

- https://github.com/apple/swift/blob/main/docs/ReferenceGuides/UnderscoredAttributes.md

---

## 2024.02.10

### Questions and Discussion

#### Apple Vision Pro

Lots of discussion about virtual avatars, Zoom implementation, bugs, etc.

Frank shared this top 10 app list:

- https://www.youtube.com/watch?v=AeSK-Ilmu38

Humberto shared this best app for teens. 😂

- https://x.com/aaditsh/status/1754219177089675287?s=20

Discussion of Polyspatial 

- https://apps.apple.com/us/app/lego-builders-journey/id1441636691?platform=appleVisionPro

Discussion of Godot

- https://apps.apple.com/us/app/defend-cow-castle/id6476968953


- https://github.com/kevinw/GodotVision


#### Swift Collections

There is a new release of Swift collections (1.1) that now includes `Heap` `BitSet` `BitArray` `TreeSet` and `TreeDictionary`

- https://github.com/apple/swift-collections


#### Code Organization and Tracing Tools

How to name SwiftUI files:

- https://scottsmithdev.com/screen-vs-view-in-swiftui

Log function names with `#function`

Also, Josh notes:

```swift
let _ = Self._printChanges()
```

- https://developer.apple.com/documentation/os/logger


---

## 2024.02.03

###

#### Safari Extension in Swift

Carlyn took us on a voyage exploring web extensions. It is a little tricky to setup if you want your extension to talk to your app.

- https://www.whynotestflight.com/excuses/getting-started-with-safari-web-extensions/

- https://www.whynotestflight.com/excuses/but-whats-a-plain-web-extension/


### Sequences Presentation

Josh gave a short presentation on iterating through grid composed of two grids.

```swift
func lazyCartesianProduct<X: Sequence, Y: Collection>(_ x: X, _ y: Y) -> some Sequence<(X.Element, Y.Element)> {
        x.lazy.flatMap { x in y.lazy.map { y in (x, y) } }
    }
    
func cartesianProduct<X: Sequence, Y: Collection>(_ x: X, _ y: Y) -> some Sequence<(X.Element, Y.Element)> {
    sequence(state: (
        column: x.makeIterator(),
        row: y.makeIterator(),
        currentColumn: Optional<X.Element>.none
    )) { state in
        state.currentColumn = state.currentColumn ?? state.column.next()
        let y = state.row.next() ?? {
            state.currentColumn = state.column.next()
            state.row = y.makeIterator()
            return state.row.next()
        }()
        return state.currentColumn.flatMap { x in y.map { y in (x, y) } }
    }
}
```

It is also interesting to look at the product type defined in the algorithms library:

- https://github.com/apple/swift-algorithms/blob/main/Sources/Algorithms/Product.swift

### Connect3D Available in the Store 🥳

Ed released an Apple Vision Pro app. Congratulations! Quite an accomplishment considering he developed it all without hardware.

https://apps.apple.com/us/app/connect3d-spatial/id6476113222


### Questions and Discussion

#### Apple Vision Pro Day

John and Ed attended the meeting using AVP. We had fun seeing their avatars and getting a firsthand description of the platform.

- https://support.apple.com/en-ca/HT213949


#### AI and Software Development

How is it changing what people are doing?

- https://www.kodeco.com/44206375-kodeco-podcast-putting-ai-to-use-in-software-development-v2-s2-e3


It is possible that the code quality is better for other languages such as Python and C++ because the corpus is larger.






## 2024.01.27

### Optimization Presentation

Josh walked us through the documents in the Swift repo https://github.com/apple/swift/blob/main/docs/OptimizationTips.rst


### Questions and Discussion

#### Supporting in-app Purchases and Verifying Certificates

You can stand up your own server or use one of these services:

- https://www.revenuecat.com
- https://www.purchasely.com

If you are a small shop, you might just choose on-device verification knowing that it will be possible some to crack.

#### Bug in Form HStack's

Here is the sample project from Monty.

https://github.com/MontyHarper/Bug-With-Form-HStack-ForEach.git


#### Working with JSON

- https://jsonlint.com
- https://quicktype.io


You could write your own viewer:

- https://swiftwithmajid.com/2020/09/02/displaying-recursive-data-using-outlinegroup-in-swiftui/


#### Editing Notifications

- https://developer.apple.com/documentation/usernotifications/modifying_content_in_newly_delivered_notifications/


#### Schemes are XML!

Carlyn has been hacking schemes from the command line.

- https://github.com/carlynorama/BuildPluginExampleTarget/tree/main/.swiftpm/xcode/xcshareddata/xcschemes

#### Computer History

It was the 40th anniverary of the Mac this week.

- https://computerhistory.org/events/insanely-great/


#### RayTracing

Ray is starting the Ray Tracing challenge. Here are some good resources for Ray Tracing:

- https://pbr-book.org
- http://raytracerchallenge.com

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

Generating your xcode project from scratch, or updating it from the command line: [Xcodeproj](https://github.com/CocoaPods/Xcodeproj)

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
[Perception](https://github.com/pointfreeco/swift-perception) back ported to older iOS versions and bridged to Observable in iOS 17+.  
Apple swift [source code](https://github.com/apple/swift/blob/main/stdlib/public/Observation/Sources/Observation/ObservationTracking.swift) for observation tracking.  

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
