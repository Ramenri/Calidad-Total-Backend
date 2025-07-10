from flask import Blueprint, jsonify, Request, request
from app.services.centro_trabajo_servicios import CentroServicios
from app.models.entities.centro_Trabajo_entity import CentroTrabajoEntity
from app.utils.utils_jwt import UtilsJWT

centro_routes: Blueprint = Blueprint('centroTrabajo',__name__, url_prefix='/centroTrabajo')

class CentroController:

    @centro_routes.route("/actualizar/<id>", methods=['PUT'])
    @UtilsJWT.token_required(roles=["administrador"])
    @staticmethod
    def actualizar(id: int) -> tuple[Request, int]:
        try:
            data = request.get_json()
            nombre: str = data.get('nombre')
            codigo: int = data.get('codigo')
            estado: bool = data.get('estado')
            CentroServicios.actualizar(id, nombre, codigo, estado)
            return jsonify({"message": "Centro actualizado correctamente"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @centro_routes.route("/eliminar/<id>", methods=['DELETE'])
    @UtilsJWT.token_required(roles=["administrador"])
    @staticmethod
    def eliminar(id: int) -> tuple[Request, int]:
        try:
            CentroServicios.eliminar(id)
            return jsonify({"message": "Centro eliminado correctamente"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @centro_routes.route('/crear', methods=['POST'])
    @UtilsJWT.token_required(roles=["administrador"])
    @staticmethod
    def crear () -> tuple[Request, int]:

        data: dict = request.get_json()
        nombre: str = data.get('nombre')
        codigo: int = data.get('codigo')
        empresa_id: str = data.get('empresa_id')

        if not nombre:
            return jsonify ({'error': 'El nombre del centro de trabajo es requerido'}), 400
        if not empresa_id:
            return jsonify({'error': 'El id de la empresa a la que pertenece el centro de trabajo es requerido'}), 400 
        if not codigo:
            return jsonify ({'error': 'El codigo del centro de trabajo es requerido'}), 400
        
        centro_trabajo: CentroTrabajoEntity = CentroTrabajoEntity (nombre=nombre, empresa_id=empresa_id, codigo=codigo)
        CentroServicios.crear(centro_trabajo)
        return jsonify(centro_trabajo.get_json()), 201 

    @centro_routes.route('/obtener/<empresa_id>', methods=['GET'])
    def obtener_centros_por_empresa(empresa_id: int):
        centros = CentroServicios.filtrar_por_empresa(empresa_id)

        if not centros:
            return{'message': 'No se encontraron centros de trabajo para esta empresa'}, 404
        
        return {'centros_de_trabajo': [centro.get_json() for centro in centros]}, 200
    
    @centro_routes.route('/todo', methods=['GET'])
    @staticmethod
    def obtener_todo() -> tuple[Request, int]:
        centros: list[CentroTrabajoEntity] = CentroServicios.obtener_todo()
        centro_list_request: list[dict] = [centro.get_json() for centro in centros]

        return jsonify(centro_list_request), 200
    
    
    @centro_routes.route('/centroTrabajo/buscarPorId/<id>', methods=['GET'])
    def obtener_centro_trabajo_por_id(id):
        centro = CentroTrabajoEntity.query.get(id)
        if not centro:
            return jsonify({"error": "Centro no encontrado"}), 404
        return jsonify(centro.get_json()), 200