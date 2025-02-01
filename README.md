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

---

## Notes

## 2025.02.01


---

## 2025.01.25

- How to share resources among multiple Swift packages.
- Continued working on Mine Sweeper

---

## 2025.01.18

### Making CoW Types Sendable

We modernized a small app to Swift 6. Making a type CoW and isolating all mutation
allows you to declare a type sendable. The mutable state is not shared so these 
properties can be marked sendable (unsafe).

### Performance

Measure the performance of a new collection type using the Swift performance package.

https://www.swift.org/blog/benchmarks/


### Mine Sweeper

Continued the mine sweeper example.

---

## 2025.01.10

### Debugging SceneKit Audio

We spent some time debugging a problem with a SceneKit app that was leaking audio players.

### Animating Text

Rainer was trying to animate text along a Bézier curve.

Josh reminded us of this project example from last year:

- https://github.com/aflockofswifts/meetings/tree/main/2024#20240518

Also, a Primer on Bézier curves: https://pomax.github.io/bezierinfo/
    

Rainer noted that the example he was trying to emulate: 

- https://github.com/objcio/S01E166-geometry-effects
  

His code here:
  
- https://github.com/minsOne/custom-ui-prototype-in-swiftui
  

### Continuing the Mine Sweeper Example

This week we looked at a serious performance problem in what we built so far.
Changing the color of a handful of tile taking almost a second to perform.

A nice video from Ben Cohen about Fast Safe Mutable State:

- https://www.youtube.com/watch?v=BXJIIQ-B4-E
    

An internal way to do in-place mutation:

- https://jano.dev/apple/2024/12/10/Modify-and-Yield.html
- https://forums.swift.org/t/modify-accessors/31872
    

But the biggest performance win was had by using a properly identifiable type in the ForEach statement of the grid.

---

## 2025.01.03

### A functional solution to Ed's game
  * Ed is making a game where he needs to match n distinct items in a row.  Josh offered a solution in functional swift:
  * We start with an assumption that we have a node, a sequence of adjacencies that can transform a node into another node, and the number of distinct items we want to match
```swift
let n = 6
let adjacency: some Sequence<(Node) -> Node?>
let node: Node
```
![layout](materials/blocks.png)
  * We can express the algorithm we want to apply as a node represents a winning state if there is a way to transform it into a sequence of n distinct elements. or more formally:
![layout](materials/existential.png)
  * Equivalently in swift:
```swift
let isWon = adjacency.contains { [node, n] adjacency in
	Set(sequence(first: node) { adjacency(node)}.prefix(n))).count == n
}
```
  * We can further express our intent with the use of explanatory variables:
```swift
let isWon = adjacency.contains { [node, n] adjacency in
    let adjacentUnique = Set(sequence(first: node) { adjacency(node)}.prefix(n))
	let isWinningRun = adjacentUnique.count == n
	return isWinningRun
}
```
* Ed asked how to get the winning nodes.  We can do this by changing the operator to `compactMap`:
```swift
let winningSets = adjacency.compactMap { [node, n] adjacency in
    let adjacentUnique = Set(sequence(first: node) { adjacency(node)}.prefix(n))
	let isWinningRun = adjacentUnique.count == n
	return isWinningRun ? adjacentUnique : nil
}
.reduce(into: Set<Node>()) { $0.formUnion($1) }
```

### Mine sweeper continued
* We updated the Layout to use a cache and added a viewModel:
```swift
@Observable
final class ViewModel: ObservableObject {
    private(set) var cells: Grid2D<Cell> = .init(rows: 8, columns: 8) { x, y in
        .init(id: x + y * 8, position: .init(x, y), color: .allCases.randomElement()!)
    }
    func tap(index: SIMD2<Int>) {
        cells[index].color = .blue
    }
}

struct Cell: Identifiable, Hashable {
    let id: Int
    let position: SIMD2<Int>
    var color: ViewModel.BoardColor
}

extension ViewModel {
    enum BoardColor: Hashable, CaseIterable {
        case red, green, blue
    }
}

struct ContentView: View {
    @StateObject private var viewModel = ViewModel()
    var body: some View {
        Board(dimension: 8) {
            ForEach(viewModel.cells.indices, id: \.self) { index in
                Group {
                    switch viewModel.cells[index].color {
                    case .red: Color.red
                    case .green: Color.green
                    case .blue: Color.blue
                    }
                }
                .onTapGesture {
                    viewModel.tap(index:  viewModel.cells[index].position)
                }
                .boardPosition(index)
            }
        }
    }
}

extension View {
    func boardPosition(_ position: SIMD2<Int>) -> some View {
        layoutValue(key: BoardPosition.self, value: position)
    }
    func boardPosition(x: Int, y: Int) -> some View {
        boardPosition(.init(x, y))
    }
}

struct Board: Layout {
    let dimension: Int

    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout Cache) -> CGSize {
        let size = proposal.replacingUnspecifiedDimensions(by: .zero)
        let minimumDimension = min(size.width, size.height)
        return .init(width: minimumDimension, height: minimumDimension)
    }

    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout Cache) {
        if cache.bounds != bounds {
            cache.bounds = bounds
            cache.cellSize = CGSize(width: bounds.width / Double(dimension), height: bounds.height / Double(dimension))
            let transform = CGAffineTransform
                .identity
                .translatedBy(x: bounds.origin.x, y: bounds.origin.y)
                .scaledBy(x: cache.cellSize.width, y: cache.cellSize.height)
            cache.grid = .init(rows: dimension, columns: dimension) { x, y in
                CGPoint(x: x, y: y).applying(transform)
            }
        }
        for view in subviews {
            let position = cache.grid[safe: view[BoardPosition.self]] ?? bounds.origin
            view.place(
                at: position,
                proposal: .init(cache.cellSize)
            )
        }
    }

    func makeCache(subviews: Subviews) -> Cache {
        .init()
    }

    struct Cache {
        var bounds = CGRect.zero
        var cellSize = CGSize.zero
        var grid: Grid2D<CGPoint> = .init(repeating: .zero, rows: 0, columns: 0)
    }
}

struct BoardPosition: LayoutValueKey {
    static let defaultValue = SIMD2<Int>.zero
}
```
