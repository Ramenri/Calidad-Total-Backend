import uuid
from app.configuration.configuracion_Database import db

#association_table = db.Table('association', db.metadata,
#    db.Column('empresa_id', db.BigInteger, db.ForeignKey('empresa.id')),
#    db.Column('operario_id', db.BigInteger, db.ForeignKey('operario.id'))
#)

class OperarioEmpresaAsociacion(db.Model):
    __tablename__ = 'association' 

    empresa_id = db.Column(db.BigInteger, db.ForeignKey('empresa.id'), primary_key=True)
    operario_id = db.Column(db.BigInteger, db.ForeignKey('operario.id'), primary_key=True)
    estado = db.Column(db.Boolean, default=True, nullable=False)

    # Relaciones
    empresa = db.relationship('EmpresaEntity', back_populates='operario_asociaciones')
    operario = db.relationship('OperarioEntity', back_populates='empresa_asociaciones')

class OperarioEntity(db.Model):
    
    __tablename__ = 'operario'

    id: int = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    nombre: str = db.Column(db.String(100), nullable=False)
    apellido: str = db.Column(db.String(100), nullable=False)
    numero_cedula: str = db.Column(db.String(30), nullable=False, unique=True)
    numero_telefonico: str = db.Column(db.String(30), nullable=False)
    correo: str = db.Column(db.String(100), nullable=False)

    def get_json(self) -> dict:
        contrato_mas_reciente = None
        if self.contratos:
            contrato_mas_reciente = sorted(self.contratos, key=lambda c: c.fecha_inicio, reverse=True)[0]

        return {
            "id": self.id,
            "empresaIDs": [asociacion.empresa_id for asociacion in self.empresa_asociaciones],
            "empresas": [
                {
                    "id": asociacion.empresa_id,
                    "nombre": asociacion.empresa.nombre,
                    "codigo": asociacion.empresa.codigo,
                    "estado_empresa": asociacion.empresa.estado,
                    "estado_operario_en_empresa": asociacion.estado
                } for asociacion in self.empresa_asociaciones
            ],
            "nombre": self.nombre,
            "apellido": self.apellido,
            "numeroCedula": self.numero_cedula,
            "numeroTelefonico": self.numero_telefonico,
            "correo": self.correo,
            "contrato_estado": contrato_mas_reciente.estado if contrato_mas_reciente else None,
            "contrato_id": contrato_mas_reciente.id if contrato_mas_reciente else None
        }

    contratos = db.relationship("ContratoEntity", backref="operario", lazy=True, cascade="all, delete-orphan")
    usuarios = db.relationship("UsuarioEntity", backref="operario", lazy=True, cascade="all, delete-orphan")
    empresa_asociaciones = db.relationship(
        'OperarioEmpresaAsociacion',
        back_populates='operario',
        cascade='all, delete-orphan'
    )

    empresas = db.relationship(
        'EmpresaEntity',
        secondary='association',
        viewonly=True,
        back_populates='operarios'
    )
