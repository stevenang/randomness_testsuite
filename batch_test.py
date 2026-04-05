#!/usr/bin/env python3
"""
Batch randomness testing per NIST SP 800-22 Section 4.

Reads multiple binary sequences (one per line) from a file, runs all 15
statistical tests on each sequence, then reports:
  - Proportion of sequences passing each test (with NIST confidence interval)
  - P-value uniformity across sequences (chi-square over 10 subintervals)

Usage:
    python3 batch_test.py <sequences_file>

The sequences file must be a plain text file with one binary string (only
'0' and '1' characters) per line.  Lines that are empty or contain
non-binary characters are silently skipped.

For Random Excursions and Random Excursions Variant, all states that appear
in at least one sequence are reported individually.
"""

import sys
from math import sqrt
from numpy import histogram as np_histogram
from scipy.special import gammaincc

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

ALPHA = 0.01
UNIFORMITY_THRESHOLD = 0.0001


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _extract(result):
    """
    Return the p-value from a standard test result tuple, or None if the
    test was skipped / returned an error.

    Handles:
      (p_value, bool)             – normal result
      (p_value, bool, error_str)  – new error format (3-tuple)
      (-1.0, False)               – legacy error format
    """
    if len(result) >= 3:
        return None
    p = float(result[0])
    return None if p < 0 else p


def _run_all(binary_data):
    """
    Run all 15 NIST tests on *binary_data*.

    Returns a dict mapping test-name -> p_value (float) or None (skipped).
    Serial produces two entries; Random Excursions and its Variant produce
    one entry per state encountered.
    """
    out = {}

    out['Frequency (Monobit)']     = _extract(FrequencyTest.monobit_test(binary_data))
    out['Block Frequency']         = _extract(FrequencyTest.block_frequency(binary_data))
    out['Runs']                    = _extract(RunTest.run_test(binary_data))
    out['Longest Run of Ones']     = _extract(RunTest.longest_one_block_test(binary_data))
    out['Binary Matrix Rank']      = _extract(Matrix.binary_matrix_rank_text(binary_data))
    out['Spectral (DFT)']          = _extract(SpectralTest.spectral_test(binary_data))
    out['Non-overlapping Template']= _extract(TemplateMatching.non_overlapping_test(binary_data))
    out['Overlapping Template']    = _extract(TemplateMatching.overlapping_patterns(binary_data))
    out["Maurer's Universal"]      = _extract(Universal.statistical_test(binary_data))
    out['Linear Complexity']       = _extract(ComplexityTest.linear_complexity_test(binary_data))

    serial = Serial.serial_test(binary_data)
    out['Serial (1)'] = float(serial[0][0])
    out['Serial (2)'] = float(serial[1][0])

    out['Approximate Entropy']     = _extract(ApproximateEntropy.approximate_entropy_test(binary_data))
    out['Cumulative Sums (Fwd)']   = _extract(CumulativeSums.cumulative_sums_test(binary_data, 0))
    out['Cumulative Sums (Bwd)']   = _extract(CumulativeSums.cumulative_sums_test(binary_data, 1))

    # Random Excursions – one entry per state
    for state_str, _, _, p_val, _ in RandomExcursions.random_excursions_test(binary_data):
        key = f'Random Excursions ({state_str})'
        out[key] = float(p_val) if p_val != 0.0 else None

    # Random Excursions Variant – one entry per state
    for state_str, _, _, p_val, _ in RandomExcursions.variant_test(binary_data):
        key = f'RE Variant ({state_str})'
        out[key] = float(p_val) if p_val is not None else None

    return out


# ---------------------------------------------------------------------------
# NIST Section 4 analysis
# ---------------------------------------------------------------------------

def _proportion_analysis(p_values):
    """
    NIST SP 800-22 Section 4.2.1 – Proportion of Sequences Passing a Test.

    Returns (proportion, m, status) where status is 'PASS', 'FAIL', or
    'SKIP' (fewer than 1 valid p-value).
    """
    valid = [p for p in p_values if p is not None]
    m = len(valid)
    if m == 0:
        return None, 0, 'SKIP'
    passing = sum(1 for p in valid if p >= ALPHA)
    proportion = passing / m
    margin = 3 * sqrt(ALPHA * (1 - ALPHA) / m)
    lo, hi = (1 - ALPHA) - margin, (1 - ALPHA) + margin
    return proportion, m, ('PASS' if lo <= proportion <= hi else 'FAIL')


def _uniformity_analysis(p_values):
    """
    NIST SP 800-22 Section 4.2.2 – Uniform Distribution of P-values.

    Divides [0, 1) into 10 equal subintervals, computes chi-square, and
    returns (p_T, status) where status is 'PASS', 'FAIL', or 'SKIP'.
    """
    valid = [p for p in p_values if p is not None]
    if len(valid) < 10:
        return None, 'SKIP'
    counts, _ = np_histogram(valid, bins=[i / 10.0 for i in range(11)])
    expected = len(valid) / 10.0
    chi_sq = sum((c - expected) ** 2 / expected for c in counts)
    p_T = float(gammaincc(9.0 / 2.0, chi_sq / 2.0))
    return p_T, ('PASS' if p_T >= UNIFORMITY_THRESHOLD else 'FAIL')


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) != 2:
        print('Usage: python3 batch_test.py <sequences_file>')
        print('  sequences_file: plain text file, one binary sequence per line')
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        with open(filepath) as fh:
            sequences = [
                line.strip() for line in fh
                if line.strip() and all(c in '01' for c in line.strip())
            ]
    except OSError as exc:
        print(f'Error opening file: {exc}')
        sys.exit(1)

    if not sequences:
        print(f'No valid binary sequences found in {filepath}')
        sys.exit(1)

    m = len(sequences)
    print(f'Loaded {m} sequences from {filepath}\n')

    # Accumulate p-values per test name across all sequences
    accumulated = {}
    for i, seq in enumerate(sequences, 1):
        print(f'\rRunning tests: {i}/{m}', end='', flush=True)
        for test_name, p_val in _run_all(seq).items():
            accumulated.setdefault(test_name, []).append(p_val)
    print('\n')

    # Confidence interval bounds for proportion check (printed once in header)
    margin = 3 * sqrt(ALPHA * (1 - ALPHA) / m)
    lo, hi = (1 - ALPHA) - margin, (1 - ALPHA) + margin

    # Print results table
    name_w = 34
    header = (
        f'{"Test":<{name_w}} '
        f'{"Proportion":>10}  {"m":>6}  {"Prop.":>5}  '
        f'{"Unif. p-T":>10}  {"Unif.":>5}'
    )
    print(header)
    print(f'Acceptable proportion range: [{lo:.4f}, {hi:.4f}]  '
          f'(α={ALPHA}, m={m})')
    print('-' * len(header))

    for test_name, p_vals in accumulated.items():
        proportion, count, prop_status = _proportion_analysis(p_vals)
        p_T, unif_status = _uniformity_analysis(p_vals)

        prop_str  = f'{proportion:.4f}' if proportion is not None else '   N/A'
        count_str = str(count)
        p_T_str   = f'{p_T:.6f}' if p_T is not None else '       N/A'

        print(
            f'{test_name:<{name_w}} '
            f'{prop_str:>10}  {count_str:>6}  {prop_status:>5}  '
            f'{p_T_str:>10}  {unif_status:>5}'
        )


if __name__ == '__main__':
    main()
