from functools import wraps
from flask import request
from app.services.historial_servicios import HistorialServicios
from app.utils.utils_jwt import UtilsJWT

def registrar_historial(accion: str, peticion: str, descripcion_fn):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            resultado = func(*args, **kwargs)

            try:
                usuario = getattr(request, "user", UtilsJWT.get_usuario_info_autenticado())
                descripcion = descripcion_fn(*args, **kwargs, resultado=resultado)
                HistorialServicios.registrar(
                    usuario_id=usuario.get("id"),
                    accion=accion,
                    peticion=peticion,
                    rol=usuario.get("rol"),
                    descripcion=descripcion
                )
            except Exception as e:
                print(f"Error registrando historial automáticamente: {e}")

            return resultado
        return wrapper
    return decorator
