from flask import Blueprint, jsonify, Request, request
from app.services.usuario_servicios import UsuarioServicios
from app.models.entities.usuario_entity import UsuarioEntity
from app.services.operario_servicios import OperarioServicios
from app.configuration.configuracion_Bcrypt import bcrypt
from app.utils.utils_jwt import UtilsJWT

usuario_routes: Blueprint = Blueprint('usuario',__name__, url_prefix='/usuario')

class UsuarioController:

    @usuario_routes.route('/crearUnionConOperario', methods=['POST'])
    @UtilsJWT.token_required(roles=["administrador"])
    @staticmethod
    def crear_union_con_operario():
        try:
            data: dict = request.get_json()
            
            # Validar datos requeridos
            if not data.get('nombre_usuario') or not data.get('contraseña') or not data.get('operarioId'):
                return jsonify({"message": "Faltan datos requeridos"}), 400

            usuario = UsuarioEntity()
            usuario.nombre_usuario = data.get('nombre_usuario')
            usuario.contraseña = data.get('contraseña')
            usuario.rol = "administrador"
            usuario.operario_id = data.get('operarioId')
            
            resultado = UsuarioServicios.crear_union_con_operario(usuario)
            
            if "correctamente" in resultado:
                return jsonify({"message": resultado}), 200
            else:
                return jsonify({"message": resultado}), 400
            
        except Exception as e:
            return jsonify({"message": f"Error interno del servidor: {str(e)}"}), 500

    @usuario_routes.route('/eliminarAdmin/<id>', methods=['DELETE'])
    @UtilsJWT.token_required(roles=["administrador"])
    @staticmethod
    def eliminar_admin(id):
        try:
            resultado = UsuarioServicios.eliminar_admin_por_usuario_id(id)
            
            if "correctamente" in resultado:
                return jsonify({"message": resultado}), 200
            else:
                return jsonify({"message": resultado}), 404
                
        except Exception as e:
            return jsonify({"message": f"Error interno del servidor: {str(e)}"}), 500

    @usuario_routes.route('/crearAdmin', methods=['POST'])
    @UtilsJWT.token_required(roles=["administrador"])
    @staticmethod
    def crear_admin():
        data: dict = request.get_json()

        operarioData = {
            "numero_cedula": data.get('numero_cedula'),
            "nombre": data.get('nombre'),
            "apellido": data.get('apellido'),
            "correo": data.get('correo'),
            "numero_telefonico": data.get('numero_telefonico'),
            "estado": data.get('estado')
        }

        usuarioData = {
            "nombre_usuario": operarioData.get('nombre'),
            "contraseña": bcrypt.generate_password_hash(data.get('contraseña')).decode('utf-8'),
            "rol": data.get('rol'),
            "operario_id": ""
        }
                
        usuario = UsuarioServicios.crear_admin(operarioData, usuarioData)
        return jsonify(usuario.get_json()), 201

    @usuario_routes.route('/buscar/<id>', methods=['GET'])
    @staticmethod
    def buscar_por_id(id):
        usuario = UsuarioServicios.buscar_por_id(id)
        return jsonify(usuario.get_json()), 200 


    @usuario_routes.route('/obtenerTodos', methods=['GET'])
    @UtilsJWT.token_required(roles=["administrador"])
    @staticmethod
    def obtenerTodos() -> tuple [Request, int]:
        usuarios = UsuarioServicios.obtenerTodos()
        return jsonify([usuario.get_json() for usuario in usuarios]), 200

    @usuario_routes.route('/crear', methods=['POST'])
    @UtilsJWT.token_required(roles=["administrador"])
    @staticmethod
    def crear() -> tuple [Request, int]:

        data: dict = request.get_json()
        nombre_usuario: str = data.get('nombre_usuario')
        contraseña: str = data.get('contraseña')
        rol: str = data.get('rol')
        operario_id: int = data.get('operario_id')

        if not nombre_usuario:
            return jsonify({'error': 'El nombre del usuario es requerido'}), 400
        if not contraseña:
            return jsonify({'error': 'La contraseña es requerida'}), 400
        if not rol:
            return jsonify({'error': 'El rol es requerida'}), 400
        if not operario_id:
            return jsonify({'error': 'El id del Operario del Usuario es requerida'}), 400
        
        operario = OperarioServicios.buscar_por_id(operario_id)
        if not operario:
            return jsonify({'error': 'El operario no existe'}), 404
        
        usuario_existente = UsuarioEntity.query.filter_by(operario_id=operario_id).first()
        if usuario_existente:
            return jsonify({'error': 'Este operario ya tiene un usuario asignado'}), 400
        
        contraseña_hash = bcrypt.generate_password_hash(contraseña).decode('utf-8')
        
        usuario: UsuarioEntity = UsuarioEntity(nombre_usuario=nombre_usuario, contraseña=contraseña_hash, rol=rol, operario_id=operario_id)
        UsuarioServicios.crear(usuario)
        return jsonify(usuario.get_json()), 201
    
    @usuario_routes.route('/login', methods=['POST' , 'OPTIONS'])
    @staticmethod
    def login():

        if request.method == 'OPTIONS':
            return '', 200

        data = request.get_json()
        nombre_usuario = data.get('nombre_usuario')
        contraseña = data.get('contraseña')

        if not nombre_usuario or not contraseña:
            return jsonify({'error': 'Usuario y contraseña son obligatorios'}), 400
        
        usuario_encontrado = UsuarioServicios.autenticar_usuario(nombre_usuario, contraseña)

        if not usuario_encontrado:
            return jsonify({'message': 'Credenciales inválidas'}), 401

        token = UtilsJWT.generatedToken(user=usuario_encontrado)

        return jsonify({'token': token}), 200
    
