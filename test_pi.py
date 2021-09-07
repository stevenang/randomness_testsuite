import os
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

# Open Data File and read the binary data of e
data_path = os.path.join(os.getcwd(), 'data', 'data.pi')
handle = open(data_path)
data_list = []

for line in handle:
    data_list.append(line.strip().rstrip())

binary_data = ''.join(data_list)

print('The statistical test of the Binary Expansion of PI')
print('2.1. Frequency Test:\t\t\t\t\t\t\t\t\t', FrequencyTest.monobit_test(binary_data[:1000000]))
print('2.2. Block Frequency Test:\t\t\t\t\t\t\t\t', FrequencyTest.block_frequency(binary_data[:1000000]))
print('2.3. Run Test:\t\t\t\t\t\t\t\t\t\t\t', RunTest.run_test(binary_data[:1000000]))
print('2.4. Run Test (Longest Run of Ones): \t\t\t\t\t', RunTest.longest_one_block_test(binary_data[:1000000]))
print('2.5. Binary Matrix Rank Test:\t\t\t\t\t\t\t', Matrix.binary_matrix_rank_text(binary_data[:1000000]))
print('2.6. Discrete Fourier Transform (Spectral) Test: \t\t', SpectralTest.spectral_test(binary_data[:1000000]))
print('2.7. Non-overlapping Template Matching Test:\t\t\t', TemplateMatching.non_overlapping_test(binary_data[:1000000], '000000001'))
print('2.8. Overlappong Template Matching Test: \t\t\t\t', TemplateMatching.overlapping_patterns(binary_data[:1000000]))
print('2.9. Universal Statistical Test:\t\t\t\t\t\t', Universal.statistical_test(binary_data[:1000000]))
print('2.10. Linear Complexity Test:\t\t\t\t\t\t\t', ComplexityTest.linear_complexity_test(binary_data[:1000000]))
print('2.11. Serial Test:\t\t\t\t\t\t\t\t\t\t', Serial.serial_test(binary_data[:1000000]))
print('2.12. Approximate Entropy Test:\t\t\t\t\t\t\t', ApproximateEntropy.approximate_entropy_test(binary_data[:1000000]))
print('2.13. Cumulative Sums (Forward):\t\t\t\t\t\t', CumulativeSums.cumulative_sums_test(binary_data[:1000000], 0))
print('2.13. Cumulative Sums (Backward):\t\t\t\t\t\t', CumulativeSums.cumulative_sums_test(binary_data[:1000000], 1))
result = RandomExcursions.random_excursions_test(binary_data[:1000000])
print('2.14. Random Excursion Test:')
print('\t\t STATE \t\t\t xObs \t\t\t\t P-Value \t\t\t Conclusion')

for item in result:
    print('\t\t', repr(item[0]).rjust(4), '\t\t', item[1], '\t\t', repr(item[2]).ljust(14), '\t\t',
          (item[3] >= 0.01))

result = RandomExcursions.variant_test(binary_data[:1000000])

print('2.15. Random Excursion Variant Test:\t\t\t\t\t\t')
print('\t\t STATE \t\t COUNTS \t\t\t P-Value \t\t Conclusion')
for item in result:
    print('\t\t', repr(item[0]).rjust(4), '\t\t', item[1], '\t\t', repr(item[2]).ljust(14), '\t\t',
          (item[3] >= 0.01))