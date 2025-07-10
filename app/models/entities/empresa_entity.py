import uuid
from app.configuration.configuracion_Database import db
from app.models.entities.operario_entity import association_table

class EmpresaEntity(db.Model):
    
    __tablename__ = 'empresa'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    codigo: int = db.Column(db.Integer, nullable=False, unique=True)
    nombre: str = db.Column(db.String(100), nullable=False)
    estado: bool = db.Column(db.Boolean, default=True)    
    Centros_trabajo = db.relationship("CentroTrabajoEntity", backref="empresa", lazy=True)
    operarios = db.relationship(
        'OperarioEntity',
        secondary=association_table,
        back_populates='empresas'
    )

    def get_json(self) -> dict:
        return{
            "id": self.id,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "estado": self.estado,
            "centrosTrabajo": [centro.get_json() for centro in self.Centros_trabajo]
        }
