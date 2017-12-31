from math import fabs as fabs
from math import floor as floor
from math import sqrt as sqrt
from scipy.special import erfc as erfc
from scipy.special import gammaincc as gammaincc
from scipy import zeros as zeros

class RunTest:

    @staticmethod
    def run_test(binary_data:str, verbose=False):
        """
        The focus of this test is the total number of runs in the sequence,
        where a run is an uninterrupted sequence of identical bits.
        A run of length k consists of exactly k identical bits and is bounded before
        and after with a bit of the opposite value. The purpose of the runs test is to
        determine whether the number of runs of ones and zeros of various lengths is as
        expected for a random sequence. In particular, this test determines whether the
        oscillation between such zeros and ones is too fast or too slow.

        :param      binary_data:        The seuqnce of bit being tested
        :param      verbose             True to display the debug messgae, False to turn off debug message
        :return:    (p_value, bool)     A tuple which contain the p_value and result of frequency_test(True or False)
        """
        one_count = 0
        vObs = 0
        length_of_binary_data = len(binary_data)

        # Predefined tau = 2 / sqrt(n)
        # TODO Confirm with Frank about the discrepancy between the formula and the sample of 2.3.8
        tau = 2 / sqrt(length_of_binary_data)

        # Step 1 - Compute the pre-test proportion πof ones in the input sequence: π = Σjεj / n
        one_count = binary_data.count('1')

        pi = one_count / length_of_binary_data

        # Step 2 - If it can be shown that absolute value of (π - 0.5) is greater than or equal to tau
        # then the run test need not be performed.
        if abs(pi - 0.5) >= tau:
            ##print("The test should not have been run because of a failure to pass test 1, the Frequency (Monobit) test.")
            return (0.0000, False)
        else:
            # Step 3 - Compute vObs
            for item in range(1, length_of_binary_data):
                if binary_data[item] != binary_data[item - 1]:
                    vObs += 1
            vObs += 1

            # Step 4 - Compute p_value = erfc((|vObs − 2nπ * (1−π)|)/(2 * sqrt(2n) * π * (1−π)))
            p_value = erfc(abs(vObs - (2 * (length_of_binary_data) * pi * (1 - pi))) / (2 * sqrt(2 * length_of_binary_data) * pi * (1 - pi)))

        if verbose:
            print('Run Test DEBUG BEGIN:')
            print("\tLength of input:\t\t\t\t", length_of_binary_data)
            print("\tTau (2/sqrt(length of input)):\t", tau)
            print('\t# of \'1\':\t\t\t\t\t\t', one_count)
            print('\t# of \'0\':\t\t\t\t\t\t', binary_data.count('0'))
            print('\tPI (1 count / length of input):\t', pi)
            print('\tvObs:\t\t\t\t\t\t\t', vObs)
            print('\tP-Value:\t\t\t\t\t\t', p_value)
            print('DEBUG END.')

        return (p_value, (p_value > 0.01))

    @staticmethod
    def longest_one_block_test(binary_data:str, verbose=False):
        """
        The focus of the test is the longest run of ones within M-bit blocks. The purpose of this test is to determine
        whether the length of the longest run of ones within the tested sequence is consistent with the length of the
        longest run of ones that would be expected in a random sequence. Note that an irregularity in the expected
        length of the longest run of ones implies that there is also an irregularity in the expected length of the
        longest run of zeroes. Therefore, only a test for ones is necessary.

        :param      binary_data:        The sequence of bits being tested
        :param      verbose             True to display the debug messgae, False to turn off debug message
        :return:    (p_value, bool)     A tuple which contain the p_value and result of frequency_test(True or False)
        """
        length_of_binary_data = len(binary_data)
        # print('Length of binary string: ', length_of_binary_data)

        # Initialized k, m. n, pi and v_values
        if length_of_binary_data < 128:
            # Not enough data to run this test
            return (0.00000, False, 'Error: Not enough data to run this test')
        elif length_of_binary_data < 6272:
            k = 3
            m = 8
            v_values = [1, 2, 3, 4]
            pi_values = [0.2148, 0.3672, 0.2305, 0.1875]
        elif length_of_binary_data < 750000:
            k = 5
            m = 128
            v_values = [4, 5, 6, 7, 8, 9]
            pi_values = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
        else:
            # If length_of_bit_string > 750000
            k = 6
            m = 10000
            v_values = [10, 11, 12, 13, 14, 15, 16]
            pi_values = [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]

        number_of_blocks = floor(length_of_binary_data / m)
        block_start = 0
        block_end = m
        xObs = 0
        # This will intialized an array with a number of 0 you specified.
        frequencies = zeros(k + 1)

        # print('Number of Blocks: ', number_of_blocks)

        for count in range(number_of_blocks):
            block_data = binary_data[block_start:block_end]
            max_run_count = 0
            run_count = 0

            # This will count the number of ones in the block
            for bit in block_data:
                if bit == '1':
                    run_count += 1
                    max_run_count = max(max_run_count, run_count)
                else:
                    max_run_count = max(max_run_count, run_count)
                    run_count = 0

            max(max_run_count, run_count)

            #print('Block Data: ', block_data, '. Run Count: ', max_run_count)

            if max_run_count < v_values[0]:
                frequencies[0] += 1
            for j in range(k):
                if max_run_count == v_values[j]:
                    frequencies[j] += 1
            if max_run_count > v_values[k - 1]:
                frequencies[k] += 1

            block_start += m
            block_end += m

        # print("Frequencies: ", frequencies)
        # Compute xObs
        for count in range(len(frequencies)):
            xObs += pow((frequencies[count] - (number_of_blocks * pi_values[count])), 2.0) / (
                    number_of_blocks * pi_values[count])

        p_value = gammaincc(float(k / 2), float(xObs / 2))

        if verbose:
            print('Run Test (Longest Run of Ones in a Block) DEBUG BEGIN:')
            print("\tLength of input:\t\t\t\t", length_of_binary_data)
            print("\tSize of each Block:\t\t\t\t", m)
            print('\tNumber of Block:\t\t\t\t', number_of_blocks)
            print("\tValue of K:\t\t\t\t\t\t", k)
            print('\tValue of PIs:\t\t\t\t\t', pi_values)
            print('\tFrequencies:\t\t\t\t\t', frequencies)
            print('\txObs:\t\t\t\t\t\t\t', xObs)
            print('\tP-Value:\t\t\t\t\t\t', p_value)
            print('DEBUG END.')

        return (p_value, (p_value > 0.01))