from flask import Flask
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from config import Config
from extensions import db
import yaml
from flask_cors import CORS

from auth.jwt import auth_bp
from controllers.comanda_ctrl import comanda_bp
from controllers.usuario_ctrl import usuario_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)  # Aqui ativa o JWT na aplicação
app.config['SWAGGER'] = {
    'title': 'Minha API',
    'uiversion': 3,
    'securityDefinitions': {
        'BearerAuth': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Insira seu token JWT no formato **Bearer &lt;seu_token&gt;**'
        }
    },
    'security': [
        {
            'BearerAuth': []
        }
    ]
}

with open('swagger/swagger.yaml', 'r', encoding='utf-8') as f:
    swagger_template = yaml.safe_load(f)

swagger = Swagger(app, template=swagger_template)

app.register_blueprint(usuario_bp, url_prefix='/RestAPIFurb')
app.register_blueprint(auth_bp, url_prefix='/RestAPIFurb')
app.register_blueprint(comanda_bp, url_prefix='/RestAPIFurb')
CORS(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)
