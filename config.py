import os

from dotenv import load_dotenv

from os_handle import config_load


# Radar graph axes names for practice and lectors.
# WARNING axes names must be same as answers index.
# Histogram axes names. In current state consider format names as two line text.
radar_l, radar_p, y_hist, hist_11_name, hist_12_name=config_load()


# Dictionary of questions format 1_5 in two groups for histograms and for radar graphs.
# max_mark uses in parse module does not affect to graphs
l_ans_mask = {"radar":[1,2,3,4,5,6,7,8], "hist":[11,12]}
p_ans_mask = {"radar":[4,5,6,7,8,14], "hist":[11,12]}
max_mark = 5


#debug state if True generate results only for "fbme" faculty
debug = True

load_dotenv()

#Database connection variables see README to get structure of .env file
host = os.getenv("HOST")
port = os.getenv("PORT")
db_name = os.getenv("DB_NAME")
user = os.getenv("USER")
password = os.getenv("PASS")
