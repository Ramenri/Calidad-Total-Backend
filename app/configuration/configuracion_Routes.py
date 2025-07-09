from app.controllers.empresa_controller import empresa_routes
from app.controllers.operario_controller import operario_routes
from app.controllers.centro_trabajo_controller import centro_routes
from app.controllers.contrato_controller import contrato_routes
from app.controllers.documento_controller import documento_routes
from app.controllers.usuario_controller import usuario_routes
from app.controllers.historial_controller import historial_routes

def iniciar_routes(app):
    app.register_blueprint(empresa_routes)
    app.register_blueprint(operario_routes)
    app.register_blueprint(centro_routes)
    app.register_blueprint(contrato_routes)
    app.register_blueprint(documento_routes)
    app.register_blueprint(usuario_routes)
    app.register_blueprint(historial_routes)
