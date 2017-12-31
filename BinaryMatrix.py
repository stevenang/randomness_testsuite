from copy import copy as copy

class BinaryMatrix:

    def __init__(self, matrix, rows, cols):
        """
        This class contains the algorithm specified in the NIST suite for computing the **binary rank** of a matrix.
        :param matrix: the matrix we want to compute the rank for
        :param rows: the number of rows
        :param cols: the number of columns
        :return: a BinaryMatrix object
        """
        self.M = rows
        self.Q = cols
        self.A = matrix
        self.m = min(rows, cols)

    def compute_rank(self, verbose=False):
        """
        This method computes the binary rank of self.matrix
        :param verbose: if this is true it prints out the matrix after the forward elimination and backward elimination
        operations on the rows. This was used to testing the method to check it is working as expected.
        :return: the rank of the matrix.
        """
        if verbose:
            print("Original Matrix\n", self.A)

        i = 0
        while i < self.m - 1:
            if self.A[i][i] == 1:
                self.perform_row_operations(i, True)
            else:
                found = self.find_unit_element_swap(i, True)
                if found == 1:
                    self.perform_row_operations(i, True)
            i += 1

        if verbose:
            print("Intermediate Matrix\n", self.A)

        i = self.m - 1
        while i > 0:
            if self.A[i][i] == 1:
                self.perform_row_operations(i, False)
            else:
                if self.find_unit_element_swap(i, False) == 1:
                    self.perform_row_operations(i, False)
            i -= 1

        if verbose:
            print("Final Matrix\n", self.A)

        return self.determine_rank()

    def perform_row_operations(self, i, forward_elimination):
        """
        This method performs the elementary row operations. This involves xor'ing up to two rows together depending on
        whether or not certain elements in the matrix contain 1's if the "current" element does not.
        :param i: the current index we are are looking at
        :param forward_elimination: True or False.
        """
        if forward_elimination:
            j = i + 1
            while j < self.M:
                if self.A[j][i] == 1:
                    self.A[j, :] = (self.A[j, :] + self.A[i, :]) % 2
                j += 1
        else:
            j = i - 1
            while j >= 0:
                if self.A[j][i] == 1:
                    self.A[j, :] = (self.A[j, :] + self.A[i, :]) % 2
                j -= 1

    def find_unit_element_swap(self, i, forward_elimination):
        """
        This given an index which does not contain a 1 this searches through the rows below the index to see which rows
        contain 1's, if they do then they swapped. This is done on the forward and backward elimination
        :param i: the current index we are looking at
        :param forward_elimination: True or False.
        """
        row_op = 0
        if forward_elimination:
            index = i + 1
            while index < self.M and self.A[index][i] == 0:
                index += 1
            if index < self.M:
                row_op = self.swap_rows(i, index)
        else:
            index = i - 1
            while index >= 0 and self.A[index][i] == 0:
                index -= 1
            if index >= 0:
                row_op = self.swap_rows(i, index)
        return row_op

    def swap_rows(self, i, ix):
        """
        This method just swaps two rows in a matrix. Had to use the copy package to ensure no memory leakage
        :param i: the first row we want to swap and
        :param ix: the row we want to swap it with
        :return: 1
        """
        temp = copy(self.A[i, :])
        self.A[i, :] = self.A[ix, :]
        self.A[ix, :] = temp
        return 1

    def determine_rank(self):
        """
        This method determines the rank of the transformed matrix
        :return: the rank of the transformed matrix
        """
        rank = self.m
        i = 0
        while i < self.M:
            all_zeros = 1
            for j in range(self.Q):
                if self.A[i][j] == 1:
                    all_zeros = 0
            if all_zeros == 1:
                rank -= 1
            i += 1
        return rank