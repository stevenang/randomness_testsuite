from math import floor as floor
from numpy import array as array
from numpy import exp as exp
from numpy import zeros as zeros
from scipy.special import gammaincc as gammaincc
from scipy.special import hyp1f1 as hyp1f1


class TemplateMatching:

    @staticmethod
    def non_overlapping_test(binary_data:str, verbose=False, template_pattern='000000001', block=8):
        """
        Note that this description is taken from the NIST documentation [1]
        [1] http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf
        The focus of this test is the number of occurrences of pre-specified target strings. The purpose of this
        test is to detect generators that produce too many occurrences of a given non-periodic (aperiodic) pattern.
        For this test and for the Overlapping Template Matching test of Section 2.8, an m-bit window is used to
        search for a specific m-bit pattern. If the pattern is not found, the window slides one bit position. If the
        pattern is found, the window is reset to the bit after the found pattern, and the search resumes.
        :param      binary_data:        The seuqnce of bit being tested
        :param      template_pattern:   The pattern to match to
        :param      verbose             True to display the debug messgae, False to turn off debug message
        :param      block               The number of independent blocks. Has been fixed at 8 in the test code.
        :return:    (p_value, bool)     A tuple which contain the p_value and result of frequency_test(True or False)
        """

        length_of_binary = len(binary_data)
        pattern_size = len(template_pattern)
        block_size = floor(length_of_binary / block)
        pattern_counts = zeros(block)

        # For each block in the data
        for count in range(block):
            block_start = count * block_size
            block_end = block_start + block_size
            block_data = binary_data[block_start:block_end]
            # Count the number of pattern hits
            inner_count = 0
            while inner_count < block_size:
                sub_block = block_data[inner_count:inner_count+pattern_size]
                if sub_block == template_pattern:
                    pattern_counts[count] += 1
                    inner_count += pattern_size
                else:
                    inner_count += 1

            # Calculate the theoretical mean and variance
            # Mean - µ = (M-m+1)/2m
            mean = (block_size - pattern_size + 1) / pow(2, pattern_size)
            # Variance - σ2 = M((1/pow(2,m)) - ((2m -1)/pow(2, 2m)))
            variance = block_size * ((1 / pow(2, pattern_size)) - (((2 * pattern_size) - 1) / (pow(2, pattern_size * 2))))

        # Calculate the xObs Squared statistic for these pattern matches
        xObs = 0
        for count in range(block):
            xObs += pow((pattern_counts[count] - mean), 2.0) / variance

        # Calculate and return the p value statistic
        p_value = gammaincc((block / 2), (xObs / 2))

        if verbose:
            print('Non-Overlapping Template Test DEBUG BEGIN:')
            print("\tLength of input:\t\t", length_of_binary)
            print('\tValue of Mean (µ):\t\t', mean)
            print('\tValue of Variance(σ):\t', variance)
            print('\tValue of W:\t\t\t\t', pattern_counts)
            print('\tValue of xObs:\t\t\t', xObs)
            print('\tP-Value:\t\t\t\t', p_value)
            print('DEBUG END.')

        return (p_value, (p_value >= 0.01))

    @staticmethod
    def overlapping_patterns(binary_data:str, verbose=False, pattern_size=9, block_size=1032):
        """
        Note that this description is taken from the NIST documentation [1]
        [1] http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf
        The focus of the Overlapping Template Matching test is the number of occurrences of pre-specified target
        strings. Both this test and the Non-overlapping Template Matching test of Section 2.7 use an m-bit
        window to search for a specific m-bit pattern. As with the test in Section 2.7, if the pattern is not found,
        the window slides one bit position. The difference between this test and the test in Section 2.7 is that
        when the pattern is found, the window slides only one bit before resuming the search.

        :param      binary_data:    a binary string
        :param      verbose         True to display the debug messgae, False to turn off debug message
        :param      pattern_size:   the length of the pattern
        :param      block_size:     the length of the block
        :return:    (p_value, bool) A tuple which contain the p_value and result of frequency_test(True or False)
        """
        length_of_binary_data = len(binary_data)
        pattern = ''
        for count in range(pattern_size):
            pattern += '1'

        number_of_block = floor(length_of_binary_data / block_size)

        # λ = (M-m+1)/pow(2, m)
        lambda_val = float(block_size - pattern_size + 1) / pow(2, pattern_size)
        # η = λ/2
        eta = lambda_val / 2.0

        pi = [TemplateMatching.get_prob(i, eta) for i in range(5)]
        diff = float(array(pi).sum())
        pi.append(1.0 - diff)

        pattern_counts = zeros(6)
        for i in range(number_of_block):
            block_start = i * block_size
            block_end = block_start + block_size
            block_data = binary_data[block_start:block_end]
            # Count the number of pattern hits
            pattern_count = 0
            j = 0
            while j < block_size:
                sub_block = block_data[j:j + pattern_size]
                if sub_block == pattern:
                    pattern_count += 1
                j += 1
            if pattern_count <= 4:
                pattern_counts[pattern_count] += 1
            else:
                pattern_counts[5] += 1

        xObs = 0.0
        for i in range(len(pattern_counts)):
            xObs += pow(pattern_counts[i] - number_of_block * pi[i], 2.0) / (number_of_block * pi[i])

        p_value = gammaincc(5.0 / 2.0, xObs / 2.0)

        if verbose:
            print('Overlapping Template Test DEBUG BEGIN:')
            print("\tLength of input:\t\t", length_of_binary_data)
            print('\tValue of Vs:\t\t\t', pattern_counts)
            print('\tValue of xObs:\t\t\t', xObs)
            print('\tP-Value:\t\t\t\t', p_value)
            print('DEBUG END.')


        return (p_value, (p_value >= 0.01))

    @staticmethod
    def get_prob(u, x):
        out = 1.0 * exp(-x)
        if u != 0:
            out = 1.0 * x * exp(2 * -x) * (2 ** -u) * hyp1f1(u + 1, 2, x)
        return out