import jwt

class ExceptionExpiredSignatureError(jwt.ExpiredSignatureError):
    def __init__(self, message):
        self.message = message

class ExceptionInvalidTokenError(jwt.InvalidTokenError):
    def __init__(self, message):
        self.message = message

class ExceptionRoleNotAllowedError(Exception):
    def __init__(self, message):
        self.message = message

class ExceptionRoleNotPermittedError(Exception):
    def __init__(self, message):
        self.message = message
