from app.models.entities.usuario_entity import UsuarioEntity
from app.models.entities.operario_entity import OperarioEntity
from app.models.entities.empresa_entity import EmpresaEntity
from app.models.entities.centro_Trabajo_entity import CentroTrabajoEntity
from app.models.entities.contrato_entity import ContratoEntity
from app.models.entities.documento_entity import DocumentoEntity
from app.configuration.configuracion_Database import db
from app.configuration.configuracion_Bcrypt import bcrypt
import uuid
import datetime



def crear_usuario_admin_si_no_existe(operario_id: str):
    if UsuarioEntity.query.filter_by(nombre_usuario="Rafael").first() is None:
        usuario_admin = UsuarioEntity(
            nombre_usuario="Rafael",
            contraseña=bcrypt.generate_password_hash("admin123").decode('utf-8'),
            rol="administrador",
            operario_id=operario_id
        )
        db.session.add(usuario_admin)
        db.session.commit()
        print("✅ Usuario administrador creado.")
        return usuario_admin.id # Retorna el ID del operario admin
    else:
        print("ℹ️ Ya existe el usuario 'Rafael', no se crea el administrador.")
        return UsuarioEntity.query.filter_by(nombre_usuario="Rafael").first().id

def crear_operario_admin_si_no_existe():
    if OperarioEntity.query.filter_by(numero_cedula="0000000000").first() is None:
        operario_admin = OperarioEntity(
            numero_cedula="0000000000",
            nombre="Rafael Antonio",
            apellido="Mendez Rios",
            correo="admin@sistema.com",
            estado=True,
            numero_telefonico="0018820000"
        )
        db.session.add(operario_admin)
        db.session.commit()
        print("✅ Operario administrador creado.")
        return operario_admin.id # Retorna el ID del operario admin
    else:
        print("ℹ️ Ya existe el operario 'Rafael', no se crea el administrador.")
        return OperarioEntity.query.filter_by(numero_cedula="0000000000").first().id


# Función para ejecutar todas las creaciones
def inicializar_datos_prueba():
    print("--- Iniciando proceso de inicialización de datos ---")

    operario_id = crear_operario_admin_si_no_existe()
    crear_usuario_admin_si_no_existe(operario_id)

    print("\n--- Proceso de inicialización de datos completado ---")