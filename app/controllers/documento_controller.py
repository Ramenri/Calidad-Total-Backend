import os
from flask import send_file, abort
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.services.documento_servicios import DocumentoServicios
from app.models.entities.documento_entity import DocumentoEntity
from app.utils.utils_jwt import UtilsJWT
from flask import send_from_directory
from app.utils.utils_file import UtilsFile

documento_routes: Blueprint =  Blueprint('documento', __name__, url_prefix='/documento')

class DocumentoController:

    @documento_routes.route("/pdf/<contrato_id>", methods=["GET"])
    def generarPdf(contrato_id):
        return jsonify(DocumentoServicios.generarPdf(contrato_id)), 200

    @documento_routes.route("/juntar/pdf/<id_contrato>", methods=["GET"])
    def unificarPdfs(id_contrato):
        return jsonify(DocumentoServicios.unificarPdfs(id_contrato)), 200
    
    @documento_routes.route("/guardar", methods=["POST"])
    @UtilsJWT.token_required(roles=["administrador"])
    def guardarDocumento():
        file = request.files['file']
        tipoArchivo = request.form.get("tipoArchivo")
        id_contrato = request.form.get("id_contrato")
        fecha_expedicion = request.form.get("fecha_expedicion")
        cedula = request.form.get("cedula")
        
        if not file:
            return jsonify({"error": "El archivo es requerido"}), 400
        print("Datos para guardar archivo:")
        resultado = DocumentoServicios.guardar(file, tipoArchivo, id_contrato, fecha_expedicion, cedula)
        return jsonify({"message": "Documento guardado"}), 200

    @documento_routes.route("/eliminarPorId/<id>", methods=["DELETE"])
    @UtilsJWT.token_required(roles=["administrador"])
    def eliminarPorId(id):
        return jsonify(DocumentoServicios.eliminarPorId(id=id)), 200
    
    @documento_routes.route("/buscarPorContrato/<integer:id_contrato>", methods=["GET"])
    def obtener_documentos_por_contrato(id_contrato):
        try:
            documentos = DocumentoServicios.obtener_documentos_por_contrato(id_contrato)
            return jsonify(documentos), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    @documento_routes.route("/cambiar_estado/<id>", methods=["PUT"])
    @UtilsJWT.token_required(roles=["administrador"])
    def cambiar_estado_documento(id):
        nuevo_estado = request.json.get('estado')
        print(f"estado: {nuevo_estado}, id: {id}")
        return jsonify(DocumentoServicios.cambiar_estado_documento(id, nuevo_estado))
    
    @documento_routes.route("/archivos/<path:subpath>")
    def servir_archivo(subpath):
        base_folder = os.path.join(os.getcwd(), "archivos")
        normalized_url = subpath.replace('\\', '/')
            
        ruta_completa = os.path.abspath(os.path.join(base_folder, normalized_url))  

        fileBase64 = UtilsFile.obtenerContenidoArchivo(ruta_completa)

        if not os.path.isfile(ruta_completa):
            return abort(404, description="Archivo no encontrado")

        return jsonify(fileBase64), 200
