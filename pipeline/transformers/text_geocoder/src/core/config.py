import os


data_dir = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(data_dir, exist_ok=True)
# change DeepPavlov Download path. Default is $HOME/.deeppavlov
os.environ["HOME"] = data_dir

gazetteer_filepath = os.path.join(data_dir, "gazetteer.json.zip")
