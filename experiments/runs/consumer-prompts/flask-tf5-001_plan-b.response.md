**Answer**
The clue highlights security-relevant behavior around load_logged_in_user, login, wrapped_view, login_required in examples/tutorial/flaskr/auth.py, examples/tutorial/tests/conftest.py, examples/tutorial/tests/test_auth.py, so those symbols are the main places where security-sensitive logic appears to concentrate. The surfaced behavior says: Function load_logged_in_user. Function login. Function wrapped_view. The listed relations indicate the local flow is n12 -> n10 via calls, which is the main evidence for how this subsystem is connected. Within the limits of the clue, this is a grounded reading of the surfaced code path rather than a full implementation-level reconstruction.

**Key nodes**
- n1: load_logged_in_user (utility) in examples/tutorial/flaskr/auth.py
- n2: login (utility) in examples/tutorial/flaskr/auth.py
- n3: wrapped_view (utility) in examples/tutorial/flaskr/auth.py
- n4: login_required (utility) in examples/tutorial/flaskr/auth.py
- n5: logout (utility) in examples/tutorial/flaskr/auth.py
- n6: register (utility) in examples/tutorial/flaskr/auth.py
- n7: __init__ (utility) in examples/tutorial/tests/conftest.py
- n8: login (utility) in examples/tutorial/tests/conftest.py
- n9: logout (utility) in examples/tutorial/tests/conftest.py
- n10: AuthActions (handler) in examples/tutorial/tests/conftest.py
- n11: app (utility) in examples/tutorial/tests/conftest.py
- n12: auth (entrypoint) in examples/tutorial/tests/conftest.py
- n13: client (utility) in examples/tutorial/tests/conftest.py
- n14: runner (utility) in examples/tutorial/tests/conftest.py
- n15: test_login (utility) in examples/tutorial/tests/test_auth.py

**Evidence**
- n1: load_logged_in_user -> Function load_logged_in_user. File: examples/tutorial/flaskr/auth.py.
- n2: login -> Function login. File: examples/tutorial/flaskr/auth.py.
- n3: wrapped_view -> Function wrapped_view. File: examples/tutorial/flaskr/auth.py.
- n4: login_required -> Function login_required. File: examples/tutorial/flaskr/auth.py.
- n5: logout -> Function logout. File: examples/tutorial/flaskr/auth.py.
- n6: register -> Function register. File: examples/tutorial/flaskr/auth.py.
- n7: __init__ -> Function __init__. File: examples/tutorial/tests/conftest.py.
- n8: login -> Function login. File: examples/tutorial/tests/conftest.py.
- n9: logout -> Function logout. File: examples/tutorial/tests/conftest.py.
- n10: AuthActions -> Leaf handler invoked by auth. File: examples/tutorial/tests/conftest.py.
- n11: app -> Function app. File: examples/tutorial/tests/conftest.py.
- n12: auth -> Entrypoint that delegates to AuthActions. File: examples/tutorial/tests/conftest.py.
- n13: client -> Function client. File: examples/tutorial/tests/conftest.py.
- n14: runner -> Function runner. File: examples/tutorial/tests/conftest.py.
- n15: test_login -> Function test_login. File: examples/tutorial/tests/test_auth.py.
- Relation: n12 -> n10 via calls.

**Confidence**
high

**Gaps**
The clue does not include full implementations, complete control-flow branches, or behavior outside the surfaced nodes/relations/assertions.
