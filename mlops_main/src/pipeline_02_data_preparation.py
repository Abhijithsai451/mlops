import glob
import logging
import os
import argparse
from mlops_main import project_secrets
from mlops_main.src.utils.common import read_yaml
import pandas as pd

STAGE = "State 02 Data Importing and Feature Engineering"

log_path = project_secrets.log_path
home_path = project_secrets.home_path

logging.basicConfig(
    filename=os.path.join(home_path,log_path,'running_logs.log'),
    level=logging.DEBUG,
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def main(config_path):
    # TO DO
    # 3. Exploratory Data Analysis (Matplotlib and sklearn)
    # 4. Prepare and archive the data (stage into a temp location)


    ## read config files
    config = read_yaml(os.path.join(home_path,config_path))

    # 1. Importing the data -> using YAML & Creating the data frame
    data_path = os.path.join(home_path,config['data_source']['batch_files'])
    csv_files = glob.glob(data_path + "/*.csv")
    logging.info(">>>>>>>>>>2.1 Importing the Data  <<<<<<<<<")
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
        df.to_csv(os.path.join(archive_path,'data.csv'))
    else:
        logging.info("Archive path does not exist. creating the file location ")
        os.mkdir(archive_path)
        logging.info("Created the file location and Saving the file to the location")
        df.to_csv(os.path.join(archive_path,'data.csv'))

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



