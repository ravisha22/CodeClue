**Answer**
The clue highlights security-relevant behavior around GuardsConsumer, ExecutionContextHost, packages/core/guards/guards-consumer.ts in packages/core/guards/guards-consumer.ts, packages/core/helpers/execution-context-host.ts, so those symbols are the main places where security-sensitive logic appears to concentrate. The surfaced behavior says: Leaf handler invoked by dispatcher. Class ExecutionContextHost. Module containing 1 projected symbol(s). The listed relations indicate the local flow is n3 -> n1 via contains; n3 -> n1 via contains, which is the main evidence for how this subsystem is connected. Within the limits of the clue, this is a grounded reading of the surfaced code path rather than a full implementation-level reconstruction.

**Key entities**
- n1: GuardsConsumer (handler) in packages/core/guards/guards-consumer.ts
- n2: ExecutionContextHost (utility) in packages/core/helpers/execution-context-host.ts
- n3: packages/core/guards/guards-consumer.ts (module_root) in packages/core/guards/guards-consumer.ts

**Evidence**
- n1: GuardsConsumer -> Leaf handler invoked by dispatcher. File: packages/core/guards/guards-consumer.ts.
- n2: ExecutionContextHost -> Class ExecutionContextHost. File: packages/core/helpers/execution-context-host.ts.
- n3: packages/core/guards/guards-consumer.ts -> Module containing 1 projected symbol(s). File: packages/core/guards/guards-consumer.ts.
- Relation: n3 -> n1 via contains.
- Relation: n3 -> n1 via contains.

**Confidence**
high

**Gaps**
The clue does not show full implementations, exact branch conditions, or any code outside the projected entity set.
