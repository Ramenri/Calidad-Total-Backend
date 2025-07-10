from app.configuration.configuracion_Database import db
from flask import Request, request
from app.utils.utils_file import UtilsFile
from app.models.entities.operario_entity import OperarioEntity
from app.models.entities.documento_entity import DocumentoEntity
from app.models.entities.contrato_entity import ContratoEntity
from app.models.entities.centro_Trabajo_entity import CentroTrabajoEntity
from app.utils.utils_file import UtilsFile
from app.utils.utils_historial import registrar_historial
from app.configuration.config import Config
import datetime

filtros = {
    "hojaVida": "hojaVida", 
    "contrato": "contrato", 
    "incapacidades": "incapacidades", 
    "licenciaNoRemunerada": "licenciaNoRemunerada", 
    "otrosDocumentos": "otrosDocumentos",
    "cedula": "cedula",
    "carnetVacunas": "carnetVacunas",
    "liquidacion": "liquidacion",
    "otroSi": "otroSi",
    "conduccion": "conduccion",
    "antecedentes": "antecedentes",
    "certificadoLaboral": "certificadoLaboral",
    "bachillerato": "bachillerato",
    "certificadoEPS": "certificadoEPS",
    "induccion": "induccion",
    "otrosCursos": "otrosCursos",
    "cursosPosgrado": "cursosPosgrado",
    "cursosPregrado": "cursosPregrado",
    "libretaMilitar": "libretaMilitar",    
}

class DocumentoServicios:

    @staticmethod
    @registrar_historial(
        accion="Generar PDF Unificado",
        peticion="GET",
        descripcion_fn=lambda contrato_id, resultado, **kwargs:
            f"Se generó un documento PDF unificado para el contrato ID {contrato_id}"
            if isinstance(resultado, bytes) else f"Error al generar PDF para contrato ID {contrato_id}"
    )
    def generarPdf(contrato_id):
        contrato: ContratoEntity = ContratoEntity.query.filter_by(id=contrato_id, estado=True).first()  
        if not contrato:
            return "Contrato no encontrado", 404
        documentoGenerado = DocumentoServicios.unificarPdfs(contrato.id)
        return documentoGenerado

    @staticmethod
    @registrar_historial(
        accion="Unificar PDFs",
        peticion="GET",
        descripcion_fn=lambda id_contrato, resultado, **kwargs:
            f"Se unificaron los documentos PDF del contrato ID {id_contrato}"
            if isinstance(resultado, bytes) else f"No se pudo unificar documentos del contrato ID {id_contrato}"
    )
    def unificarPdfs(id_contrato):
        documentos: list[DocumentoEntity] = DocumentoEntity.query.filter_by(id_contrato=id_contrato, estado=True).all()

        #coincidir con los filtros
        listaCarneVacunas = []
        listaCedula = []
        listaCertifcadoPensiones = []
        listaLibretaMilitar = []
        listaCursosPregrado = []
        listaCursosPosgrado = []
        listaInduccion = []
        listaOtrosCursos = []
        listaContratos = []
        listaLicenciaNoRemunerada = []
        listaIncapacidades = []
        listaOtrosSi = []
        listLiquidacion = []
        listaOtrosDocumentos = []
        listaCertificadoLaboral = []
        listaBachillerato = []
        listaCertificadoEPS = []
        listaConduccion = []
        listaAntecedentes = []
        listaHojaVida = []
        
        for documento in documentos:

            #coincidir con las listas

            if documento.tipoArchivo == filtros["hojaVida"]:
                listaHojaVida.append(documento) 

            if documento.tipoArchivo == filtros["contrato"]:
                listaContratos.append(documento)

            if documento.tipoArchivo == filtros["incapacidades"]:
                listaIncapacidades.append(documento)

            if documento.tipoArchivo == filtros["licenciaNoRemunerada"]:
                listaLicenciaNoRemunerada.append(documento)

            if documento.tipoArchivo == filtros["otrosDocumentos"]:
                listaOtrosDocumentos.append(documento)

            if documento.tipoArchivo == filtros["carnetVacunas"]:
                listaCarneVacunas.append(documento)

            if documento.tipoArchivo == filtros["cedula"]:
                listaCedula.append(documento)

            if documento.tipoArchivo == filtros["certificadoLaboral"]:
                listaCertificadoLaboral.append(documento)

            if documento.tipoArchivo == filtros["bachillerato"]:
                listaBachillerato.append(documento)

            if documento.tipoArchivo == filtros["certificadoEPS"]:
                listaCertificadoEPS.append(documento)

            if documento.tipoArchivo == filtros["conduccion"]:
                listaConduccion.append(documento)

            if documento.tipoArchivo == filtros["antecedentes"]:
                listaAntecedentes.append(documento)

        documentoCarnetVacunas: DocumentoEntity = obtenerDocumentoMasReciente(listaCarneVacunas)
        documentoCertificadoPensiones: DocumentoEntity = obtenerDocumentoMasReciente(listaCertifcadoPensiones)
        documentoLibretaMilitar: DocumentoEntity = obtenerDocumentoMasReciente(listaLibretaMilitar)
        documentoCursosPregrado: DocumentoEntity = obtenerDocumentoMasReciente(listaCursosPregrado)
        documentoCursosPosgrado: DocumentoEntity = obtenerDocumentoMasReciente(listaCursosPosgrado)
        documentoInduccion: DocumentoEntity = obtenerDocumentoMasReciente(listaInduccion)
        documentoOtrosCursos: DocumentoEntity = obtenerDocumentoMasReciente(listaOtrosCursos)
        documentoContratos: DocumentoEntity = obtenerDocumentoMasReciente(listaContratos)
        documentoLicenciaNoRemunerada: DocumentoEntity = obtenerDocumentoMasReciente(listaLicenciaNoRemunerada)
        documentoIncapacidades: DocumentoEntity = obtenerDocumentoMasReciente(listaIncapacidades)
        documentoOtrosSi: DocumentoEntity = obtenerDocumentoMasReciente(listaOtrosSi)
        documentoLiquidacion: DocumentoEntity = obtenerDocumentoMasReciente(listLiquidacion)
        documentoOtrosDocumentos: DocumentoEntity = obtenerDocumentoMasReciente(listaOtrosDocumentos)
        documentoHojaVida: DocumentoEntity = obtenerDocumentoMasReciente(listaHojaVida)
        documentoCedula: DocumentoEntity = obtenerDocumentoMasReciente(listaCedula)
        documentoCertificadoLaboral: DocumentoEntity = obtenerDocumentoMasReciente(listaCertificadoLaboral)
        documentoBachillerato: DocumentoEntity = obtenerDocumentoMasReciente(listaBachillerato)
        documentoCertificadoEPS: DocumentoEntity = obtenerDocumentoMasReciente(listaCertificadoEPS)
        documentoConduccion: DocumentoEntity = obtenerDocumentoMasReciente(listaConduccion)
        documentoAntecedentes: DocumentoEntity = obtenerDocumentoMasReciente(listaAntecedentes)

        urls = []

        if documentoHojaVida:
            urls.append(documentoHojaVida.ruta_archivo)

        if documentoCedula:
            urls.append(documentoCedula.ruta_archivo)

        if documentoCarnetVacunas:
            urls.append(documentoCarnetVacunas.ruta_archivo)

        if documentoInduccion:
            urls.append(documentoInduccion.ruta_archivo)

        if documentoConduccion:
            urls.append(documentoConduccion.ruta_archivo)

        if documentoAntecedentes:
            urls.append(documentoAntecedentes.ruta_archivo)

        if documentoBachillerato:
            urls.append(documentoBachillerato.ruta_archivo)

        if documentoCertificadoLaboral:
            urls.append(documentoCertificadoLaboral.ruta_archivo)

        if documentoCertificadoEPS:
            urls.append(documentoCertificadoEPS.ruta_archivo)
      
        if documentoOtrosCursos:
            urls.append(documentoOtrosCursos.ruta_archivo)

        if documentoCursosPosgrado:
            urls.append(documentoCursosPosgrado.ruta_archivo)

        if documentoCursosPregrado:
            urls.append(documentoCursosPregrado.ruta_archivo)

        if documentoLibretaMilitar:
            urls.append(documentoLibretaMilitar.ruta_archivo)

        if documentoCertificadoPensiones:
            urls.append(documentoCertificadoPensiones.ruta_archivo)

        if documentoContratos:
            urls.append(documentoContratos.ruta_archivo)

        if documentoLicenciaNoRemunerada:
            urls.append(documentoLicenciaNoRemunerada.ruta_archivo)

        if documentoIncapacidades:
            urls.append(documentoIncapacidades.ruta_archivo)

        if documentoOtrosSi:
            urls.append(documentoOtrosSi.ruta_archivo)

        if documentoOtrosDocumentos:
            urls.append(documentoOtrosDocumentos.ruta_archivo)

        if documentoLiquidacion:
            urls.append(documentoLiquidacion.ruta_archivo)

        print(f"urls: {urls}")

        return UtilsFile.unificarPDFS(urls)
        
        
    @staticmethod
    @registrar_historial(
        accion="Guardar Documento",
        peticion="POST",
        descripcion_fn=lambda file, tipoArchivo, id_contrato, fecha_expedicion, cedula, resultado, **kwargs:
            f"Se guardó el documento '{tipoArchivo}' para contrato ID {id_contrato} con fecha {fecha_expedicion}"
            if resultado is None else str(resultado)
    )
    def guardar(file, tipoArchivo, id_contrato, fecha_expedicion, cedula):
        contrato = ContratoEntity.query.filter_by(id=id_contrato).first()
        if not contrato:
            return "Contrato no encontrado", 404

        operario = OperarioEntity.query.filter_by(id=contrato.operario_id).first()
        if not operario:
            return "Operario no encontrado", 404

        apellido = operario.apellido
        numero_cedula = operario.numero_cedula
        contrato_id = contrato.id

        url_relativa = UtilsFile.guardarArchivoEnElDirectorio(
            file=file,
            tipoArchivo=tipoArchivo,
            uploadFolder=Config.DOCUMENTS_PATH,  
            apellido=apellido,
            contrato_id=contrato_id,
            cedula=cedula
        )

        documento = DocumentoEntity(
            fecha_expedicion=fecha_expedicion,
            tipoArchivo=tipoArchivo,
            id_contrato=id_contrato,
            ruta_archivo=url_relativa  
        )

        db.session.add(documento)
        db.session.commit()

    @staticmethod
    def obtenerPorId(id: str) -> DocumentoEntity:
        return db.session.query(DocumentoEntity).filter(DocumentoEntity.id == id).first()

    @staticmethod
    def eliminarPorId(id: str):
        documento: DocumentoEntity = db.session.query(DocumentoEntity).filter_by(id=id).first()
        if documento is None:
            return {"error": "El documento no existe"}, 404  
        
        print(documento.ruta_archivo)

        UtilsFile.eliminarPorUrl(url=documento.ruta_archivo)

        db.session.query(DocumentoEntity).filter(DocumentoEntity.id == id).delete()
        db.session.commit()
        
        return {"message": "se ha eliminado correctamente"}
    
    @staticmethod
    def obtener_documentos_por_contrato(id_contrato: str) -> list:
        documentos = DocumentoEntity.query.filter_by(id_contrato=id_contrato, estado=True).all()
        return [doc.get_json() for doc in documentos]
    
    @staticmethod
    @registrar_historial(
        accion="Cambiar estado de documento",
        peticion="PUT",
        descripcion_fn=lambda id, nuevo_estado, resultado, **kwargs:
            f"Cambió el estado del documento ID {id} a {'activo' if nuevo_estado else 'inactivo'}"
            if isinstance(resultado, dict) and "message" in resultado else f"Error al cambiar estado del documento ID {id}"
    )
    def cambiar_estado_documento(id: str, nuevo_estado: bool) -> DocumentoEntity:

        documento= DocumentoEntity.query.get(id)

        if not documento:
            return {"error": "El documento no existe"}, 404
        
        documento.estado = nuevo_estado
        db.session.commit()

        return {"message": "se ha eliminado correctamente"}


def obtenerDocumentoMasReciente(documentos: list[DocumentoEntity]) -> DocumentoEntity:
    fecha_hoy = datetime.datetime.now().date()
    documento_mas_reciente = None
    fecha_mas_reciente = None 

    for documento in documentos:
        fecha_expedicion_doc = datetime.datetime.strptime(documento.fecha_expedicion, '%Y-%m-%d').date()

        if fecha_expedicion_doc <= fecha_hoy:
            if (documento_mas_reciente is None or
                fecha_expedicion_doc > fecha_mas_reciente):
                documento_mas_reciente = documento
                fecha_mas_reciente = fecha_expedicion_doc

    if documento_mas_reciente:
        return documento_mas_reciente
    else:
        print("No se encontraron documentos")

def obtenerContratoMasReciente(contratos: list[ContratoEntity]) -> ContratoEntity:
    fecha_hoy = datetime.datetime.now().date()
    contrato_mas_reciente = None
    fecha_mas_reciente = None 

    for contrato in contratos:
        fecha_inicio_contrato = contrato.fecha_inicio

        if fecha_inicio_contrato <= fecha_hoy:
            if (contrato_mas_reciente is None or
                fecha_inicio_contrato > fecha_mas_reciente):
                contrato_mas_reciente = contrato
                fecha_mas_reciente = fecha_inicio_contrato

    if contrato_mas_reciente:
        return contrato_mas_reciente
    else:
        print("No se encontraron contratos")
