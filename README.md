# Animated NFL play viewer

This is a [streamlit](https://streamlit.io) app that animates NFL game plays 
using data from the Kaggle project
[NFL Big Data Bowl 2021](https://www.kaggle.com/c/nfl-big-data-bowl-2021).
It is based on code from an excellent talk that I saw at 
[PyCon 2022](https://us.pycon.org/2022/schedule/presentation/25/) by Miranda 
Auhl. 

To run the code in this repo you'll need to:

1. run the `fetch_data.sh` script after following the instructions in the
   comments to install the Kaggle API
1. Install streamlit by running `pip install streamlit`
1. Start the streamlit app by running `streamlit run app.py`