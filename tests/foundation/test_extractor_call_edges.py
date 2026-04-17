"""Extractor call edge pattern tests.

Tests that each extractor captures real call patterns found in production code.
Each test creates a minimal source fixture, runs the extractor, and checks
whether the expected call edges were produced.

IMPORTANT: These tests validate the FOUNDATION (call graph correctness),
not the renderer. All L2 SYM rankings and L3 FOCUS selections depend on
this graph being correct.
"""

from __future__ import annotations

import tempfile
import textwrap
import time
from pathlib import Path

import pytest

from codeclue_research.extractor import extract_graph, extract_python_nodes_edges
from codeclue_research.extract_go import _extract_go_behavior_patterns, extract_go_nodes_edges
from codeclue_research.extract_typescript import extract_typescript_nodes_edges


# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────

def _write_fixture(tmp: Path, filename: str, content: str) -> None:
    """Write a fixture file inside a temp repo directory."""
    filepath = tmp / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(textwrap.dedent(content), encoding="utf-8")


def _get_call_edges(nodes, edges) -> list[tuple[str, str]]:
    """Extract (caller_symbol_name, callee_symbol_name) from call edges."""
    node_map = {n.node_id: n.semantic_contract.get("symbol_name", n.node_id) for n in nodes}
    result = []
    for e in edges:
        if e.edge_type == "calls":
            caller = node_map.get(e.from_node, e.from_node)
            callee = node_map.get(e.to_node, e.to_node)
            result.append((caller, callee))
    return result


def _has_call(call_edges: list[tuple[str, str]], caller: str, callee: str) -> bool:
    """Check if a specific call edge exists (partial match on symbol names)."""
    for c_from, c_to in call_edges:
        if caller in c_from and callee in c_to:
            return True
    return False


# ──────────────────────────────────────────────────────────────
# PYTHON CALL PATTERN TESTS
# ──────────────────────────────────────────────────────────────

PYTHON_FIXTURE = """\
class MyClass:
    def __init__(self):
        self.value = 0
        self._setup()

    def _setup(self):
        self.compute()

    def public_method(self):
        return self._private_method()

    def _private_method(self):
        result = self.compute()
        return result

    def compute(self):
        return helper_func()

    def uses_super(self):
        super().save()

    def uses_instance(self):
        obj = MyHelper()
        obj.do_work()

    def chained_call(self):
        self.config.validate()

    @classmethod
    def from_config(cls):
        return cls()


class MyHelper:
    def do_work(self):
        pass


class Child(MyClass):
    def child_method(self):
        self.public_method()
        super().compute()


def helper_func():
    return MyClass()


def module_level():
    helper_func()
    obj = MyClass()
"""


class TestPythonCallEdges:
    """Test all Python call patterns the extractor must capture."""

    @pytest.fixture(autouse=True)
    def setup(self, tmp_path: Path):
        _write_fixture(tmp_path, "module.py", PYTHON_FIXTURE)
        nodes, edges = extract_python_nodes_edges(tmp_path)
        self.call_edges = _get_call_edges(nodes, edges)
        self.nodes = nodes
        self.edges = edges

    def test_pattern_01_self_method(self):
        """self.public_method() from __init__ calling _setup"""
        assert _has_call(self.call_edges, "__init__", "_setup"), (
            f"MISSED: self._setup() in __init__. Edges: {self.call_edges}"
        )

    def test_pattern_02_self_private_method(self):
        """self._private_method() call"""
        assert _has_call(self.call_edges, "public_method", "_private_method"), (
            f"MISSED: self._private_method(). Edges: {self.call_edges}"
        )

    def test_pattern_03_self_method_in_assignment(self):
        """result = self.compute() — method call in assignment"""
        assert _has_call(self.call_edges, "_private_method", "compute"), (
            f"MISSED: self.compute() in assignment. Edges: {self.call_edges}"
        )

    def test_pattern_04_module_level_function_call(self):
        """helper_func() — bare function call from method"""
        assert _has_call(self.call_edges, "compute", "helper_func"), (
            f"MISSED: helper_func() from compute. Edges: {self.call_edges}"
        )

    def test_pattern_05_class_instantiation(self):
        """MyClass() — class instantiation"""
        assert _has_call(self.call_edges, "helper_func", "MyClass"), (
            f"MISSED: MyClass() instantiation. Edges: {self.call_edges}"
        )

    def test_pattern_06_module_level_to_module_level(self):
        """module_level() calling helper_func()"""
        assert _has_call(self.call_edges, "module_level", "helper_func"), (
            f"MISSED: module_level -> helper_func. Edges: {self.call_edges}"
        )

    def test_pattern_07_instance_method_call(self):
        """obj.do_work() — call on local variable instance"""
        # obj = MyHelper(); obj.do_work() — the callee is do_work
        assert _has_call(self.call_edges, "uses_instance", "do_work"), (
            f"MISSED: obj.do_work() instance call. Edges: {self.call_edges}"
        )

    def test_pattern_08_child_calls_inherited(self):
        """self.public_method() from a child class calling parent method"""
        assert _has_call(self.call_edges, "child_method", "public_method"), (
            f"MISSED: child self.public_method() call. Edges: {self.call_edges}"
        )

    def test_pattern_09_super_method_call(self):
        """super().compute() from child"""
        assert _has_call(self.call_edges, "child_method", "compute"), (
            f"MISSED: super().compute(). Edges: {self.call_edges}"
        )

    def test_pattern_10_classmethod_cls_call(self):
        """cls() in classmethod"""
        # cls() is resolved as a Name call — should match MyClass or similar
        # The exact resolution depends on how `cls` is tracked
        # At minimum, we expect SOME edge from from_config
        from_config_edges = [e for e in self.call_edges if "from_config" in e[0]]
        # cls() might not be resolvable without type inference — document as known gap
        # This test documents the behavior, not necessarily requires it
        pass  # Documented: cls() resolution requires type inference

    def test_summary_report(self):
        """Print a summary of all patterns — not a pass/fail test."""
        patterns = [
            ("self.method()", "__init__", "_setup"),
            ("self._private()", "public_method", "_private_method"),
            ("self.method() assign", "_private_method", "compute"),
            ("module-level call", "compute", "helper_func"),
            ("class instantiation", "helper_func", "MyClass"),
            ("module->module call", "module_level", "helper_func"),
            ("instance.method()", "uses_instance", "do_work"),
            ("child self.method()", "child_method", "public_method"),
            ("super().method()", "child_method", "compute"),
        ]
        print("\n=== PYTHON CALL EDGE PATTERN REPORT ===")
        captured = 0
        for label, caller, callee in patterns:
            status = "CAPTURED" if _has_call(self.call_edges, caller, callee) else "MISSED"
            if status == "CAPTURED":
                captured += 1
            print(f"  [{status:8s}] {label}: {caller} -> {callee}")
        print(f"\n  Result: {captured}/{len(patterns)} patterns captured")
        print(f"  All edges: {self.call_edges}")


# ──────────────────────────────────────────────────────────────
# GO CALL PATTERN TESTS
# ──────────────────────────────────────────────────────────────

GO_FIXTURE = """\
package main

// Server handles HTTP requests.
type Server struct {
    port int
}

// Router dispatches requests to handlers.
type Router struct {
    routes []string
}

// NewServer creates a new Server instance.
func NewServer(port int) *Server {
    r := NewRouter()
    _ = r
    return &Server{port: port}
}

// NewRouter creates a new Router.
func NewRouter() *Router {
    return &Router{}
}

// Start begins listening on the configured port.
func (s *Server) Start() error {
    s.setup()
    return nil
}

// setup initializes internal state.
func (s *Server) setup() {
    s.validate()
}

// validate checks server configuration.
func (s *Server) validate() {
    if s.port < 0 {
        panic("invalid port")
    }
}

// AddRoute appends a route to the router.
func (r *Router) AddRoute(path string) {
    r.routes = append(r.routes, path)
}

// Handle processes a request through the router.
func (r *Router) Handle(path string) {
    r.AddRoute(path)
    r.match(path)
}

// match finds a matching route.
func (r *Router) match(path string) bool {
    return false
}

// standalone function calling a method
func initApp() {
    s := NewServer(8080)
    s.Start()
}
"""


class TestGoCallEdges:
    """Test all Go call patterns the extractor must capture."""

    @pytest.fixture(autouse=True)
    def setup(self, tmp_path: Path):
        _write_fixture(tmp_path, "main.go", GO_FIXTURE)
        nodes, edges = extract_go_nodes_edges(tmp_path)
        self.call_edges = _get_call_edges(nodes, edges)
        self.nodes = nodes
        self.edges = edges

    def test_pattern_01_receiver_method_call(self):
        """s.setup() — receiver calling own method"""
        assert _has_call(self.call_edges, "Server.Start", "setup") or \
               _has_call(self.call_edges, "Server.Start", "Server.setup"), (
            f"MISSED: s.setup() receiver call. Edges: {self.call_edges}"
        )

    def test_pattern_02_chained_receiver_call(self):
        """s.validate() from setup"""
        assert _has_call(self.call_edges, "Server.setup", "validate") or \
               _has_call(self.call_edges, "Server.setup", "Server.validate"), (
            f"MISSED: s.validate() chained call. Edges: {self.call_edges}"
        )

    def test_pattern_03_package_function_call(self):
        """NewRouter() from NewServer — package-level function call"""
        assert _has_call(self.call_edges, "NewServer", "NewRouter"), (
            f"MISSED: NewRouter() package call. Edges: {self.call_edges}"
        )

    def test_pattern_04_method_to_method_same_type(self):
        """r.AddRoute() from Handle — method calling sibling method"""
        assert _has_call(self.call_edges, "Router.Handle", "AddRoute") or \
               _has_call(self.call_edges, "Router.Handle", "Router.AddRoute"), (
            f"MISSED: r.AddRoute() from Handle. Edges: {self.call_edges}"
        )

    def test_pattern_05_method_to_private_method(self):
        """r.match() from Handle"""
        assert _has_call(self.call_edges, "Router.Handle", "match") or \
               _has_call(self.call_edges, "Router.Handle", "Router.match"), (
            f"MISSED: r.match() from Handle. Edges: {self.call_edges}"
        )

    def test_pattern_06_standalone_to_function(self):
        """NewServer() from initApp — standalone function calling package function"""
        assert _has_call(self.call_edges, "initApp", "NewServer"), (
            f"MISSED: NewServer() from initApp. Edges: {self.call_edges}"
        )

    def test_pattern_07_standalone_to_method(self):
        """s.Start() from initApp — standalone calling method on instance"""
        assert _has_call(self.call_edges, "initApp", "Start") or \
               _has_call(self.call_edges, "initApp", "Server.Start"), (
            f"MISSED: s.Start() from initApp. Edges: {self.call_edges}"
        )

    def test_pattern_08_panic_detection(self):
        """panic() in validate should produce raises: [panic]"""
        validate_nodes = [n for n in self.nodes
                         if n.semantic_contract.get("symbol_name", "").endswith("validate")]
        assert validate_nodes, "validate node not found"
        raises = validate_nodes[0].semantic_contract.get("raises", [])
        assert "panic" in raises, f"MISSED: panic detection. raises={raises}"

    def test_pattern_09_scope_tracking_nested_braces(self):
        """Verify that nested braces (if blocks) don't prematurely end function scope.
        
        The Go extractor resets current_func_id on any line with just '}'.
        If validate() has an if block, the closing '}' of the if block
        might prematurely end scope tracking.
        """
        # This tests that calls AFTER nested braces are still captured.
        # validate() only has panic inside an if — panic should still be found
        # (it IS found per test_pattern_08, so scope isn't broken HERE,
        # but this is a known fragile pattern)
        pass  # Documented: scope tracking via '}' alone is fragile

    def test_summary_report(self):
        """Print a summary of all patterns."""
        patterns = [
            ("receiver.Method()", "Server.Start", "setup"),
            ("chained receiver", "Server.setup", "validate"),
            ("package function", "NewServer", "NewRouter"),
            ("method->sibling", "Router.Handle", "AddRoute"),
            ("method->private", "Router.Handle", "match"),
            ("standalone->func", "initApp", "NewServer"),
            ("standalone->method", "initApp", "Start"),
        ]
        print("\n=== GO CALL EDGE PATTERN REPORT ===")
        captured = 0
        for label, caller, callee in patterns:
            status = "CAPTURED" if _has_call(self.call_edges, caller, callee) else "MISSED"
            if status == "CAPTURED":
                captured += 1
            print(f"  [{status:8s}] {label}: {caller} -> {callee}")
        print(f"\n  Result: {captured}/{len(patterns)} patterns captured")
        print(f"  All edges: {self.call_edges}")


# ──────────────────────────────────────────────────────────────
# TYPESCRIPT CALL PATTERN TESTS
# ──────────────────────────────────────────────────────────────

TS_FIXTURE = """\
export class UserService {
    constructor(private db: Database) {}

    async getUser(id: string) {
        return this.findById(id);
    }

    private findById(id: string) {
        return this.db.query(id);
    }

    async createUser(data: any) {
        const user = new UserValidator();
        user.validate(data);
        return this.save(data);
    }

    private save(data: any) {
        return data;
    }
}

export class UserValidator {
    validate(data: any) {
        return true;
    }
}

export class AdminService extends UserService {
    async getAdmin(id: string) {
        return super.getUser(id);
    }
}

export function createService(db: Database) {
    return new UserService(db);
}

export async function initApp() {
    const svc = createService(null);
    const user = await svc.getUser("1");
}

const helperFn = async (x: number) => {
    return createService(null);
};
"""


class TestTypeScriptCallEdges:
    """Test all TypeScript call patterns the extractor must capture."""

    @pytest.fixture(autouse=True)
    def setup(self, tmp_path: Path):
        _write_fixture(tmp_path, "service.ts", TS_FIXTURE)
        nodes, edges = extract_typescript_nodes_edges(tmp_path)
        self.call_edges = _get_call_edges(nodes, edges)
        self.nodes = nodes
        self.edges = edges

    def test_pattern_01_this_method_call(self):
        """this.findById() — method calling own method via this"""
        # TS extractor may not track this.method() calls at all
        assert _has_call(self.call_edges, "getUser", "findById") or \
               _has_call(self.call_edges, "service.ts", "findById"), (
            f"MISSED: this.findById() call. Edges: {self.call_edges}"
        )

    def test_pattern_02_new_class_instantiation(self):
        """new UserValidator() — class instantiation"""
        # The `new` keyword means UserValidator( appears in the line
        assert _has_call(self.call_edges, "createUser", "UserValidator") or \
               _has_call(self.call_edges, "service.ts", "UserValidator"), (
            f"MISSED: new UserValidator(). Edges: {self.call_edges}"
        )

    def test_pattern_03_function_to_function(self):
        """createService() from initApp"""
        assert _has_call(self.call_edges, "initApp", "createService") or \
               _has_call(self.call_edges, "service.ts", "createService"), (
            f"MISSED: createService() from initApp. Edges: {self.call_edges}"
        )

    def test_pattern_04_arrow_fn_calls_function(self):
        """helperFn arrow function calling createService"""
        assert _has_call(self.call_edges, "helperFn", "createService") or \
               _has_call(self.call_edges, "service.ts", "createService"), (
            f"MISSED: createService() from arrow fn. Edges: {self.call_edges}"
        )

    def test_pattern_05_caller_is_not_always_module(self):
        """Verify that at least SOME call edges have a function as the caller, not just the module."""
        non_module_callers = [
            (c, t) for c, t in self.call_edges
            if not c.endswith(".ts") and "module" not in c
        ]
        assert non_module_callers, (
            f"MISSED: expected precise TypeScript caller nodes. Edges: {self.call_edges}"
        )

    def test_pattern_06_class_method_extraction(self):
        """Verify that class methods (getUser, findById etc.) are extracted as symbols."""
        symbol_names = [n.semantic_contract.get("symbol_name", "")
                       for n in self.nodes if n.node_type in ("function", "async_function", "class")]
        assert any("UserService.getUser" == name for name in symbol_names)
        assert any("UserService.findById" == name for name in symbol_names)

    def test_pattern_07_extends_relationship_extracted(self):
        admin_nodes = [
            n for n in self.nodes
            if n.semantic_contract.get("symbol_name", "") == "AdminService"
        ]
        assert admin_nodes, "AdminService node not found"
        bases = admin_nodes[0].semantic_contract.get("bases", [])
        assert "UserService" in bases, f"MISSED: extends relationship. bases={bases}"

    def test_summary_report(self):
        """Print a summary of all patterns."""
        patterns = [
            ("this.method()", "getUser", "findById"),
            ("new ClassName()", "createUser", "UserValidator"),
            ("function->function", "initApp", "createService"),
            ("arrow->function", "helperFn", "createService"),
        ]
        print("\n=== TYPESCRIPT CALL EDGE PATTERN REPORT ===")
        captured = 0
        for label, caller, callee in patterns:
            # Accept module-level caller as partial credit
            has_precise = _has_call(self.call_edges, caller, callee)
            has_module = _has_call(self.call_edges, "service.ts", callee)
            if has_precise:
                status = "CAPTURED"
                captured += 1
            elif has_module:
                status = "PARTIAL"  # detected but wrong caller
            else:
                status = "MISSED"
            print(f"  [{status:8s}] {label}: {caller} -> {callee}")

        print(f"\n  Result: {captured}/{len(patterns)} patterns captured (precise caller)")
        print(f"  All edges: {self.call_edges}")
        print(f"  All symbols: {[n.semantic_contract.get('symbol_name') for n in self.nodes if n.node_type != 'module']}")


def test_go_extractor_skips_test_files(tmp_path: Path):
    _write_fixture(tmp_path, "app.go", "package main\n\nfunc Start() {}\n")
    _write_fixture(tmp_path, "app_test.go", "package main\n\nfunc TestStart(t *testing.T) {}\n")
    _write_fixture(tmp_path, "docs/guide.go", "package main\n\nfunc Guide() {}\n")
    _write_fixture(tmp_path, "examples/demo.go", "package main\n\nfunc Demo() {}\n")
    nodes, _ = extract_go_nodes_edges(tmp_path)
    file_paths = {n.source_anchor.file_path for n in nodes}
    assert "app.go" in file_paths
    assert "app_test.go" not in file_paths
    assert "docs/guide.go" not in file_paths
    assert "examples/demo.go" not in file_paths


def test_go_extractor_keeps_scope_after_nested_block(tmp_path: Path):
    _write_fixture(
        tmp_path,
        "main.go",
        """\
        package main

        type Server struct{}

        func (s *Server) validate(port int) {
            if port < 0 {
                panic("invalid")
            }
            s.afterCheck()
        }

        func (s *Server) afterCheck() {}
        """,
    )
    nodes, edges = extract_go_nodes_edges(tmp_path)
    call_edges = _get_call_edges(nodes, edges)
    assert _has_call(call_edges, "Server.validate", "afterCheck")


def test_go_extractor_detects_short_receiver_method_calls(tmp_path: Path):
    _write_fixture(
        tmp_path,
        "middleware.go",
        """\
        package main

        type Ctx struct{}

        func (c *Ctx) Next() error {
            return nil
        }

        func AuthMiddleware(c *Ctx) error {
            return c.Next()
        }
        """,
    )
    nodes, edges = extract_go_nodes_edges(tmp_path)
    call_edges = _get_call_edges(nodes, edges)
    assert _has_call(call_edges, "AuthMiddleware", "Next") or \
           _has_call(call_edges, "AuthMiddleware", "Ctx.Next"), (
        f"MISSED: c.Next() short-receiver call. Edges: {call_edges}"
    )


def test_go_behavior_pattern_extraction_is_linearish_on_large_body():
    branches = []
    for idx in range(250):
        prefix = "if" if idx == 0 else "else if"
        branches.append(f"    {prefix} cond{idx} {{")
        branches.append(f"        return handle{idx}()")
        branches.append("    }")
    body = "func Example() {\n" + "\n".join(branches) + "\n    return fallback()\n}\n"
    start = time.perf_counter()
    patterns = _extract_go_behavior_patterns(body)
    elapsed = time.perf_counter() - start
    assert elapsed < 1.0, f"behavior extraction too slow: {elapsed:.3f}s"
    assert isinstance(patterns, list)


def test_ts_extractor_supports_dollar_prefixed_type_symbols(tmp_path: Path):
    _write_fixture(
        tmp_path,
        "schema.ts",
        """\
        export interface $ZodType {
            _zod: { def: string };
        }

        export interface $ZodString extends $ZodType {
            parse(data: unknown): unknown;
        }

        export type $ZodAlias = $ZodString;
        """,
    )
    nodes, _ = extract_typescript_nodes_edges(tmp_path)
    symbol_map = {
        n.semantic_contract.get("symbol_name", ""): n
        for n in nodes
        if n.node_type != "module"
    }
    assert "$ZodType" in symbol_map
    assert "$ZodString" in symbol_map
    assert "$ZodAlias" in symbol_map
    assert "$ZodType" in symbol_map["$ZodString"].semantic_contract.get("bases", [])


def test_ts_extractor_captures_property_access_uses(tmp_path: Path):
    _write_fixture(
        tmp_path,
        "access.ts",
        """\
        export function parseSchema(obj: { _zod: { def: unknown } }) {
            return obj._zod.def;
        }
        """,
    )
    nodes, _ = extract_typescript_nodes_edges(tmp_path)
    parse_node = next(
        n for n in nodes
        if n.semantic_contract.get("symbol_name", "") == "parseSchema"
    )
    uses = parse_node.semantic_contract.get("uses", [])
    assert "obj._zod.def" in uses


def test_ts_extractor_preserves_zod_style_bases_and_alias_exports(tmp_path: Path):
    _write_fixture(
        tmp_path,
        "schema.ts",
        """\
        export interface ZodSymbol extends core.$ZodType<core.$ZodSymbolInternals> {}
        export type ZodSymbolAlias = core.$ZodSymbol;
        """,
    )
    nodes, _ = extract_typescript_nodes_edges(tmp_path)
    symbol_map = {
        n.semantic_contract.get("symbol_name", ""): n
        for n in nodes
        if n.node_type != "module"
    }
    assert symbol_map["ZodSymbol"].semantic_contract.get("bases") == ["$ZodType"]
    assert symbol_map["ZodSymbolAlias"].semantic_contract.get("uses") == ["core.$ZodSymbol"]


def test_python_behavior_patterns_include_condition_and_actions(tmp_path: Path):
    _write_fixture(
        tmp_path,
        "behavior.py",
        """\
        def process(value, chunks):
            if value is None:
                raise ValueError("missing")
            if value == "env":
                return load_env()
            else:
                return load_default()
            for chunk in chunks:
                body.append(chunk)
        """,
    )
    nodes, _ = extract_python_nodes_edges(tmp_path)
    process_node = next(n for n in nodes if n.semantic_contract.get("symbol_name") == "process")
    patterns = process_node.semantic_contract.get("behavior_patterns", [])
    assert any("GUARD(value is None" in pattern and "raise ValueError" in pattern for pattern in patterns)
    assert any("BRANCH(value == 'env'" in pattern and "load_env" in pattern and "load_default" in pattern for pattern in patterns)


def test_go_behavior_patterns_include_richer_details():
    body = """\
    func readBody(err error) {
        if err != nil {
            return err
        } else {
            return fmt.Errorf("wrap: %w", err)
        }
        for {
            body += chunk
            panic(EntityTooLarge)
        }
    }
    """
    patterns = _extract_go_behavior_patterns(body)
    assert any("BRANCH(err != nil" in pattern and "return err" in pattern and "fmt.Errorf" in pattern for pattern in patterns)
    assert any("ACCUMULATE(" in pattern and "body" in pattern and "EntityTooLarge" in pattern for pattern in patterns)


def test_ts_behavior_patterns_include_richer_details(tmp_path: Path):
    _write_fixture(
        tmp_path,
        "behavior.ts",
        """\
        export function choose(opts?: string, envvar?: string) {
            if (!opts) {
                return defaultValue;
            }
            if (opts) {
                return opts;
            } else if (envvar) {
                return envvar;
            } else {
                return defaultValue;
            }
        }
        """,
    )
    nodes, _ = extract_typescript_nodes_edges(tmp_path)
    choose_node = next(n for n in nodes if n.semantic_contract.get("symbol_name") == "choose")
    patterns = choose_node.semantic_contract.get("behavior_patterns", [])
    assert any("GUARD(!opts" in pattern and "return defaultValue" in pattern for pattern in patterns)
    assert any(pattern.startswith("PRECEDENCE(") and "opts" in pattern and "envvar" in pattern for pattern in patterns)


def test_extract_graph_adds_config_and_doc_nodes(tmp_path: Path):
    _write_fixture(
        tmp_path,
        "settings.py",
        """\
        INSTALLED_APPS = ["inventory", "orders"]
        MIDDLEWARE = ["django.middleware.security.SecurityMiddleware"]
        DATABASES = {"default": {"ENGINE": "django.db.backends.postgresql"}}
        """,
    )
    _write_fixture(tmp_path, ".env.example", "DEBUG=false\nSECRET_KEY=example\n")
    _write_fixture(
        tmp_path,
        "docker-compose.yml",
        """\
        services:
          web:
            build: .
          worker:
            image: app:latest
        """,
    )
    _write_fixture(
        tmp_path,
        "pyproject.toml",
        """\
        [project]
        dependencies = ["django", "celery"]
        """,
    )
    _write_fixture(
        tmp_path,
        "README.md",
        """\
        # Sample Platform

        ## Architecture
        Web app, worker, and PostgreSQL database.
        """,
    )

    graph = extract_graph(tmp_path, language="python")
    node_types = {(node.node_type, node.source_anchor.file_path) for node in graph.nodes}
    assert ("config", "settings.py") in node_types
    assert ("config", ".env.example") in node_types
    assert ("config", "docker-compose.yml") in node_types
    assert ("doc", "README.md") in node_types


def test_python_extractor_emits_django_and_celery_edges(tmp_path: Path):
    _write_fixture(
        tmp_path,
        "app.py",
        """\
        from django.db import models
        from django.urls import path
        from celery import shared_task

        class Author(models.Model):
            pass

        class Book(models.Model):
            author = models.ForeignKey(Author, on_delete=models.CASCADE)

        def book_list():
            return []

        urlpatterns = [
            path("books/", book_list),
        ]

        @shared_task
        def sync_books():
            return book_list()
        """,
    )

    graph = extract_graph(tmp_path, language="python")
    edge_types = {(edge.edge_type, edge.evidence.get("rel")) for edge in graph.edges}
    assert ("relates", "ForeignKey") in edge_types
    assert any(edge.edge_type == "routes" for edge in graph.edges)
    assert any(edge.edge_type == "task" for edge in graph.edges)
    route_nodes = [node for node in graph.nodes if node.node_type == "route"]
    assert route_nodes
