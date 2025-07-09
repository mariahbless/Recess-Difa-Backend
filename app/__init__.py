from flask import Flask
from app.extension import db,migrate
from app.controllers.program_controller import program
from app.controllers.donor_controller import donor
from app.controllers.organisation_controller import organisation


#application factory function
def create_app():
    
    #app instance
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    migrate.init_app(app,db)


    #Calling models to the init file
    from app.models.organisation_model import Organisation
    from app.models.donor_model import Donor
    from app.models.program_model import Program




    # Register the blue prints
    app.register_blueprint(program)
    app.register_blueprint(donor)
    app.register_blueprint(organisation)




    @app.route("/")
    def home():
        return "Difa-ug Recess project"
    
  
    
    return app

