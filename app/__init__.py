from flask import Flask
from app.extension import db,migrate,bcrypt,jwt,cors,mail
from app.controllers.program_controller import program
from app.controllers.donor_controller import donor
from app.controllers.organisation_controller import organisation
from app.controllers.partner_controller import partner
import os
from flask_mail import Mail
from dotenv import load_dotenv









#application factory function
def create_app():
    load_dotenv()  # load variables from .env
    
    #app instance
    app = Flask(__name__)
    app.config.from_object('config.Config')

    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

    
    db.init_app(app)
    migrate.init_app(app,db)
    cors.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    
    


    #Calling models to the init file
    from app.models.organisation_model import Organisation
    from app.models.donor_model import Donor
    from app.models.program_model import Program
    from app.models.partner_model import Partner




    # Register the blue prints
    app.register_blueprint(program)
    app.register_blueprint(donor)
    app.register_blueprint(organisation)
    app.register_blueprint(partner)




    @app.route("/")
    def home():
        return "Difa-ug Recess project"
    
  
    
    return app

