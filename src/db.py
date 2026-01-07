import pandas as pd
from src.config import Config
import pickle

config = Config("configs/main.yaml").read()
price_config = Config("configs/prices.yaml").read()
model_config = Config("configs/model.yaml").read()
shap_config = Config("configs/shap.yaml").read()
USER_INPUT_CSV = config["user_predictions_path"]["path"]

class Database:
    def __init__(self):
        self.model = self.load_model()


    def load_model(self):
        with open("models/lgbm_ehtirom.pkl", "rb") as f:
            model = pickle.load(f)
        return model


database = Database()