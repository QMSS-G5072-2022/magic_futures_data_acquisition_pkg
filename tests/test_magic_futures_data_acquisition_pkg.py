from magic_futures_data_acquisition_pkg.magic_futures_data_acquisition_pkg import FuturesInfo
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta
import jqdatasdk as jq
import os

def test_get_large():

    path ='/Users/tylerwang/Desktop/get_futures_data/AP1805.XZCE.csv'  
    expected_df = pd.DataFrame(columns=['time', 'open', 'close', 'high', 'low', 'volume', 'money'])
    actual_df = pd.read_csv(path)
    assert (expected_df.columns == actual_df.columns).all()
