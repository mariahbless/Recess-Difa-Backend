
from app.extension import db
from datetime import datetime  # The extension for updating the date


class Program(db.Model):
        __tablename__ = 'programs'
        id = db.Column(db.Integer, primary_key=True)
        name= db.Column(db.String(100), nullable = False)
        description = db.Column(db.String(100), nullable = False)
        duration = db.Column(db.String(100),nullable= False)
        outcome = db.Column(db.String(100),nullable=False)
        organisations_id = db.Column(db.Integer,db.ForeignKey('organisations.id'))
        created_at = db.Column(db.DateTime, default = datetime.now)   # This is a time stamp
        updated_at = db.Column(db.DateTime, onupdate = datetime.now)  # This is a time stamp
        
        # Defining all the attributes (Creating a constractor) This is because  incase you create any new user, all these fields will be required
        def __init__(self,name,description,duration,outcome):

         self.name = name
         self.description = description
         self.duration = duration
         self.outcome = outcome
 
              

         
              
         

