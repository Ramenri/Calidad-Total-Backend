from app.models.entities.usuario_entity import UsuarioEntity

class ValidatorsUserEntity:

    @staticmethod
    def validateFields(user_entity: UsuarioEntity):

        if not user_entity.getUsername():
            raise ValueError("Username are required")
        
        if not user_entity.getPassword():
            raise ValueError("password are required")
        
        if not user_entity.getRole():
            raise ValueError("role are required")
        
    @staticmethod
    def validateRoles(user_entity: UsuarioEntity):
        if user_entity.getRole() != "administrador" and user_entity.getRole() != "usuario":
            raise ValueError("role not allowed")
        
    @staticmethod
    def validateField(field:object, field_name: str):
        if not field:
            raise ValueError(f"{field_name} are required")
