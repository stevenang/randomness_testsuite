import os
import threading
import numpy as np
from tkinter import *
from tkinter.filedialog import askopenfilename
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
        self._latest_results = [] # Stores results of the last successfully processed file or single run
        self._ui_queue = queue.Queue()
        self._batch_file_paths = [] 
        self._current_processing_mode = None # 'single' or 'batch'

        # Minimum data lengths for tests (index: min_length_in_bits)
        # These are placeholders and should be verified against NIST documentation.
        self._test_min_lengths = {
            0: 100,  # Frequency (Monobit) Test
            1: 100,  # Frequency Test within a Block (e.g., m=20, N=5. Actual: M*N, M>=20)
            2: 100,  # Runs Test
            3: 128,  # Test for the Longest Run of Ones in a Block
            4: 1000, # Binary Matrix Rank Test (e.g. 38*M*Q, for M=Q=32 -> ~38k. Placeholder for now)
            5: 1000, # Discrete Fourier Transform (Spectral) Test
            6: 100,  # Non-overlapping Template Matching Test (depends on template length m and N)
            7: 1000, # Overlapping Template Matching Test (depends on template length m and N)
            8: 100000,# Maurer's "Universal Statistical" Test (e.g. L*Q+K, L=7,Q=1280,K=~7e5. Placeholder.)
            9: 1000, # Linear Complexity Test
            10: 500, # Serial Test (depends on block length m)
            11: 500, # Approximate Entropy Test (depends on block length m)
            12: 100, # Cumulative Sums Test (Forward)
            13: 100, # Cumulative Sums Test (Backward)
            14: 1000000, # Random Excursions Test (requires many cycles)
            15: 1000000  # Random Excursions Variant Test (requires many cycles)
        }

    def init_window(self):
        frame_title = 'A Statistical Test Suite for Random and Pseudorandom Number Generators for Cryptographic Applications'
        title_label = LabelTag(self.master, frame_title, 0, 5, 1260) # Assuming LabelTag uses ttk.Label now

        # Setup LabelFrame for Input - Increased height for batch UI
        input_label_frame = LabelFrame(self.master, text="Input Data") 
        input_label_frame.config(font=("Calibri", 14))
        input_label_frame.propagate(0)
        input_label_frame.place(x=20, y=30, width=1260, height=250) # Increased height from 125 to 250

        # Single sequence input
        single_seq_label = ttk.Label(input_label_frame, text="For single sequence (type/paste):", font=("Calibri", 10, "italic"))
        single_seq_label.place(x=10, y=5)
        self.__binary_input = Input(input_label_frame, 'Binary Data', 10, 25, change_callback=self._update_binary_input_info)
        
        self.data_info_label = ttk.Label(input_label_frame, text="Input length: N/A", font=("Calibri", 9))
        self.data_info_label.place(x=1060, y=25, height=25) # Positioned to the right of the binary input entry

        # Batch testing UI
        batch_testing_label = ttk.Label(input_label_frame, text="For batch testing (select files):", font=("Calibri", 10, "italic"))
        batch_testing_label.place(x=10, y=60)

        batch_management_frame = ttk.Frame(input_label_frame)
        batch_management_frame.place(x=10, y=80, width=1240, height=160)

        # Listbox with Scrollbar
        listbox_frame = ttk.Frame(batch_management_frame)
        listbox_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

        self.file_listbox_scrollbar = ttk.Scrollbar(listbox_frame, orient=VERTICAL)
        self.file_listbox = Listbox(listbox_frame, yscrollcommand=self.file_listbox_scrollbar.set, selectmode=EXTENDED, font=("Calibri", 10))
        self.file_listbox_scrollbar.config(command=self.file_listbox.yview)
        self.file_listbox_scrollbar.pack(side=RIGHT, fill=Y)
        self.file_listbox.pack(side=LEFT, fill=BOTH, expand=True)

        # Buttons for Listbox management
        batch_buttons_frame = ttk.Frame(batch_management_frame)
        batch_buttons_frame.pack(side=LEFT, fill=Y, padx=5, pady=5)

        add_files_button = ttk.Button(batch_buttons_frame, text="Add File(s)", command=self._add_files_to_batch)
        add_files_button.pack(side=TOP, pady=5, fill=X)

        remove_file_button = ttk.Button(batch_buttons_frame, text="Remove Selected", command=self._remove_selected_file_from_batch)
        remove_file_button.pack(side=TOP, pady=5, fill=X)
        
        # NOTE: self.__binary_data_file_input and self.__string_data_file_input are intentionally not created/placed
        # to "remove" them from the UI as per requirements. Their associated methods 
        # self.select_binary_file and self.select_data_file will become unused.

        # Setup LabelFrame for Randomness Test
        # Adjusted y position due to increased height of input_label_frame
        self._stest_selection_label_frame = LabelFrame(self.master, text="Randomness Testing", padx=5, pady=5)
        self._stest_selection_label_frame.config(font=("Calibri", 14))
        self._stest_selection_label_frame.place(x=20, y=285, width=1260, height=345) # y changed from 155 to 285, height reduced to fit

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
        # This method is now effectively unused due to UI changes for batch processing.
        # Kept for potential future single binary file selection if UI is re-added.
        print('Select Binary File (method potentially unused)')
        # Original logic:
        # self.__file_name = askopenfilename(initialdir=os.getcwd(), title="Select Binary Input File.")
        # if self.__file_name:
        #     self.__binary_input.set_data('')
        #     # self.__binary_data_file_input.set_data(self.__file_name) # This UI element is removed
        #     # self.__string_data_file_input.set_data('') # This UI element is removed
        #     self.__is_binary_file = True
        #     self.__is_data_file = False
        pass # Pass for now as the UI element it primarily served is removed

    def select_data_file(self):
        """
        Called tkinter.askopenfilename to give user an interface to select the string input file and perform the following:
        1.  Clear Binary Data Input Field. (The textfield)
        2.  Clear Binary Data File Input Field.
        3.  Set selected file name to String Data File Input Field.

        :return: None
        """
        # This method is now effectively unused due to UI changes for batch processing.
        print('Select Data File (method potentially unused)')
        # Original logic:
        # self.__file_name = askopenfilename(initialdir=os.getcwd(), title="Select Data File.")
        # if self.__file_name:
        #     self.__binary_input.set_data('')
        #     # self.__binary_data_file_input.set_data('') # This UI element is removed
        #     # self.__string_data_file_input.set_data(self.__file_name) # This UI element is removed
        #     self.__is_binary_file = False
        #     self.__is_data_file = True
        pass # Pass for now as the UI element it primarily served is removed

    def _add_files_to_batch(self):
        """
        Opens a dialog to select multiple binary files and adds them to the listbox.
        """
        # Using askopenfilenames to select multiple files
        filepaths = askopenfilenames(
            title="Select Binary Files for Batch",
            filetypes=[("All files", "*.*")] # Or more specific like [("Binary files", "*.bin"), ("Text files", "*.txt")]
        )
        if filepaths:
            current_items = self.file_listbox.get(0, END)
            for filepath in filepaths:
                if filepath not in current_items: # Add only if not already in the list
                    self.file_listbox.insert(END, filepath)
            # Update self._batch_file_paths if it's meant to be a separate synchronized list
            self._batch_file_paths = list(self.file_listbox.get(0, END))


    def _remove_selected_file_from_batch(self):
        """
        Removes selected files from the listbox.
        """
        selected_indices = self.file_listbox.curselection()
        # Remove items in reverse order of index to avoid issues with changing indices
        for index in reversed(selected_indices):
            self.file_listbox.delete(index)
        # Update self._batch_file_paths if it's meant to be a separate synchronized list
        self._batch_file_paths = list(self.file_listbox.get(0, END))

    def _get_selected_test_indices(self):
        """Helper method to get the indices of currently selected tests."""
        return [i for i, test_item in enumerate(self._test) if test_item.get_check_box_value() == 1]

    def _update_binary_input_info(self, *args): # Added *args to accept trace callback arguments
        """
        Updates the data_info_label with the length of the direct binary input.
        Called by the trace on self.__binary_input's StringVar.
        """
        current_data = self.__binary_input.get_data()
        length = len(current_data)
        
        if hasattr(self, 'data_info_label'):
            if length == 0:
                self.data_info_label.config(text="Input length: N/A")
            else:
                self.data_info_label.config(text=f"Input length: {length} bits")
        # Optional: Non-modal validation feedback here (deferred for now)

    def _validate_input_length(self, data_length, selected_test_indices):
        """
        Validates if the input data length is sufficient for the selected tests.
        Returns True if valid, or an error message string if not.
        """
        warnings = []
        for index in selected_test_indices:
            test_name = self._test_type[index]
            min_length = self._test_min_lengths.get(index, 0) # Default to 0 if not found
            
            if data_length < min_length:
                warnings.append(f"- {test_name.split('. ')[1]}: needs {min_length} bits, got {data_length} bits.")
        
        if warnings:
            return "Input data is too short for the following selected tests:\n" + "\n".join(warnings)
        return True

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
        
        test_data_to_process = None
        operation_mode = "" # "single" or "batch"

        batch_files_from_listbox = list(self.file_listbox.get(0, END))
        direct_binary_input_data = self.__binary_input.get_data().strip()
        
        selected_test_indices = [i for i, test_item in enumerate(self._test) if test_item.get_check_box_value() == 1]
        if not selected_test_indices:
            messagebox.showwarning("Warning", "No tests selected. Please select at least one test.")
            return None

        if batch_files_from_listbox:
            operation_mode = "batch"
            test_data_to_process = batch_files_from_listbox
            # Validation for batch files will occur in _execute_tests_worker for each file.
            print(f"Starting batch mode with {len(test_data_to_process)} files.")
            status_message = f"Preparing for batch processing of {len(test_data_to_process)} files..."
        elif direct_binary_input_data:
            operation_mode = "single"
            if not all(c in '01' for c in direct_binary_input_data):
                messagebox.showerror("Error", "Direct binary input contains non-binary characters ('0' or '1').")
                return None
            
            data_len = len(direct_binary_input_data)
            validation_result = self._validate_input_length(data_len, selected_test_indices)
            if isinstance(validation_result, str): # Validation failed, error message returned
                messagebox.showwarning("Input Data Warning", validation_result)
                return None
                
            test_data_to_process = direct_binary_input_data
            print(f"Starting single mode with direct binary input of length {data_len}.")
            status_message = "Preparing for single sequence processing..."
        else:
            messagebox.showwarning("Warning", "No input data provided. Please type a binary sequence or add files for batch testing.")
            return None

        # Common setup for starting the test execution process
        try:
            self.execute_button.config(state=DISABLED)
            self.status_label.config(text=status_message)
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
        Handles batch processing by iterating through files.
        """
        selected_test_indices = self._get_selected_test_indices() # Get once
        num_selected_tests = len(selected_test_indices)

        if num_selected_tests == 0: # This check is also in execute(), but good to have in worker too.
            self._ui_queue.put({'type': 'error', 'message': 'No tests selected.'})
            return

        if isinstance(test_data_input, str): # Single mode
            self._current_processing_mode = 'single'
            # Length validation for single mode is done in execute() before starting the worker
            self._ui_queue.put({'type': 'start', 
                                'total_tests': num_selected_tests, 
                                'mode': 'single'})
            try:
                current_run_results = [() for _ in range(len(self._test_type))]
                completed_count = 0
                for test_idx in selected_test_indices: # Iterate only over selected tests
                    if test_idx == 13: # Cumulative Sums Test (Backward)
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
                
                self._latest_results = current_run_results
                self._test_result.insert(0, self._latest_results) 
                self._ui_queue.put({'type': 'complete', 'results': self._latest_results, 'mode': 'single'})
                print("Single test run completed in worker. Results sent to UI queue.")
            except Exception as e:
                print(f"Error in worker thread (single mode): {e}")
                self._ui_queue.put({'type': 'error', 'message': str(e)})

        elif isinstance(test_data_input, list): # Batch mode
            self._current_processing_mode = 'batch'
            total_files = len(test_data_input)
            files_processed_successfully = 0
            files_skipped_due_to_error = 0 # Includes read errors and validation errors

            self._ui_queue.put({'type': 'start', 'total_files': total_files, 'mode': 'batch'})
            
            for file_index, file_path in enumerate(test_data_input):
                try:
                    with open(file_path, 'r') as f:
                        file_data = f.read().strip().replace('\n', '').replace(' ', '')[:1000000]
                    
                    if not all(c in '01' for c in file_data):
                        self._ui_queue.put({'type': 'file_error', 'file_path': file_path, 'error': 'Contains non-binary characters.'})
                        files_skipped_due_to_error += 1
                        continue 
                    if not file_data:
                        self._ui_queue.put({'type': 'file_error', 'file_path': file_path, 'error': 'File is empty or contains only whitespace.'})
                        files_skipped_due_to_error += 1
                        continue

                    # Validate data length for the current file
                    file_data_length = len(file_data)
                    validation_result = self._validate_input_length(file_data_length, selected_test_indices)
                    if isinstance(validation_result, str): # Validation failed
                        self._ui_queue.put({'type': 'validation_error', 
                                           'file_path': file_path, 
                                           'message': validation_result})
                        files_skipped_due_to_error += 1
                        continue

                    current_file_results = [() for _ in range(len(self._test_type))]
                    for test_idx in selected_test_indices:
                        if test_idx == 13:
                            current_file_results[test_idx] = self.__test_function[test_idx](file_data, mode=1)
                        else:
                            current_file_results[test_idx] = self.__test_function[test_idx](file_data)
                    
                    self._latest_results = current_file_results
                    self._ui_queue.put({
                        'type': 'save_report',
                        'original_file_path': file_path,
                        'results': current_file_results,
                        'file_index': file_index + 1, # For progress bar (1-based)
                        'total_files': total_files
                    })
                    files_processed_successfully += 1
                except FileNotFoundError:
                    self._ui_queue.put({'type': 'file_error', 'file_path': file_path, 'error': 'File not found.'})
                    files_skipped_due_to_error += 1
                except Exception as e: # Other read errors or unexpected issues
                    self._ui_queue.put({'type': 'file_error', 'file_path': file_path, 'error': str(e)})
                    files_skipped_due_to_error += 1
            
            self._ui_queue.put({'type': 'batch_complete', 
                                'total_files_processed': files_processed_successfully, 
                                'total_files_skipped': files_skipped_due_to_error}) # Use the new counter
            print("Batch processing completed in worker. Summary sent to UI queue.")
        else:
            self._ui_queue.put({'type': 'error', 'message': 'Invalid input type to worker.'})


    def _process_ui_queue(self):
        """
        Process messages from the UI queue to update the GUI.
        """
        try:
            while True: # Process all messages currently in the queue
                msg = self._ui_queue.get_nowait()

                if msg['type'] == 'start':
                    self._current_processing_mode = msg.get('mode', 'single') # default to single if not specified
                    if self._current_processing_mode == 'batch':
                        self.progress_bar['maximum'] = msg['total_files'] if msg.get('total_files', 0) > 0 else 100
                        self.progress_bar['value'] = 0
                        self.status_label.config(text=f"Batch processing started for {msg['total_files']} files.")
                        self.write_results([]) # Clear previous results from GUI
                    else: # single mode
                        self.progress_bar['maximum'] = msg['total_tests'] if msg.get('total_tests', 0) > 0 else 100
                        self.progress_bar['value'] = 0
                        self.status_label.config(text=f"Single test run started. Total selected tests: {msg['total_tests']}.")
                        self.write_results([]) # Clear previous results from GUI
                
                elif msg['type'] == 'progress': # This is for tests within a single run
                    if self._current_processing_mode == 'single':
                        self.progress_bar['value'] = msg['completed_tests']
                        self.status_label.config(text=f"Running test {msg['completed_tests']}/{msg['total_tests_in_current_run']}: {msg['test_name']}...")
                    # In batch mode, detailed per-test progress is currently suppressed for simplicity.
                    # The main progress bar reflects file processing progress via 'save_report'.
                
                elif msg['type'] == 'validation_error':
                    self.status_label.config(text=f"Skipping {os.path.basename(msg['file_path'])}: Data length insufficient.")
                    # Optionally, could show full message in a non-modal way or log it.
                    # messagebox.showwarning("Validation Error", f"Skipping file {msg['file_path']}:\n{msg['message']}") # This would be modal

                elif msg['type'] == 'file_error':
                    # Update status but don't stop batch or re-enable button yet
                    self.status_label.config(text=f"Error processing file {os.path.basename(msg['file_path'])}: {msg['error']}")
                    # Optionally, log this error more permanently

                elif msg['type'] == 'save_report':
                    base_name = os.path.splitext(os.path.basename(msg['original_file_path']))[0]
                    output_filename = f"{base_name}_report.txt" 
                    # Ensure output_filename is a full path if needed, e.g., in a specific reports directory
                    # For now, it saves in the current working directory.
                    
                    file_info_string = f"Test Data File: {msg['original_file_path']}"
                    try:
                        self.save_result_to_file(output_filename, msg['results'], file_info_string)
                        status_text = f"Report for {os.path.basename(msg['original_file_path'])} saved. ({msg['file_index']}/{msg['total_files']})"
                        self.write_results(msg['results']) # Update GUI with results of this file
                    except Exception as e:
                        status_text = f"Error saving report for {os.path.basename(msg['original_file_path'])}: {e}"
                    
                    self.status_label.config(text=status_text)
                    self.progress_bar['value'] = msg['file_index']

                elif msg['type'] == 'complete' and msg.get('mode') == 'single': # Single run complete
                    self.status_label.config(text="Single test run completed successfully.")
                    self.write_results(msg['results']) # Display results of the single run
                    messagebox.showinfo("Execute", "Test Run Complete.")
                    self.progress_bar['value'] = 0 
                    self.execute_button.config(state=NORMAL)
                    self._current_processing_mode = None
                    return 
                
                elif msg['type'] == 'batch_complete':
                    skipped_info = f" ({msg['total_files_skipped']} skipped)" if msg['total_files_skipped'] > 0 else ""
                    final_message = f"Batch processing finished. Processed: {msg['total_files_processed']}{skipped_info}."
                    self.status_label.config(text=final_message)
                    messagebox.showinfo("Batch Execute", final_message)
                    self.progress_bar['value'] = 0 
                    self.execute_button.config(state=NORMAL)
                    self._current_processing_mode = None
                    return

                elif msg['type'] == 'error': # General error from worker or no tests selected
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

    def save_result_to_file(self, output_filename, results_to_save, original_file_info_string):
        """
        Saves the test results to a specified file.
        :param output_filename: The name of the file to save the results to.
        :param results_to_save: The test results data.
        :param original_file_info_string: A string describing the source of the data (e.g., file path or "Direct Input").
        """
        print(f'Saving results to File: {output_filename}')
        try:
            with open(output_filename, 'w') as output_file:
                output_file.write(original_file_info_string + '\n\n\n')
                output_file.write('%-50s\t%-20s\t%-10s\n' % ('Type of Test', 'P-Value', 'Conclusion'))
                
                # Call the existing helper method to write detailed results
                self._write_detailed_results_to_file(output_file, results_to_save)
            print(f"File save to {output_filename} finished.")
            # Messagebox.showinfo is handled by the queue processor for 'save_report' completion.
        except Exception as e:
            print(f"Error saving file {output_filename}: {e}")
            # Optionally, inform the user via messagebox or status bar if saving fails critically
            messagebox.showerror("Save Error", f"Could not save report to {output_filename}:\n{e}")


    def _write_detailed_results_to_file(self, output_file, result_data):
        """
        Helper method to write the detailed test results to an open file object.
        This method was originally named write_result_to_file. Renamed for clarity.
        :param output_file: The open file object to write to.
        :param result_data: The results data for the tests.
        """
        for test_idx in range(len(self._test_type)): # Iterate up to the number of known test types
            if test_idx < len(result_data) and self._test[test_idx].get_check_box_value() == 1 and result_data[test_idx]:
                current_result = result_data[test_idx]
                if not current_result: # Skip if result is empty tuple or None
                    continue

                if test_idx == 10: # Serial Test (typically has two sets of p-values/results)
                    output_file.write(self._test_type[test_idx] + ':\n')
                    if isinstance(current_result, list) and len(current_result) == 2 and \
                       isinstance(current_result[0], tuple) and isinstance(current_result[1], tuple):
                        # Expected format for Serial test: [(p_val1, res1), (p_val2, res2)]
                        output = '\t\t\t\t\t\t\t\t\t\t\t\t\t%-20s\t%s\n' % (
                        str(current_result[0][0]), self.get_result_string(current_result[0][1]))
                        output_file.write(output)
                        output = '\t\t\t\t\t\t\t\t\t\t\t\t\t%-20s\t%s\n' % (
                        str(current_result[1][0]), self.get_result_string(current_result[1][1]))
                        output_file.write(output)
                    else:
                        output_file.write("\t\t\t\t\t\t\t\t\t\t\t\t\tError: Unexpected result format for Serial Test.\n")

                elif test_idx == 14: # Random Excursions Test
                    output_file.write(self._test_type[test_idx] + ':\n')
                    output = '\t\t\t\t%-10s\t%-20s\t%-20s\t%s\n' % ('State ', 'Chi Squared', 'P-Value', 'Conclusion')
                    output_file.write(output)
                    if isinstance(current_result, list): # Expect a list of tuples
                        for item in current_result:
                             if isinstance(item, tuple) and len(item) >= 5:
                                output = '\t\t\t\t%-10s\t%-20s\t%-20s\t%s\n' % (
                                str(item[0]), str(item[2]), str(item[3]), self.get_result_string(item[4]))
                                output_file.write(output)
                             else:
                                output_file.write(f"\t\t\t\tError: Unexpected item format in Random Excursions Test: {item}\n")
                    else:
                        output_file.write("\t\t\t\tError: Unexpected result format for Random Excursions Test.\n")
                
                elif test_idx == 15: # Random Excursions Variant Test
                    output_file.write(self._test_type[test_idx] + ':\n')
                    output = '\t\t\t\t%-10s\t%-20s\t%-20s\t%s\n' % ('State ', 'COUNTS', 'P-Value', 'Conclusion')
                    output_file.write(output)
                    if isinstance(current_result, list): # Expect a list of tuples
                        for item in current_result:
                            if isinstance(item, tuple) and len(item) >= 5:
                                output = '\t\t\t\t%-10s\t%-20s\t%-20s\t%s\n' % (
                                str(item[0]), str(item[2]), str(item[3]), self.get_result_string(item[4]))
                                output_file.write(output)
                            else:
                                output_file.write(f"\t\t\t\tError: Unexpected item format in Random Excursions Variant Test: {item}\n")
                    else:
                        output_file.write("\t\t\t\tError: Unexpected result format for Random Excursions Variant Test.\n")

                else: # For most other tests
                    if isinstance(current_result, tuple) and len(current_result) >= 2:
                        output = '%-50s\t%-20s\t%s\n' % (
                        self._test_type[test_idx], str(current_result[0]), self.get_result_string(current_result[1]))
                        output_file.write(output)
                    else:
                         output_file.write(f"{self._test_type[test_idx]}\tError: Unexpected result format.\n")
            elif self._test[test_idx].get_check_box_value() == 1: # Test was selected but result is missing/empty
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
        # self.__binary_data_file_input.set_data('') # Element removed
        # self.__string_data_file_input.set_data('') # Element removed
        if hasattr(self, 'file_listbox'): # Clear the listbox
            self.file_listbox.delete(0, END)
        self._batch_file_paths = []
        self.__is_binary_file = False # This flag might be less relevant now or needs re-evaluation
        self.__is_data_file = False   # Same for this flag

        # Resetting UI elements
        if hasattr(self, 'status_label'): # Check if status_label exists
            self.status_label.config(text="")
        if hasattr(self, 'progress_bar'): # Check if progress_bar exists
            self.progress_bar['value'] = 0
        if hasattr(self, 'data_info_label'): # Reset data info label
            self.data_info_label.config(text="Input length: N/A")
            
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
    root.geometry("%dx%d+0+0" % (1300, 700)) # Increased height for larger input frame and batch UI
    title = 'Test Suite for NIST Random Numbers'
    root.title(title)
    app = Main(root)
    app.focus_displayof()
    app.mainloop()