import os
import uuid
import PyPDF2
import base64
import io 
from app.configuration.config import Config
from werkzeug.utils import secure_filename

class UtilsFile:

    @staticmethod
    def obtenerContenidoArchivo(ruta_archivo: str) -> str:
        with open(ruta_archivo, "rb") as archivo:
            contenido = archivo.read()
            return base64.b64encode(contenido).decode('utf-8')

    @staticmethod
    def unificarPDFS(urls: list[str]) -> str:
        base_folder = Config.DOCUMENTS_PATH
        pdf_merger = PyPDF2.PdfMerger()

        for url in urls:
            normalized_url = url.replace('\\', '/')
            
            ruta_completa = os.path.abspath(os.path.join(base_folder, normalized_url))

            print(f"Procesando archivo: {ruta_completa}")

            if not ruta_completa.startswith(base_folder):
                raise ValueError(f"Ruta inválida detectada: {ruta_completa}. No está dentro de {base_folder}")

            if not os.path.exists(ruta_completa):
                raise FileNotFoundError(f"El archivo no existe en la ruta: {ruta_completa}")
            
            try:
                pdf_merger.append(ruta_completa)
            except Exception as e:
                raise IOError(f"No se pudo añadir el archivo PDF '{ruta_completa}'. Error: {e}")

        output_pdf_buffer = io.BytesIO()
        pdf_merger.write(output_pdf_buffer)
        pdf_merger.close()

        output_pdf_buffer.seek(0)
        
        pdf_base64 = base64.b64encode(output_pdf_buffer.read()).decode('utf-8')
        
        return pdf_base64

    @staticmethod
    def crearDirectorioCarpeta(uploadFolder: str):
        os.makedirs(uploadFolder, exist_ok=True)

    @staticmethod
    def guardarArchivoEnElDirectorio(file, tipoArchivo: str, uploadFolder: str, cedula: str, apellido: str, contrato_id: int) -> str:
        print(f"[DEBUG] Guardando archivo: tipo={tipoArchivo}, cedula={cedula}, apellido={apellido}, contrato_id={contrato_id}")
        carpetaOperario = os.path.join(uploadFolder, f"{apellido}_{cedula}")
        carpetaContrato = os.path.join(carpetaOperario, contrato_id)
        carpetaTipoArchivo = os.path.join(carpetaContrato, f"{tipoArchivo}")

        UtilsFile.crearDirectorioCarpeta(carpetaTipoArchivo)


        filename: str = secure_filename(str(uuid.uuid4()) + file.filename)
        filePath: str = os.path.join(carpetaTipoArchivo, filename)
        print(f"[DEBUG] Ruta completa donde se guardará: {filePath}")
        try:
            file.save(filePath)
        except Exception as e:
            print("Error al guardar archivo:", str(e))

        relative_path = os.path.relpath(filePath, uploadFolder)

        return relative_path

    @staticmethod
    def eliminarPorUrl(url: str):
        base_folder = Config.DOCUMENTS_PATH
        ruta_completa = os.path.abspath(os.path.join(base_folder, url))
        
        if not ruta_completa.startswith(base_folder):
            raise ValueError("Ruta inválida")

        if os.path.exists(ruta_completa):
            os.remove(ruta_completa)
        else:
            print(f"[Advertencia] El archivo no existe: {ruta_completa}")