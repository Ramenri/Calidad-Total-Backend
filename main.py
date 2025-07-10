from flask import Flask
from flask_cors import CORS
from app.configuration.config import Config
from app.configuration.configuracion_Database import inciar_database, db
from app.configuration.configuracion_Bcrypt import iniciar_bcrypt
from app.exceptions.exception_handler import responseErrorHandlersGlobal
from app.configuration.configuracion_Routes import iniciar_routes
from app.utils.crear_usuario_admin import inicializar_datos_prueba
app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
inciar_database(app)
iniciar_bcrypt(app)
responseErrorHandlersGlobal(app=app)

if __name__ == "__main__":

    print(f"Ruta donde se guardarán los documentos: {app.config['DOCUMENTOS_PATH']}")

    iniciar_routes(app)

    with app.app_context():
        db.create_all()
        inicializar_datos_prueba()

    app.run(debug=True, host="0.0.0.0", port=5000)
