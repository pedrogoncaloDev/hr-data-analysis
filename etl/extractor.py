import pandas as pd

class ExtractorExcel:
    def __init__(self, file_path: str):
        self.file_path = file_path


    def extract(self) -> pd.DataFrame:
        dataframe = pd.read_excel(self.file_path)
        return dataframe