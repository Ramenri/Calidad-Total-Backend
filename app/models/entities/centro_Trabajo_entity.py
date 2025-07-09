import uuid
from app.configuration.configuracion_Database import db

class CentroTrabajoEntity(db.Model):

    __tablename__ = "centro_trabajo"

    id: str = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    codigo: int = db.Column(db.Integer, nullable=False, unique=True)
    nombre: str = db.Column(db.String(100), nullable=False)
    estado: bool = db.Column(db.Boolean, default=True)
    empresa_id: str = db.Column(db.String(36), db.ForeignKey('empresa.id'), nullable=False)

    def get_json(self) -> dict:
        return{
            "id": self.id,
            "codigo": self.codigo,
            "empresaID": self.empresa_id,
            "nombre": self.nombre,
            "estado": self.estado
        }
    
    Contratos = db.relationship("ContratoEntity", backref="centro_trabajo", lazy=True)