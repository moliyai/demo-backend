import pandas as pd
from src.config import Config
from pathlib import Path

config = Config("configs/main.yaml").read()
price_config = Config("configs/prices.yaml").read()
model_config = Config("configs/model.yaml").read()
USER_INPUT_CSV = config["user_predictions_path"]["path"]

class Database:
    def __init__(self):
        self.model = self.load_model()

    def get_model_path(self):
        demo_root = Path(__file__).resolve().parent.parent 
        model_path = demo_root / config['database']['path'] / "lgbm_ehtirom.pkl"

        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found at {model_path}")
        return model_path


    def load_model(self):
        path = self.get_model_path()
        model = pd.read_pickle(path)
        print(f"Loaded model from {path}")
        return model

database = Database()
