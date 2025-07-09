from flask import Blueprint, jsonify, Request, request
from app.services.historial_servicios import HistorialServicios
from app.models.entities.historial_entity import HistorialEntity

historial_routes: Blueprint = Blueprint('historial',__name__, url_prefix='/historial')

class HistorialController:
    
    @historial_routes.route('/obtenerTodos', methods=['GET'])
    @staticmethod
    def obtenerTodos():
        historial = HistorialServicios.obtenerTodos()
        return jsonify(historial), 200
    