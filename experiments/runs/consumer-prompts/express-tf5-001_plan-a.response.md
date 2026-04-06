**Answer**
The clue highlights security-relevant behavior around authenticate, restrict, defineGetter, header in examples/auth/index.js, lib/request.js, so those symbols are the main places where security-sensitive logic appears to concentrate. The surfaced behavior says: Function authenticate. Function restrict. Function defineGetter. This clue is compact, so the answer has to stay limited to the projected symbols, their files, and the brief behavior summaries that were surfaced. Within the limits of the clue, this is a grounded reading of the surfaced code path rather than a full implementation-level reconstruction.

**Key entities**
- n1: authenticate (utility) in examples/auth/index.js
- n2: restrict (utility) in examples/auth/index.js
- n3: defineGetter (utility) in lib/request.js
- n4: header (utility) in lib/request.js
- n5: host (utility) in lib/request.js
- n6: hostname (utility) in lib/request.js
- n7: ip (utility) in lib/request.js
- n8: ips (utility) in lib/request.js
- n9: is (utility) in lib/request.js
- n10: path (utility) in lib/request.js
- n11: protocol (utility) in lib/request.js
- n12: query (data_accessor) in lib/request.js
- n13: range (utility) in lib/request.js
- n14: secure (utility) in lib/request.js
- n15: stale (utility) in lib/request.js

**Evidence**
- n1: authenticate -> Function authenticate. File: examples/auth/index.js.
- n2: restrict -> Function restrict. File: examples/auth/index.js.
- n3: defineGetter -> Function defineGetter. File: lib/request.js.
- n4: header -> Function header. File: lib/request.js.
- n5: host -> Function host. File: lib/request.js.
- n6: hostname -> Function hostname. File: lib/request.js.
- n7: ip -> Function ip. File: lib/request.js.
- n8: ips -> Function ips. File: lib/request.js.
- n9: is -> Function is. File: lib/request.js.
- n10: path -> Function path. File: lib/request.js.
- n11: protocol -> Function protocol. File: lib/request.js.
- n12: query -> Accesses data store. File: lib/request.js.
- n13: range -> Function range. File: lib/request.js.
- n14: secure -> Function secure. File: lib/request.js.
- n15: stale -> Function stale. File: lib/request.js.

**Confidence**
high

**Gaps**
The clue does not show full implementations, exact branch conditions, or any code outside the projected entity set.
