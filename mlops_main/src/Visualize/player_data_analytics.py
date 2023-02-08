import logging
import os

import pandas as pd

from mlops_main.project_secrets import data_save_path
from mlops_main.src.utils import queries

logging.basicConfig(
    # filename=os.path.join(home_path,log_path,'running_logs.log'),
    level=logging.DEBUG,
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a")


def create_player_stats(conn):
    logging.info("Creating player stats plot >>>>>>>>>>")
    query = queries.player_salary_stats
    df = pd.read_sql(query, conn)
    df.to_csv(os.path.join(data_save_path + '/player_stats.csv'))
    logging.info("Creating player stats plot >>>>>>>>>> SUCCESS")


def create_top_10_player_stats(conn):
    logging.info("Creating top 10 player stats plot >>>>>>>>>>")
    query = queries.player_salary_stats
    df = pd.read_sql(query, conn)
    df.to_csv(os.path.join(data_save_path + '/top_10_player_Stats.csv'))
    logging.info("Creating top 10 player stats plot >>>>>>>>>> SUCCESS")


def data_analysis(conn):
    create_player_stats(conn)
    create_top_10_player_stats(conn)

    return "EDA on Player data:SUCCESS"
