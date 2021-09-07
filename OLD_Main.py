import os
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox

from ApproximateEntropy import ApproximateEntropy as aet
from Complexity import ComplexityTest as ct
from CumulativeSum import CumulativeSums as cst
from FrequencyTest import FrequencyTest as ft
from Matrix import Matrix as mt
from RandomExcursions import RandomExcursions as ret
from RunTest import RunTest as rt
from Serial import Serial as serial
from Spectral import SpectralTest as st
from TemplateMatching import TemplateMatching as tm
from Universal import Universal as ut

from GUI import CustomButton
from GUI import Input
from GUI import LabelTag
from GUI import Options
from GUI import RandomExcursionTestItem
from GUI import TestItem

from Tools import Tools

class Main(Frame):

    # Constructor.  Initialized the variables.
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_variables()
        self.init_window()

    def init_variables(self):
        self.__test_type = ['01. Frequency Test (Monobit)', '02. Frequency Test within a Block', '03. Run Test',
                            '04. Longest Run of Ones in a Block', '05. Binary Matrix Rank Test',
                            '06. Discrete Fourier Transform (Spectral) Test',
                            '07. Non-Overlapping Template Matching Test',
                            '08. Overlapping Template Matching Test', '09. Maurer\'s Universal Statistical test',
                            '10. Linear Complexity Test', '11. Serial test', '12. Approximate Entropy Test',
                            '13. Cummulative Sums (Forward) Test', '14. Cummulative Sums (Reverse) Test',
                            '15. Random Excursions Test', '16. Random Excursions Variant Test']

        self.__test_function = {
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

        self.__test_result = []
        self.__test_string = []

    def init_window(self):

        # Title Label
        frame_title = 'A Statistical Test Suite for Random and Pseudorandom Number Generators for Cryptographic Applications'
        title_label = LabelTag(self.master, frame_title, 0, 5, 1280)

        # Setup LabelFrame for Input
        input_label_frame = LabelFrame(self.master, text="Input Data")
        input_label_frame.config(font=("Calibri", 14))
        input_label_frame.propagate(0)
        input_label_frame.place(x=20, y=30, width=1240, height=125)

        self.__binary_input = Input(input_label_frame, 'Binary Data', 10, 5)
        self.__binary_data_file_input = Input(input_label_frame, 'Binary Data File', 10, 35, True, self.select_binary_file)
        self.__string_data_file_input = Input(input_label_frame, 'String Data File', 10, 65, True, self.select_data_file)

        # Setup LabelFrame for Randomness Test
        self.__stest_selection_label_frame = LabelFrame(self.master, text="Randomness Testing", padx=5, pady=5)
        self.__stest_selection_label_frame.config(font=("Calibri", 14))
        self.__stest_selection_label_frame.place(x=20, y=155, width=1240, height=600)

        #self.__test_data = Options(self.__stest_selection_label_frame, 'Input Data', [''], 10, 5, 900)
        #change_data_button = CustomButton(self.__stest_selection_label_frame, 'Change Data', 1050, 5, 180, action=self.change_data)

        test_type_label = LabelTag(self.__stest_selection_label_frame, 'Test Type', 10, 5, 350, 12, border=2,relief="groove")
        p_value_label = LabelTag(self.__stest_selection_label_frame, 'P-Value', 365, 5, 500, 12, border=2,relief="groove")
        result_label = LabelTag(self.__stest_selection_label_frame, 'Result', 870, 5, 350, 12, border=2,relief="groove")

        self.__test = []

        self.__monobit = TestItem(self.__stest_selection_label_frame, self.__test_type[0], 10, 35)
        self.__test.append(self.__monobit)

        self.__block = TestItem(self.__stest_selection_label_frame, self.__test_type[1], 10, 60)
        self.__test.append(self.__block)

        self.__run = TestItem(self.__stest_selection_label_frame, self.__test_type[2], 10, 85)
        self.__test.append(self.__run)

        self.__long_run = TestItem(self.__stest_selection_label_frame, self.__test_type[3], 10, 110)
        self.__test.append(self.__long_run)

        self.__rank = TestItem(self.__stest_selection_label_frame, self.__test_type[4], 10, 135)
        self.__test.append(self.__rank)

        self.__spectral = TestItem(self.__stest_selection_label_frame, self.__test_type[5], 10, 160)
        self.__test.append(self.__spectral)

        self.__non_overlappong = TestItem(self.__stest_selection_label_frame, self.__test_type[6], 10, 185)
        self.__test.append(self.__non_overlappong)

        self.__overlapping = TestItem(self.__stest_selection_label_frame, self.__test_type[7], 10, 210)
        self.__test.append(self.__overlapping)

        self.__universal = TestItem(self.__stest_selection_label_frame, self.__test_type[8], 10, 235)
        self.__test.append(self.__universal)

        self.__linear = TestItem(self.__stest_selection_label_frame, self.__test_type[9], 10, 260)
        self.__test.append(self.__linear)

        self.__serial = TestItem(self.__stest_selection_label_frame, self.__test_type[10], 10, 285, serial=True)
        self.__test.append(self.__serial)

        self.__entropy = TestItem(self.__stest_selection_label_frame, self.__test_type[11], 10, 310)
        self.__test.append(self.__entropy)

        self.__cusum_f = TestItem(self.__stest_selection_label_frame, self.__test_type[12], 10, 335)
        self.__test.append(self.__cusum_f)

        self.__cusum_r = TestItem(self.__stest_selection_label_frame, self.__test_type[13], 10, 360)
        self.__test.append(self.__cusum_r)

        self.__excursion = RandomExcursionTestItem(self.__stest_selection_label_frame, self.__test_type[14], 10, 385,
                                                   ['-4', '-3', '-2', '-1', '+1', '+2', '+3', '+4'])
        self.__test.append(self.__excursion)

        self.__variant = RandomExcursionTestItem(self.__stest_selection_label_frame, self.__test_type[15], 10, 475,
                                                   ['-9.0', '-8.0', '-7.0', '-6.0', '-5.0', '-4.0', '-3.0', '-2.0', '-1.0',
                                                    '+1.0', '+2.0', '+3.0', '+4.0', '+5.0', '+6.0', '+7.0', '+8.0', '+9.0'], variant=True)
        self.__test.append(self.__variant)

        self.__result_field = [
            self.__monobit,
            self.__block,
            self.__run,
            self.__long_run,
            self.__rank,
            self.__spectral,
            self.__non_overlappong,
            self.__overlapping,
            self.__universal,
            self.__linear,
            self.__serial,
            self.__entropy,
            self.__cusum_f,
            self.__cusum_r
        ]

        select_all_button = CustomButton(self.master, 'Select All Test', 20, 760, 100, self.select_all)
        deselect_all_button = CustomButton(self.master, 'De-Select All Test', 125, 760, 150, self.deselect_all)
        execute_button = CustomButton(self.master, 'Execute Test', 280, 760, 100, self.execute)
        save_button = CustomButton(self.master, 'Save as Text File', 385, 760, 100, self.save_result_to_file)
        reset_button = CustomButton(self.master, 'Reset', 490, 760, 100, self.reset)
        exit = CustomButton(self.master, 'Exit Program', 595, 760, 100, self.exit)

    def select_binary_file(self):
        """
        Called tkinter.askopenfilename to give user an interface to select the binary input file and perform the following:
        1.  Clear Binary Data Input Field. (The textfield)
        2.  Set selected file name to Binary Data File Input Field.
        3.  Clear String Data file input field.

        :return: None
        """
        print('Select Binary File')
        self.__file_name = askopenfilename(initialdir=os.getcwd(), title="Select Binary Input File.")
        if self.__file_name:
            self.__binary_input.set_data('')
            self.__binary_data_file_input.set_data(self.__file_name)
            self.__string_data_file_input.set_data('')
            self.__is_binary_file = True
            self.__is_data_file = False

    def select_data_file(self):
        """
        Called tkinter.askopenfilename to give user an interface to select the string input file and perform the following:
        1.  Clear Binary Data Input Field. (The textfield)
        2.  Clear Binary Data File Input Field.
        3.  Set selected file name to String Data File Input Field.

        :return: None
        """
        print('Select Data File')
        self.__file_name = askopenfilename(initialdir=os.getcwd(), title="Select Data File.")
        if self.__file_name:
            self.__binary_input.set_data('')
            self.__binary_data_file_input.set_data('')
            self.__string_data_file_input.set_data(self.__file_name)
            self.__is_binary_file = False
            self.__is_data_file = True

    def select_all(self):
        """
        Select all test type displayed in the GUI. (Check all checkbox)

        :return: None
        """
        print('Select All Test')
        for item in self.__test:
            item.set_check_box_value(1)

    def deselect_all(self):
        """
        Unchecked all checkbox

        :return: None
        """
        print('Deselect All Test')
        for item in self.__test:
            item.set_check_box_value(0)

    def execute(self):
        """
        Execute the tests and display the result in the GUI

        :return: None
        """
        print('Execute')

        if len(self.__binary_input.get_data().strip().rstrip()) == 0 and\
                len(self.__binary_data_file_input.get_data().strip().rstrip()) == 0 and\
                len(self.__string_data_file_input.get_data().strip().rstrip()) == 0:
            messagebox.showwarning("Warning",
                                   'You must input the binary data or read the data from from the file.')
            return None
        elif len(self.__binary_input.get_data().strip().rstrip()) > 0 and\
                len(self.__binary_data_file_input.get_data().strip().rstrip()) > 0 and\
                len(self.__string_data_file_input.get_data().strip().rstrip()) > 0:
            messagebox.showwarning("Warning",
                                   'You can either input the binary data or read the data from from the file.')
            return None

        input = []

        if not len(self.__binary_input.get_data()) == 0:
            input.append(self.__binary_input.get_data())
        elif not len(self.__binary_data_file_input.get_data()) == 0:
            temp = []
            if self.__file_name:
                handle = open(self.__file_name)
            for data in handle:
                temp.append(data.strip().rstrip())
            test_data = ''.join(temp)
            input.append(test_data[:1000000])
        elif not len(self.__string_data_file_input.get_data()) == 0:
            data = []
            count = 1
            if self.__file_name:
                handle = open(self.__file_name)
            for item in handle:
                if item.startswith('http://'):
                    url = Tools.url_to_binary(item)
                    data.append(Tools.string_to_binary(url))
                else:
                    data.append(Tools.string_to_binary(item))
                count += 1
            print(data)
            input.append(''.join(data))

            #print(data)
            #self.__test_data = Options(self.__stest_selection_label_frame, 'Input Data', data, 10, 5, 900)

        for test_data in input:
            count = 0
            results = [(), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()]
            for item in self.__test:
                if item.get_check_box_value() == 1:
                    print(self.__test_type[count], ' selected. ', self.__test_function[count](test_data))
                    if count == 13:
                        results[count] = self.__test_function[count](test_data, mode=1)
                    else:
                        results[count] = self.__test_function[count](test_data)
                count += 1
            self.__test_result.append(results)

        self.write_results(self.__test_result[0])
        messagebox.showinfo("Execute", "Test Complete.")

    def write_results(self, results):
        """
        Write the result in the GUI

        :param results: result of the randomness test
        :return: None
        """
        count = 0
        for result in results:
            if not len(result) == 0:
                if count == 10:
                    self.__result_field[count].set_p_value(result[0][0])
                    self.__result_field[count].set_result_value(self.get_result_string(result[0][1]))
                    self.__result_field[count].set_p_value_02(result[1][0])
                    self.__result_field[count].set_result_value_02(self.get_result_string(result[1][1]))
                elif count == 14:
                    print(result)
                    self.__excursion.set_results(result)
                elif count == 15:
                    print(result)
                    self.__variant.set_results(result)
                else:
                    self.__result_field[count].set_p_value(result[0])
                    self.__result_field[count].set_result_value(self.get_result_string(result[1]))


            count += 1

    def save_result_to_file(self):
        print('Save to File')
        print(self.__test_result)
        if not len(self.__binary_input.get_data()) == 0:
            output_file = asksaveasfile(mode='w', defaultextension=".txt")
            output_file.write('Test Data:' + self.__binary_input.get_data() + '\n\n\n')
            result = self.__test_result[0]
            output_file.write('%-50s\t%-20s\t%-10s\n' % ('Type of Test', 'P-Value', 'Conclusion'))
            self.write_result_to_file(output_file, result)
            output_file.close()
            messagebox.showinfo("Save",  "File save finished.  You can check the output file for complete result.")
        elif not len(self.__binary_data_file_input.get_data()) == 0:
            output_file = asksaveasfile(mode='w', defaultextension=".txt")
            output_file.write('Test Data File:' + self.__binary_data_file_input.get_data() + '\n\n\n')
            result = self.__test_result[0]
            output_file.write('%-50s\t%-20s\t%-10s\n' % ('Type of Test', 'P-Value', 'Conclusion'))
            self.write_result_to_file(output_file, result)
            output_file.close()
            messagebox.showinfo("Save",  "File save finished.  You can check the output file for complete result.")
        elif not len(self.__string_data_file_input.get_data()) == 0:
            output_file = asksaveasfile(mode='w', defaultextension=".txt")
            output_file.write('Test Data File:' + self.__string_data_file_input.get_data() + '\n\n')
            #count = 0
            #for item in self.__test_string:
            #    output_file.write('Test ' + str(count+1) + ':\n')
            #    output_file.write('String to be tested: %s' % item)
            #    output_file.write('Binary of the given String: %s\n\n' % Tools.string_to_binary(item))
            #    output_file.write('Result:\n')
            #    output_file.write('%-50s\t%-20s\t%-10s\n' % ('Type of Test', 'P-Value', 'Conclusion'))
            #    self.write_result_to_file(output_file, self.__test_result[count])
            #    output_file.write('\n\n')
            #    count += 1
            result = self.__test_result[0]
            output_file.write('%-50s\t%-20s\t%-10s\n' % ('Type of Test', 'P-Value', 'Conclusion'))
            self.write_result_to_file(output_file, result)
            output_file.close()
            messagebox.showinfo("Save",  "File save finished.  You can check the output file for complete result.")

    def write_result_to_file(self, output_file, result):
        for count in range(16):
            if self.__test[count].get_check_box_value() == 1:
                if count == 10:
                    output_file.write(self.__test_type[count] + ':\n')
                    output = '\t\t\t\t\t\t\t\t\t\t\t\t\t%-20s\t%s\n' % (
                    str(result[count][0][0]), self.get_result_string(result[count][0][1]))
                    output_file.write(output)
                    output = '\t\t\t\t\t\t\t\t\t\t\t\t\t%-20s\t%s\n' % (
                    str(result[count][1][0]), self.get_result_string(result[count][1][1]))
                    output_file.write(output)
                    pass
                elif count == 14:
                    output_file.write(self.__test_type[count] + ':\n')
                    output = '\t\t\t\t%-10s\t%-20s\t%-20s\t%s\n' % ('State ', 'Chi Squared', 'P-Value', 'Conclusion')
                    output_file.write(output)
                    for item in result[count]:
                        output = '\t\t\t\t%-10s\t%-20s\t%-20s\t%s\n' % (
                        item[0], item[2], item[3], self.get_result_string(item[4]))
                        output_file.write(output)
                elif count == 15:
                    output_file.write(self.__test_type[count] + ':\n')
                    output = '\t\t\t\t%-10s\t%-20s\t%-20s\t%s\n' % ('State ', 'COUNTS', 'P-Value', 'Conclusion')
                    output_file.write(output)
                    for item in result[count]:
                        output = '\t\t\t\t%-10s\t%-20s\t%-20s\t%s\n' % (
                        item[0], item[2], item[3], self.get_result_string(item[4]))
                        output_file.write(output)
                else:
                    output = '%-50s\t%-20s\t%s\n' % (
                    self.__test_type[count], str(result[count][0]), self.get_result_string(result[count][1]))
                    output_file.write(output)
            count += 1

    #def change_data(self):
    #    index = int(self.__test_data.get_selected().split(' ')[0])
    #    print(self.__test_result[index-1])
    #    self.write_results(self.__test_result[index-1])

    def reset(self):
        """
        Reset the GUI:
        1.  Clear all input in the textfield.
        2.  Unchecked all checkbox

        :return: None
        """
        print('Reset')
        self.__binary_input.set_data('')
        self.__binary_data_file_input.set_data('')
        self.__string_data_file_input.set_data('')
        self.__is_binary_file = False
        self.__is_data_file = False
        self.__monobit.reset()
        self.__block.reset()
        self.__run.reset()
        self.__long_run.reset()
        self.__rank.reset()
        self.__spectral.reset()
        self.__non_overlappong.reset()
        self.__overlapping.reset()
        self.__universal.reset()
        self.__linear.reset()
        self.__serial.reset()
        self.__entropy.reset()
        self.__cusum_f.reset()
        self.__cusum_r.reset()
        self.__excursion.reset()
        self.__variant.reset()
        #self.__test_data = Options(self.__stest_selection_label_frame, 'Input Data', [''], 10, 5, 900)
        self.__test_result = []
        self.__test_string = []

    def exit(self):
        """
        Exit this program normally

        :return: None
        """
        print('Exit')
        exit(0)

    def get_result_string(self, result):
        """
        Interpret the result and return either 'Random' or 'Non-Random'

        :param result: Result of the test (either True or False)
        :return: str (Either 'Random' for True and 'Non-Random' for False
        """
        if result == True:
            return 'Random'
        else:
            return 'Non-Random'

if __name__ == '__main__':
    root = Tk()
    root.resizable(0,0)
    root.geometry("%dx%d+0+0" % (1280, 800))
    title = 'Test Suite for NIST Random Numbers'
    root.title(title)
    app = Main(root)
    app.focus_displayof()
    app.mainloop()