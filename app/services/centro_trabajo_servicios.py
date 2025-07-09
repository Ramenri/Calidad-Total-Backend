from app.models.entities.centro_Trabajo_entity import CentroTrabajoEntity
from app.utils.utils_historial import registrar_historial
from app.configuration.configuracion_Database import db

class CentroServicios:

    @staticmethod
    @registrar_historial(
        accion="Actualizar centro de trabajo",
        peticion="PUT",
        descripcion_fn=lambda id, nombre, codigo, estado, resultado, **kwargs: (
            f"Se actualizó el centro de trabajo ID {id} con nombre '{nombre}', código {codigo} y estado {'activo' if estado else 'inactivo'}"
            if resultado is None else f"Error al actualizar centro ID {id}"
        )
    )
    def actualizar(id: str, nombre: str, codigo: int, estado: bool):
        centroEncontrado = CentroTrabajoEntity.query.get(id)
        if centroEncontrado:
            centroEncontrado.nombre = nombre
            centroEncontrado.codigo = codigo
            centroEncontrado.estado = estado
            db.session.commit()

    @staticmethod
    @registrar_historial(
        accion="Eliminar centro de trabajo",
        peticion="DELETE",
        descripcion_fn=lambda id, resultado, **kwargs: (
            f"Se eliminó el centro de trabajo ID {id}"
            if resultado is None else f"Error al eliminar centro ID {id}"
        )
    )
    def eliminar(id):
        centroEncontrado = CentroTrabajoEntity.query.get(id)
        if centroEncontrado:
            db.session.delete(centroEncontrado)
            db.session.commit()

    @staticmethod
    @registrar_historial(
        accion="Crear centro de trabajo",
        peticion="POST",
        descripcion_fn=lambda centroTrabajoEntity, resultado, **kwargs: (
            f"Se creó un centro de trabajo con nombre '{centroTrabajoEntity.nombre}', código {centroTrabajoEntity.codigo}"
            if resultado else "Error al crear centro de trabajo"
        )
    )
    def crear(centroTrabajoEntity: CentroTrabajoEntity) -> CentroTrabajoEntity:
       db.session.add(centroTrabajoEntity)
       db.session.commit()
       return centroTrabajoEntity
    
    @staticmethod
    def filtrar_por_empresa(empresa_id: str):
        return CentroTrabajoEntity.query.filter_by(empresa_id=empresa_id).all()

    @staticmethod
    def obtener_todo() -> list[CentroTrabajoEntity]:
        return CentroTrabajoEntity.query.all()