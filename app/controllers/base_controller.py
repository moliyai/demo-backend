from fastapi import Request


class BaseController:
    def __init__(self, request: Request):
        self.code = 200
        self.message = 'ok!'
        self.request = request

    def set_code(self, code: int):
        self.code = code

    def set_message(self, message: str):
        self.message = message

    def compose_data(self, data):
        return {
            'code': self.code,
            'message': self.message,
            'data': data
        }
