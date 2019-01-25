# A library for sets of integer ranges

This library provides some set theory operations on sets represented by arrays
containing integer intervals.
If this sounds weird, here's an example: the set { 1, 2, 3, 7, 8, 9 } contains
the two contiguous integer intervals 1..3 and 7..9.
This library represents these values using half-closed intervals (end is not
included in the interval), so `[1, 4)` and `[7, 10)`.
The corresponding python data structure is suspiciously similar:
`[ (1, 4), (7, 10) ]`.

On this kind of set, the library now provides the following operations:

```python
from interval_sets import *

setB = coalesce(setA)
# Sorts (potentially ill-formed) setA, removes overlaps and merges adjacent
# ranges. This function is useful to bring a set of random intervals into the
# correct format.

setC = union(setA, setB)
# Computes the union of setA and setB, or A ∪ B

setC = intersect(setA, setB)
# Computes the intersection of setA and setB , or A ∩ B

setC = difference(setA, setB)
# Computes the relative complement of setA in setB, or A \ B

vol = volume(setA)
# Computes the number of elements contained in setA, or | A |
```

This library treats sets as immutable, so none of these operations modify any
of the arrays passed to them.

Attention: Within each set, intervals are required to be sorted and
non-overlapping. Behavior is undefined if these criteria are not met. You can
bring any array of unsorted, overlapping intervals into the correct form using
the coalesce function.

This is a library I needed for analysis @ [unihd-ceg](https://github.com/UniHd-CEG).

# License: MIT

Copyright (c) 2018 Alexander Matz, Heidelberg University

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
