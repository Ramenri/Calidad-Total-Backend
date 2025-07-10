import uuid
from app.configuration.configuracion_Database import db

association_table = db.Table('association', db.metadata,
    db.Column('empresa_id', db.String, db.ForeignKey('empresa.id')),
    db.Column('operario_id', db.String, db.ForeignKey('operario.id'))
)

class OperarioEntity(db.Model):
    
    __tablename__ = 'operario'

    id: str = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre: str = db.Column(db.String(100), nullable=False)
    apellido: str = db.Column(db.String(100), nullable=False)
    estado: bool = db.Column(db.Boolean, default=True)
    numero_cedula: str = db.Column(db.String(30), nullable=False, unique=True)
    numero_telefonico: str = db.Column(db.String(30), nullable=False)
    correo: str = db.Column(db.String(100), nullable=False)

    def get_json(self) -> dict:

        contrato_mas_reciente = None
        if self.contratos:
            contrato_mas_reciente = sorted(self.contratos, key=lambda c: c.fecha_inicio, reverse=True)[0]

        return {
            "id": self.id,
            "empresaIDs": [empresa.id for empresa in self.empresas],
            "nombre": self.nombre,
            "apellido": self.apellido,
            "estado": self.estado,
            "numeroCedula": self.numero_cedula,
            "numeroTelefonico": self.numero_telefonico,
            "contrato_estado": contrato_mas_reciente.estado if contrato_mas_reciente else None,
            "contrato_id": contrato_mas_reciente.id if contrato_mas_reciente else None,
            "correo": self.correo
        }
    contratos = db.relationship("ContratoEntity", backref="operario", lazy=True, cascade="all, delete-orphan")
    usuarios = db.relationship("UsuarioEntity", backref="operario", lazy=True, cascade="all, delete-orphan")
    empresas = db.relationship(
        'EmpresaEntity',
        secondary=association_table,
        back_populates='operarios'
    )
