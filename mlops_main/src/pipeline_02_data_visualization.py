import argparse
import logging
import os
import sqlite3 as sql
import warnings

import pandas as pd

from Visualize import gameplay_data_analytics
from Visualize import player_data_analytics
from Visualize import team_data_analytics
from mlops_main import project_secrets
from mlops_main.src.utils.common import read_yaml

warnings.filterwarnings("ignore")

STAGE = "State 02 Data Visualization"

log_path = project_secrets.log_path
home_path = project_secrets.home_path
logging.basicConfig(
    # filename=os.path.join(home_path,log_path,'running_logs.log'),
    level=logging.DEBUG,
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
)


def sqlite_connect(path):
    logging.info("Establishing the connection to the database.")
    connection = sql.connect(path)
    logging.info("Establishing the connection to the database -> SUCCESS")
    return connection


# Data Present in Archive
# Import the data and perform EDA on mulitple tables.
# Search for sample EDA in kaggle.

def main(config_path):
    # Read config files
    config = read_yaml(os.path.join(home_path, config_path))
    data_dir = config["data_source"]["batch_files"]
    data_path = os.path.join(home_path, data_dir)
    data_path = os.path.join(data_path, "basketball.sqlite")
    conn = sqlite_connect(data_path)
    # EDA
    # 1. Gameplay Data
    status = gameplay_data_analytics.data_analysis(conn)
    logging.info(status)

    # 2. Player Data
    player_df = pd.read_csv(data_path + 'Player.csv')
    player_salary_df = pd.read_csv(data_path + 'Player_Salary.csv')
    player_attributes_df = pd.read_csv(data_path + 'Player_Attributes.csv')
    status = player_data_analytics.data_analysis(player_df, player_salary_df, player_attributes_df)
    logging.info(status)

    # 3. Team Data
    team_df = pd.read_csv(data_path + 'Team.csv')
    player_salary_df = pd.read_csv(data_path + 'Player_Salary.csv')
    status = team_data_analytics.data_analysis(team_df, player_salary_df)
    logging.info(status)


'''
    df_list = (pd.read_csv(file) for file in csv_files)
    df = pd.concat(df_list,ignore_index=True)
    logging.info(">>>>>>>>>> Importing the Data --> SUCCESS <<<<<<<<<")

    # 2. Feature Engineering
    columns = df.columns
    logging.info(">>>>>>>>>> 2.2 Feature Engineering <<<<<<<<<")
    logging.info(">>>>>>>>>> Displaying first 5 rows of the dataframe <<<<<<<<<")
    logging.info(df.count())
    logging.info(">>>>>>>>Columns in the data set are <<<<<<<< \n ")
    logging.info(columns)

    # 3. Exploratory Data Analysis
    # TO DO

    # 4. Archiving the data
    archive_path = config['data_preparation']['archive']
    archive_path = os.path.join(home_path,archive_path)

    if (os.path.exists(archive_path)):
        logging.info("Archive path Already exists. Saving the file to the location ")
        df.to_csv(os.path.join(archive_path,'*.csv'))
    else:
        logging.info("Archive path does not exist. creating the file location ")
        os.mkdir(archive_path)
        logging.info("Created the file location and Saving the file to the location")
        df.to_csv(os.path.join(archive_path,'data.csv'),encoding='utf-8')
'''
if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="mlops/mlops_main/config/config.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main(config_path=parsed_args.config)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e
