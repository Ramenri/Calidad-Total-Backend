from flask import jsonify

from app.exceptions.exception_token import ExceptionExpiredSignatureError, ExceptionInvalidTokenError, ExceptionRoleNotAllowedError, ExceptionRoleNotPermittedError
from app.models.response.response_error import ResponseError

def responseErrorHandlersGlobal(app):

    @app.errorhandler(ValueError)
    def handlerValueError(error):
        responseError: ResponseError = ResponseError(
            status_code=400,
            status="BAD REQUEST",
            message=str(error)
        )
        return jsonify(responseError.getJSON()), 400

    @app.errorhandler(ExceptionExpiredSignatureError)
    def handlerExceptionExpiredSignatureError(error):
        responseError: ResponseError = ResponseError(
            status_code=401,
            status="UNAUTHORIZED",
            message=str(error)
        )
        return jsonify(responseError.getJSON()), 401

    @app.errorhandler(ExceptionInvalidTokenError)
    def handlerExceptionInvalidTokenError(error):
        responseError: ResponseError = ResponseError(
            status_code=401,
            status="UNAUTHORIZED",
            message=str(error)
        )
        return jsonify(responseError.getJSON()), 401

    @app.errorhandler(ExceptionRoleNotAllowedError)
    def handlerExceptionRoleNotAllowedError(error):
        responseError: ResponseError = ResponseError(
            status_code=403,
            status="FORBIDDEN",
            message=str(error)
        )
        return jsonify(responseError.getJSON()), 403

    @app.errorhandler(ExceptionRoleNotPermittedError)
    def handlerExceptionRoleNotPermittedError(error):
        responseError: ResponseError = ResponseError(
            status_code=401,
            status="UNAUTHORIZED",
            message=str(error)
        )
        return jsonify(responseError.getJSON()), 401