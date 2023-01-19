import argparse
import logging
import os
import shlex
import sqlite3 as sql
import subprocess
import warnings
from shlex import shlex

import pandas as pd

from mlops_main import project_secrets
from mlops_main.src.utils.common import read_yaml

warnings.filterwarnings("ignore")

STAGE = "Data Preparation"
log_path = project_secrets.log_path
home_path = project_secrets.home_path

logging.basicConfig(
    filename=os.path.join(home_path, log_path, 'running_logs.log'),
    level=logging.DEBUG,
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
)


def sqlite_connect(path):
    logging.info("Establishing the connection to the database.")
    connection = sql.connect(path)
    logging.info("Establishing the connection to the database -> SUCCESS")
    return connection


def load_to_pd(conn, config):
    meta_df = pd.read_sql_query("SELECT name FROM sqlite_schema WHERE type='table'", conn)
    tables = meta_df['name']
    logging.info("creating a csv file from the sqlite.")
    for table in tables:
        df = pd.read_sql_query("SELECT * from " + table, conn)
        logging.info(f'Created a csv file for the table : {table}')
        df.to_csv(os.path.join(home_path, config['data_preparation']['archive'], table + '.csv'))
    logging.info("Data import to csv files: SUCCESS ")


def load_data(data_path, config):
    conn = sqlite_connect(data_path)
    logging.info("Loading the required Databases")
    load_to_pd(conn, config)


def main(config_path):
    # 1. Check if the data is preset.
    config = read_yaml(os.path.join(home_path, config_path))
    data_dir = config["data_source"]["batch_files"]
    data_path = os.path.join(home_path, data_dir)

    if (os.path.exists(data_path)):
        logging.info("data path exists")
        data_path = os.path.join(data_path, "basketball.sqlite")
        logging.info("Extracting the database from the path")
        conn = load_data(data_path, config)
    else:
        logging.info("executing the shell script which imports and extracts the data to desired location ")
        subprocess.call(shlex.split('./data_import.sh'))


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="mlops/mlops_main/config/config.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n*************************************")
        logging.info(f">>>>>>>> stage {STAGE} started  <<<<<<<<<<<<")
        main(config_path=parsed_args.config)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e
