import uuid
from app.configuration.configuracion_Database import db

class CentroTrabajoEntity(db.Model):

    __tablename__ = "centro_trabajo"

    id: int = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    codigo: int = db.Column(db.Integer, nullable=False, unique=True)
    nombre: str = db.Column(db.String(100), nullable=False)
    estado: bool = db.Column(db.Boolean, default=True)
    empresa_id: int = db.Column(db.BigInteger, db.ForeignKey('empresa.id'), nullable=False)

    def get_json(self) -> dict:
        return{
            "id": self.id,
            "codigo": self.codigo,
            "empresaID": self.empresa_id,
            "nombre": self.nombre,
            "estado": self.estado
        }
    
    Contratos = db.relationship("ContratoEntity", backref="centro_trabajo", lazy=True)