from math import fabs as fabs
from math import floor as floor
from math import sqrt as sqrt
from scipy.special import erfc as erfc
from scipy.special import gammaincc as gammaincc

class FrequencyTest:

    @staticmethod
    def monobit_test(binary_data:str, verbose=False):
        """
        The focus of the test is the proportion of zeroes and ones for the entire sequence.
        The purpose of this test is to determine whether the number of ones and zeros in a sequence are approximately
        the same as would be expected for a truly random sequence. The test assesses the closeness of the fraction of
        ones to 陆, that is, the number of ones and zeroes in a sequence should be about the same.
        All subsequent tests depend on the passing of this test.

        if p_value < 0.01, then conclude that the sequence is non-random (return False).
        Otherwise, conclude that the the sequence is random (return True).

        :param      binary_data         The seuqnce of bit being tested
        :param      verbose             True to display the debug messgae, False to turn off debug message
        :return:    (p_value, bool)     A tuple which contain the p_value and result of frequency_test(True or False)

        """

        length_of_bit_string = len(binary_data)

        # Variable for S(n)
        count = 0
        # Iterate each bit in the string and compute for S(n)
        for bit in binary_data:
            if bit == '0':
                # If bit is 0, then -1 from the S(n)
                count -= 1
            elif bit == '1':
                # If bit is 1, then +1 to the S(n)
                count += 1

        # Compute the test statistic
        sObs = count / sqrt(length_of_bit_string)

        # Compute p-Value
        p_value = erfc(fabs(sObs) / sqrt(2))

        if verbose:
            print('Frequency Test (Monobit Test) DEBUG BEGIN:')
            print("\tLength of input:\t", length_of_bit_string)
            print('\t# of \'0\':\t\t\t', binary_data.count('0'))
            print('\t# of \'1\':\t\t\t', binary_data.count('1'))
            print('\tS(n):\t\t\t\t', count)
            print('\tsObs:\t\t\t\t', sObs)
            print('\tf:\t\t\t\t\t',fabs(sObs) / sqrt(2))
            print('\tP-Value:\t\t\t', p_value)
            print('DEBUG END.')

        # return a p_value and randomness result
        return (p_value, (p_value >= 0.01))

    @staticmethod
    def block_frequency(binary_data:str, block_size=128, verbose=False):
        """
        The focus of the test is the proportion of ones within M-bit blocks.
        The purpose of this test is to determine whether the frequency of ones in an M-bit block is approximately M/2,
        as would be expected under an assumption of randomness.
        For block size M=1, this test degenerates to test 1, the Frequency (Monobit) test.

        :param      binary_data:        The length of each block
        :param      block_size:         The seuqnce of bit being tested
        :param      verbose             True to display the debug messgae, False to turn off debug message
        :return:    (p_value, bool)     A tuple which contain the p_value and result of frequency_test(True or False)
        """

        length_of_bit_string = len(binary_data)


        if length_of_bit_string < block_size:
            block_size = length_of_bit_string

        # Compute the number of blocks based on the input given.  Discard the remainder
        number_of_blocks = floor(length_of_bit_string / block_size)

        if number_of_blocks == 1:
            # For block size M=1, this test degenerates to test 1, the Frequency (Monobit) test.
            return FrequencyTest.monobit_test(binary_data[0:block_size])

        # Initialized variables
        block_start = 0
        block_end = block_size
        proportion_sum = 0.0

        # Create a for loop to process each block
        for counter in range(number_of_blocks):
            # Partition the input sequence and get the data for block
            block_data = binary_data[block_start:block_end]

            # Determine the proportion 蟺i of ones in each M-bit
            one_count = 0
            for bit in block_data:
                if bit == '1':
                    one_count += 1
            # compute π
            pi = one_count / block_size

            # Compute Σ(πi -½)^2.
            proportion_sum += pow(pi - 0.5, 2.0)

            # Next Block
            block_start += block_size
            block_end += block_size

        # Compute 4M Σ(πi -½)^2.
        result = 4.0 * block_size * proportion_sum

        # Compute P-Value
        p_value = gammaincc(number_of_blocks / 2, result / 2)

        if verbose:
            print('Frequency Test (Block Frequency Test) DEBUG BEGIN:')
            print("\tLength of input:\t", length_of_bit_string)
            print("\tSize of Block:\t\t", block_size)
            print('\tNumber of Blocks:\t', number_of_blocks)
            print('\tCHI Squared:\t\t', result)
            print('\t1st:\t\t\t\t', number_of_blocks / 2)
            print('\t2nd:\t\t\t\t', result / 2)
            print('\tP-Value:\t\t\t', p_value)
            print('DEBUG END.')

        return (p_value, (p_value >= 0.01))