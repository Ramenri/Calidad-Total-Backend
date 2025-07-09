from app.configuration.configuracion_Database import db
from app.models.entities.historial_entity import HistorialEntity
from app.models.entities.usuario_entity import UsuarioEntity
import pytz
from datetime import datetime

class HistorialServicios:

    @staticmethod
    def registrar(usuario_id, accion, peticion, rol, descripcion) -> HistorialEntity:
        try:
            historialEntity = HistorialEntity()
            zona_colombia = pytz.timezone('America/Bogota')
            ahora_colombia = datetime.now(zona_colombia)
            historialEntity.usuario_id = usuario_id
            historialEntity.accion = accion
            historialEntity.peticion = peticion
            historialEntity.rol = rol
            historialEntity.fecha = ahora_colombia.date()
            historialEntity.hora = ahora_colombia.time()
            historialEntity.descripcion = descripcion
            db.session.add(historialEntity)
            db.session.commit()
            return historialEntity
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def obtenerTodos() -> list[HistorialEntity]:
        try:
            todosHistorial: list[HistorialEntity] = (
                HistorialEntity.query.order_by(HistorialEntity.fecha.desc(), HistorialEntity.hora.desc()).all()
            )

            respuestaLista: list[dict] = []

            for historial in todosHistorial:
                usuario = UsuarioEntity.query.get(historial.usuario_id)
                data: dict = {
                    "id": historial.id,
                    "usuario": usuario.get_json(),
                    "accion": historial.accion,
                    "peticion": historial.peticion,
                    "rol": historial.rol,
                    "fecha": historial.fecha.strftime("%Y-%m-%d"),
                    "hora": historial.hora.strftime("%I:%M:%S %p"),
                    "descripcion": historial.descripcion
                }
                respuestaLista.append(data)

            return respuestaLista
        except Exception as e:
            raise e