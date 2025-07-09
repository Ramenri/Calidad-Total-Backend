from flask import Blueprint, jsonify, Request, request
from app.services.contrato_servicios import ContratoServicios
from app.models.entities.contrato_entity import ContratoEntity
from datetime import datetime
from app.utils.utils_jwt import UtilsJWT

contrato_routes: Blueprint = Blueprint('contrato',__name__, url_prefix='/contrato')
   
class ContratoCrontroller:

    @contrato_routes.route('/crear', methods=['POST'])
    @UtilsJWT.token_required(roles=["administrador"])
    @staticmethod
    def crear() -> tuple[Request, int]:

        data: dict = request.get_json()

        try:
            fecha_inicio: datetime.date = datetime.strptime(data.get('fechaInicio'), "%Y-%m-%d").date()
            fecha_fin: datetime.date = datetime.strptime(data.get('fechaFin'), "%Y-%m-%d").date()
        except (TypeError, ValueError):
            return jsonify({'error': 'Formato de fecha inválido. Use "YYYY-MM-DD"'}), 400

        centro_id: str = data.get('centro_id')
        operario_id: str = data.get('operario_id')
        cargo: str= data.get('cargo')

        if not fecha_inicio:
            return jsonify({'error': 'La fecha de incio del contrato es requerido'}), 400
        if not fecha_fin:
            return jsonify({'error': 'La fecha de finalizacion del contrato es requerido'}), 400
        if not centro_id:
            return jsonify({'error': 'El id del centro de trabajo es requerido'}), 400

        contrato: ContratoEntity = ContratoEntity( fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, centro_id=centro_id, operario_id=operario_id, cargo=cargo)
        ContratoServicios.crear(contrato)
        return jsonify(contrato.get_json()), 201
    
    @contrato_routes.route('/buscarPorEmpresa/<empresa_id>', methods=['GET'])
    def obtener_contratos_por_empresa(empresa_id):
        contratos = ContratoServicios.obtener_contratos_por_empresa(empresa_id)
        return jsonify(contratos), 200

    @contrato_routes.route('/actualizarEstado/<id>', methods=['PUT'])
    @UtilsJWT.token_required(roles=["administrador"])
    def cambiar_estado_contrato(id):
        data = request.get_json()
        nuevo_estado = data.get('estado')

        return jsonify(ContratoServicios.cambiar_estado_contrato(id, nuevo_estado))
    
    @contrato_routes.route('/cargos', methods=['GET'])
    def obtener_cargos():
        try:
            cargos = ContratoServicios.obtener_cargos()
            return jsonify(cargos), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    
    @contrato_routes.route('/buscarPorOperario/<operario_id>', methods=['GET'])
    def obtener_contratos_por_operario_y_empresa(operario_id):
        try:
            empresa_id = request.args.get('empresa')
            if not empresa_id:
                return jsonify({"error": "Falta el parámetro 'empresa' en la URL"}), 400

            contratos = ContratoServicios.obtener_contratos_por_operario_y_empresa(operario_id, empresa_id)

            return jsonify(contratos), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @contrato_routes.route("/extender/<contrato_id>", methods=["POST"])
    @UtilsJWT.token_required(roles=["administrador"])
    def extender_contrato(contrato_id):
        data = request.get_json()

        nueva_fecha = data.get("fechaFin")
        print(nueva_fecha)
        if not nueva_fecha:
            return jsonify({"error": "La nueva fecha de finalización es requerida"}), 400

        try:
            nuevo_contrato = ContratoServicios.extender_contrato(
                contrato_id, nueva_fecha
            )
            return jsonify(nuevo_contrato), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception:
            return jsonify({"error": "Error interno al extender el contrato"}), 500
