class APIError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"Code: {code} Message: {message}")

    def __str__(self) -> str:
        return super().__str__()


class AuthError(Exception):
    def __init__(self, code: int, message: str):
        self._code = code
        self._message = message
        super().__init__(f"Code: {code} Message: {message}")

    def code(self) -> int:
        return self._code
    
    def message(self) -> str:
        return self._message

    def __str__(self) -> str:
        return self._message    