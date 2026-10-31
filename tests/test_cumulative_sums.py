"""Focused bounds and numerical-tail regressions for cumulative sums."""

import math
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from CumulativeSum import CumulativeSums


def reference_p_value(bits):
    """Direct small-input formula, with integer bounds and a stdlib CDF."""
    n = len(bits)
    walk = 0
    z = 0
    for bit in bits:
        walk += 1 if bit == '1' else -1
        z = max(z, abs(walk))

    def cdf(multiplier):
        return (1 + math.erf(multiplier * z / math.sqrt(2 * n))) / 2

    upper = (n - z) // (4 * z)
    first = math.fsum(cdf(4 * k + 1) - cdf(4 * k - 1)
                      for k in range((-n + z) // (4 * z), upper + 1))
    second = math.fsum(cdf(4 * k + 3) - cdf(4 * k + 1)
                       for k in range((-n - 3 * z) // (4 * z), upper + 1))
    return 1 - first + second


@pytest.mark.parametrize('bits', ['1011010111', '11110000', '10101010', '11010010', '111100'])
@pytest.mark.parametrize('mode', [0, 1])
def test_summation_bounds(bits, mode):
    # These short fixtures isolate the summation algebra, not statistical
    # validity: NIST SP 800-22 section 2.13.7 recommends at least 100 bits.
    # Below that recommendation, the approximation can even exceed one
    # (as it does for '10101010' in both modes).
    expected = reference_p_value(bits if mode == 0 else bits[::-1])
    p_value, accepted = CumulativeSums.cumulative_sums_test(bits, mode)
    assert p_value == pytest.approx(expected, rel=1e-13, abs=1e-15)
    assert bool(accepted) == (expected >= 0.01)


@pytest.mark.parametrize('mode', [0, 1])
def test_summation_bounds_at_acceptance_threshold(mode):
    bits = '1' * 28 + '01' * 36
    ordered_bits = bits if mode == 0 else bits[::-1]
    walk = 0
    z = 0
    for bit in ordered_bits:
        walk += 1 if bit == '1' else -1
        z = max(z, abs(walk))
    assert len(bits) == 100
    assert z == 28

    # Meets NIST's length recommendation. The former second-sum upper bound
    # omitted k=0, producing about 0.00766539 and an incorrect rejection.
    expected = reference_p_value(ordered_bits)
    assert expected == pytest.approx(0.010220521321711664, rel=1e-13, abs=1e-15)
    p_value, accepted = CumulativeSums.cumulative_sums_test(bits, mode)
    assert p_value == pytest.approx(expected, rel=1e-13, abs=1e-15)
    assert bool(accepted) is True


@pytest.mark.parametrize('bit', ['0', '1'])
@pytest.mark.parametrize('mode', [0, 1])
def test_strong_bias_retains_small_tail(bit, mode):
    # For n=z=100, the bounds are [0, 0] and [-1, 0]. The exact
    # formula is 4*sf(10) - 2*sf(30), expressed independently via erfc.
    expected = 2 * math.erfc(10 / math.sqrt(2)) - math.erfc(30 / math.sqrt(2))
    p_value, accepted = CumulativeSums.cumulative_sums_test(bit * 100, mode)
    assert p_value > 0
    assert p_value == pytest.approx(expected, rel=1e-13, abs=0)
    assert not accepted


def test_reverse_mode_uses_reversed_walk():
    bits = '111100'
    forward = CumulativeSums.cumulative_sums_test(bits, 0)
    backward = CumulativeSums.cumulative_sums_test(bits, 1)
    assert backward == CumulativeSums.cumulative_sums_test(bits[::-1], 0)
    assert forward[0] != backward[0]
