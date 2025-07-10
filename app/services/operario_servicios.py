from app.models.entities.operario_entity import OperarioEntity
from app.models.entities.contrato_entity import ContratoEntity
from app.models.entities.centro_Trabajo_entity import CentroTrabajoEntity
from app.models.entities.empresa_entity import EmpresaEntity
from app.utils.utils_historial import registrar_historial
from app.configuration.configuracion_Database import db
from sqlalchemy.orm import aliased
import datetime

class OperarioServicios:

    @staticmethod
    def obtenerTodos() -> list[OperarioEntity]:
        return OperarioEntity.query.all()
        
    @staticmethod
    def crear(operarioEntity: OperarioEntity) -> OperarioEntity:
       db.session.add(operarioEntity)
       db.session.commit()
       return operarioEntity
    
    @staticmethod
    @registrar_historial(
        accion="Actualizar estado de operario",
        peticion="PUT",
        descripcion_fn=lambda numero_cedula, nuevo_estado, resultado, **kwargs: (
            f"Estado del operario con cédula {numero_cedula} "
            f"actualizado a {'activo' if nuevo_estado else 'inactivo'}"
            if resultado else f"No se encontró el operario con cédula {numero_cedula}"
        )
    )
    def actualizar_estado(numero_cedula: int, nuevo_estado: bool) -> bool:
        operario = OperarioEntity.query.filter_by(numero_cedula=numero_cedula).first()

        if not operario:
            return False       
        operario.estado = nuevo_estado
        db.session.commit()
        return True
    
    @staticmethod
    def buscar_por_id(id: int) -> OperarioEntity | None:
        return OperarioEntity.query.filter_by(id=id).first()
    
    @staticmethod
    def filtrar_operario(filtros: dict):
        query = db.session.query(OperarioEntity)
        contrato_alias = aliased(ContratoEntity)

        necesita_contrato = filtros.get('centro_id') or filtros.get('cargo')
        if necesita_contrato:
            query = query.outerjoin(contrato_alias, OperarioEntity.contratos)

        if filtros.get('empresa_id'):
            query = query.join(OperarioEntity.empresas).filter(EmpresaEntity.id == filtros['empresa_id'])

        if filtros.get('numero_cedula'):
            query = query.filter(OperarioEntity.numero_cedula == filtros['numero_cedula'])

        if filtros.get('nombre'):
            query = query.filter(OperarioEntity.nombre.ilike(f"%{filtros['nombre']}%"))

        if filtros.get('estado'):
            estado = filtros['estado'].lower() == 'activo'
            query = query.filter(OperarioEntity.estado == estado)

        if filtros.get('centro_id'):
            query = query.filter(contrato_alias.centro_id == filtros['centro_id'])

        if filtros.get('cargo'):
            query = query.filter(contrato_alias.cargo == filtros['cargo'])

        operarios = query.all()

        operarios_con_estado_contrato = []
        for operario in operarios:
            contrato = operario.contratos[0] if operario.contratos else None

            if contrato is not None:
                estado_contrato = "activo" if contrato.estado else "finalizado"
            else:
                estado_contrato = "sin contrato"

            operario_dict = operario.get_json()
            operario_dict["estado_contrato"] = estado_contrato
            operarios_con_estado_contrato.append(operario_dict)

        return operarios_con_estado_contrato
    
    @staticmethod
    def obtener_por_empresa(empresa_id: int) -> list[OperarioEntity]:
        operarios = (
            db.session.query(OperarioEntity)
            .join(OperarioEntity.empresas)
            .filter(EmpresaEntity.id == empresa_id)
            .all()
        )

        operarios_con_estado_contrato = []
        for operario in operarios:
            contrato = operario.contratos[0] if operario.contratos else None

            if contrato is not None:
                estado_contrato = "activo" if contrato.estado else "finalizado"
            else:
                estado_contrato = "sin contrato"

            operario_dict = operario.get_json()
            operario_dict["estado_contrato"] = estado_contrato
            operarios_con_estado_contrato.append(operario_dict)

        return operarios_con_estado_contrato
    
    @staticmethod
    def eliminar_operario_por_id(operario_id):
        operario = OperarioEntity.query.get(operario_id)

        if not operario:
            return {"status": "error", "msg": "Operario no encontrado"}

        db.session.delete(operario)
        db.session.commit()

        return {"status": "success", "msg": "Operario, contratos y documentos eliminados correctamente"}
    
    @staticmethod
    @registrar_historial(
        accion="Actualizar operario",
        peticion="PUT",
        descripcion_fn=lambda operario_id, data, resultado, **kwargs: (
            f"Operario con ID {operario_id} actualizado correctamente"
            if "error" not in resultado else f"Error al actualizar operario: {resultado.get('error')}"
        )
    )
    def actualizar_operario(operario_id: int, data: dict) -> dict:
        operario = OperarioEntity.query.filter_by(id=operario_id).first()
        if not operario:
            return {"error": "Operario no encontrado"}
        
        nueva_cedula = data.get("numero_cedula")
        if nueva_cedula and nueva_cedula != operario.numero_cedula:
            operario_existente = OperarioEntity.query.filter_by(numero_cedula=nueva_cedula).first()
            if operario_existente:
                return {"error": "Ya existe un operario con esa cédula"}
        
        print(f"Datos antes de actualizar:")
        print(f"nombre: {data.get('nombre')}")
        print(f"apellido: {data.get('apellido')}")
        print(f"numero_cedula: {data.get('numero_cedula')}")
        print(f"numero_telefonico: {data.get('numero_telefonico')}")
        print(f"correo: {data.get('correo')}")
        print(f"estado: {data.get('estado')}")
        
        if data.get("nombre") is not None:
            operario.nombre = data.get("nombre")
        if data.get("apellido") is not None:
            operario.apellido = data.get("apellido")
        if data.get("numero_cedula") is not None:
            operario.numero_cedula = data.get("numero_cedula")
        if data.get("numero_telefonico") is not None:
            operario.numero_telefonico = data.get("numero_telefonico")
        if data.get("correo") is not None:
            operario.correo = data.get("correo")
        if data.get("estado") is not None:
            estado_valor = data.get("estado")
            if isinstance(estado_valor, str):
                operario.estado = estado_valor.lower() == 'true'
            else:
                operario.estado = bool(estado_valor)
        
        try:
            db.session.commit()
            return operario.get_json()
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}

    @staticmethod
    @registrar_historial(
        accion="Crear operario con relaciones",
        peticion="POST",
        descripcion_fn=lambda data, resultado, **kwargs: (
            f"Se creó un nuevo operario con cédula {data.get('cedula')}"
            if resultado.get("status") == "success" else f"Error al crear operario: {resultado.get('message')}"
        )
    )
    def crear_operario_relacionando_todo(data: dict) -> dict:
        try:
            empresa_id = data.get("empresa")
            if not empresa_id:
                return {"status": "error", "message": "Se requiere el ID de la empresa para crear el operario."}
            
            # Verificar que la empresa existe
            empresa = EmpresaEntity.query.get(empresa_id)
            if not empresa:
                return {"status": "error", "message": f"Empresa con ID {empresa_id} no encontrada."}
            
            # Verificar si ya existe un operario con esa cédula
            operario_existente = OperarioEntity.query.filter_by(numero_cedula=str(data["cedula"])).first()
            
            if operario_existente:
                # Verificar si el operario ya está asociado a esta empresa
                if empresa not in operario_existente.empresas:
                    # Si no está asociado, hacer la asociación
                    operario_existente.empresas.append(empresa)
                    operario_a_usar = operario_existente
                    mensaje_operario = "Operario existente asociado a nueva empresa"
                else:
                    # Si ya está asociado, usar el operario existente
                    operario_a_usar = operario_existente
                    mensaje_operario = "Operario existente ya asociado a la empresa"
            else:
                # 1. Crear el Operario nuevo
                operario_a_usar = OperarioEntity(
                    nombre=data["nombre"],
                    apellido=data["apellido"],
                    numero_cedula=int(data["cedula"]),
                    numero_telefonico=int(data["telefono"]),
                    correo=data["correo"],
                    estado=True
                )
                
                # 2. Asociar el Operario a la Empresa
                operario_a_usar.empresas.append(empresa)
                db.session.add(operario_a_usar)
                mensaje_operario = "Operario nuevo creado y asociado a empresa"
            
            # Hacer flush para obtener el ID del operario antes de crear el contrato
            db.session.flush()
            
            # 3. Validar centro de trabajo
            centro_trabajo_id = data.get("centroTrabajo")
            if not centro_trabajo_id:
                db.session.rollback()
                return {"status": "error", "message": "Se requiere el ID del centro de trabajo para crear el contrato."}
            
            centro_trabajo = CentroTrabajoEntity.query.get(centro_trabajo_id)
            if not centro_trabajo:
                db.session.rollback()
                return {"status": "error", "message": f"Centro de trabajo con ID {centro_trabajo_id} no encontrado."}
            
            # 4. Crear el Contrato
            fecha_inicio = datetime.datetime.strptime(data["fechaInicioContrato"], "%Y-%m-%d").date()
            fecha_fin = datetime.datetime.strptime(data["fechaFinContrato"], "%Y-%m-%d").date()
            
            nuevo_contrato = ContratoEntity(
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                estado=True,
                centro_id=centro_trabajo_id,
                operario_id=operario_a_usar.id,
                cargo=data["cargo"]
            )
            db.session.add(nuevo_contrato)
            
            db.session.commit()

            operario_json = operario_a_usar.get_json()
            operario_json["contrato_id"] = nuevo_contrato.id 
            
            return {
                "status": "success",
                "message": mensaje_operario,
                "operario": operario_json,
                "contrato": nuevo_contrato.get_json()
            }
            
        except KeyError as e:
            db.session.rollback()
            return {"status": "error", "message": f"Falta un campo requerido en los datos: {e}"}
        except ValueError as e:
            db.session.rollback()
            return {"status": "error", "message": f"Error en el formato de datos: {e}. Asegúrate que las fechas estén en 'YYYY-MM-DD'."}
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": f"Error desconocido al crear operario: {e}"}

    @staticmethod
    def filtrar_operarios_completo(filtros: dict):
        try:
            query = db.session.query(OperarioEntity)
            
            contrato_alias = aliased(ContratoEntity)
            empresa_alias = aliased(EmpresaEntity)
            centro_trabajo_alias = aliased(CentroTrabajoEntity)
            
            necesita_contrato = any([
                filtros.get('cargo'),
                filtros.get('centro_trabajo_id'),
                filtros.get('estado_contrato')
            ])
            
            necesita_empresa = filtros.get('empresa_id') is not None
            necesita_centro_trabajo = filtros.get('centro_trabajo_id') is not None
            
            if necesita_contrato:
                query = query.outerjoin(contrato_alias, OperarioEntity.contratos)
            
            if necesita_empresa:
                query = query.join(OperarioEntity.empresas).filter(
                    EmpresaEntity.id == filtros['empresa_id']
                )
            
            if necesita_centro_trabajo and necesita_contrato:
                query = query.join(
                    centro_trabajo_alias, 
                    contrato_alias.centro_id == centro_trabajo_alias.id
                )
            
            if filtros.get('nombre'):
                nombre = filtros['nombre'].strip()
                if nombre:
                    query = query.filter(
                        OperarioEntity.nombre.ilike(f"%{nombre}%")
                    )
            
            if filtros.get('numero_cedula'):
                try:
                    cedula = int(filtros['numero_cedula'])
                    query = query.filter(OperarioEntity.numero_cedula == cedula)
                except (ValueError, TypeError):
                    return {
                        "error": "El número de cédula debe ser un número válido",
                        "operarios": []
                    }
            
            if filtros.get('estado_operario'):
                estado_str = filtros['estado_operario'].lower().strip()
                if estado_str in ['activo', 'inactivo']:
                    estado_bool = estado_str == 'activo'
                    query = query.filter(OperarioEntity.estado == estado_bool)
            
            if necesita_contrato:
                if filtros.get('cargo'):
                    cargo = filtros['cargo'].strip()
                    if cargo:
                        query = query.filter(
                            contrato_alias.cargo.ilike(f"%{cargo}%")
                        )
                
                if filtros.get('centro_trabajo_id'):
                    query = query.filter(
                        contrato_alias.centro_id == filtros['centro_trabajo_id']
                    )
                
                if filtros.get('estado_contrato'):
                    estado_contrato = filtros['estado_contrato'].lower().strip()
                    if estado_contrato == 'activo':
                        query = query.filter(contrato_alias.estado == True)
                    elif estado_contrato == 'inactivo':
                        query = query.filter(contrato_alias.estado == False)
                    elif estado_contrato == 'sin_contrato':
                        query = query.filter(~OperarioEntity.contratos.any())
            
            operarios = query.distinct().all()
            operarios = query.distinct().all()
            
            operarios_procesados = []
            for operario in operarios:
                contrato_activo = None
                contratos_activos = [c for c in operario.contratos if c.estado]
                
                if contratos_activos:
                    contrato_activo = sorted(
                        contratos_activos, 
                        key=lambda c: c.fecha_inicio, 
                        reverse=True
                    )[0]
                
                operario_dict = operario.get_json()
                
                if contrato_activo:
                    operario_dict.update({
                        "estado_contrato": "activo",
                        "cargo_actual": contrato_activo.cargo,
                        "centro_trabajo_id": contrato_activo.centro_id,
                        "centro_trabajo_nombre": contrato_activo.centro_trabajo.nombre if contrato_activo.centro_trabajo else None,
                        "fecha_inicio_contrato": contrato_activo.fecha_inicio.isoformat() if contrato_activo.fecha_inicio else None,
                        "fecha_fin_contrato": contrato_activo.fecha_fin.isoformat() if contrato_activo.fecha_fin else None
                    })
                else:
                    contratos_inactivos = [c for c in operario.contratos if not c.estado]
                    if contratos_inactivos:
                        contrato_mas_reciente = sorted(
                            contratos_inactivos,
                            key=lambda c: c.fecha_inicio,
                            reverse=True
                        )[0]
                        operario_dict.update({
                            "estado_contrato": "inactivo",
                            "cargo_actual": contrato_mas_reciente.cargo,
                            "centro_trabajo_id": contrato_mas_reciente.centro_id,
                            "centro_trabajo_nombre": contrato_mas_reciente.centro_trabajo.nombre if contrato_mas_reciente.centro_trabajo else None,
                            "fecha_inicio_contrato": contrato_mas_reciente.fecha_inicio.isoformat() if contrato_mas_reciente.fecha_inicio else None,
                            "fecha_fin_contrato": contrato_mas_reciente.fecha_fin.isoformat() if contrato_mas_reciente.fecha_fin else None
                        })
                    else:
                        operario_dict.update({
                            "estado_contrato": "sin_contrato",
                            "cargo_actual": None,
                            "centro_trabajo_id": None,
                            "centro_trabajo_nombre": None,
                            "fecha_inicio_contrato": None,
                            "fecha_fin_contrato": None
                        })
                
                empresas_info = []
                for empresa in operario.empresas:
                    empresas_info.append({
                        "id": empresa.id,
                        "nombre": empresa.nombre,
                        "codigo": empresa.codigo,
                        "estado": empresa.estado
                    })
                operario_dict["empresas"] = empresas_info
                
                operarios_procesados.append(operario_dict)
            
            return {
                "success": True,
                "total": len(operarios_procesados),
                "operarios": operarios_procesados,
                "filtros_aplicados": {k: v for k, v in filtros.items() if v is not None and v != ""}
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                "error": f"Error al filtrar operarios: {str(e)}",
                "operarios": [],
                "total": 0
            }

            
