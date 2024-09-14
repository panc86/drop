import os

api_config = {
    "description": "REST API to geocode disaster based text",
    "license_info": {
        "name": "Change me",
        "url": "https://example.com",
    },
    "title": "Text Geocoder API",
    "version": "0.1.0"
}

data_dir = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(data_dir, exist_ok=True)

# change DeepPavlov Download path. Default is $HOME/.deeppavlov
os.environ["HOME"] = data_dir

gazetteer_filepath = os.path.join(data_dir, "gazetteer.json.zip")
