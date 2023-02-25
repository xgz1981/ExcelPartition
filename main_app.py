# encoding: utf8
import pathlib
from tkinter import BOTTOM, RIGHT, X, Y, Scrollbar, StringVar, filedialog, ttk
import pygubu
from excel.excel_operation import ExcelPartition

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / 'ui/excel-group.ui'


class ExcelDataPartition:
    def __init__(self):
        self._builder = pygubu.Builder()
        self._builder.add_resource_path(PROJECT_PATH)
        self._builder.add_from_file(PROJECT_UI)
        self._init_components(self._builder)
        self._regist_events()
        self._regist_values()
        self._excel: ExcelPartition = None

    def _init_components(self, builder):
        self._main_window = builder.get_object('main_window')
        self._file_select_button: ttk.Button = builder.get_object(
            'file_select')
        self._file_path_entry: ttk.Entry = builder.get_object('excel_path')
        self._column_box: ttk.Combobox = builder.get_object('column_box')
        self._dialog_button: ttk.Button = builder.get_object('preview_button')
        self._data_dialog: pygubu.builder.widgets.dialog = builder.get_object(
            'data_dialog')

    def __on_dialog_button_click(self):
        self._data_dialog.run()
        GroupDataViewer(self._builder, self._excel).display_data()

    def _regist_events(self):
        self._file_select_button.configure(command=self.__open_excel_path)
        self._dialog_button.configure(command=self.__on_dialog_button_click)

    def _regist_values(self):
        self._path_value = StringVar()
        self._file_path_entry.configure(textvariable=self._path_value)

    def __open_excel_path(self):
        file_type = (('Excel Files', '.*xlsx'), ('All Files', '*.'))
        excel_path = filedialog.askopenfilename(title='选择Excel',
                                                filetype=file_type)
        self._path_value.set(excel_path)
        self._excel = ExcelPartition(excel_path)
        self._excel.read()
        self._column_box.set('')
        self._column_box['values'] = self._excel.headers

    def run(self):
        self._main_window.mainloop()


class GroupDataViewer:
    def __init__(self, builder, excel: ExcelPartition):
        mainwindow = builder.get_object("main_window")
        self._data_dialog: pygubu.builder.widgets.dialog = builder.get_object(
            'data_dialog', mainwindow)
        self._frame_group: ttk.Frame = builder.get_object("frame_group")
        self._group_data_treeview: ttk.Treeview = builder.get_object(
            'group_data_treeview')
        self._excel = excel
        self._regist_events()
        builder.connect_callbacks(self)

    def display_data(self):
        tree_view = self._group_data_treeview
        tree_view.delete(*tree_view.get_children())

        tree_view["column"] = self._excel.headers
        tree_view["show"] = "headings"

        # For Headings iterate over the columns
        for col in tree_view["column"]:
            tree_view.heading(col, text=col)

        # Put Data in Rows
        df_rows = self._excel.excel_data.to_numpy().tolist()
        for row in df_rows:
            tree_view.insert("", "end", values=row)

    def _regist_events(self):
        tree_view = self._group_data_treeview
        sb_vertical = Scrollbar(
            self._frame_group, orient="vertical", command=tree_view.yview)
        sb_horizontal = Scrollbar(
            self._frame_group, orient="horizontal", command=tree_view.xview)

        tree_view.configure(
            yscrollcommand=sb_vertical.set, xscrollcommand=sb_horizontal.set)
        sb_vertical.grid(row=0, column=1, sticky="ns")
        sb_horizontal.grid(row=1, column=0, sticky="ew")

    def _on_dialog_close_clicked(self, event=None):
        self._data_dialog.close()


if __name__ == '__main__':
    app = ExcelDataPartition()
    app.run()
