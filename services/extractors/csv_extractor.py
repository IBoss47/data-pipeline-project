import pandas as pd

"""
Script Purpose:
    This service module extracts data from local CSV files and converts them into Pandas DataFrames.
    It inspects dataset configuration to automatically parse `Date` and `DateTime` fields during reading.

    Class: CSVExtractor
    Entry Point Method: extractor(config)

Warnings & Edge Cases:
    - High Memory Footprint (OOM Risk): Loading large CSV files completely into memory via `pd.read_csv()` 
      without chunking can cause Out-Of-Memory (OOM) errors on Airflow worker nodes.
    - Path & Parsing Failures: If `config['source']['path']` does not exist or if date fields fail parsing 
      due to unexpected format strings or corrupt data, `pd.read_csv()` will raise a `FileNotFoundError` or `ValueError`.
    - Escape Character Conflicts: The hardcoded `escapechar='\\'` parameter assumes standard escaping in source CSVs; 
      unescaped backslashes in raw data strings may cause unexpected parsing errors or skipped rows.
"""

class CSVExtractor:
    """
    Extractor class responsible for reading data from local CSV files.
    """
    def extractor(self, config):
        """
        Extracts data from a CSV file specified in the configuration and returns a pandas DataFrame.

        Args:
            config (dict): Configuration dictionary containing source path and column types.
            
        Returns:
            pd.DataFrame: A pandas DataFrame containing the extracted CSV data.
        """
        path = config['source']['path']

        # Identify date/datetime columns from config to parse them correctly during read
        parse_dates = [
            column
            for column, dtype in config["column_types"].items()
            if dtype in ("Date", "DateTime")
        ]

        df = pd.read_csv(
            path,
            parse_dates=parse_dates,
            escapechar='\\'
        )
        return df