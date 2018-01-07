from math import isnan as isnan
from numpy import abs as abs
from numpy import append as append
from numpy import array as array
from numpy import clip as clip
from numpy import cumsum as cumsum
from numpy import ones as ones
from numpy import sqrt as sqrt
from numpy import sum as sum
from numpy import transpose as transpose
from numpy import where as where
from numpy import zeros as zeros
from scipy.special import erfc as erfc
from scipy.special import gammaincc as gammaincc

class RandomExcursions:

    @staticmethod
    def random_excursions_test(binary_data:str, verbose=False, state=1):
        """
        from the NIST documentation http://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-22r1a.pdf

        The focus of this test is the total number of times that a particular state is visited (i.e., occurs) in a
        cumulative sum random walk. The purpose of this test is to detect deviations from the expected number
        of visits to various states in the random walk. This test is actually a series of eighteen tests (and
        conclusions), one test and conclusion for each of the states: -9, -8, …, -1 and +1, +2, …, +9.

        :param      binary_data:    a binary string
        :param      verbose         True to display the debug messgae, False to turn off debug message
        :return:    (p_value, bool) A tuple which contain the p_value and result of frequency_test(True or False)
        """

        length_of_binary_data = len(binary_data)
        # Form the normalized (-1, +1) sequence X in which the zeros and ones of the input sequence (ε)
        # are converted to values of –1 and +1 via X = X1, X2, … , Xn, where Xi = 2εi – 1.
        sequence_x = zeros(length_of_binary_data)
        for i in range(len(binary_data)):
            if binary_data[i] == '0':
                sequence_x[i] = -1.0
            else:
                sequence_x[i] = 1.0

        # Compute partial sums Si of successively larger subsequences, each starting with x1. Form the set S
        cumulative_sum = cumsum(sequence_x)

        # Form a new sequence S' by attaching zeros before and after the set S. That is, S' = 0, s1, s2, … , sn, 0.
        cumulative_sum = append(cumulative_sum, [0])
        cumulative_sum = append([0], cumulative_sum)

        # These are the states we are going to look at
        x_values = array([-4, -3, -2, -1, 1, 2, 3, 4])
        index = x_values.tolist().index(state)

        # Identify all the locations where the cumulative sum revisits 0
        position = where(cumulative_sum == 0)[0]
        # For this identify all the cycles
        cycles = []
        for pos in range(len(position) - 1):
            # Add this cycle to the list of cycles
            cycles.append(cumulative_sum[position[pos]:position[pos + 1] + 1])
        num_cycles = len(cycles)

        state_count = []
        for cycle in cycles:
            # Determine the number of times each cycle visits each state
            state_count.append(([len(where(cycle == state)[0]) for state in x_values]))
        state_count = transpose(clip(state_count, 0, 5))

        su = []
        for cycle in range(6):
            su.append([(sct == cycle).sum() for sct in state_count])
        su = transpose(su)

        pi = ([([RandomExcursions.get_pi_value(uu, state) for uu in range(6)]) for state in x_values])
        inner_term = num_cycles * array(pi)
        xObs = sum(1.0 * (array(su) - inner_term) ** 2 / inner_term, axis=1)
        p_values = ([gammaincc(2.5, cs / 2.0) for cs in xObs])

        if verbose:
            print('Random Excursion Test DEBUG BEGIN:')
            print("\tLength of input:\t", length_of_binary_data)
            count = 0
            print('\t\t STATE \t\t\t xObs \t\t\t\t\t\t p_value  \t\t\t\t\t Result')
            for item in p_values:
                print('\t\t', repr(x_values[count]).rjust(2), ' \t\t ', xObs[count],' \t\t ', repr(item).rjust(21), ' \t\t\t ', (item >= 0.01))
                count += 1
            print('DEBUG END.')

        states = ['-4', '-3', '-2', '-1', '+1', '+2', '+3', '+4',]
        result = []
        count = 0
        for item in p_values:
            result.append((states[count], x_values[count], xObs[count], item, (item >= 0.01)))
            count += 1

        return result

    @staticmethod
    def variant_test(binary_data:str, verbose=False):
        """
        from the NIST documentation http://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-22r1a.pdf

        :param binary_data:
        :param verbose:
        :return:
        """
        length_of_binary_data = len(binary_data)
        int_data = zeros(length_of_binary_data)

        for count in range(length_of_binary_data):
            int_data[count] = int(binary_data[count])

        sum_int = (2 * int_data) - ones(len(int_data))
        cumulative_sum = cumsum(sum_int)

        li_data = []
        index = []
        for count in sorted(set(cumulative_sum)):
            if abs(count) <= 9:
                index.append(count)
                li_data.append([count, len(where(cumulative_sum == count)[0])])

        j = RandomExcursions.get_frequency(li_data, 0) + 1

        p_values = []
        for count in (sorted(set(index))):
            if not count == 0:
                den = sqrt(2 * j * (4 * abs(count) - 2))
                p_values.append(erfc(abs(RandomExcursions.get_frequency(li_data, count) - j) / den))

        count = 0
        # Remove 0 from li_data so the number of element will be equal to p_values
        for data in li_data:
            if data[0] == 0:
                li_data.remove(data)
                index.remove(0)
                break
            count += 1

        if verbose:
            print('Random Excursion Variant Test DEBUG BEGIN:')
            print("\tLength of input:\t", length_of_binary_data)
            print('\tValue of j:\t\t', j)
            print('\tP-Values:')
            print('\t\t STATE \t\t COUNTS \t\t P-Value \t\t Conclusion')
            count = 0
            for item in p_values:
                print('\t\t', repr(li_data[count][0]).rjust(4), '\t\t', li_data[count][1], '\t\t', repr(item).ljust(14), '\t\t', (item >= 0.01))
                count += 1
            print('DEBUG END.')


        states = []
        for item in index:
            if item < 0:
                states.append(str(item))
            else:
                states.append('+' + str(item))

        result = []
        count = 0
        for item in p_values:
            result.append((states[count], li_data[count][0], li_data[count][1], item, (item >= 0.01)))
            count += 1

        return result

    @staticmethod
    def get_pi_value(k, x):
        """
        This method is used by the random_excursions method to get expected probabilities
        """
        if k == 0:
            out = 1 - 1.0 / (2 * abs(x))
        elif k >= 5:
            out = (1.0 / (2 * abs(x))) * (1 - 1.0 / (2 * abs(x))) ** 4
        else:
            out = (1.0 / (4 * x * x)) * (1 - 1.0 / (2 * abs(x))) ** (k - 1)
        return out

    @staticmethod
    def get_frequency(list_data, trigger):
        """
        This method is used by the random_excursions_variant method to get frequencies
        """
        frequency = 0
        for (x, y) in list_data:
            if x == trigger:
                frequency = y
        return frequency