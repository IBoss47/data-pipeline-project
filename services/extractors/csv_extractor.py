import pandas as pd

class CSVExtractor:
    
    def extractor(self, config):
        path = config['source']['path']

        parse_dates = [
            column
            for column, dtype in config["column_types"].items()
            if dtype in ("Date", "DateTime")
        ]

        df = pd.read_csv(
            config["source"]["path"],
            parse_dates=parse_dates,
            escapechar='\\'
        )
        return df