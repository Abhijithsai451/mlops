# downloading the dataset
pip install kaggle
# download the Kaggle API key and add to path
# ---->>>>> Goes here <<<<<------
kaggle datasets download -d wyattowalsh/basketball

# Creating a directory and inflating the data to that directory
mkdir mlops_main/data/kaggle_data
unzip basketball.zip -d mlops_main/data/kaggle_data/


# Installing the required Packages
pip install -r mlops_main/requirements.txt

cd mlops_main/src/
python pipeline_01_data_gathering.py






