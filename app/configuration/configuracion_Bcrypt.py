from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def iniciar_bcrypt(app):
    bcrypt.init_app(app)