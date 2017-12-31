from copy import copy as copy
from numpy import dot as dot
from numpy import histogram as histogram
from numpy import zeros as zeros
from scipy.special import gammaincc as gammaincc

class ComplexityTest:

    @staticmethod
    def linear_complexity_test(binary_data:str, verbose=False, block_size=500):
        """
        Note that this description is taken from the NIST documentation [1]
        [1] http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf
        The focus of this test is the length of a linear feedback shift register (LFSR). The purpose of this test is to
        determine whether or not the sequence is complex enough to be considered random. Random sequences are
        characterized by longer LFSRs. An LFSR that is too short implies non-randomness.

        :param      binary_data:    a binary string
        :param      verbose         True to display the debug messgae, False to turn off debug message
        :param      block_size:     Size of the block
        :return:    (p_value, bool) A tuple which contain the p_value and result of frequency_test(True or False)

        """

        length_of_binary_data = len(binary_data)

        # The number of degrees of freedom;
        # K = 6 has been hard coded into the test.
        degree_of_freedom = 6

        #  π0 = 0.010417, π1 = 0.03125, π2 = 0.125, π3 = 0.5, π4 = 0.25, π5 = 0.0625, π6 = 0.020833
        #  are the probabilities computed by the equations in Section 3.10
        pi = [0.01047, 0.03125, 0.125, 0.5, 0.25, 0.0625, 0.020833]

        t2 = (block_size / 3.0 + 2.0 / 9) / 2 ** block_size
        mean = 0.5 * block_size + (1.0 / 36) * (9 + (-1) ** (block_size + 1)) - t2

        number_of_block = int(length_of_binary_data / block_size)

        if number_of_block > 1:
            block_end = block_size
            block_start = 0
            blocks = []
            for i in range(number_of_block):
                blocks.append(binary_data[block_start:block_end])
                block_start += block_size
                block_end += block_size

            complexities = []
            for block in blocks:
                complexities.append(ComplexityTest.berlekamp_massey_algorithm(block))

            t = ([-1.0 * (((-1) ** block_size) * (chunk - mean) + 2.0 / 9) for chunk in complexities])
            vg = histogram(t, bins=[-9999999999, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 9999999999])[0][::-1]
            im = ([((vg[ii] - number_of_block * pi[ii]) ** 2) / (number_of_block * pi[ii]) for ii in range(7)])

            xObs = 0.0
            for i in range(len(pi)):
                xObs += im[i]

            # P-Value = igamc(K/2, xObs/2)
            p_value = gammaincc(degree_of_freedom / 2.0, xObs / 2.0)

            if verbose:
                print('Linear Complexity Test DEBUG BEGIN:')
                print("\tLength of input:\t", length_of_binary_data)
                print('\tLength in bits of a block:\t', )
                print("\tDegree of Freedom:\t\t", degree_of_freedom)
                print('\tNumber of Blocks:\t', number_of_block)
                print('\tValue of Vs:\t\t', vg)
                print('\txObs:\t\t\t\t', xObs)
                print('\tP-Value:\t\t\t', p_value)
                print('DEBUG END.')


            return (p_value, (p_value >= 0.01))
        else:
            return (-1.0, False)

    @staticmethod
    def berlekamp_massey_algorithm(block_data):
        """
        An implementation of the Berlekamp Massey Algorithm. Taken from Wikipedia [1]
        [1] - https://en.wikipedia.org/wiki/Berlekamp-Massey_algorithm
        The Berlekamp–Massey algorithm is an algorithm that will find the shortest linear feedback shift register (LFSR)
        for a given binary output sequence. The algorithm will also find the minimal polynomial of a linearly recurrent
        sequence in an arbitrary field. The field requirement means that the Berlekamp–Massey algorithm requires all
        non-zero elements to have a multiplicative inverse.
        :param block_data:
        :return:
        """
        n = len(block_data)
        c = zeros(n)
        b = zeros(n)
        c[0], b[0] = 1, 1
        l, m, i = 0, -1, 0
        int_data = [int(el) for el in block_data]
        while i < n:
            v = int_data[(i - l):i]
            v = v[::-1]
            cc = c[1:l + 1]
            d = (int_data[i] + dot(v, cc)) % 2
            if d == 1:
                temp = copy(c)
                p = zeros(n)
                for j in range(0, l):
                    if b[j] == 1:
                        p[j + i - m] = 1
                c = (c + p) % 2
                if l <= 0.5 * i:
                    l = i + 1 - l
                    m = i
                    b = temp
            i += 1
        return l