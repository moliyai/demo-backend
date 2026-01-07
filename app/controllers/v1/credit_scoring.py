from fastapi import Request
from app.controllers.base_controller import BaseController
from src.predict import predictor


class CreditScoring(BaseController):
    def __init__(self, request: Request):
        super().__init__(request)
        self.language = getattr(request.state, "language", "en")

    def make_credit_score(self, data: dict):
        if not data or not isinstance(data, dict):
            self.set_code(400)
            self.set_message(
                {
                    "en": "Invalid input data",
                    "ru": "Неверные входные данные",
                    "uz": "Noto‘g‘ri kiritilgan ma’lumotlar"
                }[self.language]
            )
            return self.compose_data(data=[])

        result = predictor.run(data, self.language)

        return self.compose_data(data=result)
