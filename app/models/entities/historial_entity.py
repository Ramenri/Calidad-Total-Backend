from datetime import datetime
import uuid
from app.configuration.configuracion_Database import db

class HistorialEntity(db.Model):
    __tablename__ = 'historial'

    id: int = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    usuario_id: int = db.Column(db.BigInteger, nullable=False)
    accion = db.Column(db.String(50), nullable=False)
    peticion = db.Column(db.String(10), nullable=False)
    rol = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.Date, default=lambda: datetime.utcnow().date())
    hora = db.Column(db.Time, default=lambda: datetime.utcnow().time())
    descripcion = db.Column(db.Text, nullable=False)

    def get_json(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "accion": self.accion,
            "peticion": self.peticion,
            "rol": self.rol,
            "fecha": self.fecha.strftime("%Y-%m-%d"),
            "hora": self.hora.strftime("%I:%M:%S %p"),  
            "descripcion": self.descripcion
        }
