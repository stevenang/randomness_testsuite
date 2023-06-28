from tkinter import Button
from tkinter import Canvas
from tkinter import Checkbutton
from tkinter import DISABLED
from tkinter import Entry
from tkinter import Frame
from tkinter import IntVar
from tkinter import Label
from tkinter import LabelFrame
from tkinter import OptionMenu
from tkinter import Scrollbar
from tkinter import StringVar

class CustomButton:

    def __init__(self, master, title, x_coor, y_coor, width, action=None):
        button = Button(master, text=title, command=action)
        button.config(font=("Calibri", 10))
        button.place(x=x_coor, y=y_coor, width=width, height=25)

class Input:

    def __init__(self, master, title, x_coor, y_coor, has_button=False, action=None, state='disabled', button_xcoor=1050, button_width=180):
        # Setup Labels
        label = Label(master, text=title)
        label.config(font=("Calibri", 12))
        label.place(x=x_coor, y=y_coor, height=25)

        self.__data = StringVar()
        self.__data_entry = Entry(master, textvariable=self.__data)
        self.__data_entry.place(x=150, y=y_coor, width=900, height=25)

        if has_button:
            self.__data_entry.config(state='disabled')
            button_title = 'Select ' + title
            button = Button(master, text=button_title, command=action)
            button.config(font=("Calibri", 10))
            button.place(x=button_xcoor, y=y_coor, width=180, height=25)

    def set_data(self, value):
        self.__data.set(value)

    def get_data(self):
        return self.__data.get()

    def change_state(self, state):
        self.__data_entry.config(state=state)

class LabelTag:

    def __init__(self, master, title, x_coor, y_coor, width, font_size=18, border=0, relief='flat'):
        label = Label(master, text=title, borderwidth=border, relief=relief)
        label.config(font=("Calibri", font_size))
        label.place(x=x_coor, y=y_coor, width=width, height=25)

class Options:

    def __init__(self, master, title, data, x_coor, y_coor, width):

        self.__selected = StringVar()
        label = Label(master, text=title)
        label.config(font=("Calibri", 12))
        self.__selected.set(data[0])
        label.place(x=x_coor, y=y_coor, height=25, width=100)
        self.__option = OptionMenu(master, self.__selected, *data)
        self.__option.place(x=150, y=y_coor, height=25, width=width)

    def set_selected(self, data):
        self.__selected.set(data)

    def get_selected(self):
        return self.__selected.get()

    def update_data(self, data):
        self.__option.option_clear()
        self.__option.option_add(data, '')
        self.__option.update()

class TestItem:

    def __init__(self, master, title, x_coor, y_coor, serial=False, p_value_x_coor=365, p_value_width=500, result_x_coor=870, result_width=350, font_size=12, two_columns=False):
        self.__chb_var = IntVar()
        self.__p_value = StringVar()
        self.__result = StringVar()
        self.__p_value_02 = StringVar()
        self.__result_02 = StringVar()
        checkbox = Checkbutton(master, text=title, variable=self.__chb_var)
        checkbox.config(font=("Calibri", font_size))
        checkbox.place(x=x_coor, y=y_coor)

        p_value_entry = Entry(master, textvariable=self.__p_value)
        p_value_entry.config(state=DISABLED)
        p_value_entry.place(x=p_value_x_coor, y=y_coor, width=p_value_width, height=25)

        result_entry = Entry(master, textvariable=self.__result)
        result_entry.config(state=DISABLED)
        result_entry.place(x=result_x_coor, y=y_coor, width=result_width, height=25)

        if serial and two_columns:
            p_value_entry_02 = Entry(master, textvariable=self.__p_value_02)
            p_value_entry_02.config(state=DISABLED)
            p_value_entry_02.place(x=875, y=y_coor, width=235, height=25)

            result_entry_02 = Entry(master, textvariable=self.__result_02)
            result_entry_02.config(state=DISABLED)
            result_entry_02.place(x=1115, y=y_coor, width=110, height=25)
        elif serial and not two_columns:
            p_value_entry_02 = Entry(master, textvariable=self.__p_value_02)
            p_value_entry_02.config(state=DISABLED)
            p_value_entry_02.place(x=365, y=y_coor+25, width=500, height=25)

            result_entry_02 = Entry(master, textvariable=self.__result_02)
            result_entry_02.config(state=DISABLED)
            result_entry_02.place(x=870, y=y_coor+25, width=350, height=25)

    def get_check_box_value(self):
        return self.__chb_var.get()

    def set_check_box_value(self, value):
        self.__chb_var.set(value)

    def set_p_value(self, value):
        self.__p_value.set(value)

    def set_result_value(self, value):
        self.__result.set(value)

    def set_p_value_02(self, value):
        self.__p_value_02.set(value)

    def set_result_value_02(self, value):
        self.__result_02.set(value)

    def set_values(self, values):
        self.__p_value.set(values[0])
        self.__result.set(self.__get_result_string(values[1]))

    def set_p_2_values(self, values):
        self.__p_value_02(values[0])
        self.__result_02(self.__get_result_string(values[1]))

    def reset(self):
        self.set_check_box_value(0)
        self.set_p_value('')
        self.set_result_value('')
        self.set_p_value_02('')
        self.set_result_value_02('')

    def __get_result_string(self, result):
        if result == True:
            return 'Random'
        else:
            return 'Non-Random'

class RandomExcursionTestItem:

    def __init__(self, master, title, x_coor, y_coor, data, variant=False, font_size=11):
        self.__chb_var = IntVar()
        self.__state = StringVar()
        self.__count = StringVar()
        self.__xObs = StringVar()
        self.__p_value = StringVar()
        self.__result = StringVar()
        self.__results = []
        self.__variant = variant

        checkbox = Checkbutton(master, text=title, variable=self.__chb_var)
        checkbox.config(font=("Calibri", font_size))
        checkbox.place(x=x_coor, y=y_coor)

        state_label = LabelTag(master, 'State', (x_coor + 60), (y_coor + 30), width=100, font_size=font_size, border=2, relief='groove')
        if variant:
            self.__state.set('-1.0')
        else:
            self.__state.set('+1')
        state_option = OptionMenu(master, self.__state, *data)
        state_option.place(x=(x_coor + 60), y=(y_coor + 60), height=25, width=100)
        self.__state.trace("w", self.update)
        if not variant:
            xObs_label = LabelTag(master, 'Chi^2', (x_coor + 165), (y_coor + 30), width=350, font_size=font_size, border=2,
                                   relief='groove')
            xObs_Entry = Entry(master, textvariable=self.__xObs)
            xObs_Entry.config(state=DISABLED)
            xObs_Entry.place(x=(x_coor + 165), y=(y_coor + 60), width=350, height=25)
        else:
            count_label = LabelTag(master, 'Count', (x_coor + 165), (y_coor + 30), width=350, font_size=font_size,
                                  border=2, relief='groove')
            count_Entry = Entry(master, textvariable=self.__count)
            count_Entry.config(state=DISABLED)
            count_Entry.place(x=(x_coor + 165), y=(y_coor + 60), width=350, height=25)
            pass
        p_value_label = LabelTag(master, 'P-Value', (x_coor + 520), (y_coor + 30), width=350, font_size=font_size, border=2,
                               relief='groove')
        p_value_Entry = Entry(master, textvariable=self.__p_value)
        p_value_Entry.config(state=DISABLED)
        p_value_Entry.place(x=(x_coor + 520), y=(y_coor + 60), width=350, height=25)
        conclusion_label = LabelTag(master, 'Result', (x_coor + 875), (y_coor + 30), width=150, font_size=font_size, border=2,
                               relief='groove')
        conclusion_Entry = Entry(master, textvariable=self.__result)
        conclusion_Entry.config(state=DISABLED)
        conclusion_Entry.place(x=(x_coor + 875), y=(y_coor + 60), width=150, height=25)

    def get_check_box_value(self):
        return self.__chb_var.get()

    def set_check_box_value(self, value):
        self.__chb_var.set(value)

    def set_results(self, results):
        self.__results = results
        self.update()

    def update(self, *_):
        match = False
        for result in self.__results:
            if result[0] == self.__state.get():
                if self.__variant:
                    self.__count.set(result[2])
                else:
                    self.__xObs.set(result[2])

                self.__p_value.set(result[3])
                self.__result.set(self.get_result_string(result[4]))
                match = True

        if not match:
            if self.__variant:
                self.__count.set('')
            else:
                self.__xObs.set('')

            self.__p_value.set('')
            self.__result.set('')

    def get_result_string(self, result):
        if result == True:
            return 'Random'
        else:
            return 'Non-Random'

    def reset(self):
        self.__chb_var.set('0')
        if self.__variant:
            self.__state.set('-1.0')
            self.__count.set('')
        else:
            self.__state.set('+1')
            self.__xObs.set('')

        self.__p_value.set('')
        self.__result.set('')

class ScrollLabelFrame(LabelFrame):
    def __init__(self, parent, label):
        super().__init__(master=parent, text=label, padx=5, pady=5)
        self._canvas = Canvas(self, background="#ffffff")
        self.inner_frame = Frame(self._canvas, background="#ffffff")
        self._scroll_bar = Scrollbar(self, orient="vertical", command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=self._scroll_bar.set)
        self._scroll_bar.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)
        self._canvas_window = self._canvas.create_window((4,4), window=self.inner_frame, anchor="nw",            #add view port frame to canvas
                                  tags="self.inner_frame")

        self.inner_frame.bind("<Configure>", self.onFrameConfigure)  # bind an event whenever the size of the viewPort frame changes.
        self._canvas.bind("<Configure>", self.onCanvasConfigure)  # bind an event whenever the size of the viewPort frame changes.

        self.onFrameConfigure(None)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self._canvas.configure(scrollregion=self._canvas.bbox(
            "all"))  # whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self._canvas.itemconfig(self._canvas_window, width=canvas_width)