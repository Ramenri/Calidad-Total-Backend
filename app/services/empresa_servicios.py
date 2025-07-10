from app.models.entities.empresa_entity import EmpresaEntity
from app.models.entities.operario_entity import OperarioEntity
from app.models.entities.operario_entity import association_table
from app.configuration.configuracion_Database import db
from app.utils.utils_historial import registrar_historial
from sqlalchemy import and_

class EmpresaServicios:

    @staticmethod
    def obtener_empresas_del_operario_no_afiliadas(cedulaOperario: int) -> list[EmpresaEntity]:        
        operario = OperarioEntity.query.filter_by(numero_cedula=cedulaOperario).first()
        
        if not operario:
            todasEmpresas = EmpresaEntity.query.filter_by(estado=True).all()
            return todasEmpresas
        
        empresas_no_afiliadas = db.session.query(EmpresaEntity)\
            .outerjoin(association_table, 
                      and_(EmpresaEntity.id == association_table.c.empresa_id,
                           association_table.c.operario_id == operario.id))\
            .filter(association_table.c.operario_id.is_(None))\
            .filter(EmpresaEntity.estado == True)\
            .all()
        
        return empresas_no_afiliadas

    @staticmethod
    @registrar_historial(
        accion="Actualizar empresa",
        peticion="PUT",
        descripcion_fn=lambda id, codigo, nombre, estado, resultado, **kwargs:
            f"Actualizó la empresa ID {id} con código {codigo}, nombre '{nombre}' y estado {'activo' if estado else 'inactivo'}"
            if resultado else f"No se encontró la empresa con ID {id} para actualizar"
    )
    def actualizar_empresa(id: int, codigo: int, nombre: str, estado: bool) -> bool:
        empresa: EmpresaEntity = EmpresaEntity.query.filter_by(id=id).first()

        if not empresa:
            return False
        
        empresa.codigo = codigo
        empresa.nombre = nombre
        empresa.estado = estado
        db.session.commit()
        return True

    @staticmethod
    def obtener_todo() -> list[EmpresaEntity]:
        return EmpresaEntity.query.all()
    
    @staticmethod
    @registrar_historial(
        accion="Crear empresa",
        peticion="POST",
        descripcion_fn=lambda empresaEntity, resultado, **kwargs:
            f"Se creó la empresa '{empresaEntity.nombre}' con código {empresaEntity.codigo}"
    )
    def crear(empresaEntity: EmpresaEntity) -> EmpresaEntity:
       db.session.add(empresaEntity)
       db.session.commit()
       return empresaEntity
    
    @staticmethod
    def obtener_codigo(codigo: int) -> EmpresaEntity | None:
        return EmpresaEntity.query.filter_by(codigo=codigo).first()
    
    @staticmethod
    @registrar_historial(
        accion="Eliminar empresa",
        peticion="DELETE",
        descripcion_fn=lambda codigo, resultado, **kwargs:
            f"Se eliminó la empresa con código {codigo}"
            if resultado else f"No se encontró la empresa con código {codigo} para eliminar"
    )
    def eliminar_empresa(codigo: int) -> bool:
        empresa = EmpresaEntity.query.filter_by(codigo=codigo).first()

        if not empresa:
            return False
        
        db.session.delete(empresa)
        db.session.commit()
        return True 
        
    @staticmethod
    @registrar_historial(
        accion="Actualizar estado de empresa",
        peticion="PUT",
        descripcion_fn=lambda codigo, nuevo_estado, resultado, **kwargs:
            f"Actualizó el estado de la empresa con código {codigo} a {'activo' if nuevo_estado else 'inactivo'}"
            if resultado else f"No se encontró la empresa con código {codigo} para actualizar estado"
    )
    def actualizar_estado(codigo: int, nuevo_estado: bool) -> bool:
        empresa = EmpresaEntity.query.filter_by(codigo=codigo).first()

        if not empresa:
            return False
        
        empresa.estado = nuevo_estado
        db.session.commit()
        return True
    
    @staticmethod
    def obtener_por_id(id_empresa: int) -> EmpresaEntity | None:
        return EmpresaEntity.query.get(id_empresa)


    