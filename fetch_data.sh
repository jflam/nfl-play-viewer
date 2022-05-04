# Install Kaggle API from: https://github.com/Kaggle/kaggle-api
# If you follow instructions, you will download a kaggle.json file from
# Kaggle and copy it to here: ~/.kaggle/kaggle.json 
# Make sure to chmod 600 ~/.kaggle/kaggle.json

# Once this is done, the following command will download the dataset
# into the current directory. The streamlit program assumes that the
# data files games.csv and week1.csv is in the same directory as app.py
kaggle competitions download -c nfl-big-data-bowl-2021