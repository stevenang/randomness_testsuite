from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import os
from FrequencyTest import FrequencyTest as ft
from RunTest import RunTest as rt
from Matrix import Matrix as mt
from Spectral import SpectralTest as st
from TemplateMatching import TemplateMatching as tm
from Universal import Universal as ut
from Complexity import ComplexityTest as ct
from Serial import Serial as serial
from ApproximateEntropy import ApproximateEntropy as aet
from CumulativeSum import CumulativeSums as cst
from RandomExcursions import RandomExcursions as ret

class GUI(Frame):

    # Constructor.  Initialized the variables.
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()


    def init_window(self):
        # Title Label
        frame_title = 'A Statistical Test Suite for Random and Pseudorandom Number Generators for Cryptographic Applications'
        self.__title_label = Label(self.master, text=frame_title)
        self.__title_label.config(font=("Calibri", 18))
        #self.__title_label.pack(fill=X)
        self.__title_label.place(x=0, y=0, width=1280, height=25)


        #Setup LabelFrame for Input
        self.__input_label_frame = LabelFrame(self.master, text="Binary Data")
        self.__input_label_frame.config(font=("Calibri", 14))
        self.__input_label_frame.propagate(0)
        #self.__input_label_frame.pack(fill="both", expand="yes", padx=10, pady=10)
        self.__input_label_frame.place(x=20, y=30, width=1240, height=100)


        #Setup Labels
        self.__binary_data_label = Label(self.__input_label_frame, text='Binary Data Input')
        self.__binary_data_label.config(font=("Calibri", 12))
        self.__binary_data_label.place(x=10, y=5, height=25)

        self.__binary_data = StringVar()
        self.__binary_data_entry = Entry(self.__input_label_frame, textvariable=self.__binary_data)
        self.__binary_data_entry.place(x=150, y=5, width=900, height=25)

        #self.__binary_data_input.pack()
        self.__file_input_label = Label(self.__input_label_frame, text='Input File')
        self.__file_input_label.config(font=("Calibri", 12))
        self.__file_input_label.place(x=10, y=35, height=25)
        #self.__file_input.pack()

        self.__file_name = StringVar()
        self.__file_input_entry = Entry(self.__input_label_frame, textvariable=self.__file_name)
        self.__file_input_entry.place(x=150, y=35, width=900, height=25)

        self.__file_select_button = Button(self.__input_label_frame, text='Select File', command=self.file_select)
        self.__file_select_button.config(font=("Calibri", 10))
        self.__file_select_button.place(x=1080, y=35, width=100, height=25)

        # Setup LabelFrame for Randomness Test
        self.__test_selection_label_frame = LabelFrame(self.master, text="Randomness Testing", padx=5, pady=5)
        self.__test_selection_label_frame.config(font=("Calibri", 14))
        #self.__test_selection_label_frame.propagate(0)
        #self.__test_selection_label_frame.pack(fill="both", expand="yes", padx=10, pady=10)
        self.__test_selection_label_frame.place(x=20, y=135, width=1240, height=580)

        self.__test_type = ['01. Frequency Test (Monobit)', '02. Frequency Test within a Block', '03. Run Test',
                            '04. Longest Run of Ones in a Block', '05. Binary Matrix Rank Test',
                            '06. Discrete Fourier Transform (Spectral) Test', '07. Non-Overlapping Template Matching Test',
                            '08. Overlapping Template Matching Test', '09. Maurer\'s Universal Statistical test',
                            '10. Linear Complexity Test', '11. Serial test', '12. Approximate Entropy Test',
                            '13. Cummulative Sums (Forward) Test', '14. Cummulative Sums (Reverse) Test',
                            '15. Random Excursions Test', '16. Random Excursions Variant Test']

        self.__test_type_label = Label(self.__test_selection_label_frame, text='Test Type', borderwidth=2, relief="groove")
        self.__test_type_label.place(x=10, y=5, width=350, height=25)

        self.__p_value_label = Label(self.__test_selection_label_frame, text='P-Value', borderwidth=2, relief="groove")
        self.__p_value_label.place(x=365, y=5, width=500, height=25)

        self.__result_label = Label(self.__test_selection_label_frame, text='Result', borderwidth=2, relief="groove")
        self.__result_label.place(x=870, y=5, width=350, height=25)

        self.__chb_var = [IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(),
                          IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()]
        
        self.__monobit_chb = Checkbutton(self.__test_selection_label_frame, text=self.__test_type[0], variable=self.__chb_var[0])
        self.__monobit_chb.place(x=10, y=35)
        self.__monobit_p_value = StringVar()
        self.__monobit_p_value_entry = Entry(self.__test_selection_label_frame, textvariable=self.__monobit_p_value)
        self.__monobit_p_value_entry.config(state=DISABLED)
        self.__monobit_p_value_entry.place(x=365, y=35, width=500, height=25)
        self.__monobit_result = StringVar()
        self.__monobit_result_entry = Entry(self.__test_selection_label_frame, textvariable=self.__monobit_result)
        self.__monobit_result_entry.config(state=DISABLED)
        self.__monobit_result_entry.place(x=870, y=35, width=350, height=25)

        self.__block_chb = Checkbutton(self.__test_selection_label_frame, text=self.__test_type[1], variable=self.__chb_var[1])
        self.__block_chb.place(x=10, y=65)
        self.__block_p_value = StringVar()
        self.__block_p_value_entry = Entry(self.__test_selection_label_frame, textvariable=self.__block_p_value)
        self.__block_p_value_entry.config(state=DISABLED)
        self.__block_p_value_entry.place(x=365, y=65, width=500, height=25)
        self.__block_result = StringVar()
        self.__block_result_entry = Entry(self.__test_selection_label_frame, textvariable=self.__block_result)
        self.__block_result_entry.config(state=DISABLED)
        self.__block_result_entry.place(x=870, y=65, width=350, height=25)

        self.__run_chb = Checkbutton(self.__test_selection_label_frame, text=self.__test_type[2], variable=self.__chb_var[2])
        self.__run_chb.place(x=10, y=95)
        self.__run_p_value = StringVar()
        self.__run_p_value_entry = Entry(self.__test_selection_label_frame, textvariable=self.__run_p_value)
        self.__run_p_value_entry.config(state=DISABLED)
        self.__run_p_value_entry.place(x=365, y=95, width=500, height=25)
        self.__run_result = StringVar()
        self.__run_result_entry = Entry(self.__test_selection_label_frame, textvariable=self.__run_result)
        self.__run_result_entry.config(state=DISABLED)
        self.__run_result_entry.place(x=870, y=95, width=350, height=25)

        self.__long_run_chb = Checkbutton(self.__test_selection_label_frame, text=self.__test_type[3], variable=self.__chb_var[3])
        self.__long_run_chb.place(x=10, y=125)
        self.__long_run_p_value = StringVar()
        self.__long_run_p_value_entry = Entry(self.__test_selection_label_frame, textvariable=self.__long_run_p_value)
        self.__long_run_p_value_entry.config(state=DISABLED)
        self.__long_run_p_value_entry.place(x=365, y=125, width=500, height=25)
        self.__long_run_result = StringVar()
        self.__long_run_result_entry = Entry(self.__test_selection_label_frame, textvariable=self.__long_run_result)
        self.__long_run_result_entry.config(state=DISABLED)
        self.__long_run_result_entry.place(x=870, y=125, width=350, height=25)

        self.__matrix_chb = Checkbutton(self.__test_selection_label_frame, text=self.__test_type[4], variable=self.__chb_var[4])
        self.__matrix_chb.place(x=10, y=155)
        self.__matrix_p_value = StringVar()
        self.__matrix_p_value_entry = Entry(self.__test_selection_label_frame, textvariable=self.__matrix_p_value)
        self.__matrix_p_value_entry.config(state=DISABLED)
        self.__matrix_p_value_entry.place(x=365, y=155, width=500, height=25)
        self.__matrix_result = StringVar()
        self.__matrix_result_entry = Entry(self.__test_selection_label_frame, textvariable=self.__matrix_result)
        self.__matrix_result_entry.config(state=DISABLED)
        self.__matrix_result_entry.place(x=870, y=155, width=350, height=25)

        self.__spectral_chb = Checkbutton(self.__test_selection_label_frame, text=self.__test_type[5], variable=self.__chb_var[5])
        self.__spectral_chb.place(x=10, y=185)
        self.__spectral_p_value = StringVar()
        self.__spectral_p_value_entry = Entry(self.__test_selection_label_frame, textvariable=self.__spectral_p_value)
        self.__spectral_p_value_entry.config(state=DISABLED)
        self.__spectral_p_value_entry.place(x=365, y=185, width=500, height=25)
        self.__spectral_result = StringVar()
        self.__spectral_result_entry = Entry(self.__test_selection_label_frame, textvariable=self.__spectral_result)
        self.__spectral_result_entry.config(state=DISABLED)
        self.__spectral_result_entry.place(x=870, y=185, width=350, height=25)

        self.__non_overlapping_chb = Checkbutton(self.__test_selection_label_frame, text=self.__test_type[6], variable=self.__chb_var[6])
        self.__non_overlapping_chb.place(x=10, y=215)
        self.__non_overlapping_p_value = StringVar()
        self.__non_overlapping_p_value_entry = Entry(self.__test_selection_label_frame, textvariable=self.__non_overlapping_p_value)
        self.__non_overlapping_p_value_entry.config(state=DISABLED)
        self.__non_overlapping_p_value_entry.place(x=365, y=215, width=500, height=25)
        self.__non_overlapping_result = StringVar()
        self.__non_overlapping_result_entry = Entry(self.__test_selection_label_frame, textvariable=self.__non_overlapping_result)
        self.__non_overlapping_result_entry.config(state=DISABLED)
        self.__non_overlapping_result_entry.place(x=870, y=215, width=350, height=25)

        self.__overlapping_chb = Checkbutton(self.__test_selection_label_frame, text=self.__test_type[7], variable=self.__chb_var[7])
        self.__overlapping_chb.place(x=10, y=245)
        self.__overlapping_p_value = StringVar()
        self.__overlapping_p_value_entry = Entry(self.__test_selection_label_frame, textvariable=self.__overlapping_p_value)
        self.__overlapping_p_value_entry.config(state=DISABLED)
        self.__overlapping_p_value_entry.place(x=365, y=245, width=500, height=25)
        self.__overlapping_result = StringVar()
        self.__overlapping_result_entry = Entry(self.__test_selection_label_frame, textvariable=self.__overlapping_result)
        self.__overlapping_result_entry.config(state=DISABLED)
        self.__overlapping_result_entry.place(x=870, y=245, width=350, height=25)

        self.__overlapping_chb = Checkbutton(self.__test_selection_label_frame, text=self.__test_type[8], variable=self.__chb_var[8])
        self.__overlapping_chb.place(x=10, y=275)
        self.__statistical_p_value = StringVar()
        self.__statistical_p_value_entry = Entry(self.__test_selection_label_frame, textvariable=self.__statistical_p_value)
        self.__statistical_p_value_entry.config(state=DISABLED)
        self.__statistical_p_value_entry.place(x=365, y=275, width=500, height=25)
        self.__statistical_result = StringVar()
        self.__statistical_result_entry = Entry(self.__test_selection_label_frame, textvariable=self.__statistical_result)
        self.__statistical_result_entry.config(state=DISABLED)
        self.__statistical_result_entry.place(x=870, y=275, width=350, height=25)

        self.__linear_chb = Checkbutton(self.__test_selection_label_frame, text=self.__test_type[9], variable=self.__chb_var[9])
        self.__linear_chb.place(x=10, y=305)
        self.__linear_p_value = StringVar()
        self.__linear_p_value_entry = Entry(self.__test_selection_label_frame, textvariable=self.__linear_p_value)
        self.__linear_p_value_entry.config(state=DISABLED)
        self.__linear_p_value_entry.place(x=365, y=305, width=500, height=25)
        self.__linear_result = StringVar()
        self.__linear_result_entry = Entry(self.__test_selection_label_frame, textvariable=self.__linear_result)
        self.__linear_result_entry.config(state=DISABLED)
        self.__linear_result_entry.place(x=870, y=305, width=350, height=25)

        self.__serial_chb = Checkbutton(self.__test_selection_label_frame, text=self.__test_type[10], variable=self.__chb_var[10])
        self.__serial_chb.place(x=10, y=335)
        self.__serial_p_value_01 = StringVar()
        self.__serial_p_value_entry_01 = Entry(self.__test_selection_label_frame, textvariable=self.__serial_p_value_01)
        self.__serial_p_value_entry_01.config(state=DISABLED)
        self.__serial_p_value_entry_01.place(x=365, y=335, width=500, height=25)
        self.__serial_p_result_01 = StringVar()
        self.__serial_p_result_entry_01 = Entry(self.__test_selection_label_frame, textvariable=self.__serial_p_result_01)
        self.__serial_p_result_entry_01.config(state=DISABLED)
        self.__serial_p_result_entry_01.place(x=870, y=335, width=350, height=25)

        self.__serial_p_value_02 = StringVar()
        self.__serial_p_value_entry_02 = Entry(self.__test_selection_label_frame, textvariable=self.__serial_p_value_02)
        self.__serial_p_value_entry_02.config(state=DISABLED)
        self.__serial_p_value_entry_02.place(x=365, y=360, width=500, height=25)
        self.__serial_p_result_02 = StringVar()
        self.__serial_p_result_entry_02 = Entry(self.__test_selection_label_frame, textvariable=self.__serial_p_result_02)
        self.__serial_p_result_entry_02.config(state=DISABLED)
        self.__serial_p_result_entry_02.place(x=870, y=360, width=350, height=25)

        self.__entropy_chb = Checkbutton(self.__test_selection_label_frame, text=self.__test_type[11], variable=self.__chb_var[11])
        self.__entropy_chb.place(x=10, y=390)
        self.__entropy_p_value = StringVar()
        self.__entropy_p_value_entry = Entry(self.__test_selection_label_frame, textvariable=self.__entropy_p_value)
        self.__entropy_p_value_entry.config(state=DISABLED)
        self.__entropy_p_value_entry.place(x=365, y=390, width=500, height=25)
        self.__entropy_result = StringVar()
        self.__entropy_result_entry = Entry(self.__test_selection_label_frame, textvariable=self.__entropy_result)
        self.__entropy_result_entry.config(state=DISABLED)
        self.__entropy_result_entry.place(x=870, y=390, width=350, height=25)

        self.__cusum_f_chb = Checkbutton(self.__test_selection_label_frame, text=self.__test_type[12], variable=self.__chb_var[12])
        self.__cusum_f_chb.place(x=10, y=420)
        self.__cusum_f_p_value = StringVar()
        self.__cusum_f_p_value_entry = Entry(self.__test_selection_label_frame, textvariable=self.__cusum_f_p_value)
        self.__cusum_f_p_value_entry.config(state=DISABLED)
        self.__cusum_f_p_value_entry.place(x=365, y=420, width=500, height=25)
        self.__cusum_f_result = StringVar()
        self.__cusum_f_result_entry = Entry(self.__test_selection_label_frame, textvariable=self.__cusum_f_result)
        self.__cusum_f_result_entry.config(state=DISABLED)
        self.__cusum_f_result_entry.place(x=870, y=420, width=350, height=25)

        self.__cusum_r_chb = Checkbutton(self.__test_selection_label_frame, text=self.__test_type[13], variable=self.__chb_var[13])
        self.__cusum_r_chb.place(x=10, y=450)
        self.__cusum_r_p_value = StringVar()
        self.__cusum_r_p_value_entry = Entry(self.__test_selection_label_frame, textvariable=self.__cusum_r_p_value)
        self.__cusum_r_p_value_entry.config(state=DISABLED)
        self.__cusum_r_p_value_entry.place(x=365, y=450, width=500, height=25)
        self.__cusum_r_result = StringVar()
        self.__cusum_r_result_entry = Entry(self.__test_selection_label_frame, textvariable=self.__cusum_r_result)
        self.__cusum_r_result_entry.config(state=DISABLED)
        self.__cusum_r_result_entry.place(x=870, y=450, width=350, height=25)

        self.__excursion_chb = Checkbutton(self.__test_selection_label_frame, text=self.__test_type[14], variable=self.__chb_var[14])
        self.__excursion_chb.place(x=10, y=480)

        self.__variant_chb = Checkbutton(self.__test_selection_label_frame, text=self.__test_type[15], variable=self.__chb_var[15])
        self.__variant_chb.place(x=10, y=510)

        self.__execute_button = Button(self.master, text='Execute Test', command=self.execute)
        self.__execute_button.config(font=("Calibri", 10))
        self.__execute_button.place(x=20, y=760, width=100, height=30)

        self.__reset_button = Button(self.master, text='Save to File', command=self.save)
        self.__reset_button.config(font=("Calibri", 10))
        self.__reset_button.place(x=125, y=760, width=100, height=30)

        self.__reset_button = Button(self.master, text='Reset', command=self.reset)
        self.__reset_button.config(font=("Calibri", 10))
        self.__reset_button.place(x=230, y=760, width=100, height=30)

        self.__exit_button = Button(self.master, text='Exit', command=self.exit)
        self.__exit_button.config(font=("Calibri", 10))
        self.__exit_button.place(x=330, y=760, width=100, height=30)

    def file_select(self):
        print('File Select')
        file_name = askopenfilename(initialdir=os.getcwd(), title="Choose a file.")
        load = False
        print(self.__file_name)
        # Check whther user select a file or not
        if file_name:
            self.__file_name.set(file_name)

    def execute(self):

        input = ''
        if not len(self.__binary_data.get().strip()) == 0:
            print('User Input')
            input = self.__binary_data.get()
        elif not len(self.__file_name.get()) == 0:
            print('File Input')
            print(self.__file_name.get())
            handle = open(self.__file_name.get())
            data_list = []
            for line in handle:
                data_list.append(line.strip().rstrip())
            input = ''.join(data_list)
        elif (not len(self.__binary_data.get().strip()) == 0) and (not len(self.__file_name.get()) == 0):
            print('You can only select either input data or read from the file.')
        else:
            print('You must enter either  input data or file name to read.')

        if len(input) > 1000000:
            input = input[:1000000]

        if self.__chb_var[0].get() == 1:
            print(self.__test_type[0], 'selected.')
            result = ft.monobit_test(input)
            self.__monobit_p_value.set(result[0])
            self.__monobit_result.set(result[1])

        if self.__chb_var[1].get() == 1:
            print(self.__test_type[1], 'selected.')
            result = ft.block_frequency(input)
            self.__block_p_value.set(result[0])
            self.__block_result.set(result[1])

        if self.__chb_var[2].get() == 1:
            print(self.__test_type[2], 'selected.')
            result = rt.run_test(input)
            self.__run_p_value.set(result[0])
            self.__run_result.set(result[1])

        if self.__chb_var[3].get() == 1:
            print(self.__test_type[3], 'selected.')
            result = rt.longest_one_block_test(input)
            self.__long_run_p_value.set(result[0])
            self.__long_run_result.set(result[1])

        if self.__chb_var[4].get() == 1:
            print(self.__test_type[4], 'selected.')
            result = mt.binary_matrix_rank_text(input)
            print(result[1])
            self.__matrix_p_value.set(result[0])
            self.__matrix_result.set(result[1])

        if self.__chb_var[5].get() == 1:
            print(self.__test_type[5], 'selected.')
            result = st.sepctral_test(input)
            self.__spectral_p_value.set(result[0])
            self.__spectral_result.set(result[1])

        if self.__chb_var[6].get() == 1:
            print(self.__test_type[6], 'selected.')
            result = tm.non_overlapping_test(input)
            self.__non_overlapping_p_value.set(result[0])
            self.__non_overlapping_result.set(result[1])

        if self.__chb_var[7].get() == 1:
            print(self.__test_type[7], 'selected.')
            result = tm.overlapping_patterns(input)
            self.__overlapping_p_value.set(result[0])
            self.__overlapping_result.set(result[1])

        if self.__chb_var[8].get() == 1:
            print(self.__test_type[8], 'selected.')
            result = ut.statistical_test(input)
            self.__statistical_p_value.set(result[0])
            self.__statistical_result.set(result[1])

        if self.__chb_var[9].get() == 1:
            print(self.__test_type[9], 'selected.')
            result = ct.linear_complexity_test(input)
            self.__linear_p_value.set(result[0])
            self.__linear_result.set(result[1])

        if self.__chb_var[10].get() == 1:
            print(self.__test_type[10], 'selected.')
            result = serial.serial_test(input)
            self.__serial_p_value_01.set(result[0][0])
            self.__serial_p_result_01.set(result[0][1])
            self.__serial_p_value_02.set(result[1][0])
            self.__serial_p_result_02.set(result[1][1])

        if self.__chb_var[11].get() == 1:
            print(self.__test_type[11], 'selected.')
            result = aet.approximate_entropy_test(input)
            self.__entropy_p_value.set(result[0])
            self.__entropy_result.set(result[1])

        if self.__chb_var[12].get() == 1:
            print(self.__test_type[12], 'selected.')
            result = cst.cumulative_sums_test(input, 0)
            self.__cusum_f_p_value.set(result[0])
            self.__cusum_f_result.set(result[1])

        if self.__chb_var[13].get() == 1:
            print(self.__test_type[13], 'selected.')
            result = cst.cumulative_sums_test(input, 1)
            self.__cusum_r_p_value.set(result[0])
            self.__cusum_r_result.set(result[1])

        if self.__chb_var[14].get() == 1:
            print(self.__test_type[14], 'selected.')
            result = ret.random_excursions_test(input, 1)

        if self.__chb_var[15].get() == 1:
            print(self.__test_type[15], 'selected.')
            result = ret.variant_test(input, 1)


    def save(self):
        print('save')

    def reset(self):
        self.__binary_data.set('')
        self.__file_name.set('')
        self.__chb_var[0].set(0)
        self.__monobit_p_value.set('')
        self.__monobit_result.set('')
        self.__chb_var[1].set(0)
        self.__block_p_value.set('')
        self.__block_result.set('')
        self.__chb_var[2].set(0)
        self.__run_p_value.set('')
        self.__run_result.set('')
        self.__chb_var[3].set(0)
        self.__long_run_p_value.set('')
        self.__long_run_result.set('')
        self.__chb_var[4].set(0)
        self.__matrix_p_value.set('')
        self.__matrix_result.set('')
        self.__chb_var[5].set(0)
        self.__spectral_p_value.set('')
        self.__spectral_result.set('')
        self.__chb_var[6].set(0)
        self.__non_overlapping_p_value.set('')
        self.__non_overlapping_result.set('')
        self.__chb_var[7].set(0)
        self.__overlapping_p_value.set('')
        self.__overlapping_result.set('')
        self.__chb_var[8].set(0)
        self.__statistical_p_value.set('')
        self.__statistical_result.set('')
        self.__chb_var[9].set(0)
        self.__linear_p_value.set('')
        self.__linear_result.set('')
        self.__chb_var[10].set(0)
        self.__serial_p_value_01.set('')
        self.__serial_p_result_01.set('')
        self.__serial_p_value_02.set('')
        self.__serial_p_result_02.set('')
        self.__chb_var[11].set(0)
        self.__entropy_p_value.set('')
        self.__entropy_result.set('')
        self.__chb_var[12].set(0)
        self.__cusum_f_p_value.set('')
        self.__cusum_f_result.set('')
        self.__chb_var[13].set(0)
        self.__cusum_r_p_value.set('')
        self.__cusum_r_result.set('')
        self.__chb_var[14].set(0)
        self.__chb_var[15].set(0)


    def exit(self):
        exit(0)


if __name__ == '__main__':
    root = Tk()
    root.resizable(0,0)
    root.geometry("%dx%d+0+0" % (1280, 800))
    title = 'Test Suite for NIST Random Numbers'
    root.title(title)
    app = GUI(root)
    app.focus_displayof()
    app.mainloop()