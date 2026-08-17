import itertools
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from Algoritmos.Backtracking import Backtracking
from Algoritmos.BranchAndBound import BranchAndBound
from Algoritmos.EstrategiaGulosa import EstrategiaGulosa
from Algoritmos.ProgramacaoDinamica import ProgramacaoDinamica
from Algoritmos.TwoOpt import TwoOpt


def brute_force_optimal(matrix):
    n = len(matrix) - 1
    cities = list(range(1, n + 1))
    best_distance = float("inf")
    best_route = None

    for perm in itertools.permutations(cities):
        route = (0,) + perm + (0,)
        dist = sum(matrix[route[i]][route[i + 1]] for i in range(len(route) - 1))
        if dist < best_distance:
            best_distance = dist
            best_route = route

    return best_distance, best_route


def small_matrix():
    return [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]


def test_exact_algorithms_match_optimal_distance():
    matrix = small_matrix()
    expected_distance, _ = brute_force_optimal(matrix)

    for cls in [Backtracking, BranchAndBound, ProgramacaoDinamica]:
        distance, route, states = cls(matrix).resolver()
        assert distance == pytest.approx(expected_distance, rel=1e-6, abs=1e-6), (
            cls.__name__, distance, expected_distance, route, states
        )


def test_heuristics_produce_feasible_routes():
    matrix = small_matrix()
    expected_distance, _ = brute_force_optimal(matrix)

    for cls in [EstrategiaGulosa, TwoOpt]:
        distance, route, states = cls(matrix).resolver()
        assert len(route) == len(matrix) - 1, (cls.__name__, route)
        assert set(route) == set(range(1, len(matrix))), (cls.__name__, route)
        assert distance >= 0, (cls.__name__, distance)
        assert distance <= expected_distance * 1.5, (
            cls.__name__, distance, expected_distance
        )


def test_benchmark_runner_accepts_small_range():
    import subprocess
    import os

    root = ROOT
    cmd = [sys.executable, "scripts/run_benchmarks.py", "--min-n", "3", "--max-n", "3", "--seed", "42"]
    result = subprocess.run(cmd, cwd=root, capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stderr or result.stdout
    assert (root / "Relatorios" / "benchmark_metrics.csv").exists()
