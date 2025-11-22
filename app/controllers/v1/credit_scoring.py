from fastapi import Request
from app.controllers.base_controller import BaseController
from src.predict import predictor


class CreditScoring(BaseController):
    def __init__(self, request: Request):
        super().__init__(request)

    def make_credit_score(self, data: dict):
        if not data or not isinstance(data, dict):
            self.set_code(400)
            self.set_message("Invalid input data")
            return self.compose_data(data=[])

        result = predictor.run(data)

        return self.compose_data(data=result)
