from app.models.entities.usuario_entity import UsuarioEntity
from app.models.entities.operario_entity import OperarioEntity, OperarioEmpresaAsociacion
from app.models.entities.empresa_entity import EmpresaEntity
from app.models.entities.centro_Trabajo_entity import CentroTrabajoEntity
from app.models.entities.contrato_entity import ContratoEntity
from app.models.entities.documento_entity import DocumentoEntity
from app.configuration.configuracion_Database import db
from app.configuration.configuracion_Bcrypt import bcrypt
import uuid
import datetime

def crear_usuario_normal_si_no_existe(operario_id: int):
    ya_hay_usuarios = UsuarioEntity.query.filter_by(nombre_usuario="CalidadTotalUsuario").first() is not None

    if ya_hay_usuarios:
        print("ℹ️ Ya existe un usuario. No se crea el usuario 'CalidadTotalUsuario'.")
        return None

    # Crear el usuario con rol usuario
    usuario = UsuarioEntity(
        nombre_usuario="CalidadTotalUsuario",
        contraseña=bcrypt.generate_password_hash("usuariocalidad2025*").decode('utf-8'),
        rol="usuario",
        operario_id=operario_id
    )
    db.session.add(usuario)
    db.session.commit()
    print("✅ Usuario con rol 'usuario' creado.")
    return usuario.id


def crear_operario_usuario_si_no_existe():
    operario_existente = OperarioEntity.query.filter_by(numero_cedula="0000000001").first()
    
    if operario_existente is None:
        operario_usuario = OperarioEntity(
            numero_cedula="0000000001",
            nombre="Usuario",
            apellido="Calidad",
            correo="usuario@sistema.com",
            numero_telefonico="0018820001"
        )
        db.session.add(operario_usuario)
        db.session.commit()

        print("✅ Operario usuario creado sin asociación a empresa.")
        return operario_usuario.id
    else:
        print("ℹ️ Ya existe el operario 'Usuario', no se crea otro.")
        return operario_existente.id

def crear_usuario_admin_si_no_existe(operario_id: int):
    ya_hay_admins = UsuarioEntity.query.filter_by(nombre_usuario="CalidadTotalAdmin").first() is not None

    if ya_hay_admins:
        print("ℹ️ Ya existe al menos un administrador. No se crea el usuario 'CalidadTotalAdmin'.")
        return None

    # Crear el usuario administrador solo si no existen administradores
    usuario_admin = UsuarioEntity(
        nombre_usuario="CalidadTotalAdmin",
        contraseña=bcrypt.generate_password_hash("calidadadmintotal2025*").decode('utf-8'),
        rol="administrador",
        operario_id=operario_id
    )
    db.session.add(usuario_admin)
    db.session.commit()
    print("✅ Usuario administrador 'Rafael' creado.")
    return usuario_admin.id

def crear_operario_admin_si_no_existe():
    operario_existente = OperarioEntity.query.filter_by(numero_cedula="0000000000").first()
    
    if operario_existente is None:
        operario_admin = OperarioEntity(
            numero_cedula="0000000000",
            nombre="Total",
            apellido="Calidad",
            correo="admin@sistema.com",
            numero_telefonico="0018820000"
        )
        db.session.add(operario_admin)
        db.session.commit()

        print("✅ Operario administrador creado sin asociación a empresa.")
        return operario_admin.id
    else:
        print("ℹ️ Ya existe el operario 'Rafael', no se crea el administrador.")
        return operario_existente.id

# Función para ejecutar todas las creaciones
def inicializar_datos_prueba():
    print("--- Iniciando proceso de inicialización de datos ---")

    operario_id = crear_operario_admin_si_no_existe()
    crear_usuario_admin_si_no_existe(operario_id)

    operario_usuario_id = crear_operario_usuario_si_no_existe()
    crear_usuario_normal_si_no_existe(operario_usuario_id)
    

    print("\n--- Proceso de inicialización de datos completado ---")