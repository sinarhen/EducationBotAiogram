import pandas as pd
import dataframe_image as dfi
from config import PLOTS_DIRECTORY

pd.set_option("display.max_column", None)
pd.set_option("display.max_colwidth", None)
pd.set_option('display.width', -1)
pd.set_option('display.max_rows', None)


def get_pd_dataframe(data, columns):
    df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
    return df


def export_image(df, filename, directory=PLOTS_DIRECTORY):
    print(f'{export_image.__name__} directory={directory} filename={filename}')
    dfi.export(df, f"{directory}/{filename}", table_conversion='matplotlib')


def get_image_bytecode(filename, directory=PLOTS_DIRECTORY):
    with open(f"{directory}/{filename}", 'rb') as photo:
        ph_b = photo.read()
    return ph_b
