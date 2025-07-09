
from app.extension import db
from datetime import datetime  # The extension for updating the date


class Donor(db.Model):
        __tablename__ = 'donors'
        id = db.Column(db.Integer, primary_key=True)
        first_name= db.Column(db.String(100), nullable = False)
        last_name = db.Column(db.String(100), nullable = False)
        email = db.Column(db.String(100),nullable= False)
        contact = db.Column(db.String(100),nullable= False)
        amount = db.Column(db.String(100),nullable= False)
        organisations_id = db.Column(db.Integer,db.ForeignKey('organisations.id'))
        created_at = db.Column(db.DateTime, default = datetime.now)   # This is a time stamp
        updated_at = db.Column(db.DateTime, onupdate = datetime.now)  # This is a time stamp
        
        # Defining all the attributes (Creating a constractor) This is because  incase you create any new user, all these fields will be required
        def __init__(self,first_name,last_name,email,contact,amount):

         self.first_name = first_name
         self.last_name = last_name
         self.email = email
         self.contact = contact
         self.amount = amount
 
              

         
              
         

