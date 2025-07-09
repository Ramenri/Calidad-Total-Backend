import uuid
from sqlalchemy.orm import Mapped, relationship
from app.configuration.configuracion_Database import db
from werkzeug.security import generate_password_hash
from app.models.entities.operario_entity import OperarioEntity

class UsuarioEntity(db.Model):
    __tablename__ = 'usuario'

    id: Mapped[str] = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre_usuario: Mapped[str] = db.Column(db.String(100), nullable=False)
    contraseña: Mapped[str] = db.Column(db.String(100), nullable=False)
    rol: Mapped[str] = db.Column(db.String(100), nullable=False)
    operario_id: Mapped[str] = db.Column(db.String(36), db.ForeignKey('operario.id'), nullable=False)


    def getUsername(self) -> str:
        return self.nombre_usuario

    def getPassword(self) -> str:
        return self.contraseña

    def getRole(self) -> str:
        return self.rol

    def get_json(self) -> dict:
        
        getOperario = OperarioEntity.query.filter_by(id=self.operario_id).first()

        if getOperario:
            return {
                "id": self.id,
                "nombre_usuario": self.nombre_usuario,
                "contraseña": self.contraseña,
                "rol": self.rol,
                "id_operario": self.operario_id,
                "informacion_operario": getOperario.get_json()
            }
        return {
            "id": self.id,
            "nombre_usuario": self.nombre_usuario,
            "contraseña": self.contraseña,
            "rol": self.rol,
            "id_operario": self.operario_id,
            "informacion_operario": "no ha sido asignado aun"
        }