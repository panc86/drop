import os


filedir = os.path.dirname(__file__)
os.makedirs(os.path.join(filedir, "log"), exist_ok=True)

log_file = os.path.join(filedir, "logging.ini")
log_defaults = {'logfilename': os.path.join(filedir, "log", "error.lor")}
