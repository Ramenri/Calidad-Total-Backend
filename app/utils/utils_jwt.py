from datetime import datetime, timedelta
from functools import wraps

import jwt
import json

from app.exceptions.exception_token import ExceptionExpiredSignatureError, ExceptionInvalidTokenError, \
    ExceptionRoleNotAllowedError, ExceptionRoleNotPermittedError
from app.models.entities.usuario_entity import UsuarioEntity
from flask import Request, request

from app.validators.validators_jwt import ValidatorsJWT

SECRET:str = "$9J54j9SMCE2Abfln$24b77a5c238dd03b71f11cc4c754fb1d48eb64548c65c028a8ffb5d3fa9f1b42"

class UtilsJWT:

    @staticmethod
    def getToken(requestData: Request) -> str:
        return requestData.headers["Authorization"].split(" ")[1]

    @staticmethod
    def generatedToken(user: UsuarioEntity) -> str:
        payload = {
            'exp': int((datetime.now() + timedelta(minutes=240)).timestamp()),
            'iat': int(datetime.now().timestamp()),
            'sub': json.dumps(user.get_json())
        }

        token = jwt.encode(payload=payload, key=SECRET, algorithm='HS256')
        return token

    @staticmethod
    def validateToken(requestData: Request) -> dict:

        ValidatorsJWT.validateHeaderAuthorization(request=requestData)

        token:str = UtilsJWT.getToken(requestData=requestData)

        ValidatorsJWT.validateToken(token=token)

        try:
            decoded_token = jwt.decode(token, SECRET, algorithms=['HS256'])
            return decoded_token
        except jwt.ExpiredSignatureError as e:
            raise ExceptionExpiredSignatureError(e)
        except jwt.InvalidTokenError as e:
            raise ExceptionInvalidTokenError(e)

    @staticmethod
    def get_usuario_info_autenticado():
        return getattr(request, "user", {})

    @staticmethod
    def token_required(roles=None):
        roles: list = ValidatorsJWT.ValidateListRolesOnTokenRequired(roles=roles)
        def wrapper(function):
            @wraps(function)
            def decorated(*args, **kwargs):
                if request.method == 'OPTIONS':
                    return '', 200
                
                try:
                    decoded_token = UtilsJWT.validateToken(request)
                    request.user = json.loads(decoded_token['sub'])
                    user_role = request.user.get('rol')

                    ValidatorsJWT.validateRolesPermitted(listRoles=roles, role=user_role)

                except Exception as e:
                    raise ExceptionRoleNotPermittedError(e)

                return function(*args, **kwargs)

            return decorated
        return wrapper