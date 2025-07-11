import uuid
from app.configuration.configuracion_Database import db

class DocumentoEntity(db.Model):
    
    __tablename__ = 'documento'

    id: int = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    ruta_archivo: str = db.Column(db.String(300), nullable=False)
    tipoArchivo: str = db.Column(db.String(100), nullable=False)
    fecha_expedicion: str = db.Column(db.String(30), nullable=False)
    estado: bool = db.Column(db.Boolean, default=True)
    id_contrato: int = db.Column(db.BigInteger, db.ForeignKey('contrato.id'), nullable=False)


    def get_json(self) -> dict:
        return{
            "id": self.id,
            "ruta_archivo": self.ruta_archivo,
            "tipoArchivo": self.tipoArchivo,
            "fecha_expedicion": self.fecha_expedicion,
            "estado": self.estado,
            "id_contrato": self.id_contrato
        }