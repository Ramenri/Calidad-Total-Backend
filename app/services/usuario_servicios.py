from app.models.entities.usuario_entity import UsuarioEntity
from app.models.entities.operario_entity import OperarioEntity
from app.services.operario_servicios import OperarioServicios
from app.configuration.configuracion_Database import db
from app.configuration.configuracion_Bcrypt import bcrypt
from app.services.historial_servicios import HistorialServicios
from app.utils.utils_jwt import UtilsJWT
from app.utils.utils_historial import registrar_historial

class UsuarioServicios:

    @staticmethod
    @registrar_historial(
        accion="Crear unión con operario", 
        peticion="POST", 
        descripcion_fn=lambda usuario, **kwargs: f"Se creó un nuevo usuario con nombre: {usuario.nombre_usuario} para el operario ID: {usuario.operario_id}"
    )
    def crear_union_con_operario(usuario: UsuarioEntity):
        try:
            # Verificar si ya existe un usuario con este operario_id
            usuario_existente = UsuarioEntity.query.filter_by(operario_id=usuario.operario_id).first()
            if usuario_existente:
                return "Ya existe un usuario administrador para este operario"
            
            # Verificar si existe el operario
            operario_existente = OperarioServicios.buscar_por_id(usuario.operario_id)
            if not operario_existente:
                return "Operario no encontrado"
            
            # Verificar si ya existe un usuario con este nombre
            usuario_por_nombre = UsuarioEntity.query.filter_by(nombre_usuario=usuario.nombre_usuario).first()
            if usuario_por_nombre:
                return "Ya existe un usuario con este nombre"
            
            # Crear el nuevo usuario
            nuevo_usuario = UsuarioEntity()
            nuevo_usuario.nombre_usuario = usuario.nombre_usuario
            nuevo_usuario.contraseña = bcrypt.generate_password_hash(usuario.contraseña).decode('utf-8')
            nuevo_usuario.rol = "administrador"
            nuevo_usuario.operario_id = usuario.operario_id
            
            # Guardar en la base de datos
            db.session.add(nuevo_usuario)
            
            # Actualizar estado del operario si es necesario
            operario_existente.estado = True
            
            db.session.commit()
            return "Unión creada correctamente"
        
        except Exception as e:
            db.session.rollback()
            return f"Error al crear la unión: {str(e)}"

    @staticmethod  
    @registrar_historial(
        accion="Eliminar administrador", 
        peticion="DELETE", 
        descripcion_fn=lambda usuario_id, **kwargs: f"Se eliminó el usuario administrador con ID: {usuario_id}"
    )
    def eliminar_admin_por_usuario_id(usuario_id: str):
        try:
            # Buscar el usuario por su ID
            usuario = UsuarioEntity.query.filter_by(id=usuario_id).first()
            
            if not usuario:
                return "Usuario administrador no encontrado"
            
            # Eliminar SOLO el usuario
            db.session.delete(usuario)
            
            db.session.commit()
            
            return "Usuario administrador eliminado correctamente"
        
        except Exception as e:
            db.session.rollback()
            return f"Error al eliminar el usuario administrador: {str(e)}"

    @staticmethod
    def crear_admin(operarioData: dict, usuarioData: dict):
        operario: OperarioEntity = OperarioEntity()
        operario.numero_cedula = operarioData.get('numero_cedula')
        operario.nombre = operarioData.get('nombre')
        operario.apellido = operarioData.get('apellido')
        operario.correo = operarioData.get('correo')
        operario.numero_telefonico = operarioData.get('numero_telefonico')
        operario.estado = operarioData.get('estado')
        db.session.add(operario)
        db.session.flush()
        usuario: UsuarioEntity = UsuarioEntity()
        usuario.nombre_usuario = usuarioData.get('nombre_usuario')
        usuario.contraseña = usuarioData.get('contraseña')
        usuario.rol = usuarioData.get('rol')
        usuario.operario_id = operario.id
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def buscar_por_id(id: str) -> UsuarioEntity:
        return UsuarioEntity.query.filter_by(id=id).first()

    @staticmethod
    def obtenerTodos() -> list[UsuarioEntity]:
        return UsuarioEntity.query.all()

    @staticmethod
    def crear(usuarioEntity : UsuarioEntity) -> UsuarioEntity:
        db.session.add(usuarioEntity)
        db.session.commit()
        return usuarioEntity
    
    @staticmethod
    @registrar_historial(
        accion="Autenticación", 
        peticion="POST", 
        descripcion_fn=lambda *args, resultado=None, **kwargs: (
            f"El usuario '{args[0]}' inició sesión correctamente" if resultado else f"Fallo en intento de autenticación para usuario '{args[0]}'"
        )
    )
    def autenticar_usuario(nombre_usuario: str, contraseña: str) -> UsuarioEntity:

        usuario: UsuarioEntity = UsuarioEntity.query.filter_by(nombre_usuario=nombre_usuario).first()

        if not usuario:
            return False
        
        if not bcrypt.check_password_hash(usuario.contraseña, contraseña):
            return False

        
        return usuario
    
    