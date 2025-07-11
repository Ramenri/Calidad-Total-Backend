from app.models.entities.contrato_entity import ContratoEntity
from app.models.entities.operario_entity import OperarioEntity
from app.models.entities.empresa_entity import EmpresaEntity
from app.models.entities.centro_Trabajo_entity import CentroTrabajoEntity
from app.configuration.configuracion_Database import db
from app.utils.utils_historial import registrar_historial
from datetime import datetime

class ContratoServicios:

    @staticmethod
    @registrar_historial(
        accion="Crear contrato",
        peticion="POST",
        descripcion_fn=lambda contratoEntity, resultado, **kwargs: (
            f"Se creó un contrato para el operario ID {contratoEntity.operario_id} con fecha de inicio {contratoEntity.fecha_inicio}"
            if resultado else "Error al crear contrato"
        )
    )
    def crear(contratoEntity: ContratoEntity) -> ContratoEntity:
       db.session.add(contratoEntity)
       db.session.commit()
       return contratoEntity
    
    @staticmethod
    def obtener_contratos_por_empresa(empresa_id: int):
        contratos = (
            db.session.query(ContratoEntity).join(OperarioEntity, ContratoEntity.operario_id == OperarioEntity.id).filter(OperarioEntity.enoresa_id == empresa_id).all()
        )

        return [contrato.get_json() for contrato in contratos]
    
    @staticmethod
    @registrar_historial(
        accion="Cambiar estado de contrato",
        peticion="PUT",
        descripcion_fn=lambda id, nuevo_estado, resultado, **kwargs: (
            f"Se cambió el estado del contrato ID {id} a {'activo' if nuevo_estado else 'inactivo'}"
            if isinstance(resultado, dict) and "message" in resultado
            else f"Error al cambiar estado del contrato ID {id}"
        )
    )
    def actualizar_contrato(id: int, data: dict):
        contrato = ContratoEntity.query.get(id)

        if not contrato:
            return {"error": "Contrato no encontrado"}, 404

        # Campos permitidos para actualizar
        campos_actualizables = ['cargo', 'fecha_inicio', 'fecha_fin', 'estado']

        for campo in campos_actualizables:
            if campo in data:
                setattr(contrato, campo, data[campo])

        db.session.commit()

        return {"message": "Contrato actualizado correctamente"}
    
    @staticmethod
    def obtener_cargos():
        cargos = db.session.query(ContratoEntity.cargo).distinct().all()
        return [cargo[0] for cargo in cargos]
    
    @staticmethod
    def obtener_contratos_por_operario_y_empresa(operario_id: int, empresa_id: int):
        contratos = (
            db.session.query(ContratoEntity)
            .join(CentroTrabajoEntity, ContratoEntity.centro_id == CentroTrabajoEntity.id)
            .filter(ContratoEntity.operario_id == operario_id)
            .filter(CentroTrabajoEntity.empresa_id == empresa_id)
            .order_by(ContratoEntity.fecha_inicio.desc())
            .all()
        )
        return [contrato.get_json() for contrato in contratos]
    
    @staticmethod
    @registrar_historial(
        accion="Extender contrato",
        peticion="PUT",
        descripcion_fn=lambda contrato_id, nueva_fecha_fin, resultado, **kwargs: (
            f"Se extendió el contrato ID {contrato_id} hasta {nueva_fecha_fin}"
            if isinstance(resultado, dict) or isinstance(resultado, ContratoEntity)
            else f"Error al extender contrato ID {contrato_id}"
        )
    )
    def extender_contrato(contrato_id: int, nueva_fecha_fin: str) -> dict:
        contrato = ContratoEntity.query.filter_by(id=contrato_id).first()

        if not contrato:
            raise ValueError("Contrato no encontrado")

        try:
            nueva_fecha = datetime.strptime(nueva_fecha_fin, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Formato de fecha inválido. Debe ser YYYY-MM-DD.")

        if nueva_fecha <= contrato.fecha_fin:
            raise ValueError("La nueva fecha debe ser posterior a la actual.")

        contrato.fecha_fin = nueva_fecha
        db.session.commit()

        return contrato.get_json()
    