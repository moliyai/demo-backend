import pandas as pd
from src.config import Config

config = Config("configs/main.yaml").read()
price_config = Config("configs/prices.yaml").read()
model_config = Config("configs/model.yaml").read()
USER_INPUT_CSV = config["user_predictions_path"]["path"]

class Database:
    def __init__(self):
        self.model = self.load_model()

    def load_model(self):
        path = config["database"]["path"]
        model = pd.read_pickle(f'{path}/lgbm_ehtirom.pkl')
        return model


database = Database()