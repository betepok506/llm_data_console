# app/data_loader.py

import pandas as pd


class DataLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self) -> pd.DataFrame:
        try:
            return pd.read_csv(self.file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл не найден: {self.file_path}")
