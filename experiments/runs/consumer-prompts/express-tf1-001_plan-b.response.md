**Answer**
The architecture exposed by the clue is centered on andRestrictTo, andRestrictToSelf, loadUser, testMethod in examples/route-middleware/index.js, test/Route.js, test/Router.js, with n1 (andRestrictTo), n2 (andRestrictToSelf), n3 (loadUser), n4 (testMethod) acting as the main surfaced components. The surfaced behavior says: Function andRestrictTo. Function andRestrictToSelf. Function loadUser. This clue is compact, so the answer has to stay limited to the projected symbols, their files, and the brief behavior summaries that were surfaced. Within the limits of the clue, this is a grounded reading of the surfaced code path rather than a full implementation-level reconstruction.

**Key nodes**
- n1: andRestrictTo (utility) in examples/route-middleware/index.js
- n2: andRestrictToSelf (utility) in examples/route-middleware/index.js
- n3: loadUser (utility) in examples/route-middleware/index.js
- n4: testMethod (utility) in test/Route.js
- n5: fn1 (utility) in test/Router.js
- n6: fn2 (utility) in test/Router.js
- n7: no (utility) in test/Router.js
- n8: testMethod (utility) in test/Router.js
- n9: createError (error_handler) in test/app.route.js
- n10: createError (error_handler) in test/app.route.js
- n11: createError (error_handler) in test/app.route.js
- n12: createError (error_handler) in test/app.route.js
- n13: createError (error_handler) in test/app.route.js
- n14: createError (error_handler) in test/app.route.js
- n15: handleError (error_handler) in test/app.route.js

**Evidence**
- n1: andRestrictTo -> Function andRestrictTo. File: examples/route-middleware/index.js.
- n2: andRestrictToSelf -> Function andRestrictToSelf. File: examples/route-middleware/index.js.
- n3: loadUser -> Function loadUser. File: examples/route-middleware/index.js.
- n4: testMethod -> Function testMethod. File: test/Route.js.
- n5: fn1 -> Function fn1. File: test/Router.js.
- n6: fn2 -> Function fn2. File: test/Router.js.
- n7: no -> Function no. File: test/Router.js.
- n8: testMethod -> Function testMethod. File: test/Router.js.
- n9: createError -> Error handler; produces error response. File: test/app.route.js.
- n10: createError -> Error handler; produces error response. File: test/app.route.js.
- n11: createError -> Error handler; produces error response. File: test/app.route.js.
- n12: createError -> Error handler; produces error response. File: test/app.route.js.
- n13: createError -> Error handler; produces error response. File: test/app.route.js.
- n14: createError -> Error handler; produces error response. File: test/app.route.js.
- n15: handleError -> Error handler; produces error response. File: test/app.route.js.

**Confidence**
high

**Gaps**
The clue does not include full implementations, complete control-flow branches, or behavior outside the surfaced nodes/relations/assertions.
