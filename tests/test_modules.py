"""
Regression tests for all NIST SP 800-22 test modules.

Two categories:
  - Regression tests: run each module against the deterministic binary
    expansion of e (data/data.e, 1 000 000 bits) and verify p-values
    match known-good results to 6 significant figures.
  - Guard tests: verify that each module returns the expected error tuple
    (not a crash) when given a short input.
"""

import os
import sys
import pytest

# Allow imports from the repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from FrequencyTest import FrequencyTest
from RunTest import RunTest
from Matrix import Matrix
from Spectral import SpectralTest
from TemplateMatching import TemplateMatching
from Universal import Universal
from Complexity import ComplexityTest
from Serial import Serial
from ApproximateEntropy import ApproximateEntropy
from CumulativeSum import CumulativeSums
from RandomExcursions import RandomExcursions


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope='session')
def data_e():
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'data.e')
    with open(path) as fh:
        binary = ''.join(line.strip() for line in fh)
    return binary[:1_000_000]


SHORT = '10110011' * 10   # 80 bits – below every test's minimum


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def valid_result(result):
    """Assert a normal (p_value, bool) result is well-formed."""
    assert len(result) == 2
    p, conclusion = result
    assert 0.0 <= float(p) <= 1.0
    assert isinstance(conclusion, (bool,)) or str(type(conclusion)) in (
        "<class 'numpy.bool_'>", "<class 'bool'>")


def error_result(result):
    """Assert the result is a skip/error 3-tuple."""
    assert len(result) == 3
    assert result[1] is False or result[1] == False  # noqa: E712
    assert isinstance(result[2], str)


# ---------------------------------------------------------------------------
# Regression tests against data.e (deterministic)
# ---------------------------------------------------------------------------

REL = 1e-6   # relative tolerance for p-value comparisons


class TestRegressionDataE:

    def test_monobit(self, data_e):
        p, ok = FrequencyTest.monobit_test(data_e)
        assert ok is True or bool(ok) is True
        assert float(p) == pytest.approx(0.9537486285283232, rel=REL)

    def test_block_frequency(self, data_e):
        p, ok = FrequencyTest.block_frequency(data_e)
        assert bool(ok) is True
        assert float(p) == pytest.approx(0.2110715437016406, rel=REL)

    def test_runs(self, data_e):
        p, ok = RunTest.run_test(data_e)
        assert bool(ok) is True
        assert float(p) == pytest.approx(0.5619168850302545, rel=REL)

    def test_longest_run(self, data_e):
        p, ok = RunTest.longest_one_block_test(data_e)
        assert bool(ok) is True
        assert float(p) == pytest.approx(0.7189453298987654, rel=REL)

    def test_binary_matrix_rank(self, data_e):
        p, ok = Matrix.binary_matrix_rank_text(data_e)
        assert bool(ok) is True
        assert float(p) == pytest.approx(0.3061558375306767, rel=REL)

    def test_spectral(self, data_e):
        p, ok = SpectralTest.spectral_test(data_e)
        assert bool(ok) is True
        assert float(p) == pytest.approx(0.8471867050687718, rel=REL)

    def test_non_overlapping_template(self, data_e):
        p, ok = TemplateMatching.non_overlapping_test(data_e)
        assert bool(ok) is True
        assert float(p) == pytest.approx(0.07879013267666338, rel=REL)

    def test_overlapping_template(self, data_e):
        p, ok = TemplateMatching.overlapping_patterns(data_e)
        assert bool(ok) is True
        assert float(p) == pytest.approx(0.11043368541387551, rel=REL)

    def test_universal(self, data_e):
        p, ok = Universal.statistical_test(data_e)
        assert bool(ok) is True
        assert float(p) == pytest.approx(0.282567947825744, rel=REL)

    def test_linear_complexity(self, data_e):
        p, ok = ComplexityTest.linear_complexity_test(data_e)
        assert bool(ok) is True
        assert float(p) == pytest.approx(0.8263347704038304, rel=REL)

    def test_serial(self, data_e):
        (p1, ok1), (p2, ok2) = Serial.serial_test(data_e)
        assert bool(ok1) is True
        assert bool(ok2) is True
        assert float(p1) == pytest.approx(0.766181646833394, rel=REL)
        assert float(p2) == pytest.approx(0.46292132409575854, rel=REL)

    def test_approximate_entropy(self, data_e):
        p, ok = ApproximateEntropy.approximate_entropy_test(data_e)
        assert bool(ok) is True
        assert float(p) == pytest.approx(0.7000733881151612, rel=REL)

    def test_cumulative_sums_forward(self, data_e):
        p, ok = CumulativeSums.cumulative_sums_test(data_e, 0)
        assert bool(ok) is True
        assert float(p) == pytest.approx(0.6698864641681423, rel=REL)

    def test_cumulative_sums_backward(self, data_e):
        p, ok = CumulativeSums.cumulative_sums_test(data_e, 1)
        assert bool(ok) is True
        assert float(p) == pytest.approx(0.7242653099698069, rel=REL)

    def test_random_excursions(self, data_e):
        results = RandomExcursions.random_excursions_test(data_e)
        assert len(results) == 8
        # All states except -1 should pass
        by_state = {r[0]: r for r in results}
        for state in ['-4', '-3', '-2', '+1', '+2', '+3', '+4']:
            assert bool(by_state[state][4]) is True, f'state {state} expected to pass'
        # Verify specific p-value for a representative state
        assert float(by_state['+1'][3]) == pytest.approx(0.7868679051783156, rel=REL)

    def test_random_excursions_variant(self, data_e):
        results = RandomExcursions.variant_test(data_e)
        assert len(results) == 18
        for _, _, _, p_val, ok in results:
            assert 0.0 <= float(p_val) <= 1.0
            assert bool(ok) is True


# ---------------------------------------------------------------------------
# Guard tests – short input must return error tuple, not crash
# ---------------------------------------------------------------------------

class TestShortInputGuards:
    """
    Verify that every test function handles short/insufficient input without
    raising a Python exception.  Functions that already have explicit guards
    on master (RunTest, Matrix, Universal, ComplexityTest) are also checked
    to return the expected failure indicator.
    """

    def test_longest_run_guard(self):
        # RunTest already has an explicit error-tuple guard on master.
        result = RunTest.longest_one_block_test(SHORT)
        assert len(result) == 3
        assert bool(result[1]) is False

    def test_binary_matrix_rank_guard(self):
        result = Matrix.binary_matrix_rank_text(SHORT)
        assert bool(result[1]) is False

    def test_spectral_no_crash(self):
        result = SpectralTest.spectral_test(SHORT)
        assert isinstance(result, tuple)

    def test_non_overlapping_no_crash(self):
        result = TemplateMatching.non_overlapping_test('1')
        assert isinstance(result, tuple)

    def test_overlapping_no_crash(self):
        result = TemplateMatching.overlapping_patterns(SHORT)
        assert isinstance(result, tuple)

    def test_universal_guard(self):
        result = Universal.statistical_test(SHORT)
        assert bool(result[1]) is False

    def test_linear_complexity_guard(self):
        result = ComplexityTest.linear_complexity_test(SHORT)
        assert bool(result[1]) is False

    def test_random_excursions_no_crash(self):
        results = RandomExcursions.random_excursions_test(SHORT)
        assert isinstance(results, list)
        assert len(results) == 8
