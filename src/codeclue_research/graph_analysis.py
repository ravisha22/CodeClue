from __future__ import annotations

from collections import defaultdict
from typing import Any

from .models import CanonicalClueGraph


def _build_adjacency(graph: CanonicalClueGraph) -> dict[str, set[str]]:
    adjacency: dict[str, set[str]] = {node.node_id: set() for node in graph.nodes}
    for edge in graph.edges:
        adjacency.setdefault(edge.from_node, set()).add(edge.to_node)
        adjacency.setdefault(edge.to_node, set())
    return adjacency


def _build_reverse_adjacency(graph: CanonicalClueGraph) -> dict[str, set[str]]:
    reverse: dict[str, set[str]] = defaultdict(set)
    for node in graph.nodes:
        reverse.setdefault(node.node_id, set())
    for edge in graph.edges:
        reverse[edge.to_node].add(edge.from_node)
        reverse.setdefault(edge.from_node, set())
    return dict(reverse)


def _reachable_from_roots(adjacency: dict[str, set[str]], roots: set[str]) -> set[str]:
    visited: set[str] = set()
    stack = list(roots)
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        for nxt in adjacency.get(current, set()):
            if nxt not in visited:
                stack.append(nxt)
    return visited


def _tarjan_scc(adjacency: dict[str, set[str]]) -> list[list[str]]:
    index = 0
    stack: list[str] = []
    on_stack: set[str] = set()
    indices: dict[str, int] = {}
    lowlink: dict[str, int] = {}
    sccs: list[list[str]] = []

    def strongconnect(v: str) -> None:
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)

        for w in adjacency.get(v, set()):
            if w not in indices:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], indices[w])

        if lowlink[v] == indices[v]:
            component: list[str] = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                component.append(w)
                if w == v:
                    break
            sccs.append(component)

    for node in adjacency:
        if node not in indices:
            strongconnect(node)

    return sccs


def _compute_dominators(
    roots: set[str],
    adjacency: dict[str, set[str]],
    reverse_adjacency: dict[str, set[str]],
) -> dict[str, set[str]]:
    all_nodes = set(adjacency.keys())
    dominators: dict[str, set[str]] = {}
    for node in all_nodes:
        dominators[node] = set(all_nodes)
    for root in roots:
        dominators[root] = {root}

    changed = True
    while changed:
        changed = False
        for node in all_nodes:
            if node in roots:
                continue
            preds = reverse_adjacency.get(node, set())
            if not preds:
                new_dom = {node}
            else:
                pred_doms = [dominators[pred] for pred in preds]
                inter = set.intersection(*pred_doms) if pred_doms else set(all_nodes)
                new_dom = inter | {node}
            if new_dom != dominators[node]:
                dominators[node] = new_dom
                changed = True

    return dominators


def analyze_graph_integrity(graph: CanonicalClueGraph) -> dict[str, Any]:
    adjacency = _build_adjacency(graph)
    reverse_adjacency = _build_reverse_adjacency(graph)
    module_roots = {node.node_id for node in graph.nodes if node.node_type == "module"}

    reachable = _reachable_from_roots(adjacency, module_roots)
    non_module_nodes = {node.node_id for node in graph.nodes if node.node_type != "module"}
    unreachable = sorted(non_module_nodes - reachable)

    degree_map = {
        node: len(adjacency.get(node, set())) + len(reverse_adjacency.get(node, set()))
        for node in adjacency
    }
    orphan_nodes = sorted(
        node for node, degree in degree_map.items() if degree == 0 and node in non_module_nodes
    )

    sccs = _tarjan_scc(adjacency)
    largest_scc = max((len(component) for component in sccs), default=0)

    dominators = _compute_dominators(module_roots, adjacency, reverse_adjacency)
    dom_sizes = [len(value) for key, value in dominators.items() if key in reachable]
    avg_dom_size = sum(dom_sizes) / len(dom_sizes) if dom_sizes else 0.0

    edge_type_counts: dict[str, int] = defaultdict(int)
    for edge in graph.edges:
        edge_type_counts[edge.edge_type] += 1

    connectivity_pass = len(unreachable) == 0
    no_gap_pass = len(orphan_nodes) == 0

    return {
        "node_count": len(graph.nodes),
        "edge_count": len(graph.edges),
        "module_roots": len(module_roots),
        "scc_count": len(sccs),
        "largest_scc": largest_scc,
        "unreachable_nodes": unreachable,
        "orphan_nodes": orphan_nodes,
        "avg_dominator_set_size": round(avg_dom_size, 4),
        "edge_type_counts": dict(edge_type_counts),
        "invariant_checks": {
            "connectivity_invariant": connectivity_pass,
            "no_gap_invariant": no_gap_pass,
        },
    }


def compare_operational_paths(
    base_graph: CanonicalClueGraph, candidate_graph: CanonicalClueGraph
) -> dict[str, Any]:
    base_nodes = {node.node_id for node in base_graph.nodes}
    cand_nodes = {node.node_id for node in candidate_graph.nodes}

    def edge_triplets(graph: CanonicalClueGraph) -> set[tuple[str, str, str]]:
        return {(e.from_node, e.to_node, e.edge_type) for e in graph.edges}

    base_edges = edge_triplets(base_graph)
    cand_edges = edge_triplets(candidate_graph)

    missing_nodes = sorted(base_nodes - cand_nodes)
    added_nodes = sorted(cand_nodes - base_nodes)
    missing_edges = sorted(base_edges - cand_edges)
    added_edges = sorted(cand_edges - base_edges)

    base_paths = len(base_edges)
    lost_paths = len(missing_edges)
    path_coverage = 1.0 if base_paths == 0 else max(0.0, 1.0 - (lost_paths / base_paths))

    return {
        "path_coverage": round(path_coverage, 6),
        "lost_path_count": lost_paths,
        "base_path_count": base_paths,
        "missing_nodes": missing_nodes,
        "added_nodes": added_nodes,
        "missing_edges": missing_edges,
        "added_edges": added_edges,
    }
