rm -rf ./venv
virtualenv venv
source venv/bin/activate

pip install streamlit pandas numpy ipython pytest coverage snakeviz
