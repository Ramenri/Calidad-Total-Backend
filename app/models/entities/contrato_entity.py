import uuid
import datetime
from app.configuration.configuracion_Database import db
from app.models.entities.operario_entity import OperarioEntity

class ContratoEntity(db.Model):
    
    __tablename__ = 'contrato'

    id: int = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    fecha_inicio: datetime.date = db.Column(db.Date, nullable=False)
    fecha_fin: datetime.date = db.Column(db.Date, nullable=False)
    estado: bool = db.Column(db.Boolean, default=True)
    centro_id: int = db.Column(db.BigInteger, db.ForeignKey('centro_trabajo.id'), nullable=False)
    operario_id: int = db.Column(db.BigInteger, db.ForeignKey('operario.id'), nullable=False)
    cargo: str = db.Column(db.String(36), nullable=False)

    def get_json(self) -> dict:

        return{
            "id": self.id,
            "fechaInicio": self.fecha_inicio.strftime("%Y-%m-%d"),
            "FechaFin": self.fecha_fin.strftime("%Y-%m-%d"),
            "estado": self.estado,
            "centro_id": self.centro_id,
            "cargo": self.cargo,
            "nombre_empresa": self.centro_trabajo.empresa.nombre if self.centro_trabajo and self.centro_trabajo.empresa else None
        }
    
    Documentos = db.relationship("DocumentoEntity", backref="contrato", lazy=True, cascade="all, delete-orphan")
    
   