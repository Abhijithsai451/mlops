import logging
import os

import pandas as pd
import plotly.express as px

from mlops_main.project_secrets import plot_path
from mlops_main.src.utils import queries

logging.basicConfig(
    # filename=os.path.join(home_path,log_path,'running_logs.log'),
    level=logging.DEBUG,
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a")


def data_analysis(conn):
    logging.info("creating background data stats plot >>>>>>>>>")
    query = queries.background_data_stats
    df = pd.read_sql(query, conn)
    plot = px.bar(df, x="team_name", y="avg_salary_in_millions",
                  text="avg_salary_in_millions", title="top 10 high paying NBA team by average salary")
    plot.write_image(os.path.join(plot_path + '/background_data.png'))
    logging.info("creating background data stats plot >>>>>>>>> SUCCESS")
    return "EDA on Background data: SUCCESS"
