import logging

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.express as px

desired_width = 500
pd.set_option('display.width',desired_width)
pd.set_option('display.max_columns',25)

logging.basicConfig(
    #filename=os.path.join(home_path,log_path,'running_logs.log'),
    level=logging.DEBUG,
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def plot_data(df1):


    pass


def data_analysis(df):

    plot_data(df1)

    return "EDA on Draft and Draft combine data:SUCCESS"



