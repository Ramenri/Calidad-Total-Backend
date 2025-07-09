from flask import Request

from app.exceptions.exception_token import ExceptionRoleNotAllowedError

class ValidatorsJWT:

    @staticmethod
    def validateHeaderAuthorization(request: Request):
        if "Authorization" not in request.headers:
            raise ValueError("Token not found")
        
    @staticmethod
    def validateToken(token:str):
        if not token:
            raise ValueError("Token not found")
        
    @staticmethod
    def ValidateListRolesOnTokenRequired(roles) -> list:
        if roles is None:
            return []
        
        return roles
    
    @staticmethod
    def validateRolesPermitted(listRoles: list, role:str):
        if not listRoles:
            raise ExceptionRoleNotAllowedError("No tienes permitido acceder a este recurso")
        
        if role not in listRoles:
            raise ExceptionRoleNotAllowedError("No tienes permitido acceder a este recurso")