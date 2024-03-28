import pandas as pd
import csv
def remove_quotes(csv_file):
    df = pd.read_csv(csv_file, quoting=csv.QUOTE_NONE)
    df = df.applymap(lambda x: x.replace('"', '') if isinstance(x, str) else x)
    df.to_csv(csv_file, index=False, quoting=csv.QUOTE_NONE)
csv_file = "output (2).csv"  #путь к CSV файлу
remove_quotes(csv_file)
