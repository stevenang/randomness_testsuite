import os
from Tools import Tools

from FrequencyTest import FrequencyTest as ft
from RunTest import RunTest as rt
from Matrix import Matrix as mt
from Spectral import SpectralTest as st
from TemplateMatching import TemplateMatching as tm
from Universal import Universal as ut
from Complexity import ComplexityTest as ct
from Serial import Serial as serial
from ApproximateEntropy import ApproximateEntropy as aet
from CumulativeSum import CumulativeSums as cst
from RandomExcursions import RandomExcursions as ret

test_type = ['01. Frequency Test (Monobit)', '02. Frequency Test within a Block', '03. Run Test',
                            '04. Longest Run of Ones in a Block', '05. Binary Matrix Rank Test',
                            '06. Discrete Fourier Transform (Spectral) Test',
                            '07. Non-Overlapping Template Matching Test',
                            '08. Overlapping Template Matching Test', '09. Maurer\'s Universal Statistical test',
                            '10. Linear Complexity Test', '11. Serial test', '12. Approximate Entropy Test',
                            '13. Cummulative Sums (Forward) Test', '14. Cummulative Sums (Reverse) Test',
                            '15. Random Excursions Test', '16. Random Excursions Variant Test']

test_function = {
            0:ft.monobit_test,
            1:ft.block_frequency,
            2:rt.run_test,
            3:rt.longest_one_block_test,
            4:mt.binary_matrix_rank_text,
            5:st.spectral_test,
            6:tm.non_overlapping_test,
            7:tm.overlapping_patterns,
            8:ut.statistical_test,
            9:ct.linear_complexity_test,
            10:serial.serial_test,
            11:aet.approximate_entropy_test,
            12:cst.cumulative_sums_test,
            13:cst.cumulative_sums_test,
            14:ret.random_excursions_test,
            15:ret.variant_test
        }

input = b''
with open(os.path.join(os.getcwd(), 'data', 'test_data.bin'), 'rb') as input_file:
   input = input_file.read()


binary = Tools.bytes_to_binary(input)
count = 0

for test in test_function:
    print(test_type[count%len(test_type)], test_function[count](binary))
    count += 1
