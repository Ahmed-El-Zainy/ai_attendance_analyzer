import pandas as pd


class DataLoader:
    """
    A class used to load data from an Excel file.

    ...

    Attributes
    ----------
    file_path : str
        a string representing the path to the Excel file
    data : DataFrame
        a pandas DataFrame containing the loaded data

    Methods
    -------
    load_data():
        Loads data from the Excel file into the DataFrame.
    get_data():
        Returns the loaded data.
    """

    def __init__(self, file_path):
        """
        Constructs all the necessary attributes for the DataLoader object.

        Parameters
        ----------
            file_path : str
                a string representing the path to the Excel file
        """

        self.file_path = file_path
        self.data = None

    def load_data(self):
        """
        Loads data from the Excel file into the DataFrame.
        """
        self.data = pd.read_excel(self.file_path)

    def get_data(self):
        """
        Returns the loaded data.
        Returns
        -------
        DataFrame
            a pandas DataFrame containing the loaded data
        """

        return self.data
