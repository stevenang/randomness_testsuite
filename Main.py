import os
import threading
import numpy as np
from tkinter import *
from tkinter.filedialog import askopenfilename # Removed askopenfilenames
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox
import queue
from tkinter import ttk

from GUI import CustomButton
from GUI import Input
from GUI import LabelTag
from GUI import RandomExcursionTestItem
from GUI import TestItem
from Tools import Tools

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

class Main(Frame):

    def __init__(self, master=None):

        Frame.__init__(self, master=master)
        self._master = master
        self.init_variables()
        self.init_window()

    def init_variables(self):

        self._test_type = ['01. Frequency (Monobit) Test',
                            '02. Frequency Test within a Block',
                            '03. Runs Test',
                            '04. Test for the Longest Run of Ones in a Block',
                            '05. Binary Matrix Rank Test',
                            '06. Discrete Fourier Transform (Spectral) Test',
                            '07. Non-overlapping Template Matching Test',
                            '08. Overlapping Template Matching Test',
                            '09. Maurer\'s "Universal Statistical" Test',
                            '10. Linear Complexity Test',
                            '11. Serial Test',
                            '12. Approximate Entropy Test',
                            '13. Cumulative Sums Test (Forward)',
                            '14. Cumulative Sums Test (Backward)',
                            '15. Random Excursions Test',
                            '16. Random Excursions Variant Test']


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

        self._test_result = []
        self._test_string = []
        self._latest_results = [] 
        self._ui_queue = queue.Queue()
        self.__is_binary_file = False # Restored
        self.__is_data_file = False   # Restored
        self.__file_name = ""         # Restored for select_binary/data_file

    def init_window(self):
        frame_title = 'A Statistical Test Suite for Random and Pseudorandom Number Generators for Cryptographic Applications'
        title_label = LabelTag(self.master, frame_title, 0, 5, 1260)

        # Setup LabelFrame for Input - Reverted to original fixed height
        input_label_frame = LabelFrame(self.master, text="Input Data") 
        input_label_frame.config(font=("Calibri", 14))
        input_label_frame.propagate(0) # Prevent resizing by children
        input_label_frame.place(x=20, y=30, width=1260, height=125) # Original height

        # Restore original Input widgets
        self.__binary_input = Input(input_label_frame, 'Binary Data', 10, 5) 
        self.__binary_data_file_input = Input(input_label_frame, 'Binary Data File', 10, 35, True, 
                                              self.select_binary_file, button_xcoor=1060, button_width=160)
        self.__string_data_file_input = Input(input_label_frame, 'String Data File', 10, 65, True,
                                              self.select_data_file, button_xcoor=1060, button_width=160)
        
        # Setup LabelFrame for Randomness Test - y position reverted
        self._stest_selection_label_frame = LabelFrame(self.master, text="Randomness Testing", padx=5, pady=5)
        self._stest_selection_label_frame.config(font=("Calibri", 14))
        self._stest_selection_label_frame.place(x=20, y=155, width=1260, height=450) # Original y and height

        test_type_label_01 = LabelTag(self._stest_selection_label_frame, 'Test Type', 10, 5, 250, 11, border=2,
                                   relief="groove")
        p_value_label_01 = LabelTag(self._stest_selection_label_frame, 'P-Value', 265, 5, 235, 11, border=2,
                                 relief="groove")
        result_label_01 = LabelTag(self._stest_selection_label_frame, 'Result', 505, 5, 110, 11, border=2,
                                relief="groove")

        test_type_label_02 = LabelTag(self._stest_selection_label_frame, 'Test Type', 620, 5, 250, 11, border=2,
                                      relief="groove")
        p_value_label_02 = LabelTag(self._stest_selection_label_frame, 'P-Value', 875, 5, 235, 11, border=2,
                                    relief="groove")
        result_label_02 = LabelTag(self._stest_selection_label_frame, 'Result', 1115, 5, 110, 11, border=2,
                                   relief="groove")

        self._test = []

        self._monobit = TestItem(self._stest_selection_label_frame, self._test_type[0], 10, 35, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._monobit)

        self._block = TestItem(self._stest_selection_label_frame, self._test_type[1], 620, 35, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._block)

        self._run = TestItem(self._stest_selection_label_frame, self._test_type[2], 10, 60, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._run)

        self._long_run = TestItem(self._stest_selection_label_frame, self._test_type[3], 620, 60, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._long_run)

        self._rank = TestItem(self._stest_selection_label_frame, self._test_type[4], 10, 85, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._rank)

        self._spectral = TestItem(self._stest_selection_label_frame, self._test_type[5], 620, 85, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._spectral)

        self._non_overlappong = TestItem(self._stest_selection_label_frame, self._test_type[6], 10, 110, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._non_overlappong)

        self._overlapping = TestItem(self._stest_selection_label_frame, self._test_type[7], 620, 110, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._overlapping)

        self._universal = TestItem(self._stest_selection_label_frame, self._test_type[8], 10, 135, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._universal)

        self._linear = TestItem(self._stest_selection_label_frame, self._test_type[9], 620, 135, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._linear)

        self._serial = TestItem(self._stest_selection_label_frame, self._test_type[10], 10, 160, serial=True, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11, two_columns=True)
        self._test.append(self._serial)

        self._entropy = TestItem(self._stest_selection_label_frame, self._test_type[11], 10, 185, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._entropy)

        self._cusum_f = TestItem(self._stest_selection_label_frame, self._test_type[12], 10, 210, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._cusum_f)

        self._cusum_r = TestItem(self._stest_selection_label_frame, self._test_type[13], 620, 210, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._cusum_r)

        self._excursion = RandomExcursionTestItem(self._stest_selection_label_frame, self._test_type[14], 10, 235,
                                                   ['-4', '-3', '-2', '-1', '+1', '+2', '+3', '+4'], font_size=11)
        self._test.append(self._excursion)

        self._variant = RandomExcursionTestItem(self._stest_selection_label_frame, self._test_type[15], 10, 325,
                                                 ['-9.0', '-8.0', '-7.0', '-6.0', '-5.0', '-4.0', '-3.0', '-2.0',
                                                  '-1.0',
                                                  '+1.0', '+2.0', '+3.0', '+4.0', '+5.0', '+6.0', '+7.0', '+8.0',
                                                  '+9.0'], variant=True, font_size=11)
        self._test.append(self._variant)

        self._result_field = [
            self._monobit,
            self._block,
            self._run,
            self._long_run,
            self._rank,
            self._spectral,
            self._non_overlappong,
            self._overlapping,
            self._universal,
            self._linear,
            self._serial,
            self._entropy,
            self._cusum_f,
            self._cusum_r
        ]

        select_all_button = CustomButton(self.master, 'Select All Test', 20, 615, 100, self.select_all)
        deselect_all_button = CustomButton(self.master, 'De-Select All Test', 125, 615, 150, self.deselect_all)
        self.execute_button = CustomButton(self.master, 'Execute Test', 280, 615, 100, self.execute)
        save_button = CustomButton(self.master, 'Save as Text File', 385, 615, 100, self.save_result_to_file)
        reset_button = CustomButton(self.master, 'Reset', 490, 615, 100, self.reset)
        exit_button = CustomButton(self.master, 'Exit Program', 595, 615, 100, self.exit) # This was 'exit' variable, changed to 'exit_button' for clarity

        # Frame for status elements - Adjusted y position
        status_frame = ttk.Frame(self.master)
        status_frame.place(x=20, y=635, width=1260, height=40) 

        self.status_label = ttk.Label(status_frame, text="", font=("Calibri", 10), anchor="w")
        self.status_label.pack(side=TOP, fill=X, padx=5, pady=(0,2)) # pady to give a little space before progressbar
        
        self.progress_bar = ttk.Progressbar(status_frame, orient=HORIZONTAL, length=1260, mode='determinate')
        self.progress_bar.pack(side=BOTTOM, fill=X, padx=5, pady=(2,0))
        self.progress_bar['value'] = 0 # Ensure initial value is 0

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
        for item in self._test:
            item.set_check_box_value(1)

    def deselect_all(self):
        """
        Unchecked all checkbox

        :return: None
        """
        print('Deselect All Test')
        for item in self._test:
            item.set_check_box_value(0)

    def execute(self):
        """
        Execute the tests and display the result in the GUI

        :return: None
        """
        print('Execute')

        # Input validation and data preparation (reverted logic)
        if len(self.__binary_input.get_data().strip().rstrip()) == 0 and \
           len(self.__binary_data_file_input.get_data().strip().rstrip()) == 0 and \
           len(self.__string_data_file_input.get_data().strip().rstrip()) == 0:
            messagebox.showwarning("Warning", 'You must input the binary data or read the data from from the file.')
            return None
        elif (len(self.__binary_input.get_data().strip().rstrip()) > 0 and \
              (len(self.__binary_data_file_input.get_data().strip().rstrip()) > 0 or \
               len(self.__string_data_file_input.get_data().strip().rstrip()) > 0)) or \
             (len(self.__binary_data_file_input.get_data().strip().rstrip()) > 0 and \
              len(self.__string_data_file_input.get_data().strip().rstrip()) > 0):
            messagebox.showwarning("Warning", 'You can only use one input method at a time: direct binary, binary data file, or string data file.')
            return None

        input_data_sequences = [] # Will hold the single binary string to test

        if not len(self.__binary_input.get_data()) == 0:
            input_data_sequences.append(self.__binary_input.get_data().strip())
            status_message = "Processing direct binary input..."
        elif self.__is_binary_file and self.__file_name: # Binary Data File
            try:
                with open(self.__file_name, 'r') as handle:
                    temp = [data.strip().rstrip() for data in handle]
                test_data = ''.join(temp)[:1000000]
                if not all(c in '01' for c in test_data):
                     messagebox.showerror("Error", f"File {self.__file_name} contains non-binary characters.")
                     return None
                if not test_data:
                    messagebox.showwarning("Warning", f"Binary data file '{os.path.basename(self.__file_name)}' is empty or resulted in empty data.")
                    return None
                input_data_sequences.append(test_data)
                status_message = f"Processing binary data file: {os.path.basename(self.__file_name)}..."
            except Exception as e:
                messagebox.showerror("Error reading binary data file", f"Could not read file {self.__file_name}: {e}")
                return None
        elif self.__is_data_file and self.__file_name: # String Data File
            processed_binary_data_list = []
            try:
                with open(self.__file_name, 'r') as handle:
                    for item in handle:
                        item_stripped = item.strip()
                        if not item_stripped: continue
                        if item_stripped.startswith('http://') or item_stripped.startswith('https://'):
                            url_content = Tools.url_to_binary(item_stripped)
                            processed_binary_data_list.append(Tools.string_to_binary(url_content))
                        else:
                            processed_binary_data_list.append(Tools.string_to_binary(item_stripped))
                test_data = "".join(processed_binary_data_list)
                if not test_data:
                     messagebox.showwarning("Warning", f"String data file '{os.path.basename(self.__file_name)}' resulted in empty binary data.")
                     return None
                # Basic validation for binary string (already done by Tools.string_to_binary generally)
                input_data_sequences.append(test_data)
                status_message = f"Processing string data file: {os.path.basename(self.__file_name)}..."
            except Exception as e:
                messagebox.showerror("Error processing string data file", f"Could not process file {self.__file_name}: {e}")
                return None
        
        if not input_data_sequences or not input_data_sequences[0]:
             messagebox.showwarning("Warning", "Input data is empty or could not be processed.")
             return None

        test_data_to_process = input_data_sequences[0] # Worker expects a single string

        # Length validation (re-add if needed, using self._test_min_lengths)
        # selected_test_indices = self._get_selected_test_indices() # This method was removed, need to inline or re-add
        # if not selected_test_indices:
        #     messagebox.showwarning("Warning", "No tests selected.")
        #     return None
        # validation_result = self._validate_input_length(len(test_data_to_process), selected_test_indices)
        # if isinstance(validation_result, str):
        #     messagebox.showwarning("Input Data Warning", validation_result)
        #     return None

        try:
            self.execute_button.config(state=DISABLED) # This should use the CustomButton's config
            self.status_label.config(text=status_message) # Use the status_message set above
            self.progress_bar['value'] = 0
            self.progress_bar['maximum'] = 100 # Default max, will be updated by 'start' msg from worker

            self._latest_results = [] # Clear previous results
            
            # Pass the determined test_data_to_process (list of paths or single string) to the worker
            worker_thread = threading.Thread(target=self._execute_tests_worker, args=(test_data_to_process,))
            worker_thread.start()
            
            self.master.after(100, self._process_ui_queue)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            print(e)

    def _execute_tests_worker(self, test_data_input):
        """
        Worker method to execute randomness tests in a separate thread.
        Stores results in self._latest_results and appends to self._test_result (for single runs).
        Handles batch processing by iterating through files. (Reverted: only single string input)
        """
        # Reverted: This worker now only processes a single string.
        # selected_test_indices = self._get_selected_test_indices() # This method is removed
        # num_selected_tests = len(selected_test_indices)
        
        num_selected_tests = sum(1 for item in self._test if item.get_check_box_value() == 1)

        if num_selected_tests == 0:
            self._ui_queue.put({'type': 'error', 'message': 'No tests selected.'})
            return
        
        self._ui_queue.put({'type': 'start', 'total_tests': num_selected_tests}) # Removed mode
        try:
            current_run_results = [() for _ in range(len(self._test_type))]
            completed_count = 0
            test_idx = 0 # Reverted from iterating selected_test_indices
            for item in self._test: # Reverted
                if item.get_check_box_value() == 1:
                    if test_idx == 13: 
                        current_run_results[test_idx] = self.__test_function[test_idx](test_data_input, mode=1)
                    else:
                        current_run_results[test_idx] = self.__test_function[test_idx](test_data_input)
                    completed_count += 1
                    self._ui_queue.put({
                        'type': 'progress',
                        'test_name': self._test_type[test_idx],
                        'completed_tests': completed_count,
                        'total_tests_in_current_run': num_selected_tests 
                    })
                test_idx += 1
            
            self._latest_results = current_run_results
            self._test_result.insert(0, self._latest_results) 
            self._ui_queue.put({'type': 'complete', 'results': self._latest_results}) # Removed mode
            print("Test run completed in worker. Results sent to UI queue.")
        except Exception as e:
            print(f"Error in worker thread: {e}")
            self._ui_queue.put({'type': 'error', 'message': str(e)})

    def _process_ui_queue(self):
        """
        Process messages from the UI queue to update the GUI.
        """
        try:
            while True: # Process all messages currently in the queue
                msg = self._ui_queue.get_nowait()

                if msg['type'] == 'start':
                    # Removed mode handling, progress bar max is always total_tests
                    self.progress_bar['maximum'] = msg['total_tests'] if msg.get('total_tests', 0) > 0 else 100
                    self.progress_bar['value'] = 0
                    self.status_label.config(text=f"Test run started. Total selected tests: {msg['total_tests']}.")
                    self.write_results([]) 
                
                elif msg['type'] == 'progress': 
                    self.progress_bar['value'] = msg['completed_tests']
                    self.status_label.config(text=f"Running test {msg['completed_tests']}/{msg['total_tests_in_current_run']}: {msg['test_name']}...")
                
                elif msg['type'] == 'complete': # Reverted: only one type of complete
                    self.status_label.config(text="Test run completed successfully.")
                    self.write_results(msg['results']) 
                    messagebox.showinfo("Execute", "Test Run Complete.")
                    self.progress_bar['value'] = 0 
                    self.execute_button.config(state=NORMAL)
                    return 
                
                elif msg['type'] == 'error': 
                    self.status_label.config(text=f"Error: {msg['message']}")
                    messagebox.showerror("Error", msg['message'])
                    self.progress_bar['value'] = 0 
                    self.execute_button.config(state=NORMAL)
                    self._current_processing_mode = None
                    return 

        except queue.Empty:
            # If queue is empty, do nothing and continue polling
            pass
        except Exception as e:
            # Handle any other unexpected errors during UI update
            print(f"Error processing UI queue: {e}")
            self.status_label.config(text="Error updating UI.")
            self.execute_button.config(state=NORMAL) # Ensure button is re-enabled
            return # Stop polling on unexpected error

        self.master.after(100, self._process_ui_queue) # Continue polling

    def write_results(self, results):
        """
        Write the result in the GUI

        :param results: result of the randomness test
        :return: None
        """
        count = 0
        for result in results:
            if len(result) == 0:
                if count == 10:
                    self._result_field[count].set_p_value('')
                    self._result_field[count].set_result_value('')
                    self._result_field[count].set_p_value_02('')
                    self._result_field[count].set_result_value_02('')
                elif count == 14:
                    self._excursion.set_results('')
                elif count == 15:
                    self._variant.set_results('')
                else:
                    self._result_field[count].set_p_value('')
                    self._result_field[count].set_result_value('')
            else:
                if count == 10:
                    self._result_field[count].set_p_value(result[0][0])
                    self._result_field[count].set_result_value(self.get_result_string(result[0][1]))
                    self._result_field[count].set_p_value_02(result[1][0])
                    self._result_field[count].set_result_value_02(self.get_result_string(result[1][1]))
                elif count == 14:
                    print(result)
                    self._excursion.set_results(result)
                elif count == 15:
                    print(result)
                    self._variant.set_results(result)
                else:
                    self._result_field[count].set_p_value(result[0])
                    self._result_field[count].set_result_value(self.get_result_string(result[1]))


            count += 1

    def save_result_to_file(self): # Reverted signature
        print('Save to File')
        if not self._test_result: # Check if there are any results to save
            messagebox.showwarning("Save Warning", "No test results available to save.")
            return

        results_to_save = self._test_result[0] # Get the latest results

        # Determine original_file_info_string based on input method
        original_file_info_string = "Test Data Source: Unknown"
        if not len(self.__binary_input.get_data()) == 0:
             original_file_info_string = 'Test Data (Direct Input):\n' + self.__binary_input.get_data()
        elif self.__is_binary_file and self.__file_name:
             original_file_info_string = 'Test Data File (Binary):\n' + self.__file_name
        elif self.__is_data_file and self.__file_name:
             original_file_info_string = 'Test Data File (String/URL):\n' + self.__file_name
        
        try:
            # Use asksaveasfile to prompt user for filename
            output_file_obj = asksaveasfile(mode='w', defaultextension=".txt",
                                        title="Save Test Report As",
                                        filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if output_file_obj is None: # User cancelled
                return

            with output_file_obj: # Ensures file is closed automatically
                output_file_obj.write(original_file_info_string + '\n\n\n')
                output_file_obj.write('%-50s\t%-20s\t%-10s\n' % ('Type of Test', 'P-Value', 'Conclusion'))
                self._write_detailed_results_to_file(output_file_obj, results_to_save)
            
            messagebox.showinfo("Save",  f"File save finished. Report saved to {output_file_obj.name}.")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save report: {e}")


    def _write_detailed_results_to_file(self, output_file, result_data): # Name kept, but logic is original
        """
        Helper method to write the detailed test results to an open file object.
        """
        for test_idx in range(len(self._test_type)): 
            # Check if test was selected and results exist for this index
            if test_idx < len(result_data) and self._test[test_idx].get_check_box_value() == 1 and result_data[test_idx]:
                current_result = result_data[test_idx]
                if not current_result: 
                    continue

                if test_idx == 10: 
                    output_file.write(self._test_type[test_idx] + ':\n') # Original logic for Serial
                    output = '\t\t\t\t\t\t\t\t\t\t\t\t\t%-20s\t%s\n' % (
                    str(current_result[0][0]), self.get_result_string(current_result[0][1]))
                    output_file.write(output)
                    output = '\t\t\t\t\t\t\t\t\t\t\t\t\t%-20s\t%s\n' % (
                    str(current_result[1][0]), self.get_result_string(current_result[1][1]))
                    output_file.write(output)
                elif test_idx == 14: # Original logic for Random Excursions
                    output_file.write(self._test_type[test_idx] + ':\n')
                    output = '\t\t\t\t%-10s\t%-20s\t%-20s\t%s\n' % ('State ', 'Chi Squared', 'P-Value', 'Conclusion')
                    output_file.write(output)
                    for item in current_result:
                        output = '\t\t\t\t%-10s\t%-20s\t%-20s\t%s\n' % (
                        item[0], item[2], item[3], self.get_result_string(item[4]))
                        output_file.write(output)
                elif test_idx == 15: # Original logic for Random Excursions Variant
                    output_file.write(self._test_type[test_idx] + ':\n')
                    output = '\t\t\t\t%-10s\t%-20s\t%-20s\t%s\n' % ('State ', 'COUNTS', 'P-Value', 'Conclusion')
                    output_file.write(output)
                    for item in current_result:
                        output = '\t\t\t\t%-10s\t%-20s\t%-20s\t%s\n' % (
                        item[0], item[2], item[3], self.get_result_string(item[4]))
                        output_file.write(output)
                else: # Original logic for other tests
                    output = '%-50s\t%-20s\t%s\n' % (
                    self._test_type[test_idx], str(current_result[0]), self.get_result_string(current_result[1]))
                    output_file.write(output)
            elif self._test[test_idx].get_check_box_value() == 1: 
                 output_file.write(f"{self._test_type[test_idx]}\t-\tTest selected but no result data.\n")


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
        self.__binary_data_file_input.set_data('') # Restored
        self.__string_data_file_input.set_data('') # Restored

        self.__is_binary_file = False 
        self.__is_data_file = False   

        # Resetting UI elements
        if hasattr(self, 'status_label'): 
            self.status_label.config(text="")
        if hasattr(self, 'progress_bar'): 
            self.progress_bar['value'] = 0
        # Removed data_info_label reset as it's being removed
            
        self._monobit.reset()
        self._block.reset()
        self._run.reset()
        self._long_run.reset()
        self._rank.reset()
        self._spectral.reset()
        self._non_overlappong.reset()
        self._overlapping.reset()
        self._universal.reset()
        self._linear.reset()
        self._serial.reset()
        self._entropy.reset()
        self._cusum_f.reset()
        self._cusum_r.reset()
        self._excursion.reset()
        self._variant.reset()
        #self.__test_data = Options(self.__stest_selection_label_frame, 'Input Data', [''], 10, 5, 900)
        self._test_result = []
        self._test_string = []

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
        if result:
            return 'Random'
        else:
            return 'Non-Random'

if __name__ == '__main__':
    np.seterr('raise') # Make exceptions fatal, otherwise GUI might get inconsistent
    root = Tk()
    root.resizable(0, 0)
    root.geometry("%dx%d+0+0" % (1300, 650)) # Reverted window height
    title = 'Test Suite for NIST Random Numbers'
    root.title(title)
    app = Main(root)
    app.focus_displayof()
    app.mainloop()