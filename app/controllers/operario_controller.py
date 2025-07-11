from flask import Blueprint, jsonify, Request, request
from app.services.operario_servicios import OperarioServicios
from app.models.entities.operario_entity import OperarioEntity
from app.models.entities.empresa_entity import EmpresaEntity
from app.models.entities.operario_entity import OperarioEmpresaAsociacion 
from app.configuration.configuracion_Database import db
from app.utils.utils_jwt import UtilsJWT

operario_routes: Blueprint = Blueprint('operario',__name__, url_prefix='/operario')

class OperarioCrontroller:

    @operario_routes.route('/crearOperarioRelacionandoTodo', methods=['POST'])
    @UtilsJWT.token_required(roles=["administrador"])
    @staticmethod
    def crear_operario_relacionando_todo() -> tuple[Request, int]:
        data: dict = request.get_json()
        resultado = OperarioServicios.crear_operario_relacionando_todo(data)
        return jsonify(resultado), 201

    @operario_routes.route('/obtenerTodos', methods=['GET'])
    @UtilsJWT.token_required(roles=["administrador"])
    @staticmethod
    def obtenerTodos() -> tuple[Request, int]:
        operarios = OperarioServicios.obtenerTodos()
        return jsonify([operario.get_json() for operario in operarios]), 200

    @operario_routes.route('/crear', methods=['POST'])
    @UtilsJWT.token_required(roles=["administrador"])
    @staticmethod
    def crear() -> tuple[Request, int]:
        print("JSON recibido:", request.json)
        data: dict = request.get_json()
        nombre: str = data.get('nombre')
        apellido: str = data.get('apellido')
        numero_cedula: str = data.get('numeroCedula')
        numero_telefonico: str = data.get('numeroTelefonico')
        correo: str = data.get('correo')
        empresa_id: int = data.get('empresa_id')

        if not nombre:
            return jsonify({'error': 'El nombre del operario es requerido'}), 400
        if not apellido:
            return jsonify({'error': 'El apellido del operario es requerido'}), 400
        if not numero_cedula:
            return jsonify({'error': 'La cedula del operario es requerido'}), 400
        if not numero_telefonico:
            return jsonify({'error': 'El numero telefonico del operario es requerido'}), 400        
        if not correo:
            return jsonify({'error': 'El correo del operario es requerido'}), 400  
        if not empresa_id:
            return jsonify({'error': 'La empresa del operario es requerida'}), 400

        if OperarioEntity.query.filter_by(numero_cedula=numero_cedula).first():
            return jsonify({"error": "Ya existe un operario con esa cédula."}), 400 

        empresa = EmpresaEntity.query.get(empresa_id)
        if not empresa:
            return jsonify({'error': 'Empresa no encontrada'}), 404

        operario: OperarioEntity = OperarioEntity(
            nombre=nombre, 
            apellido=apellido, 
            numero_cedula=numero_cedula, 
            numero_telefonico=numero_telefonico, 
            correo=correo
        )
        nueva_asociacion = OperarioEmpresaAsociacion(
            operario=operario,
            empresa=empresa,
            estado=True
        )
        db.session.add(nueva_asociacion)
        OperarioServicios.crear(operario)
        
        operario_json = operario.get_json()  
        return jsonify(operario_json), 201


    @operario_routes.route('/actualizarEstado', methods=['PUT'])
    @UtilsJWT.token_required(roles=["administrador"])
    @staticmethod
    def actualizar_estado() -> tuple:
        data: dict = request.get_json()
        numero_cedula: str = data.get('numeroCedula')
        nuevo_estado: bool = data.get('estado')

        if numero_cedula is None or nuevo_estado is None:
            return jsonify({'error': 'La cedula del operario y el nuevo estado son requeridos'}), 400

        resultado = OperarioServicios.actualizar_estado(numero_cedula, nuevo_estado)

        if not resultado:
            return jsonify({'error': 'No se encontró una operario con esa cedula'}), 404

        return jsonify({'message': 'Estado del operario fue actualizado correctamente'}), 200
    
    @operario_routes.route('/buscar/<operario_id>', methods=['GET'])
    @staticmethod
    def buscar_por_id(operario_id: int) -> tuple:
        operario = OperarioServicios.buscar_por_id(operario_id)
        if not operario:
            return jsonify({'error': 'Operario no encontrado'}), 404

        return jsonify(operario.get_json()), 200
    
    @operario_routes.route('/filtrarOperarios', methods=['POST'])
    @staticmethod
    def filtrar_operario():
        filtros = request.get_json()
        operarios = OperarioServicios.filtrar_operario(filtros)
        return jsonify(operarios), 200
    
    @operario_routes.route('/operariosPorEmpresa/<empresa_id>', methods=['POST'])
    @staticmethod
    def obtener_operarios_por_empresa(empresa_id: int):
        operarios = OperarioServicios.obtener_por_empresa(empresa_id)
        return jsonify(operarios), 200
    
    @operario_routes.route('/eliminar/<operario_id>', methods=['DELETE'])
    @UtilsJWT.token_required(roles=["administrador"])
    @staticmethod
    def eliminar_operario(operario_id):
    
        try:
            resultado = OperarioServicios.eliminar_operario_por_id(operario_id)
            if resultado["status"] == "error":
                return jsonify({"msg": resultado["msg"]}), 404
            return jsonify({"msg": resultado["msg"]})
        except Exception as e:
            return jsonify({"msg": f"Error al eliminar operario: {str(e)}"}), 500
          
    @operario_routes.route('/actualizar/<operario_id>', methods=['PUT'])
    @UtilsJWT.token_required(roles=["administrador"])
    @staticmethod
    def actualizar_operario(operario_id: int) -> tuple:
        data = request.get_json()
        print(f"Datos recibidos: {data}")
        
        resultado = OperarioServicios.actualizar_operario(operario_id, data)
        
        return jsonify(resultado), 200

    @operario_routes.route('/filtrarOperariosCompleto', methods=['POST'])
    @UtilsJWT.token_required(roles=["administrador", "usuario"])
    @staticmethod
    def filtrar_operarios_completo():
        try:
            filtros = request.get_json() or {}
            print(f"Filtros recibidos: {filtros}")
            
            resultado = OperarioServicios.filtrar_operarios_completo(filtros)
            
            if resultado.get("error"):
                return jsonify(resultado), 400
            
            return jsonify(resultado), 200
            
        except Exception as e:
            return jsonify({
                "error": f"Error en el endpoint: {str(e)}",
                "operarios": [],
                "total": 0
            }), 500

    