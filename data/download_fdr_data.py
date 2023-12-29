import FinanceDataReader as fdr
from settings.default import UNIVERSE_DATA_FILE_PATH
import datetime as dt
import argparse
import pandas as pd
import os
import chardet

def main(
    update: str,
    universe_data_file_path: str,
):
    
    if not os.path.exists(os.path.join("data", "fdr")):
        os.mkdir(os.path.join("data", "fdr"))
        
    with open(universe_data_file_path, 'rb') as f:
        encoding = chardet.detect(f.read()).get('encoding')
        
    universe_data = pd.read_csv(universe_data_file_path, encoding=encoding).iloc[:,1:]
    universe_data['code'] = universe_data['code'].str.replace('A','')
    all_universe_code = universe_data['code'].unique()
    
    for code in all_universe_code:
        print(code)
        try:
            data = fdr.DataReader(
                f"{code}",
                start="1988-01-01",
                end=update
            )
            
            if "Close" in data.columns:
                data[["Close"]].to_csv(
                    os.path.join("data", "fdr", f"A{code}.csv") # AXXXXXX 형태
            )
        except BaseException as ex:
            print(ex)
            

if __name__ == "__main__":

    def get_args():
        """Download the FDR/Factor data"""

        parser = argparse.ArgumentParser(description="Download the Quandl data.")
        parser.add_argument(
            "--update",
            type=str,
            nargs="?",
            help="date of update(YYYY-MM-DD)",
            required=True
        )

        args = parser.parse_args()

        return (
            args.update,
            UNIVERSE_DATA_FILE_PATH(args.update),
        )
    
    main(*get_args())