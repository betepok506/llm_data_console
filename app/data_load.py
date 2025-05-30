# app/data_loader.py

import pandas as pd


class DataLoader:
    """
    Класс для загрузки данных из CSV-файла.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self) -> pd.DataFrame:
        """
        Загружает данные из CSV-файла.

        Returns
        -------
        pd.DataFrame
            Датафрейм с данными фрилансеров.

        Raises
        ------
        FileNotFoundError
            Если указанный файл не найден.
        """
        try:
            return pd.read_csv(self.file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл не найден: {self.file_path}")
