# encoding: utf8
from typing import List
import pandas as pd


class ExcelPartition:

    def __init__(self, excel_path):
        self._excel_path = excel_path
        self._headers: List[str] = []
        self._excel_data: pd.DataFrame = None

    def read(self):
        self._excel_data = pd.read_excel(self._excel_path, sheet_name=0)
        self._headers = self._excel_data.columns.to_list()

    def group_by(self, *colums):
        grouped_datas = self._excel_data.groupby(colums)
        return grouped_datas

    @property
    def headers(self):
        return self._headers

    @property
    def excel_data(self):
        return self._excel_data
