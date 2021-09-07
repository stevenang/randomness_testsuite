from math import fabs as fabs
from math import floor as floor
from math import log as log
from math import sqrt as sqrt
from numpy import where as where
from scipy import fftpack as sff
from scipy.special import erfc as erfc

class SpectralTest:

    @staticmethod
    def spectral_test(binary_data:str, verbose=False):
        """
        Note that this description is taken from the NIST documentation [1]
        [1] http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf
        The focus of this test is the peak heights in the Discrete Fourier Transform of the sequence. The purpose of
        this test is to detect periodic features (i.e., repetitive patterns that are near each other) in the tested
        sequence that would indicate a deviation from the assumption of randomness. The intention is to detect whether
        the number of peaks exceeding the 95 % threshold is significantly different than 5 %.

        :param      binary_data:        The seuqnce of bit being tested
        :param      verbose             True to display the debug messgae, False to turn off debug message
        :return:    (p_value, bool)     A tuple which contain the p_value and result of frequency_test(True or False)
        """
        length_of_binary_data = len(binary_data)
        plus_one_minus_one = []

        # Step 1 - The zeros and ones of the input sequence (ε) are converted to values of –1 and +1
        # to create the sequence X = x1, x2, …, xn, where xi = 2εi – 1.
        for char in binary_data:
            if char == '0':
                plus_one_minus_one.append(-1)
            elif char == '1':
                plus_one_minus_one.append(1)

        # Step 2 - Apply a Discrete Fourier transform (DFT) on X to produce: S = DFT(X).
        # A sequence of complex variables is produced which represents periodic
        # components of the sequence of bits at different frequencies
        spectral = sff.fft(plus_one_minus_one)

        # Step 3 - Calculate M = modulus(S´) ≡ |S'|, where S´ is the substring consisting of the first n/2
        # elements in S, and the modulus function produces a sequence of peak heights.
        slice = floor(length_of_binary_data / 2)
        modulus = abs(spectral[0:slice])

        # Step 4 - Compute T = sqrt(log(1 / 0.05) * length_of_string) the 95 % peak height threshold value.
        # Under an assumption of randomness, 95 % of the values obtained from the test should not exceed T.
        tau = sqrt(log(1 / 0.05) * length_of_binary_data)

        # Step 5 - Compute N0 = .95n/2. N0 is the expected theoretical (95 %) number of peaks
        # (under the assumption of randomness) that are less than T.
        n0 = 0.95 * (length_of_binary_data / 2)

        # Step 6 - Compute N1 = the actual observed number of peaks in M that are less than T.
        n1 = len(where(modulus < tau)[0])

        # Step 7 - Compute d = (n_1 - n_0) / sqrt (length_of_string * (0.95) * (0.05) / 4)
        d = (n1 - n0) / sqrt(length_of_binary_data * (0.95) * (0.05) / 4)

        # Step 8 - Compute p_value = erfc(abs(d)/sqrt(2))
        p_value = erfc(fabs(d) / sqrt(2))

        if verbose:
            print('Discrete Fourier Transform (Spectral) Test DEBUG BEGIN:')
            print('\tLength of Binary Data:\t', length_of_binary_data)
            print('\tValue of T:\t\t\t\t', tau)
            print('\tValue of n1:\t\t\t', n1)
            print('\tValue of n0:\t\t\t', n0)
            print('\tValue of d:\t\t\t\t', d)
            print('\tP-Value:\t\t\t\t', p_value)
            print('DEBUG END.')

        return (p_value, (p_value >= 0.01))
