from flask import Blueprint, jsonify, Request, request
from app.services.empresa_servicios import EmpresaServicios
from app.models.entities.empresa_entity import EmpresaEntity
from app.utils.utils_jwt import UtilsJWT

empresa_routes: Blueprint = Blueprint('empresa',__name__, url_prefix='/empresa')

class EmpresaCrontroller:

    @empresa_routes.route('/obtenerEmpresasDelOperarioNoAfiliadas/<cedulaOperario>', methods=['GET'])
    @staticmethod
    def obtener_empresas_del_operario_no_afiliadas(cedulaOperario: str) -> tuple:
        empresas: list[EmpresaEntity] = EmpresaServicios.obtener_empresas_del_operario_no_afiliadas(cedulaOperario)
        empresa_list_request: list[dict] = [empresa.get_json() for empresa in empresas]

        return jsonify(empresa_list_request), 200

    @empresa_routes.route('/actualizar/<id>', methods=['PUT'])
    @UtilsJWT.token_required(roles=["administrador"])
    @staticmethod
    def actualizar_empresa(id: int) -> tuple:
        data: dict = request.get_json()
        codigo: int = data.get('codigo')
        nombre: str = data.get("nombre")
        estado: bool = data.get("estado")

        if codigo is None:
            return jsonify({'error': 'El código de la empresa es requerido'}), 400

        resultado = EmpresaServicios.actualizar_empresa(id, codigo, nombre, estado)

        if not resultado:
            return jsonify({'error': 'No se encontró una empresa con ese código'}), 404

        return jsonify({'message': 'Empresa actualizada correctamente'}), 200

    @empresa_routes.route('/todo', methods=['GET'])
    @staticmethod
    def obtener_todo() -> tuple[Request, int]:
        empresas: list[EmpresaEntity] = EmpresaServicios.obtener_todo()
        empresa_list_request: list[dict] = [empresa.get_json() for empresa in empresas]

        return jsonify(empresa_list_request), 200
    
    @empresa_routes.route('/crear', methods=['POST'])
    @UtilsJWT.token_required(roles=["administrador"])
    @staticmethod
    def crear() -> tuple[Request, int]:

        data: dict = request.get_json()
        nombre: str = data.get('nombre')
        codigo: int = data.get('codigo')
        if not nombre:
            return jsonify({'error': 'El nombre de la empresa es requerido'}), 400
        if not codigo:
            return jsonify({'error': 'El codigo de la empresa es requerido'}), 400

        empresa: EmpresaEntity = EmpresaEntity(nombre=nombre, codigo=codigo)
        EmpresaServicios.crear(empresa)
        return jsonify(empresa.get_json()), 201
    
    @empresa_routes.route('/buscarCodigo', methods=['GET'])
    @staticmethod
    def obtener_codigo() -> tuple:
        data: dict = request.get_json()
        codigo: int = data.get('codigo')

        if codigo is None:
            return jsonify({'error': 'El codigo de la empresa es requerido'}), 400
        
        empresa: EmpresaEntity = EmpresaServicios.obtener_codigo(codigo)

        if empresa is None:
            return jsonify({'error': 'No se encontro una empresa con ese código'}), 404
        
        return jsonify(empresa.get_json()), 200
    
    @empresa_routes.route('/eliminarEmpresa', methods=['DELETE'])
    @UtilsJWT.token_required(roles=["administrador"])
    @staticmethod
    def eliminar_empresa() -> tuple:
        data: dict = request.get_json()
        codigo: int = data.get('codigo')

        if codigo is None:
            return jsonify({'error': 'El código de la empresa es requerido'}), 400
        
        resultado = EmpresaServicios.eliminar_empresa(codigo)

        if not resultado:
            return jsonify({'error': 'No se encontró una empresa con ese código'}), 404
        
        return jsonify({'message': 'Empresa eliminada correctamente'}), 200
    
    @empresa_routes.route('/actualizarEstado', methods=['PUT'])
    @UtilsJWT.token_required(roles=["administrador"])
    @staticmethod
    def actualizar_estado() -> tuple:
        data: dict = request.get_json()
        codigo: int = data.get('codigo')
        nuevo_estado: bool = data.get('estado')

        if codigo is None or nuevo_estado is None:
            return jsonify({'error': 'El código de la empresa y el nuevo estado son requeridos'}), 400

        resultado = EmpresaServicios.actualizar_estado(codigo, nuevo_estado)

        if not resultado:
            return jsonify({'error': 'No se encontró una empresa con ese código'}), 404

        return jsonify({'message': 'Estado de la empresa actualizado correctamente'}), 200
    
    @empresa_routes.route('/buscarPorUuid', methods=['GET'])
    @staticmethod
    def obtener_empresa_por_uuid() -> tuple:
        uuid_empresa = request.args.get('uuid')

        if not uuid_empresa:
            return jsonify({'error': 'El UUID de la empresa es requerido'}), 400

        empresa = EmpresaServicios.obtener_por_uuid(uuid_empresa)

        if empresa is None:
            return jsonify({'error': 'No se encontró una empresa con ese UUID'}), 404

        return jsonify(empresa.get_json()), 200