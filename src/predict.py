import os
from datetime import datetime, date
import pandas as pd
from src.db import database, price_config, model_config, USER_INPUT_CSV


class Predictor:
    def __init__(self):
        self.model = database.model
        self.user_input_csv = USER_INPUT_CSV
        self.threshold = 60

        self.shaped_bread_prices = price_config["prices"]["shaped_bread"]
        self.cottonseed_oil_prices = price_config["prices"]["cottonseed_oil"]
        self.beef_prices = price_config["prices"]["beef"]

        self.feature_cols = model_config["model"]["feature_cols"]
        self.categorical_cols = model_config["model"]["categorical_cols"]


    def run(self, input_data: dict):

        df = pd.DataFrame([input_data])
        date_birth = df.get('date_birth')[0]
    
        try:
            birth_date = datetime.strptime(date_birth, "%d.%m.%Y").date()
        except ValueError:
            return {"error": "Invalid date format. Use DD-MM-YYYY."}
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        df.drop(columns=['date_birth'], inplace=True)
    
        df['age'] = age
        df['shaped_bread(som)'] = df['region'].map(self.shaped_bread_prices)
        df['cottonseed oil(som)'] = df['region'].map(self.cottonseed_oil_prices)
        df['beef(som)'] = df['region'].map(self.beef_prices)

        X = df[self.feature_cols].copy()

        for col in self.categorical_cols:
            X[col] = X[col].astype("category")

        y_proba_bad = self.model.predict_proba(X)[:, 1][0]
        y_proba_good = 1 - y_proba_bad

        bad_prob = round(y_proba_bad*100, 2)
        good_prob = round(y_proba_good*100, 2)

        status = "Approved" if bad_prob < self.threshold else "Not Approved"

        df['predicted_client_status'] = status
        df['good_prob'] = good_prob
        df['bad_prob'] = bad_prob


        if not os.path.exists(self.user_input_csv):
            df.to_csv(self.user_input_csv, index=False)
        else:
            df.to_csv(self.user_input_csv, mode='a', header=False, index=False)

        return {
            "prediction": status,
            "good_prob": good_prob,
            "bad_prob%": bad_prob,
        }

predictor = Predictor()
