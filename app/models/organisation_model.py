
from app.extension import db
from datetime import datetime  # The extension for updating the date


class Organisation(db.Model):
        __tablename__ = 'organisations'
        id = db.Column(db.Integer, primary_key=True)
        name= db.Column(db.String(100), nullable = False)
        location = db.Column(db.String(100), nullable = False)
        email = db.Column(db.String(100),nullable= False)
        contact = db.Column(db.String(100),nullable=False)
        password = db.Column(db.String(100),nullable=False)
        created_at = db.Column(db.DateTime, default = datetime.now)   # This is a time stamp
        updated_at = db.Column(db.DateTime, onupdate = datetime.now)  # This is a time stamp
        
        # Defining all the attributes (Creating a constractor) This is because  incase you create any new user, all these fields will be required
        def __init__(self,name,location,email,contact,password):

         self.name = name
         self.location = location
         self.email = email
         self.contact = contact
         self.password = password
         
 
              

         
              
         

