import argparse
import os
import logging
import argparse
import urllib.request as req
from git import Repo

from mlops_main import project_secrets
from mlops_main.src.utils.common import read_yaml, create_directories

STAGE = "Data Preparation"
log_path = project_secrets.log_path
home_path = project_secrets.home_path

logging.basicConfig(
    filename = os.path.join(home_path,log_path,'running_logs.log'),
    level= logging.DEBUG,
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode ="a"
)


def clone_data(git_path,data_path):
    os.mkdir(data_path)
    Repo.clone_from(git_path,data_path)
    logging.info(">>>>>>>>>>>>> Batch Files cloned from the GITHUB Repository <<<<<<<<<<<")



def main(config_path):

        config = read_yaml(os.path.join(home_path,config_path))
        local_data_dir = config["data_source"]["batch_files"]
        # 1. Check if the data path exists
        # 2. If path exists then continue
        data_path = os.path.join(project_secrets.home_path,local_data_dir)
        if os.path.exists(data_path):
            logging.info(">>>>>>>>>>>>> Batch Files already present <<<<<<<<<<<")
        else:
            git_path = config["data_path"]
            #clone_data(git_path,data_path)
        return logging.info(">>>>>>>>>>>>> CLONED the Repositiory <<<<<<<<<<<")


if __name__ =='__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config","-c",default="mlops/mlops_main/config/config.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n*************************************")
        logging.info(f">>>>>>>> stage {STAGE} started  <<<<<<<<<<<<")
        main(config_path = parsed_args.config)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e