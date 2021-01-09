# A Flock of Swifts 

A Flock of Swifts is a physical space meeting of like-minded people excited about the Swift language.  We normally meet each Saturday morning.  Here is our meetup page.  All people and all skill levels are welcome to join.  

Tim's Dropbox Paper notes: https://bit.ly/flock-of-swift-notes

---

### 2021.01.18
- **RSVP**: https://www.meetup.com/A-Flock-of-Swifts/

### 2021.01.09
We discussed the new asynchronous sequence proposal https://github.com/apple/swift-evolution/blob/main/proposals/0298-asyncsequence.md

We discussed `reduce` (fold) and its inverse (unfold) `sequence` https://developer.apple.com/documentation/swift/2011998-sequence
```
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
```
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
```
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
```
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

---

### 2021.01.02

Happy New Year!

Josh created an animated SwiftUI `RingChart` view that he plans to integrate into the **Tides** app.  The code is here: https://github.com/joshuajhomann/RingChart

![RingChart](resources/ringchart.gif)

## Archives

- [2020 Meetings](2020/README.md)
