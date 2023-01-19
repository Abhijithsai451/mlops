import logging
import os
import warnings

import pandas as pd
import plotly.express as px

from mlops_main import project_secrets

warnings.filterwarnings("ignore")

desired_width = 500
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 25)

plot_path = project_secrets.plot_path

logging.basicConfig(
    # filename=os.path.join(home_path,log_path,'running_logs.log'),
    level=logging.DEBUG,
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
)


def plot_data(df):
    print(df.head())
    df['totalDrafted'] = pd.Series(df.idPlayer.unique())
    df = df.fillna(0)
    plot = px.line(df,
                   x="yearDraft", y="totalDrafted",
                   title='NBA Drafting Trend from 1949 to 2020')
    plot.write_image(os.path.join(plot_path + '/draft_plot.png'))

    logging.info("plotting the first dataframe ")


def data_analysis(df):
    plot_data(df)

    return "EDA on Draft and Draft combine data:SUCCESS"
