from tkinter import ttk
from tkinter import Canvas
from tkinter import DISABLED # Keep for Entry state if needed, though ttk uses 'readonly'
from tkinter import Frame
from tkinter import IntVar
from tkinter import LabelFrame # ttk.LabelFrame is available if we want to switch this too
from tkinter import Scrollbar
from tkinter import StringVar

class CustomButton:

    def __init__(self, master, title, x_coor, y_coor, width, action=None):
        # ttk.Button does not have a config method for font in the same way.
        # Style objects are preferred for ttk widgets. For simplicity here, let's assume default font or
        # handle styling at a higher level if necessary (e.g. via ttk.Style).
        button = ttk.Button(master, text=title, command=action)
        button.place(x=x_coor, y=y_coor, width=width, height=25)

class Input:

    def __init__(self, master, title, x_coor, y_coor, has_button=False, action=None, button_xcoor=1050, button_width=180):
        # Setup Labels
        label = ttk.Label(master, text=title, font=("Calibri", 12))
        label.place(x=x_coor, y=y_coor, height=25)

        self.__data = StringVar()
        self.__data_entry = ttk.Entry(master, textvariable=self.__data, font=("Calibri", 10))
        self.__data_entry.place(x=150, y=y_coor, width=900, height=25)

        if has_button:
            self.__data_entry.config(state='readonly') # ttk.Entry uses 'readonly' for disabled look but selectable text
            button_title = 'Select ' + title
            # Using ttk.Button for consistency
            button = ttk.Button(master, text=button_title, command=action)
            button.place(x=button_xcoor, y=y_coor, width=180, height=25)

    def set_data(self, value):
        self.__data.set(value)

    def get_data(self):
        return self.__data.get()

    def change_state(self, state): # state can be 'normal', 'disabled', 'readonly'
        self.__data_entry.config(state=state)

class LabelTag:

    def __init__(self, master, title, x_coor, y_coor, width, font_size=18, border=0, relief='flat'):
        # ttk.Label uses 'borderwidth' and 'relief' options directly in constructor.
        # Font can be set directly too.
        label = ttk.Label(master, text=title, borderwidth=border, relief=relief, font=("Calibri", font_size))
        label.place(x=x_coor, y=y_coor, width=width, height=25)

class Options: # This class seems unused in Main.py based on current context, but updating it.

    def __init__(self, master, title, data, x_coor, y_coor, width):
        self.__selected = StringVar()
        # Ensure data is not empty and contains valid strings for OptionMenu
        if not data or not all(isinstance(item, str) for item in data):
            data = ["Default"] # Provide a default if data is invalid/empty

        label = ttk.Label(master, text=title, font=("Calibri", 12))
        label.place(x=x_coor, y=y_coor, height=25, width=100)
        
        self.__selected.set(data[0])
        # ttk.OptionMenu constructor is slightly different: master, variable, default_value, *values
        self.__option = ttk.OptionMenu(master, self.__selected, data[0], *data)
        self.__option.place(x=150, y=y_coor, height=25, width=width)

    def set_selected(self, data):
        self.__selected.set(data)

    def get_selected(self):
        return self.__selected.get()

    def update_data(self, data_list): # Assuming data_list is a list of strings
        # ttk.OptionMenu doesn't have direct option_clear/add. Recreate or set new menu.
        # For simplicity, if this method is crucial, it might need a more complex handling
        # such as destroying and recreating the OptionMenu or directly manipulating its internal menu.
        # A common approach is to update the StringVar and the list of options it points to,
        # then potentially re-initialize the OptionMenu if direct update isn't supported.
        # Given this class is likely unused, this simplification is acceptable for now.
        menu = self.__option["menu"]
        menu.delete(0, "end")
        if not data_list or not all(isinstance(item, str) for item in data_list):
            data_list = ["Default"]

        for string in data_list:
            menu.add_command(label=string, command=lambda value=string: self.__selected.set(value))
        self.__selected.set(data_list[0])


class TestItem:

    def __init__(self, master, title, x_coor, y_coor, serial=False, p_value_x_coor=365, p_value_width=500, result_x_coor=870, result_width=350, font_size=12, two_columns=False):
        self.__chb_var = IntVar()
        self.__p_value = StringVar()
        self.__result = StringVar()
        self.__p_value_02 = StringVar()
        self.__result_02 = StringVar()
        
        # ttk.Checkbutton font is typically managed by style.
        # For direct font setting, it's less straightforward than tkinter.Checkbutton.
        # Using style is preferred. For now, let's omit direct font config on Checkbutton.
        checkbox = ttk.Checkbutton(master, text=title, variable=self.__chb_var)
        checkbox.place(x=x_coor, y=y_coor) # Consider adjusting height/width if needed

        p_value_entry = ttk.Entry(master, textvariable=self.__p_value, font=("Calibri", font_size))
        p_value_entry.config(state='readonly')
        p_value_entry.place(x=p_value_x_coor, y=y_coor, width=p_value_width, height=25)

        result_entry = ttk.Entry(master, textvariable=self.__result, font=("Calibri", font_size))
        result_entry.config(state='readonly')
        result_entry.place(x=result_x_coor, y=y_coor, width=result_width, height=25)

        if serial and two_columns:
            p_value_entry_02 = ttk.Entry(master, textvariable=self.__p_value_02, font=("Calibri", font_size))
            p_value_entry_02.config(state='readonly')
            p_value_entry_02.place(x=875, y=y_coor, width=235, height=25)

            result_entry_02 = ttk.Entry(master, textvariable=self.__result_02, font=("Calibri", font_size))
            result_entry_02.config(state='readonly')
            result_entry_02.place(x=1115, y=y_coor, width=110, height=25)
        elif serial and not two_columns: # This case seems specific for Serial test layout
            p_value_entry_02 = ttk.Entry(master, textvariable=self.__p_value_02, font=("Calibri", font_size))
            p_value_entry_02.config(state='readonly')
            p_value_entry_02.place(x=p_value_x_coor, y=y_coor+25, width=p_value_width, height=25) # Adjusted y

            result_entry_02 = ttk.Entry(master, textvariable=self.__result_02, font=("Calibri", font_size))
            result_entry_02.config(state='readonly')
            result_entry_02.place(x=result_x_coor, y=y_coor+25, width=result_width, height=25) # Adjusted y

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
        self.__results = [] # This will store the list of tuples for excursion results
        self.__variant = variant

        # ttk.Checkbutton, font styling is less direct.
        checkbox = ttk.Checkbutton(master, text=title, variable=self.__chb_var)
        checkbox.place(x=x_coor, y=y_coor)

        # LabelTag is already updated to use ttk.Label
        state_label = LabelTag(master, 'State', (x_coor + 60), (y_coor + 30), width=100, font_size=font_size, border=2, relief='groove')
        
        # Ensure data for OptionMenu is valid
        if not data or not all(isinstance(item, str) for item in data):
            data = ["DefaultState"] # Fallback data

        if variant:
            self.__state.set(data[0] if data[0] in ['-9.0', '-8.0', '-7.0', '-6.0', '-5.0', '-4.0', '-3.0', '-2.0', '-1.0', '+1.0', '+2.0', '+3.0', '+4.0', '+5.0', '+6.0', '+7.0', '+8.0', '+9.0'] else data[0]) # Ensure initial value is in list
        else:
            self.__state.set(data[0] if data[0] in ['-4', '-3', '-2', '-1', '+1', '+2', '+3', '+4'] else data[0]) # Ensure initial value is in list
        
        state_option = ttk.OptionMenu(master, self.__state, self.__state.get(), *data)
        state_option.place(x=(x_coor + 60), y=(y_coor + 60), height=25, width=100)
        self.__state.trace_add("write", self.update) # Use trace_add for newer Tkinter versions

        entry_font = ("Calibri", font_size)
        if not variant:
            xObs_label = LabelTag(master, 'Chi^2', (x_coor + 165), (y_coor + 30), width=350, font_size=font_size, border=2, relief='groove')
            xObs_Entry = ttk.Entry(master, textvariable=self.__xObs, font=entry_font)
            xObs_Entry.config(state='readonly')
            xObs_Entry.place(x=(x_coor + 165), y=(y_coor + 60), width=350, height=25)
        else:
            count_label = LabelTag(master, 'Count', (x_coor + 165), (y_coor + 30), width=350, font_size=font_size, border=2, relief='groove')
            count_Entry = ttk.Entry(master, textvariable=self.__count, font=entry_font)
            count_Entry.config(state='readonly')
            count_Entry.place(x=(x_coor + 165), y=(y_coor + 60), width=350, height=25)

        p_value_label = LabelTag(master, 'P-Value', (x_coor + 520), (y_coor + 30), width=350, font_size=font_size, border=2, relief='groove')
        p_value_Entry = ttk.Entry(master, textvariable=self.__p_value, font=entry_font)
        p_value_Entry.config(state='readonly')
        p_value_Entry.place(x=(x_coor + 520), y=(y_coor + 60), width=350, height=25)

        conclusion_label = LabelTag(master, 'Result', (x_coor + 875), (y_coor + 30), width=150, font_size=font_size, border=2, relief='groove')
        conclusion_Entry = ttk.Entry(master, textvariable=self.__result, font=entry_font)
        conclusion_Entry.config(state='readonly')
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